import asyncio
from copy import deepcopy
import re
import typing as t

import parsel
import requests

from findout.domains import SensitiveLevelsEnum


class InComment:
    default_sensitive_words = (
        'user',
        'password',
        'import',
        'login',
        '.php',
        'file',
        'release',
        'version',
        'make',
        'replace',
        'called',
        'test',
        'debug',
        'see',
        'by',
        'tag'
    )

    high_sensitive_words = (
        'password',
        'user',
        'login',
        'import',
        'make'
    )

    medium_sensitive_words = (
        'replace',
        '.php',
        'file',
        'by',
        'release',
        'version'
    )

    def __init__(self, optional_words: list[str], remove_words: list[str]):
        _sensitives_words: list = deepcopy(self.default_sensitive_words)
        for word in remove_words:
            _sensitives_words.remove(word)
        self.__optional_sensitive_words = (
            set(optional_words) - set(self.default_sensitive_words)
        )
        self.sensitive_words = (
            _sensitives_words + tuple(self.__optional_sensitive_words)
        )

    @staticmethod
    async def _search(url: str) -> str:
        with requests.get(url, headers={'User-Agent': 'Mozilla'}) as response:
            html_tree = response.text
        return html_tree

    @staticmethod
    async def _read_path(path: str):
        with open(path) as f:
            html_tree = f.read()
        return html_tree

    @classmethod
    def _check_sensitive_level(
        cls, comment: str, by_optional_word: bool = False
    ) -> dict:
        if by_optional_word:
            return {SensitiveLevelsEnum.OPTIONAL.name: comment}
        elif any(string in comment for string in cls.high_sensitive_words):
            return {SensitiveLevelsEnum.HIGH.name: comment}
        elif any(string in comment for string in cls.medium_sensitive_words):
            return {SensitiveLevelsEnum.MEDIUM.name: comment}
        else:
            return {SensitiveLevelsEnum.LOW.name: comment}

    @classmethod
    async def _get_comments(cls, path: str, external_url: bool) -> list[str]:
        if external_url:
            html_tree = await cls._search(path)
        else:
            html_tree = await cls._read_path(path)
        element = parsel.Selector(html_tree)
        return element.xpath('//comment()').getall()

    @staticmethod
    def __is_commented_tag(comment: str) -> bool:
        sanitize_comment = comment.replace('<!--', '').replace('-->', '')
        return re.match('<[^>]*>', sanitize_comment)

    def return_might_sensitive_comments(
        self, path: str, external_url: bool, return_tags: bool = False
    ) -> t.Generator:
        comments: list[str] = asyncio.run(
            self._get_comments(path, external_url)
        )
        for comment in comments:
            if not return_tags and self.__is_commented_tag(comment):
                continue

            for sensitive_word in self.sensitive_words:
                if sensitive_word.lower() in comment.lower():
                    yield self._check_sensitive_level(
                        comment,
                        by_optional_word=(
                            sensitive_word in self.__optional_sensitive_words
                        )
                    )

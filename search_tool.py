import parsel, requests, asyncio, re
from typing import List


class InComment:
    def __init__(self, optional_words: List[str]=[], remove_words: List[str]=[]) -> None:
        self.might_sensitive_words = [
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
        ]
        [self.might_sensitive_words.append(f'O: {word}') for word in optional_words]
        [self.might_sensitive_words.remove(word) for word in remove_words if word in self.might_sensitive_words]
    
    
    @staticmethod
    async def _search(url: str)->str:
        return requests.get(url, headers={'User-Agent': 'Mozilla'}).text
    
    
    @staticmethod
    def _check_sensitive_level(comment: str, by_optional_word: bool=False)->dict:
        high = ['password', 'user', 'login', 'import', 'make']
        medium = ['replace', '.php', 'file', 'by', 'release', 'version']
        if by_optional_word:
            return {'optional': comment}
        elif any(string  in comment for string in high):
            return {'high': comment}
        elif any(string in comment for string in medium):
            return {'medium': comment}
        else:
            return {'low': comment}
    
    
    @classmethod
    async def _get_comments(cls, url: str, is_local: bool)->List[str]:
        html_struct = await cls._search(url) if not is_local else open(url, 'r').read()
        element = parsel.Selector(html_struct)
        return element.xpath('//comment()').getall()
    
    
    def return_might_sensitive_comments(self, url: str, is_local: bool, return_tags: bool=False)->List[dict]:
        comments: List[str] = asyncio.run(self._get_comments(url, is_local))
        for comment in comments:
            if not re.match('<[^>]*>', comment.replace('<!--', '').replace('-->', '')) or return_tags:
                for might_sensitive_word in self.might_sensitive_words:
                    if might_sensitive_word.replace('O: ', '').lower() in comment.lower() and 'input' not in comment.lower():
                        yield self._check_sensitive_level(comment, by_optional_word='O: ' in might_sensitive_word)
        

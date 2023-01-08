from __future__ import annotations

import re

from findout.domains import SensitiveLevelsEnum


_VALID_URL_REGEX = (
    r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+"
    r"[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
)


def is_external_url(string: str):
    return bool(re.match(_VALID_URL_REGEX, string))


def _print_high_sensitive(comment: str, character_content_limit: int | None):
    print(f"\033[1;31m{comment[:character_content_limit]}\033[m")


def _print_medium_sensitive(comment: str, character_content_limit: int | None):
    print(f"\033[1;33m{comment[:character_content_limit]}\033[m")


def _print_low_sensitive(comment: str, character_content_limit: int | None):
    print(f"\033[1;32m{comment[:character_content_limit]}\033[m")


def _print_optional_sensitive(comment: str, character_content_limit: int | None):
    print(f"\033[1;35m{comment[:character_content_limit]}\033[m optinal input")


def print_comment(
    comment: str, character_content_limit: int | None, level: SensitiveLevelsEnum
):
    print()
    match level:
        case SensitiveLevelsEnum.HIGH:
            _print_high_sensitive(comment, character_content_limit)
        case SensitiveLevelsEnum.MEDIUM:
            _print_high_sensitive(comment, character_content_limit)
        case SensitiveLevelsEnum.LOW:
            _print_low_sensitive(comment, character_content_limit)
        case SensitiveLevelsEnum.OPTIONAL:
            _print_optional_sensitive(comment, character_content_limit)
        case _:
            print(comment[:character_content_limit])

"""A pre-attack hacker tool which aims to find out sensitives comments in HTML
comment tag and to help on reconnaissance process
"""

from __future__ import annotations


__author__ = "Pablo Emidio"
__email__ = "p.emidiodev@gmail.com"
__version__ = "0.1.1"


version = __version__


def package_info() -> tuple[str, str, str]:
    return __author__, __email__, version

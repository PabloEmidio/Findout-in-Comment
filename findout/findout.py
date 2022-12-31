import argparse

from findout._utils import (
    is_external_url,
    print_comment
)
from findout.domains import SensitiveLevelsEnum
from findout.search_tool import InComment


_COMMENT_LIMIT_CHARS = 61


def main():
    parser = argparse.ArgumentParser(
        description='find sensitive content out in HTML comments tag'
    )
    parser.add_argument(
        '-w', nargs='+', help='add optional words to find out', default=[]
    )
    parser.add_argument(
        '-r',
        nargs='+',
        help='remove words which would be searched',
        default=[]
    )
    parser.add_argument(
        '-v',
        help='See entire comment content',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--return-tags',
        help='allow to show comments with html code',
        action='store_true',
        default=False
    )
    parser.add_argument(
        'path', help='Website URL or HTML file path'
    )

    args = parser.parse_args()

    path = args.path
    optional_words = args.w
    remove_words = args.r
    character_content_limit = None if args.v else _COMMENT_LIMIT_CHARS
    return_tags = args.return_tags

    obj = InComment(optional_words, remove_words)
    try:
        external_url = is_external_url(path)
        comments_list = obj.return_might_sensitive_comments(
            path, external_url, return_tags
        )
        for comments_dict in comments_list:
            for level, comment in comments_dict.items():
                print_comment(
                    comment,
                    character_content_limit,
                    SensitiveLevelsEnum[level]
                )
        else:
            return 0
        print(
            f'\n\nThese are some possibles sensitive comments find out in'
            f'"{path}" as specificated\n'
        )
        return 0
    except Exception as err:
        print(err)
        raise
    return 1


if __name__ == '__main__':
    SystemExit(main())

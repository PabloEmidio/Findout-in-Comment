from search_tool import InComment

import argparse

def main():
    parser = argparse.ArgumentParser(description='find sensitive content out in HTML comments tag')
    parser.add_argument('-w', nargs='+', help='optional words to find out', default=[])
    parser.add_argument('-v', help='See entire comment content', action='store_true', default=False)
    parser.add_argument('--return-tags', help='return comments which has html code', action='store_true', default=False)
    parser.add_argument('URL', help='Website url')
    args = parser.parse_args()
    url = args.URL
    return_tags = args.return_tags
    optional_words = args.w
    see_entire_content = None if args.v else 61
    obj = InComment(optional_words)
    try:
        if 'http' in url:
            print()
            comments_list = obj.return_might_sensitive_comments(url, return_tags)
            for comments_dict in comments_list:
                for level, comment in comments_dict.items():
                    if level=='high':
                        print(f'\033[1;31m{comment[:see_entire_content]}\033[m\n')
                    elif level=='medium':
                        print(f'\033[1;33m{comment[:see_entire_content]}\033[m\n')
                    elif level=='optional':
                        print(f'\033[1;35m{comment[:see_entire_content]}\033[m optinal input\n')
                    else:
                        print(f'\033[1;32m{comment[:see_entire_content]}\033[m\n')
    except Exception as error:
        print(error)
            
if __name__ == '__main__':
    main()
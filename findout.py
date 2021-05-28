from search_tool import InComment
import argparse

def main():
    parser = argparse.ArgumentParser(description='find sensitive content out in HTML comments tag')
    parser.add_argument('-w', nargs='+', help='add optional words to find out', default=[])
    parser.add_argument('-r', nargs='+', help='remove words which would be searched', default=[])
    parser.add_argument('-v', help='See entire comment content', action='store_true', default=False)
    parser.add_argument('--return-tags', help='allow to show comments with html code', action='store_true', default=False)
    parser.add_argument('URL', help='Website URL or HTML file path')
    
    args = parser.parse_args()
    
    url = args.URL
    optional_words = args.w
    remove_words = args.r
    character_content_limit = None if args.v else 61
    return_tags = args.return_tags
    
    obj = InComment(optional_words, remove_words)
    try:
        is_local = False if 'http' in url else True
        comments_list = obj.return_might_sensitive_comments(url, is_local, return_tags)
        for comments_dict in comments_list:
            for level, comment in comments_dict.items():
                print()
                if level=='high':
                    print(f'\033[1;31m{comment[:character_content_limit]}\033[m')
                elif level=='medium':
                    print(f'\033[1;33m{comment[:character_content_limit]}\033[m')
                elif level=='optional':
                    print(f'\033[1;35m{comment[:character_content_limit]}\033[m optinal input')
                else:
                    print(f'\033[1;32m{comment[:character_content_limit]}\033[m')
        print(f'\n\nThese are some possibles sensitive comments find out in "{url}" as specificated\n')
    except Exception as error:
        print(error)
            
if __name__ == '__main__':
    main()
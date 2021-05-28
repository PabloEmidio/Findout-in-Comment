from bs4 import BeautifulSoup as bs
import parsel, requests, sys, asyncio
import sys

class InComment:
    def __init__(self) -> None:
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
            'make sure',
            'replace',
            'called',
            'test',
            'debug',
            'see',
            'by'
        ]
    
    
    @staticmethod
    async def _search(url: str)->str:
        return requests.get(url, headers={'User-Agent': 'Mozilla'}).text
    
    
    @staticmethod
    def _check_sensitive_level(comment):
        high = ['password', 'user', 'login', 'import', 'make sure']
        medium = ['replace', '.php', 'file', 'by', 'release', 'version']
        if  any(string  in comment for string in high):
            return {'high': comment}
        elif any(string in comment for string in medium):
            return {'medium': comment}
        else:
            return {'low': comment}
    
    
    @classmethod
    async def _get_comments(cls, url: str)->list:
        html_struct = await cls._search(url)
        element = parsel.Selector(html_struct)
        return element.xpath('//comment()').getall()
    
    
    def return_might_sensitive_comments(self, url: str)->list:
        comments = asyncio.run(self._get_comments(url))
        for comment in comments:
            for might_sensitive_word in self.might_sensitive_words:
                if might_sensitive_word.lower() in comment.lower() and 'input' not in comment.lower():
                    yield self._check_sensitive_level(comment)
        
                


if __name__ == '__main__':
    obj = InComment()
    try:
        url = sys.argv[1]
        if 'http' in url:
            comments_list = obj.return_might_sensitive_comments(url)
            for comments_dict in comments_list:
                for level, comment in comments_dict.items():
                    if level=='high':
                        print(f'\033[1;31m{comment}\033[m')
                    elif level=='medium':
                        print(f'\033[1;33m{comment}\033[m')
                    else:
                        print(f'\033[1;32m{comment}\033[m')
    except IndexError:
        raise TypeError('TypeError: expected 1 argument')
    except Exception as error:
        print(error)
            

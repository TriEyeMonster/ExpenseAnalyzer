import requests
import time
import chardet
import urllib3
import re

URL_SEARCH = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1"
URL_NUM = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1&num={num}"

class GoogleHandler:
    def __init__(self):
        pass

    def search_page(self, keyword, language='en', num=None, start=0, pause=2):
        """
        Google search
        :param query: Keyword
        :param language: Language
        :return: result
        """
        time.sleep(pause)
        domain = 'www.google.com.sg'
        if num is None:
            url = URL_SEARCH
            url = url.format(
                domain=domain, language=language, query=keyword)
        else:
            url = URL_NUM
            url = url.format(
                domain=domain, language=language, query=keyword, num=num)
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            r = requests.get(url=url,
                             allow_redirects=False,
                             verify=False,
                             timeout=30)
            charset = chardet.detect(r.content)
            content = r.content.decode(charset['encoding'])
            # if 'en.wikipedia.org' in content:
            #     content = content[:content.rindex('en.wikipedia.org')]
            #     content = content[content.rindex('<div class="_zdb _Pxg">')+len('<div class="_zdb _Pxg">'):]
            #     content = content[:content.index('</div>')]
            #     return content
            if 'https://maps.google.com.sg' in content:
                content = content[content.index(r'https://www.google.com.sg/search'):]
                content = re.search(ur'>([\w ]+) \u00b7 ', content).group(1)
                return content.strip()
            return None
        except Exception as e:
            #logging.error(e)
            return None

if __name__ == "__main__":
    gh = GoogleHandler()
    content = gh.search_page(keyword="cheers")
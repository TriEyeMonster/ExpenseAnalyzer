import requests
import time
import chardet

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
            #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            r = requests.get(url=url,
                             allow_redirects=False,
                             verify=False,
                             timeout=30)
            charset = chardet.detect(r.content)
            content = r.content.decode(charset['encoding'])
            if 'https://maps.google.com.sg' in content:
                content = content[:content.rindex('https://maps.google.com.sg')]
                content = content[content.rindex(r'<span>') + 6:content.rindex(r'</span>')]
                return content
            return None
        except Exception as e:
            #logging.error(e)
            return None

if __name__ == "__main__":
    gh = GoogleHandler()
    content = gh.search_page(keyword="HAN'S CAFE - CHANGI CITY")
    if 'https://maps.google.com.sg' in content:
        content = content[:content.rindex('https://maps.google.com.sg')]
        content = content[content.rindex(r'<span>')+6:content.rindex(r'</span>')]
        pass
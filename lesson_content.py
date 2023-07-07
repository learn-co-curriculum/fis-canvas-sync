import requests
import markdown
import re
import saturncloud as sc
from bs4 import BeautifulSoup as bs

class HtmlBody:
    def __init__(self, lesson, new=False, sc=False):
        
        self.name = lesson_name(lesson)[0]
        print(f'Pulling HTML from {self.name}')
        try:
            branch = 'main'
            url = f'http://raw.githubusercontent.com/learn-co-curriculum/{self.name}/{branch}/README.md'
            resp = requests.get(url)
            resp.raise_for_status()
            print(f'{branch} pulled')
        except:
            print(f'Branch is not: {branch}')
            branch = 'master'
            url = f'http://raw.githubusercontent.com/learn-co-curriculum/{self.name}/{branch}/README.md'
            resp = requests.get(url)
            print(f'{branch} pulled')
        resp_text = resp.text
        self.markdown = markdown.markdown(resp_text)
        self.html = resp_text
        self.intro = get_intro(markdown.markdown(resp_text))
        if new:
            self.header = f"""<header class="fis-header" style="visibility: hidden;"><a class="fis-git-link" href="https://github.com/learn-co-curriculum/{self.name}" target="_blank" rel="noopener"><img id="repo-img" title="Open GitHub Repo" alt="GitHub Repo" /></a><a class="fis-git-link" href="https://github.com/learn-co-curriculum/{self.name}/issues/new" target="_blank" rel="noopener"><img id="issue-img" title="Create New Issue" alt="Create New Issue" /></a></header>"""
            self.data = f"""<div id="git-data-element" data-org="learn-co-curriculum" data-repo="{self.name}"></div>"""
        else:
            soup = bs(lesson['description'], 'html.parser')
            self.header = soup.find("header", {'class':'fis-header'})
            self.data = soup.find("div", {'id':"git-data-element"})
        
def get_intro(repo_markdown):
        m = re.search(r'<h2>.*?</h2>.*?<h2>.*?</h2>.*?</ul.*?>', repo_markdown, re.DOTALL)
        s = m.start()
        e = m.end() - len('<h1>')
        target_html = repo_markdown[s:e]
        return target_html

def lesson_name(lesson):
    if lesson['description'] == '':
        return 'Empty', ""
    else:
        try:
            soup = bs(lesson['description'], 'html.parser')
            href = soup.find("a", {'class':"fis-git-link"}).get('href')
            name = href.split('/')[-1]
            return name.strip(), href
        except:
            return 'Empty', ""
        

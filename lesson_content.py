import requests
import markdown
import re
import saturncloud as sc
from bs4 import BeautifulSoup as bs
import os
import subprocess

class LessonContent:
    def __init__(self, instance, local=True, github_url=None):
        if local:
            self.content = LocalContent()

class HtmlBody:
    def __init__(self, lesson, new=False, sc=False):
        
        self.resp_text = lesson
        self.markdown = markdown.markdown(self.resp_text)
        self.html = self.resp_text
        self.name = lesson_name(self.resp_text)[0]
        self.intro = get_intro(self.markdown)
        if new:
            self.header = f"""<header class="fis-header" style="visibility: hidden;"><a class="fis-git-link" href="https://github.com/learn-co-curriculum/{self.name}" target="_blank" rel="noopener"><img id="repo-img" title="Open GitHub Repo" alt="GitHub Repo" /></a><a class="fis-git-link" href="https://github.com/learn-co-curriculum/{self.name}/issues/new" target="_blank" rel="noopener"><img id="issue-img" title="Create New Issue" alt="Create New Issue" /></a></header>"""
            self.data = f"""<div id="git-data-element" data-org="learn-co-curriculum" data-repo="{self.name}"></div>"""
        else:
            soup = bs(lesson['description'], 'html.parser')
            self.header = soup.find("header", {'class':'fis-header'})
            self.data = soup.find("div", {'id':"git-data-element"})
        
            
        
def get_intro(resp_text):
    m = re.search(r'<h2>.*?</h2>.*?<h2>.*?</h2>.*?</ul.*?>', resp_text, re.DOTALL)
    s = m.start()
    e = m.end() - len('</ul>')
    target_html = resp_text[s:e]
    return target_html

def lesson_name(lesson):
    if lesson == '':
        return 'Empty', ""
    else:
        try:
            soup = bs(lesson, 'html.parser')
            href = soup.find("a", {'class':"fis-git-link"}).get('href')
            name = href.split('/')[-1]
            return name.strip(), href
        except:
            return 'Empty', ""
            


class LocalContent():
    def __init__(self):
        self.path = os.path.join(os.getcwd(), 'temp')
        print(self.path)
        with open(os.path.join(self.path, 'README.md'), 'r') as f:
            self.raw_content = f.read()
        self.markdown = self.raw_content
        self.html = markdown.markdown(self.raw_content)
        self.intro = get_intro(self.raw_content)
        # self.repo = self.path.split('/')[-1]
        origin = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True, cwd=self.path).stdout
        repo = origin.strip('\n').rstrip('.git').split('/')[-1]
        self.repo = f'https://github.com/learn-co-curriculum/{repo}'
        self.name = self.repo.split('-')[1:]
        
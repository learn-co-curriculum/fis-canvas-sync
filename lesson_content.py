import requests
import markdown
import re
import saturncloud
from bs4 import BeautifulSoup as bs
import os
import subprocess
from tempfile import TemporaryDirectory as tempdir
from latex import latex_to_img as latex
import canvas_dotfile


class HtmlBody:
    def __init__(self, lesson, github_content, lesson_url, create=False, sc=False):
        
        self.resp_text = github_content
        self.markdown = markdown.markdown(self.resp_text)
        self.html = lesson
        self.name = lesson_name(lesson)
        self.title = make_title(self.markdown)
        self.intro = get_intro(self.markdown)
        self.data = make_data_element(self.html, lesson_url)
        self.header = make_header(self.html, lesson_url)
        self.url = lesson_url

def make_header(html, url):
    soup = bs(html, 'html.parser')
    header = soup.find("header", {'class':'fis-header'})
    if header != None:
        return header
    else:
        return f"""<header class="fis-header" style="visibility: hidden;"><a class="fis-git-link" href="https://github.com/learn-co-curriculum/{url}" target="_blank" rel="noopener"><img id="repo-img" title="Open GitHub Repo" alt="GitHub Repo" /></a><a class="fis-git-link" href="https://github.com/learn-co-curriculum/{url}/issues/new" target="_blank" rel="noopener"><img id="issue-img" title="Create New Issue" alt="Create New Issue" /></a></header>"""
    
def make_title(html):
    soup = bs(html, 'html.parser')
    title = soup.find('h1').text
    return title
    

def make_data_element(html, url):
    soup = bs(html, 'html.parser')
    data_element = soup.find("div", {'id':"git-data-element"})
    if data_element != None:
        return data_element
    else:
        return f"""<div id="git-data-element" data-org="learn-co-curriculum" data-repo="{url}"></div>"""
            
        
def get_intro(markdown):
    m = re.search(r'<h2>.*?</h2>.*?<h2>.*?</h2>.*?</ul.*?>', markdown, re.DOTALL)
    s = m.start()
    e = m.end() - len('</ul>')
    target_html = markdown[s:e]
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
    def __init__(self, instance, sc=False):
        self.path = os.path.join(os.getcwd())
        self.instance = instance
        with open(os.path.join(self.path, 'README.md'), 'r') as f:
            self.raw_content = f.read()
        self.markdown = latex(self.raw_content)
        self.html = markdown.markdown(self.markdown)
        origin = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True, cwd=self.path).stdout
        repo = origin.strip('\n').rstrip('.git').split('/')[-1]
        self.repo = f'https://github.com/learn-co-curriculum/{repo}'
        self.name = self.repo.split('/')[-1]
        self.slug = self.name.split('-')[1:]
        self.header = make_header(self.html, repo)
        self.data_element = make_data_element(self.html, repo)
        self.title = make_title(self.html)
        if sc:
            self.intro = get_intro(self.html)
            df = saturncloud.UpdatedLinksDf()
            link = saturncloud.GetSaturnLink(repo, instance, df.df)
            self.button = saturncloud.make_saturn_button(link.link)
        
        
class GithubContent():
    def __init__(self, instance, sc, remote_url):
        print(f'Pulling HTML from Github')
        with tempdir() as directory:
            path = directory
            subprocess.run(['git', 'clone', remote_url],cwd=path)
            repo_name = remote_url.split('/')[-1].rstrip('.git')
            workingdir = os.path.join(path, repo_name)
            readme_file = os.path.join(workingdir, 'README.md')
            with open(readme_file, 'r')as f:
                readme = f.read()
            github_content = readme
            self.markdown = latex(github_content)
            self.html = markdown.markdown(github_content)
            self.header = make_header(repo_name)
            self.data_element = make_data_element(repo_name)
            self.title = make_title(self.html)
            self.name = repo_name.split('/')[-1]
            self.slug = self.name.split('-')[1:]
            if self.type == 'a':
                self.dot_file = canvas_dotfile.create_assignment_dot_file(remote_url)
            else:
                self.dot_file = canvas_dotfile.create_page_dot_file(remote_url)
            if sc:
                self.intro = get_intro(self.html)
                df = saturncloud.UpdatedLinksDf()
                link = saturncloud.GetSaturnLink(remote_url, instance, df)
                self.button = saturncloud.make_saturn_button(link.link)

        
        
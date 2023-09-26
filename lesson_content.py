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
from datetime import date
from base64 import b64encode
import json
import base64


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
        self.meta = make_meta()
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
    
def make_meta():
    today_date = date.today().strftime('%m-%d-%Y')
    return f"<meta name='Updated' content='{today_date}'>"

def remove_title(html):
    pattern = re.compile(r"<h1>.*?</h1>", re.DOTALL)
    return pattern.sub("", html, count=1)

            
        
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
def make_slug(name):
    name = name.replace('- ', '')
    return ("-".join(name.split(' ')).lower())
            


class LocalContent():
    def __init__(self, instance, course, sc=False):
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
        self.slug = make_slug(self.title)
        self.header = make_header(self.html, repo)
        self.data_element = make_data_element(self.html, repo)
        self.title = make_title(self.html)
        self.meta = make_meta()
        self.course = course
        if sc:
            self.intro = get_intro(self.html)
            df = saturncloud.UpdatedLinksDf()
            link = saturncloud.GetSaturnLink(repo, instance, df.df)
            self.button = saturncloud.make_saturn_button(link.link)
        
        
class GithubContent():
    def __init__(self, lesson, instance, sc, remote_url, assn_type):
        print(f'Pulling HTML from Github')

        repo_name = remote_url.split('/')[-1].rstrip('.git')
        owner = 'learn-co-curriculum'
        branches = ['main', 'master']
        MY_TOKEN = os.getenv('GITHUB_TOKEN')
    
        headers = {
            "Authorization": f"Bearer {MY_TOKEN}"
        }
        readme = None
        for branch_name in branches:
            readme_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{branch_name}/README.md"
            response = requests.get(readme_url, headers=headers)
            if response.status_code == 200:
                readme = response.text

            else:
                continue
        
        canvas_sha = None
        canvas_dotfile_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/.canvas"
        response = requests.get(canvas_dotfile_url, headers=headers)

        if response.status_code == 200:
            canvas_sha = json.loads(response.text)['sha']
            canvas_yaml = json.loads(response.text)['content']
            yaml_decoded = base64.b64decode(canvas_yaml)

        
        
                        
        github_content = remove_title(readme)
        self.markdown = latex(github_content)
        self.html = markdown.markdown(github_content)
        self.header = make_header(self.html, repo_name)
        self.data_element = make_data_element(self.html, repo_name)
        self.meta = make_meta()
        self.title = make_title(readme)
        self.name = remote_url.split('/')[-1]
        self.slug = make_slug(self.title)
        self.course = lesson.course_id
        if canvas_sha == None:
            if assn_type== 'a':
                self.dot_file = canvas_dotfile.create_assignment_dot_file(lesson)
            else:
                self.dot_file = canvas_dotfile.create_page_dot_file(lesson)
        else:
            if assn_type== 'a':
                self.dot_file = canvas_dotfile.update_assignment_dot_file(lesson, yaml_decoded)
            else:
                self.dot_file = canvas_dotfile.update_page_dot_file(lesson, yaml_decoded)
        if sc:
            self.intro = get_intro(self.html)
            df = saturncloud.UpdatedLinksDf()
            link = saturncloud.GetSaturnLink(remote_url, instance, df)
            self.button = saturncloud.make_saturn_button(link.link)
        # Create or update requirements.txt within the env folder
        MY_TOKEN = os.getenv('GITHUB_TOKEN')
    
        headers = {
            "Authorization": f"Bearer {MY_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        
        dotfile_payload = {
            "message": "Updated .canvas via FIS-canvas",
            "content": self.dot_file,
            "sha": canvas_sha
        }

        canvas_dotfile_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/.canvas"
        
        print(self.dot_file)

        response = requests.put(canvas_dotfile_url, json=dotfile_payload, headers=headers)

        if response.status_code >= 200 and response.status_code < 300:
            print(".canvas file updated successfully.")
        else:
            print("Error updating .canvas file.", "\n", response.status_code, "\n", response.text)


        
        
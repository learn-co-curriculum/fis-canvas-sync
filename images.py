from git import Repo, Git, CommandError
import os
from markdown import markdown
from bs4 import BeautifulSoup as bs
import subprocess
import nbformat
import re
import shutil

git_ssh_identity_file = os.path.expanduser('~/.ssh/id_rsa')
git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd)

def fix_image_link(original_link, s3_bucket, path):
    image_path = os.path.join(path, original_link)

    destination_directory = s3_bucket
    print(image_path, original_link)
    result = subprocess.run(['flatiron-s3-uploader', 'upload', image_path, '--bucket', 'curriculum-content', '--directory', destination_directory], capture_output=True, text=True)
    print(f'the image in {image_path} has been uploaded to the s3 bucket at {result.stdout}{result.stderr}')
    new_image_tag = (result.stdout, result.stderr)
    return new_image_tag[0].strip()


def fix_image_src(repo, s3_bucket, remote):
    repo_ssh = f"git@github.com:{'/'.join(repo.split('/')[-2:])}.git"
    print(repo_ssh)
    if remote == True:
        path = os.path.join(os.getcwd(), 'temp')
        os.mkdir('temp') 
        cloned_repo = Repo.clone_from(repo_ssh, path, env=dict(GIT_SSH_COMMAND=git_ssh_cmd))
        try:
            cloned_repo.git.checkout('curriculum')
            print(f'cloned remotely into {path}')
        except:
            print(f'No curriculum branch in {repo}')
            shutil.rmtree(path) 
    
    else:
        path = os.getcwd()
        cloned_repo = Repo.clone_from(repo_ssh, path, env=dict(GIT_SSH_COMMAND=git_ssh_cmd))
        cloned_repo.git.checkout('curriculum')
        print('Cloned locally')
    

    content = os.path.join(path, 'index.ipynb')
    notebook = nbformat.read(content, as_version=4)

    # Iterate through the cells and process image links
    for cell in notebook.cells:
        if cell.cell_type == "markdown" or cell.cell_type == "raw":
            # Find image links in the cell's source (markdown or raw)
            mkdn_pattern = r"""!\[.*?\]\((.*?)\)"""
            html_pattern = r"""<img[^>]*src=['"](.*?)['"][^>]*>"""
            image_links = re.findall(mkdn_pattern, cell.source)
            image_links += re.findall(html_pattern, cell.source, re.DOTALL)
            
            for original_link in image_links:
                if original_link.startswith('http') or original_link.startswith('data:'):
                    continue
                
                new_link = fix_image_link(original_link, s3_bucket=s3_bucket, path=path)
                print(original_link, new_link)
                cell.source = cell.source.replace(original_link, new_link)

    nbformat.write(notebook, os.path.join(path, 'index.ipynb'), version=nbformat.NO_CONVERT)

    cloned_repo.index.add('index.ipynb')
    cloned_repo.index.commit("Notebook updated by fis-canvas image script")
    origin = cloned_repo.remote(name='origin')
    origin.push()
    shutil.rmtree(path) 
        


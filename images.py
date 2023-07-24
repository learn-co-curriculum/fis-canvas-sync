from git import Repo, Git, CommandError
import os
from markdown import markdown
from bs4 import BeautifulSoup as bs
import subprocess

not_local = True

# repo_url = 'https://github.com/learn-co-curriculum/dsc-git-intro'

# subprocess.run(['ssh-agent', '-s'])
git_ssh_identity_file = os.path.expanduser('~/.ssh/id_rsa')
git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd)

def fix_image_link(list_of_image_tags, index_to_fix, directory, width=''):
    tuple_of_old_new = []
    image_path = os.path.join(os.getcwd(), 'temp', list_of_image_tags[index_to_fix]['src'])
    specified_width = width
    destination_directory = directory
    print(image_path, destination_directory)
    result = subprocess.run(['flatiron-s3-uploader', 'upload', image_path, '--bucket', 'curriculum-content', '--directory', destination_directory], capture_output=True, text=True)
    print(f'the image in {image_path} has been uploaded to the s3 bucket at {result.stdout}')
    new_image_tag = (result.stdout, result.stderr)
    old_image_tag = str(list_of_image_tags[index_to_fix])
    tuple_of_old_new.append((old_image_tag, new_image_tag))
    return tuple_of_old_new


def fix_image_src(repo, directory, local=False):
    if not local:
        path = os.path.join(os.getcwd(), 'temp')
        os.mkdir('temp') 
        cloned_repo = Repo.clone_from(repo, path, env=dict(GIT_SSH_COMMAND=git_ssh_cmd))
        #cloned_repo.git.checkout('curriculum')
    if local:
        path = os.getcwd()
        cloned_repo = Repo.clone_from(repo, path, env=dict(GIT_SSH_COMMAND=git_ssh_cmd))
        cloned_repo.git.checkout('curriculum')
    with open(os.path.join(path, 'README.md'), 'r') as f:
        content = f.read()
    repo_markdown = markdown(content, output_format='html')
    soup = bs(repo_markdown, 'html.parser')
    content_images = soup.find_all('img')
    repo_updated = repo_markdown
    for i, tag in enumerate(content_images):
        img_tag = tag['src'].split('/')[0]
        tag_prefixes = ['http:', 'https:']
        if  img_tag in tag_prefixes:
            print(f'image tag at index {i} is a direct link')
        else:
            print(f'image tag at index {i} needs to be fixed.')
            fixed = fix_image_link(content_images, i, directory)
            old = fixed[0][0]
            print(fixed)
            print(old)
            new = fixed[0][1][0].strip()
            print(new)
            new_tag = soup.new_tag('img')
            new_tag['src'] = new
            tag.replace_with(new_tag)
    repo_updated = markdown(str(soup))
    with open(os.path.join(path, 'README.md'), 'w') as f:
        f.write(repo_updated)
    cloned_repo.index.add('README.md')
    cloned_repo.index.commit("README updated by fis-canvas image script")
    origin = cloned_repo.remote(name='origin')
    origin.push()


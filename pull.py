import sys
from os import system, chdir
import requests
import ntpath
import mimetypes
from pathlib import Path

gh_token = ''
catbox_token = ''

OWNER, REPO, PULL_REQUEST_NUMBER = sys.argv[1:]
REPO_URL = f'https://github.com/{OWNER}/{REPO}'


def upload_file(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        file_name = ntpath.basename(file_path)
        file_type = mimetypes.guess_type(file_path)[0]
        file_info = file_name, file_content, file_type

    params = {
        'reqtype': 'fileupload',
        'userhash': catbox_token
    }
    files = {
        'fileToUpload': file_info
    }
    result = requests.post('https://catbox.moe/user/api.php', data=params, files=files)
    if result.status_code != 200:
        print('ERROR while uploading file on catbox (file hosting)')
        exit(-1)
    return result.text


def comment(body):
    requests.post(f'https://api.github.com/repos/{OWNER}/{REPO}/issues/{PULL_REQUEST_NUMBER}/comments', headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {gh_token}",
        "X-GitHub-Api-Version": "2022-11-28"},
                  json={"body": body}
                  )


system(f'rm -rf {REPO}')
system(f'rm -rf {REPO}_pull')
system(f'git clone {REPO_URL}')
system(f'cp -R {REPO} {REPO}_pull')
chdir(f'{REPO}_pull')
system(f'git fetch origin pull/{PULL_REQUEST_NUMBER}/head:test')  # https://stackoverflow.com/a/30584951
system('git checkout test')
chdir(f'..')

dependencies = {
    'course-1/linear-algebra/question1.tex': 'course-1/linear-algebra/exam.tex'
}

tex_files = set()
for obj in requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PULL_REQUEST_NUMBER}/files', headers={
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {gh_token}",
    "X-GitHub-Api-Version": "2022-11-28"}).json():
    file_path = obj['filename']
    if file_path in dependencies:
        system(
            f'latexdiff {REPO}/{file_path} {REPO}_pull/{file_path} > tmp')
        system(f'cat tmp > {REPO}/{file_path}')
        tex_files.add(dependencies[file_path])
chdir(REPO)
urls = []
for path in tex_files:
    path = Path(path)
    chdir(path.parent)
    file = path.name
    system(
        f'latexdiff {file} {file} > tmp')
    system(f'cat tmp > {file}')
    for _ in range(2):
        system(f'pdflatex -synctex=1 -interaction=nonstopmode --shell-escape {file}')
    name = Path(file).with_suffix('')
    urls.append(f'[{name}.pdf]({upload_file(f"{name}.pdf")})')

comment('Изменённые файлы:' + ','.join(urls))

import sys
from os import system, chdir
import requests
import ntpath
import mimetypes
from pathlib import Path
from re import fullmatch

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

# https://3widgets.com/
dependencies = {
    'course-1/linear-algebra/question([1-9]|[12][0-9]|3[0-4]).tex': 'course-1/linear-algebra/exam.tex',
    'course-1/mathematical-analysis/question([1-9]|[1-3][0-9]|40).tex': 'course-1/mathematical-analysis/exam.tex'
}

tex_files = set()
for obj in requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PULL_REQUEST_NUMBER}/files', headers={
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {gh_token}",
    "X-GitHub-Api-Version": "2022-11-28"}).json():
    file_path = obj['filename']


    def get(file_path):
        for pattern in dependencies:
            if fullmatch(pattern, file_path) is not None:
                return dependencies[pattern]
        return None


    dependence = get(file_path)
    if dependence:
        system(
            f'latexdiff {REPO}/{file_path} {REPO}_pull/{file_path} > tmp')
        system(f'cat tmp > {REPO}/{file_path}')
        tex_files.add(dependence)
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

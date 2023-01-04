# usage : uvicorn deploy_server:app --host 0.0.0.0
from fastapi import FastAPI, HTTPException
from os import system

app = FastAPI()
PY = 'python3.10'
HASH = ''

def validate(owner, repo, hash):
    return owner == '9kin' and repo == 'is-tex' and hash == HASH

@app.get("/pull/{owner}/{repo}/{pull_request_number}")
def pull(owner: str, repo: str, pull_request_number: int, hash: str):
    if not validate(owner, repo, hash):
        raise HTTPException(status_code=404, detail='(')
    system(f'{PY} pull.py {owner} {repo} {pull_request_number} &')
    return "ok"


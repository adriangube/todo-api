from typing import Union
from fastapi import FastAPI
import uvicorn
import sys

app = FastAPI()

@app.get("/")
def read_root():
  return { "Hello": "World" }


def start():
  """Launched with `poetry run start` at root level"""
  mode = sys.argv[0] if sys.argv[0] == "prod" else "dev"
  reload = mode == "dev"
  uvicorn.run('src.todo_api.main:app', host='0.0.0.0', port=8000, reload=reload)

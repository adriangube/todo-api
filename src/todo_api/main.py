import sys
import uvicorn
from fastapi import FastAPI
from .routers import users, auth
from .models import Base
from .database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


def start():
    mode = sys.argv[0] if sys.argv[0] == "prod" else "dev"
    # Reload in dev mode only
    reload = mode == "dev"
    uvicorn.run("src.todo_api.main:app", host="0.0.0.0", port=8000, reload=reload)


app.include_router(auth.router)
app.include_router(users.router)

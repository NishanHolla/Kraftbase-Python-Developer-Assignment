from fastapi import FastAPI
from .db import models
from .db.session import engine
from .api import endpoints

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(endpoints.router)

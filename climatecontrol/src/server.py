from fastapi import FastAPI
from climatecontrol.src.interfaces.v1.routes.signin import login_router
from climatecontrol.src.interfaces.v1.routes import forecast
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from climatecontrol.src.repository.mongo_connection import MongoDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    MongoDB.initialize()
    yield
    MongoDB.close()

app = FastAPI(title="Climate Control API")
app.include_router(login_router, prefix="/auth", tags=["Login"])
app.include_router(forecast.router, prefix="/weather", tags=["weather"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
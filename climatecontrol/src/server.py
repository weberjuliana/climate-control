from fastapi import FastAPI
from climatecontrol.src.interfaces.v1.routes.signin import login_router


app = FastAPI(title="Climate Control API")
app.include_router(login_router, prefix="/auth", tags=["Login"])

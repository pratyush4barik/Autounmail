from fastapi import FastAPI
from database.database import engine, Base
from routers.register_auth import router as register_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automate API",
    version="1.0.0"
)


app.include_router(register_router)


@app.get("/")
def root():
    return {
        "message": "API is running"
    }

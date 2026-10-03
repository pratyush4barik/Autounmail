from fastapi import FastAPI
from database.database import engine, Base
from routers.register_auth import router as register_router
from routers.otp import router as otp_router
from routers.login_auth import router as login_router
from routers.user_details import router as user_details_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automate API",
    version="1.0.0"
)


app.include_router(register_router)
app.include_router(otp_router)
app.include_router(login_router)
app.include_router(user_details_router)

@app.get("/")
def root():
    return {
        "message": "API is running"
    }

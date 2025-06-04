from fastapi import FastAPI
from app.links.routes import public_router, private_router

from app.auth.routers import router as users_router

app = FastAPI(
    title="URL Alias Service",
    description="привет сокращайка ссылок",
    version="1.0.0",
)

app.include_router(users_router, prefix="/api/auth", tags=["auth"])

app.include_router(public_router, tags=["redirect"])
app.include_router(private_router, prefix="/api/links", tags=["private"])

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the URL Alias Service! See /docs for API documentation."}
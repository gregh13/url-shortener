import uvicorn
from fastapi import FastAPI
from app.api import api_handlers


app = FastAPI()
app.include_router(api_handlers.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the URL Shortener App, the free and easy way to shorten long and unseemly URLs."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True)

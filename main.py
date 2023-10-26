from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    message = '''
              Welcome to the URL Shortener Application, the free and easy way to shorten long and unseemly URLs. 
              Use a custom short URL or let us randomly generate one.
              '''
    return {"message": message}


@app.post("/shorten_url")
async def shorten_url():
    pass
import uvicorn

if __name__ == '__main__':
    uvicorn.run('weatherchallenge.asgi:application', reload=True)

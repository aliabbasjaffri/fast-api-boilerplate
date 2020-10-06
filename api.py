from fastapi import FastAPI
from route.routes import router

app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    # Remove port=5000 and debug=True for running
    # the application in production environment
    # app.run(debug=True, port=5000, host='0.0.0.0')
    app.run(host='0.0.0.0')

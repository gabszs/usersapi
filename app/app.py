import uvicorn
from fastapi import FastAPI

from app.routes import auth_router
from app.routes import ping_router
from app.routes import todos_router
from app.routes import users_router

app = FastAPI(
    title="UsersApi",
    description="Users Web api with basic auth crud built by @BRDEV team",
    contact={
        "name": "Gabriel Carvalho",
        "url": "https://www.linkedin.com/in/gabzsz/",
        "email": "gabriel.carvalho@huawei.com",
    },
    summary="WebApi build on best market practices such as TDD, Clean Arch, Data Validation with Pydantic V2",
)

app.include_router(todos_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(ping_router)

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000)

from fastapi import FastAPI
from app.routes import auth_router, users_router, ping_router

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

app.include_router(auth_router)
app.include_router(ping_router)
app.include_router(users_router)


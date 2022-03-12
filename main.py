from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, travel_destinations, iternaries, votes, comments, login

app = FastAPI(title="Elective_Travel_App")
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"]
)

app.include_router(users.router)
app.include_router(travel_destinations.router)
app.include_router(iternaries.router)
app.include_router(comments.router)
app.include_router(votes.router)
app.include_router(login.router)



@app.get("/")
async def main() -> dict:
    # await add_models_to_database() 
    return {"message": "hello world"}

if __name__ == '__main__':
    main()
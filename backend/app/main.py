from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import project_routes, admin_routes

load_dotenv()

app = FastAPI(title="SocialBunny API", version="1.0")

# CORS — allow frontend on any origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to SocialBunny API"}


# Register routers
app.include_router(project_routes.router)
app.include_router(admin_routes.router)

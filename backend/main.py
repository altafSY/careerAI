from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import resume, auth


app = FastAPI()
app.include_router(resume.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "CareerMapAI backend running"}

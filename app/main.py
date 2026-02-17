from fastapi import FastAPI
from app.schemas import PostRequest, PostResponse, FacebookPostRequest, FacebookPostResponse, GenerateAndPostRequest, GenerateAndPostResponse
from app.services.post_service import generate_and_post

app = FastAPI(
    title="Hijama Bengali Post Generator",
    version="1.0.0"
)


@app.post("/generate-and-post-facebook", response_model=GenerateAndPostResponse)
def generate_and_publish(request: GenerateAndPostRequest):
    result = generate_and_post(request)
    return result
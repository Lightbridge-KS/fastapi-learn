import base64
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Base64 Image API", version="1.0.0")


class ImageResponse(BaseModel):
    """Response model for base64 image data"""

    filename: str
    image_data: str
    mime_type: str


@app.get("/")
def read_root():
    """Root endpoint with basic info"""
    return {"message": "Base64 Image API", "endpoints": ["/image/{filename}"]}


@app.get("/image/{filename}", response_model=ImageResponse)
def get_image_base64(filename: str):
    """Get base64 encoded image data from local JPEG file"""

    # Define the path to your images directory
    # You can modify this path to your preferred location
    images_dir = Path("./img")  # Adjust this path
    image_path = images_dir / filename

    # Check if file exists and is a JPEG
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Image '{filename}' not found")

    if not filename.lower().endswith((".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only JPEG files are supported")

    try:
        # Read and encode the image
        with open(image_path, "rb") as image_file:
            image_binary = image_file.read()
            base64_encoded = base64.b64encode(image_binary).decode("utf-8")

        return ImageResponse(
            filename=filename, image_data=base64_encoded, mime_type="image/jpeg"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.get("/images/list")
def list_images():
    """List available JPEG images in the directory"""
    images_dir = Path("./img")

    if not images_dir.exists():
        return {"message": "Images directory not found", "images": []}

    jpeg_files = [
        f.name
        for f in images_dir.iterdir()
        if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg"]
    ]

    return {"images": jpeg_files}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

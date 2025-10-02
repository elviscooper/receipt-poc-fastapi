import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Receipt POC")

# Allow local/mobile dev later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-receipt")
async def upload_receipt(file: UploadFile = File(...)):
    try:
        # Make a safe unique filename (preserve extension if present)
        ext = os.path.splitext(file.filename or "")[1]
        safe_name = f"{uuid.uuid4().hex}{ext or '.bin'}"
        dest_path = os.path.join(UPLOAD_DIR, safe_name)

        # Read the content (for POC; switch to chunked writes later)
        content = await file.read()
        with open(dest_path, "wb") as f:
            f.write(content)

        return {
            "filename": file.filename,
            "saved_as": safe_name,
            "path": f"./uploads/{safe_name}",
            "size_bytes": len(content),
            "content_type": file.content_type,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

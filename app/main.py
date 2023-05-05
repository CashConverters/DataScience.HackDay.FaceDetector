from tempfile import NamedTemporaryFile
import os

from typing import Union

from fastapi import FastAPI, File, UploadFile

#from app.mugshot_detector import is_mugshot

app = FastAPI()


@app.get("/api/health")
async def health():
    return {"health": "ok"}


@app.post("/api/ismugshot")
def detect_faces(file: UploadFile = File(...)):
    from app.mugshot_detector import is_mugshot
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file.file.read()
            with temp as f:
                f.write(contents);
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        
        resp = is_mugshot(temp.name)
        return resp
    except Exception:
        return {"message": "There was an error processing the file"}
    finally:
        os.remove(temp.name)
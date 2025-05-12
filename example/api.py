import os

from magika import Magika
from ninja import File, NinjaAPI
from ninja.files import UploadedFile
from typing_extensions import Any

m = Magika()

api = NinjaAPI()

chunk_size = int(os.getenv("CHUNK_SIZE", 100))


def check_file_type_magika(chunked_file: bytes) -> str:
    check_file_type = m.identify_bytes(content=chunked_file)
    if check_file_type is not None:
        return f"File Type is {check_file_type.output.ct_label} with Mime Type {check_file_type.output.mime_type}"
    return None


@api.post("/upload")
def upload(request, file: UploadedFile = File(...)) -> dict[str, Any]:
    for chunk in file.chunks(chunk_size):
        detect_filetype = check_file_type_magika(chunk)
        if detect_filetype is not None:
            return {"Detected File Type": str(detect_filetype), "Size": file.size}
    return {"Detected File Type": "Unknown", "Size": 0}


@api.get("/hello")
def hello(request) -> str:
    return "Hello world"

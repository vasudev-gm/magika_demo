from ninja import File, NinjaAPI
from ninja.files import UploadedFile
from magika import Magika
from typing_extensions import Any

m = Magika()

api = NinjaAPI()

chunk_size = 100


def check_file_type_magika(chunked_file:bytes) -> str:
    check_file_type = m.identify_bytes(content=chunked_file)
    return f"File Type is {check_file_type.output.ct_label} with Mime Type {check_file_type.output.mime_type}"


@api.post("/upload")
def upload(request, file: UploadedFile = File(...))-> dict[str, Any]:
    data = file
    for chunk in data.chunks(chunk_size):
        detect_filetype = check_file_type_magika(chunk)
    if detect_filetype is not None:
        return {"Detected File Type": str(detect_filetype), "Size": len(data)}
    return {"Detected File Type": "Unknown", "Size": 0}


@api.get("/hello")
def hello(request):
    return "Hello world"

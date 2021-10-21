import os
from flask import Flask
from werkzeug.utils import send_from_directory
from .kenzie import MAX_CONTENT_LENGTH, image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.get('/files')
def list_files():
    return image.list_files()

@app.get('/files/<string:type>')
def list_files_by_format(type: str):
    return image.list_files_by_extension(type)

@app.post('/upload')
def upload_files():
    return image.upload_files()

@app.get('/download/<filename>')
def download_file(filename):
    return image.download_specific_file(filename)

@app.get('/download-zip/<extension>')
def download_zip(extension):
    return image.download_directory_as_zip(extension)
    
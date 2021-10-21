import os
from flask import Flask
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

# @app.post('/download_file')
# def download_file(filename: str):
#     path = image.get_path(filename)
#     return send_file(path, as_attachment=True, )
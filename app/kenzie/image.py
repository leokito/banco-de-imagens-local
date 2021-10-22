import os, zipfile
from flask import request, jsonify, send_file
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
from . import MAX_CONTENT_LENGTH, directory, extensions

max_size = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

def get_path(filename: str):
    extension = filename.upper()[-3:]
    path = f'../{directory}/{extension}/{filename}'
    return path

def list_files():
    list = []
    for root, subdirectories, files in os.walk(directory):
        for file in files:
            result = os.path.join(file)
            list.append(result)
    return jsonify(list), 200
    
def list_files_by_extension(format):
    type = format.lower()
    path = f'{directory}/{type.upper()}'
    if type in extensions:
        list = os.listdir(path)
        if list == []:
            return "No files were found", 404
      
        return jsonify(list)

def upload_files():

    file = request.files["file"]
    extension = file.filename.lower()[-3:]
    filename = secure_filename(file.filename)
    path = f'{directory}/{extension.upper()}'

    if allowed_file(file.filename):
            if os.path.isfile(f'{path}/{filename}'):
                return 'File already exists', 409
            if os.path.exists(f'{path}'):
                file.save(f'{path}/{filename}')
                return jsonify(filename), 201
            else:
                os.mkdir(f'{path}')
                file.save(f'{path}/{filename}')
                return jsonify(filename), 201
    else:
        return 'file format not allowed', 415

def download_specific_file(filename):
    try:
        path = get_path(filename)
        return send_file(path, as_attachment=True), 200
    except FileNotFoundError:
        return "File doesn't exist.", 404

def download_directory_as_zip():
    try:
        file_extension = request.args.get('file_extension')
        rate_compression = request.args.get('compression_ratio')
        extension = file_extension.upper()
        path= f'{directory}/{extension}'
        if not os.listdir(path):
            return 'Directory is empty', 404
        else:
            zip_file = f'zip -{rate_compression} -r /tmp/{extension}.zip {path}'
            os.system(zip_file)
            return send_from_directory(directory='/tmp', path=f'{extension}.zip', as_attachment=True)
    except FileNotFoundError:
        return "Directory doesn't exists", 404
    except AttributeError:
        return 'Invalid url, review the address and try again', 404
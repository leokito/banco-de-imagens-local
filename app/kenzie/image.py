from genericpath import isfile
import os
from os.path import isfile, join
from os import listdir
from flask import json, request, jsonify
from werkzeug.utils import secure_filename
from . import MAX_CONTENT_LENGTH, directory, extensions

max_size = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

# def list_files():
    # files_list = []
    # list = os.listdir(directory)

    # for files in list:
    #     files_list.append(files)

    #     return files_list

# def list_files():   

#     output = []
    
#     for dirpath, dirnames, filenames in os.walk("./uploaded"):
#         if filenames == []:
#             return 'Empty folder', 404
#         output.append(filenames)

#     return jsonify(output)
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


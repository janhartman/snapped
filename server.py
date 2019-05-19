import os
import random
import string

import face_recognition as fr
from flask import abort, Flask, jsonify, request, redirect, send_file
from PIL import Image
from flask_cors import CORS  
from snap import snap, load

app = Flask(__name__)
cors = CORS(app)
images, locations, encodings = load()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/yolo', methods=['GET', 'POST'])
def upload_image():
    print("Upload single")
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'target' not in request.files:
            return redirect(request.url)

        unknownImg = request.form['unknownId']
        unknownImg = unknownImg.split("_")[1]
        unknown = f'static/faces/' + unknownImg + '.jpg'
        print(unknown)
        target = request.files['target']

        if target and allowed_file(target.filename):
            # The image file seems valid! Detect faces and return the result.
            return replace_faces(target, unknown)

        # Error
        abort(500)

    if request.method == 'GET':
        # If no valid image file was uploaded, show the file upload form:
        return '''
        <!doctype html>
        <title>SNAPPED</title>
        <h1>Snap your friends from the face of the galaxy</h1>
        <form method="POST" action="/yolo" enctype="multipart/form-data">
        <p>Your target</p>
        <input type="file" name="target">
        <p>New face</p>
        <input type="number" name="unknownId">
        <input type="submit" value="Upload">
        </form>
        '''

@app.route('/', methods=['GET', 'POST'])
def upload_images():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'unknown' not in request.files or 'target' not in request.files:
            return redirect(request.url)

        unknown = request.files['unknown']
        target = request.files['target']

        if unknown and target and allowed_file(unknown.filename) and allowed_file(target.filename):
            # The image file seems valid! Detect faces and return the result.
            return replace_faces(unknown, target)

        # Error
        abort(500)

    if request.method == 'GET':
        # If no valid image file was uploaded, show the file upload form:
        return '''
        <!doctype html>
        <title>SNAPPED</title>
        <h1>Snap your friends from the face of the galaxy</h1>
        <form method="POST" enctype="multipart/form-data">
        <p>Your target</p>
        <input type="file" name="target">
        <p>New face</p>
        <input type="file" name="unknown">
        <input type="submit" value="Upload">
        </form>
        '''

def replace_faces(unknown_file, target_file):
    # Load the uploaded image files
    unknown = fr.load_image_file(unknown_file)
    target = fr.load_image_file(target_file)

    # Snap the target from the galaxy
    print('Snapping...')
    snapped = snap(images, locations, encodings, target, unknown)

    new_dir = 'snap_' + ''.join(random.choices(string.ascii_lowercase, k=8))
    os.mkdir(f'static/{new_dir}')
    result = {}
    for i, s in enumerate(snapped):
        path = f'static/{new_dir}/image_{i}.jpg'
        Image.fromarray(s).save(path)
        result[f'{i}'] = '/' + path
   
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
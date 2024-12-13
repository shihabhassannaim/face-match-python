from flask import Flask, request, jsonify, render_template
import os
import base64
from werkzeug.utils import secure_filename
from face_matcher import is_face_matched
from database import Database

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['POST'])
def apply_nid():
    full_name = request.form['fullName']
    nid_number = request.form['nidNumber']
    email = request.form['email']
    captured_image = request.form.get('capturedImage')
    video_image = request.files.get('videoImage')

    # Validate that NID number is provided
    if not nid_number:
        return jsonify({"status": "error", "message": "NID number is required."})

    # Save the captured or uploaded image with the NID number as the file name
    if captured_image:
        # Decode and save the base64-encoded image
        image_data = base64.b64decode(captured_image)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{nid_number}.jpg')
        with open(image_path, 'wb') as f:
            f.write(image_data)
    elif video_image:
        image_filename = f"{nid_number}{os.path.splitext(video_image.filename)[-1]}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_filename))
        video_image.save(image_path)
    else:
        return jsonify({"status": "error", "message": "No image provided."})

    # Check if the face matches with existing images in the database
    users = db.fetch_all_users()
    for user in users:
        existing_image_path = os.path.join(app.config['UPLOAD_FOLDER'], user['video_image'])
        if is_face_matched(image_path, existing_image_path):
            return jsonify({
                "status": "exists",
                "message": "User already exists.",
                "user_details": user
            })

    # Save the new user's data in the database
    db.insert_user(full_name, nid_number, email, os.path.basename(image_path))
    return jsonify({
        "status": "success",
        "message": "User registered successfully."
    })

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import os
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
    video_image = request.files['videoImage']
    
    # Save the captured image
    video_image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video_image.filename))
    video_image.save(video_image_path)

    # Check if the face matches with existing images in the database
    users = db.fetch_all_users()
    for user in users:
        existing_image_path = os.path.join(app.config['UPLOAD_FOLDER'], user['video_image'])
        if is_face_matched(video_image_path, existing_image_path):
            return jsonify({
                "status": "exists",
                "message": "User already exists.",
                "user_details": user
            })

    # Save the new user's data in the database
    db.insert_user(full_name, nid_number, email, video_image.filename)
    return jsonify({
        "status": "success",
        "message": "User registered successfully."
    })

if __name__ == '__main__':
    app.run(debug=True)

from PIL import Image
from flask import current_app
import secrets
import os

def save_image(file):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(file.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)
    output_size = (45, 45)
    i = Image.open(file)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
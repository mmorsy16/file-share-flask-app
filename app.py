from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import boto3, os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# ←– your bucket & region
S3_BUCKET = 'file-share-s3-storage-may5-2025'
S3_REGION = 'eu-west-2'

s3 = boto3.client('s3', region_name=S3_REGION)
ALLOWED_EXT = {'.txt','.pdf','.png','.jpg','.jpeg','.gif'}

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXT

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    if not f or not allowed_file(f.filename):
        return "Invalid file type", 400

    filename = secure_filename(f.filename)
    s3.upload_fileobj(f, S3_BUCKET, filename)

    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': filename},
        ExpiresIn=3600
    )
    return render_template('upload_success.html',
                           filename=filename, url=url)

if __name__ == '__main__':
    # bind to all interfaces on port 80
    app.run(host='0.0.0.0', port=80)

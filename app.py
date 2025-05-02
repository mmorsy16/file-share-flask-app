import boto3
from botocore.client import Config         
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


s3 = boto3.client(
    's3',
    region_name='eu-west-2',
    config=Config(signature_version='s3v4')   
)

BUCKET = 'my-file-sharing-bucket-2025'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or file.filename == '':
        return redirect(url_for('home'))
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(file, BUCKET, filename)
    except Exception as e:
        return f"❌ Upload failed: {e}", 500
    return redirect(url_for('files'))

@app.route('/files')
def files():
    resp = s3.list_objects_v2(Bucket=BUCKET)
    files = []
    for obj in resp.get('Contents', []):
        key = obj['Key']
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET, 'Key': key},
            ExpiresIn=3600
        )
        files.append({'name': key, 'url': url})
    return render_template('files.html', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

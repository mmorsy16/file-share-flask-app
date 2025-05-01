from flask import Flask, render_template, request
import boto3
from werkzeug.utils import secure_filename

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET = 'my-file-sharing-bucket-2025'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        s3.upload_fileobj(file, BUCKET, filename)
        url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': filename}, ExpiresIn=3600)
        return f'Download Link: <a href="{url}">{url}</a>'
    return 'Upload failed!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

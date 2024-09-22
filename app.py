'''from flask import Flask, request, render_template
import boto3
import os

app = Flask(__name__)

AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
BUCKET_NAME = ''

s3_client = boto3.client('s3', 
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        
        s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)
        imgix_url = f"https://virtusa-364861243.imgix.net/{file.filename}?mask=ellipse"
        return f'<img src="{imgix_url}" alt="Processed Image"/>'
    except Exception as e:
        return f'Error occurred: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
'''
from flask import Flask, request, render_template
import boto3
from dotenv import load_dotenv
import os

app = Flask(__name__)

# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = ''

s3_client = boto3.client('s3', 
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        # Upload to S3
        s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)

        # Read parameters from the form
        width = request.form.get('width', type=int)
        height = request.form.get('height', type=int)
        mask = request.form.get('mask', default='ellipse')
        fit  = request.form.get('fit', default='crop')
        bri = request.form.get('bri', default=0, type=int)
        mask_color = request.form.get('mask_color', default='#000000')
        mask_opacity = request.form.get('mask_opacity', default=100, type=int)
        # Construct Imgix URL
        imgix_url = f"https://virtusa-3641243.imgix.net/{file.filename}"
        params = []
        if width:
            params.append(f"w={width}")
        if height:
            params.append(f"h={height}")
        if mask:
            params.append(f"mask={mask}")
        if fit:
            params.append(f"fit={fit}")
        if bri:  # Include brightness adjustment
            params.append(f"bri={bri}")
        if mask_color and mask_opacity < 100:
            params.append(f"blend-color={mask_color.lstrip('#')}")  # Apply mask color
            params.append(f"blend-alpha={mask_opacity / 100}")  # Apply mask opacity (as a decimal)
            
        if params:
            imgix_url += "?" + "&".join(params) 

        return f'<img src="{imgix_url}" alt="Processed Image"/>'
    except Exception as e:
        return f'Error occurred: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)

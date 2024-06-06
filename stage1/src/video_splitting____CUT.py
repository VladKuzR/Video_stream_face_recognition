from boto3 import client
import os
import subprocess
import json

S3 = client('s3')
lmb = client('lambda')

def yhandler(event, context):
    uploaded_object_name = event['Records'][0]['s3']['object']['key']
    video_splitting_cmd(uploaded_object_name)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
	

def video_splitting_cmd(uploaded_object_name):
    filename = getting_video(uploaded_object_name)

    os.makedirs(f'/tmp/video_{filename}', exist_ok=True)
    os.makedirs(f'/tmp/output', exist_ok=True)

    split_cmd = 'ffmpeg -i ' + f'/tmp/video_{filename}/{filename}.mp4' +' -vframes 1 ' + f'/tmp/output/{filename}.jpg'

    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)

    uploading_photos(filename)
   

def getting_video(object_key):
    filename = object_key.split('.')[0] 
    os.makedirs(f'/tmp/video_{filename}', exist_ok=True)
    response = S3. download_file(
        '1230868550-input',
        object_key,
        f'/tmp/video_{filename}/{filename}.mp4'
    )
    return filename

def uploading_photos(filename):
    S3.upload_file(f'/tmp/output/{filename}.jpg', 
                '1230868550-stage-1', 
                f'{filename}.jpg')
    lmb.invoke(
        FunctionName = 'face-recognition', 
        InvocationType='Event', 
        Payload = json.dumps({"bucket_name":"1230868550-stage-1", "image_file_name":f'{filename}.jpg'}).encode('utf-8')
    )

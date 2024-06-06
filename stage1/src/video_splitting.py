from boto3 import client
import os
import subprocess

S3 = client('s3')

def handler(event, context):
    uploaded_object_name = event['Records'][0]['s3']['object']['key']
    video_splitting_cmd(uploaded_object_name)
	

def video_splitting_cmd(uploaded_object_name):
    video_file, filename = getting_video(uploaded_object_name)

    os.makedirs(f'/tmp/video_{filename}', exist_ok=True)
    os.makedirs(f'/tmp/{filename}', exist_ok=True)
    with open(f'/tmp/video_{filename}/{filename}.mp4', 'wb') as f:
        f.write(video_file)

    split_cmd = '/usr/bin/ffmpeg -ss 0 -r 1 -i ' + f'/tmp/video_{filename}/{filename}.mp4' + ' -vf fps=1/10 -start_number 0 -vframes 10 ' + '/tmp/' + filename + "/" + 'output-%02d.jpg -y'
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)

    uploading_photos(filename)
   

def getting_video(object_key):
    response = S3. get_object(
        Bucket='1230868550-input',
        Key = object_key 
    )
    video_file = response['Body'].read()
    return video_file, object_key.split('.')[0] 

def uploading_photos(filename):
    for item in os.listdir(f'/tmp/{filename}') :
        S3.upload_file(f'/tmp/{filename}/{item}', 
                    '1230868550-stage-1', 
                    f'{filename}/{item}')

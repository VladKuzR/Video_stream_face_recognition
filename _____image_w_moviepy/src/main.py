from boto3 import client
import os
from moviepy.editor import VideoFileClip
from PIL import Image
import json 

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

    video_clip = VideoFileClip(f'/tmp/video_{filename}/{filename}.mp4')
    duration = video_clip.duration
    frames_to_extract = 10
    for i in range(frames_to_extract):
        time = i * duration / frames_to_extract
        frame = video_clip.get_frame(time)
        frame_image = Image.fromarray(frame)
        frame_image.save(f'/tmp/{filename}/output-{i:02d}.jpg')

    video_clip.close()
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

import cv2
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import torch
import boto3
import io
import os

# os.environ["EASYOCR_MODULE_PATH"] = "/tmp"
# os.environ["MODULE_PATH"] = "/tmp"
# os.environ['TORCH_HOME'] = '/tmp/'


bucket_client = boto3.client('s3')





def handler(event, context):
   
    # event = {"bucket_name":"1230868550-stage-1", "image_file_name":"test_01.jpg"}
    image = getting_neccessary_data(event)
    image_path = '/tmp/'+ event["image_file_name"]
    predicted_person = face_recognition(image_path)


    response = bucket_client.put_object(
        Bucket = '1230868550-output', 
        Key = f"{event['image_file_name'].split('.')[0]}.txt", 
        Body = predicted_person
    )


def getting_neccessary_data(event):
    bucket_client.download_file(
        'torchvision-necessities',
        'data.pt', 
        '/tmp/data.pt'
    )

    response = bucket_client.download_file(
        event['bucket_name'],
        event['image_file_name'],
        f'/tmp/{event["image_file_name"]}'
    )
    # image_for_recognition = Image.open(io.BytesIO(response["Body"].read()))

    # return image_for_recognition



def face_recognition(key_path):
    mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
    resnet = InceptionResnetV1(pretrained='vggface2').eval() 
    image = cv2.imread(key_path)
    image = np.array(image)
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    face,prob = mtcnn(image, return_prob=True, save_path=None)
    saved_data = torch.load('/tmp/data.pt') 
    try:
        emb = resnet(face.unsqueeze(0)).detach()
        embedding_list = saved_data[0] 
        name_list = saved_data[1] 
        dist_list = []
        for idx, emb_db in enumerate(embedding_list):
            dist = torch.dist(emb, emb_db).item()
            dist_list.append(dist)
        idx_min = dist_list.index(min(dist_list))
        prediction = name_list[idx_min]
    except Exception as error:
        print('Error:', error)
    
    return prediction


handler({"bucket_name":"1230868550-stage-1", "image_file_name":"test_99.jpg"}, '')
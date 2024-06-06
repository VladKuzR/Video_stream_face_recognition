# Elastic Video Analysis Application

## Description
This project focuses on developing an elastic application for video analysis using AWS Lambda and other AWS services. The application is designed to automatically scale out and in on-demand, ensuring cost-effectiveness and efficient resource utilization. It offers a multi-stage pipeline for processing user-uploaded videos, incorporating video splitting and face recognition functionalities.

## How It Works
1. **User Uploads Video**: Users can upload videos to the application through a user-friendly interface.
2. **Video Splitting (Stage 1)**: Upon video upload, the application splits the video into individual frames using FFmpeg. Each frame is processed separately to facilitate efficient face recognition.
3. **Face Recognition (Stage 2)**: The extracted frames undergo face recognition using a pre-trained Convolutional Neural Network (CNN) model, specifically ResNet-34. This model is adept at detecting and recognizing faces with high accuracy.
4. **Output Storage**: The results of face recognition, including the names of recognized faces, are stored in an output bucket for easy access and retrieval.

## Components
- **Input Bucket**: Stores user-uploaded videos awaiting processing.
- **Stage-1 Bucket**: Intermediate storage for frames generated during video splitting.
- **Output Bucket**: Stores the results of face recognition, including the names of recognized faces.
- **Video-splitting Function**: AWS Lambda function responsible for splitting uploaded videos into frames and triggering face recognition.
- **Face-recognition Function**: AWS Lambda function that performs face detection and recognition on individual frames.

## Project Diagram
![Project Diagram](https://github.com/VladKuzR/Video_stream_face_recognition/assets/123952016/e5444b51-f553-4f01-b8e8-79cda47eee5a)

## Technologies Used
- **AWS Lambda**: Serverless computing service for executing code in response to triggers without provisioning or managing servers.
- **AWS S3**: Object storage service used for storing and retrieving data.
- **FFmpeg**: Open-source multimedia framework for handling video, audio, and other multimedia files.
- **ResNet-34**: Pre-trained Convolutional Neural Network model known for its effectiveness in image classification tasks, including face recognition.

## Setup
1. **AWS Configuration**: Set up an AWS account and configure Lambda functions, S3 buckets, and necessary permissions.
2. **Lambda Function Implementation**: Implement the video splitting and face recognition logic in the Lambda functions. Ensure proper error handling and logging for debugging and monitoring purposes.
3. **Trigger Configuration**: Configure triggers to initiate the processing pipeline upon video upload to the input bucket.
4. **Testing and Monitoring**: Test the application thoroughly using sample videos and monitor its performance and resource utilization using AWS CloudWatch or other monitoring tools.

## Usage
1. **Upload Video**: Users can upload videos through the application interface.
2. **Monitor Progress**: Track the progress of video processing through Lambda function logs and monitoring dashboards.
3. **Retrieve Results**: Once processing is complete, users can retrieve the results from the output bucket, which may include text files with the names of recognized faces.

## Acknowledgments
- This project was developed as part of the Cloud Computing course and serves as a practical application of serverless computing concepts.
- Special thanks to the AWS Lambda and S3 teams for providing robust and scalable services that facilitate the development of elastic applications.

## License
This project is licensed under the terms of the MIT license. You are free to use, modify, and distribute the code as per the MIT license agreement.

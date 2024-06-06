import subprocess
import json
import time

def create_lambda_from_docker_containter(docker_reprository_name, docker_tag, function_name,  aws_account_id, aws_role_arn,  region = 'us-east-1'):
    """
    Creates an AWS Lambda function from a Docker container.

    Parameters:
    - docker_repository_name (str): The name of the Docker repository.
    - docker_tag (str): The tag of the Docker image.
    - function_name (str): The name of the Lambda function to create.
    - aws_account_id (str): The AWS account ID.
    - aws_role_arn (str): The ARN of the IAM role for the Lambda function.
    - region (str, optional): The AWS region to use. Defaults to 'us-east-1'.

    Raises:
    - Exception: If any error occurs during the process.

    Note:
    - This function assumes that AWS CLI and Docker are properly installed and configured.
    - The function first builds the Docker image, then logs in to Amazon ECR, and finally creates the Lambda function.
    - If the repository with the specified name already exists in Amazon ECR, the function will use it; otherwise, it will create a new repository.
    """
    try:
        subprocess.run(f'docker build --platform linux/amd64 -t {docker_reprository_name}:{docker_tag} .', shell=True)
        subprocess.run(f'aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {aws_account_id}.dkr.ecr.us-east-1.amazonaws.com', shell=True)
        try:
            # Creating a repository in Amazon ECR. This line can fail if reprository with this name exist
            result = subprocess.run(f'aws ecr create-repository --repository-name {function_name} --region {region} --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE', shell=True, capture_output=True, text=True)
            repository_uri  = json.loads(result.stdout)['repository']['repositoryUri']
            print(result, repository_uri)
        except Exception as e:
            repository_uri = f'{aws_account_id}.dkr.ecr.{region}.amazonaws.com/{function_name}'
            print(e)
        
        subprocess.run(f'docker tag {docker_reprository_name}:{docker_tag} {repository_uri}:latest', shell=True)
        subprocess.run(f'docker push {repository_uri}:latest', shell=True)
        subprocess.run(f'aws lambda create-function --function-name {function_name} --package-type Image --code ImageUri={repository_uri}:latest --role {aws_role_arn}', shell=True)
        time.sleep(40)
        subprocess.run(f'aws lambda update-function-configuration --function-name {function_name} --timeout 300 --memory-size 1024', shell=True)
    except Exception as e:
        print("An exception occured", e)

    
create_lambda_from_docker_containter('face-recognition', 'initial', 'face-recognition', '533267346617', 'arn:aws:iam::533267346617:role/lambda-role')
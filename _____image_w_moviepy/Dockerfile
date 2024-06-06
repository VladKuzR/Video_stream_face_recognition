FROM  public.ecr.aws/lambda/python:3.11

RUN yum update -y

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY src/* ${LAMBDA_TASK_ROOT}

# Set the CMD to the handler 
CMD [ "main.handler" ]
# Define global args
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.12"
ARG DISTRO_VERSION="3.12"

FROM alpine:latest
FROM python:${RUNTIME_VERSION}-slim AS python-alpine

RUN python${RUNTIME_VERSION} -m pip install --upgrade pip

FROM python-alpine AS build-image

# Include global args in this stage of the build
ARG FUNCTION_DIR
ARG RUNTIME_VERSION
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Install Lambda Runtime Interface Client for Python
RUN python${RUNTIME_VERSION} -m pip install awslambdaric --target ${FUNCTION_DIR}

# Stage 3 - final runtime image
# Grab a fresh copy of the Python image
FROM python-alpine
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie

COPY src/torch-2.2.2+cpu-cp312-cp312-linux_x86_64.whl ${FUNCTION_DIR}
COPY src/torchvision-0.17.2+cpu-cp312-cp312-linux_x86_64.whl ${FUNCTION_DIR}

RUN pip install ${FUNCTION_DIR}torch-2.2.2+cpu-cp312-cp312-linux_x86_64.whl --target ${FUNCTION_DIR}
RUN pip install --find-links . ${FUNCTION_DIR}torchvision-0.17.2+cpu-cp312-cp312-linux_x86_64.whl --target ${FUNCTION_DIR}

# RUN apt-get update && apt-get install -y python3-opencv

# RUN apt-get update && apt-get install facenet-pytorch
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt ${FUNCTION_DIR}


RUN python3.12 -m pip install --find-links . -r requirements.txt --target ${FUNCTION_DIR}

# Copy function code
COPY src/face_recognition.py ${FUNCTION_DIR}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "face_recognition.handler" ]
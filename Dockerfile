FROM continuumio/anaconda3

RUN apt-get update -y
RUN apt-get install -y --fix-missing \
    build-essential \
    ffmpeg libsm6 libxext6  -y && apt-get clean && rm -rf /tmp/* /var/tmp/*

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install cmake && pip install dlib && pip install opencv-python && pip install -r requirements.txt

COPY ./app /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
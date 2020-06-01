FROM tensorflow/tensorflow:latest-py3

MAINTAINER gil kedar "gilkedar1@gmail.com"

# RUN apt-get update -y && \
#     apt-get install -y python3-pip python3-dev


WORKDIR /

COPY . /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# RUN pip3 install tensorflow
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip3 install opencv-python

ENV MQTT_TOKEN_IP=amqp://wksnlndm:v7PjBqPlqjI2xDlFsgFaQx2EL4hqAq27@roedeer.rmq.cloudamqp.com/wksnlndm

ENV PYTHONPATH=.

ENTRYPOINT [ "python3" ]

EXPOSE 5000

CMD [ "Server/HttpServer.py" ]

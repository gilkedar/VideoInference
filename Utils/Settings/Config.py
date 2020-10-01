import os

# Project
PROJECT_NAME = "VideoInference"

# Environment Variables
ENV_VAR_MQTT_TOKEN = "MQTT_TOKEN_IP"

#localHost
LOCALHOST_IP = "127.0.0.1"
GLOBAL_IP = "0.0.0.0"
HTTP_PORT = 5000
ZMQ_PORT = 5555

# Image Protocol
PROTOCOL_HTTP = "http"
PROTOCOL_MQTT = "mqtt"
PROTOCOL_ZMQ = "zmq"

# Algorithm Choices
ALGORITHM_DETECT_FACES = "detect_faces"
ALGORITHM_DETECT_OBJECTS = "detect_objects"
ALGORITHM_IS_SANTA = "is_santa"

# Algorithms Models Path
PROJECT_PATH = os.path.dirname(os.path.abspath(os.curdir))
MODELS_PATH = os.path.join(PROJECT_PATH, "Utils", "Models")
MODEL_PATH_IS_SANTA_ALGORITHM = os.path.join(MODELS_PATH, ALGORITHM_IS_SANTA, "is_santa.model")
MODEL_PATH_DETECT_FACES_ALGORITHM = os.path.join(MODELS_PATH, ALGORITHM_DETECT_FACES, "detect_faces.caffemodel")
MODEL_PATH_DETECT_FACES_PROTOTEXT_ALGORITHM = os.path.join(MODELS_PATH,ALGORITHM_DETECT_FACES, "deploy.prototxt.txt")

# MQTT Parameters
MQTT_TOPIC_NAME = "InferenceReplyTest2"
MQTT_SERVER_IP = ""  # will be set from env var


# Input parameters
INPUT_PARAM_VIDEO_FILE_NAME = "videofile"
INPUT_PARAM_ALGORITHM_NAME = "algorithm"
INPUT_PARAM_IP_ADDRESS_NAME = "ip"
INPUT_PARAM_PROTOCOL_NAME = "protocol"

# Frames to skip
FRAMES_TO_SKIP_DEFAULT = 10
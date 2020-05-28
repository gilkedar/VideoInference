
# Project
PROJECT_NAME = "InferenceReply"

# Environment Variables
ENV_VAR_MQTT_TOKEN = "MQTT_TOKEN_IP"

#localHost
LOCALHOST_IP = "127.0.0.1"

# Image Protocol
PROTOCOL_HTTP = "http"
PROTOCOL_MQTT = "mqtt"
PROTOCOL_ZMQ = "zmq"

# Algorithm Choices
ALGORITHM_DETECT_FACES = "detect_faces"
ALGORITHM_DETECT_OBJECTS = "detect_objects"
ALGORITHM_IS_SANTA = "is_santa"

# Algorithms Models Path
MODEL_PATH_IS_SANTA_ALGORITHM = "/path/to/bucket"

# MQTT Parameters
MQTT_TOPIC_NAME = "InferenceReply"
MQTT_SERVER_IP = ""  # will be set from env var

# HTTP Parameters
HTTP_DEFAULT_PORT = "80"

# Input parameters
INPUT_PARAM_VIDEO_FILE_NAME = "videofile"
INPUT_PARAM_ALGORITHM_NAME = "algorithm"
INPUT_PARAM_IP_ADDRESS_NAME = "ip"
INPUT_PARAM_PROTOCOL_NAME = "protocol"
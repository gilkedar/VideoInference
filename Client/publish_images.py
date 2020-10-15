from imutils.video import VideoStream
import time
import cv2
import threading
import requests
import argparse
import datetime
import base64

from concurrent.futures import ThreadPoolExecutor

# -i https://6mfe1xgzk9.execute-api.eu-central-1.amazonaws.com/dev/detect-faces -p 5000

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, required=True, help="ip address of the device")
ap.add_argument("-p", "--port", type=str, required=True, help="ephemeral port number of the server (1024 to 65535)")
ap.add_argument("-a", "--api", type=str, required=False,default="", help="enter the desired API uri")
args = vars(ap.parse_args())

# request_lock = threading.Lock()
# last_frame = None

headers = {'Content-Type': 'image/jpeg',
           'user_id': "gilkedar",
           'algorithm': "detect_faces"}
# address = "http://{}:{}{}".format(args["ip"], args["port"], args["api"])
address = args["ip"]
request_id = 0


# def publish_image():
#     global headers
#     global request_id
#
#     if last_frame:
#         with request_lock:
#             data, frame_num = last_frame[0], last_frame[1]
#             request_id += 1
#             headers['request_id'] = "{} - {}".format(request_id, datetime.datetime.now().strftime("%H:%M:%S.%f"))
#             print(f"{request_id}/{frame_num}")
#         if data:
#             start_time = time.time()  # start time of the loop
#             ans = requests.post(address, data=data, headers=headers)
#             print(ans)
#             print("FPS: ", 1.0 / (time.time() - start_time))  # FPS = 1 / time to process loop
#

def publish_image(frame, frame_id):
    global headers
    headers['request_id'] = "{} - {}".format(frame_id, datetime.datetime.now().strftime("%H:%M:%S.%f"))
    print(f"publishing {frame_id}")
    print(type(frame))
    ans = requests.get(address, data=frame, headers=headers)
    print(ans)
    print(ans.text)


def gen():
    """Video streaming generator function."""
    global last_frame
    vs = VideoStream(src=0).start()
    # time.sleep(2.0)
    counter = 0
    while True:
        start_time = time.time()  # start time of the loop
        frame = vs.read()
        # resized = cv2.resize(frame, (10,10))
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        # bytes_str = base64.b64encode(encodedImage)
        bytes_str = encodedImage.tostring()
        counter += 1
        publish_image(bytes_str, counter)
        print("FPS: ", 1.0 / (time.time() - start_time))  # FPS = 1 / time to process loop

        # with ThreadPoolExecutor(max_workers=2) as executor:
        #     print("sending {} ".format(counter))
        #     executor.submit(publish_image, data=bytes_str, address=address, frame_num=counter)
        # time.sleep(0.025)
        

if __name__ == '__main__':
    gen()

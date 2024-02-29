import cv2

import SharedArray as sa

from os.path import isdir
from os import mkdir

LOCK_FOLDER = ".lock"

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#get the first frame to calculate size
success, frame = cap.read()
if not success:
    raise Exception("error reading from video")

shm = sa.create("shm://vcam", frame.shape, frame.dtype)

mkdir(LOCK_FOLDER)

try: #use keyboardinterrupt to quit
    while True:
        _, frame_buffer = cap.read()
        shm[:] = frame_buffer[:]
        # cv2.imshow("vcam", shm)
        # cv2.imwrite("frame.jpg", frame_buffer)
        # cv2.waitKey(1)
except KeyboardInterrupt:
    while isdir(LOCK_FOLDER):
        _, frame_buffer = cap.read()
        shm[:] = frame_buffer[:]
        # cv2.imshow("vcam", frame_buffer)
        # cv2.waitKey(1)
    cap.release()
    cv2.destroyWindow("vcam")
    sa.delete("vcam")
    raise SystemExit

#cleanup: IMPORTANT, close this one first so the reader doesn't unlink() the 
#  shm's before this file has exited. (less important on windows)
cap.release()
sa.delete("vcam")
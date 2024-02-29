import cv2
from sys import argv
import vcam_reader

buffer = vcam_reader.init(argv[1])

try:
    while True:
        cv2.imshow(argv[1], buffer)
        cv2.waitKey(1)
except KeyboardInterrupt:
    cv2.destroyWindow(argv[1])

vcam_reader.close()
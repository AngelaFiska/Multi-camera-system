from __future__ import print_function
from pyimagesearch.panorama import Stitcher
from imutils.video import VideoStream
import numpy as np
import datetime
import imutils
import time
import cv2

#Open usb cameras
cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(2)


#Check that cameras are successfully opened
if not cap.isOpened():
    print("Cannot open camera")
    exit()

if not cap1.isOpened():
    print("Cannot open camera")
    exit()

#Cameras calibration matrices
mtx =  np.array([[172.28231029,   0.     , 241.19984617],
                [ 0.     , 148.44457164, 165.515938],

                [0.000000, 0.000000, 1.000000]])
#camera n. 2
mtx1 =  np.array([[165.69174951,   0.     , 235.75765473],
                [   0.     , 142.70331794 , 162.66566056],
                [0.000000,  0.000000   ,   1. ]])

#Cameras distortion coefficients
dist = np.array([0.26670017, -0.28340368, -0.00173503, 0.00133823, 0.07382795 ])

dist1 = np.array([2.47365041e-01, -2.26491927e-01 , 5.67906105e-04,  3.96464345e-05, 5.40686533e-02])


stitcher = Stitcher()
total = 0
img_array = []
i = 0
count = 0
count1 = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret1, frame1= cap1.read()
    # if frame is read correctly ret and ret1 are True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    if not ret1:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    h,  w = frame.shape[:2]

    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    newcameramtx1, roi1=cv2.getOptimalNewCameraMatrix(mtx1,dist1,(w,h),1,(w,h))
    #undistort and crop the images
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)

    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    h,  w = frame1.shape[:2]

    dst1 = cv2.undistort(frame1, mtx1, dist1, None, newcameramtx1)

    x,y,w,h = roi1
    dst1 = dst1[y:y+h, x:x+w]

    cv2.imshow("dist", dst)
    cv2.imshow("dis1", dst1)
    print("[INFO] stitching images...")
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch([dst, dst1])
    # if the status is '0', then OpenCV successfully performed image
# stitching

    if status == 0:
	# uncomment the follow to write the output stitched image to disk
        # cv2.imwrite("image"+str(count)+".jpg", stitched)
    #     cv2.imwrite("left"+str(count)+".jpg", dst1)
    #     cv2.imwrite("right"+str(count)+".jpg", dst)
        # display the output stitched image to our screen
        cv2.imshow("Stitched", stitched)
        count = count + 1

# otherwise the stitching failed, likely due to not enough keypoints)
# being detected
    else:
	       print("[INFO] image stitching failed ({})".format(status))

    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
height, width, layers = stitched.shape
size = (width,height)

out.release()
cap.release()
cv2.destroyAllWindows()

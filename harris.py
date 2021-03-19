import matplotlib.pyplot as plt
import numpy as np
import cv2

image = cv2.imread('./fisheye1.png')
image_copy = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(image_copy, cv2.COLOR_RGB2GRAY)
fx, plots = plt.subplots(1, 2, figsize=(20,10))

plots[0].set_title("Orignal Image")
plots[0].imshow(image_copy)
plots[1].set_title("Gray Image")
plots[1].imshow(gray, cmap="gray") 

gray = cv2.cvtColor(image_copy, cv2.COLOR_RGB2GRAY)
gray = np.float32(gray)

dst = cv2.cornerHarris(gray, 2, 3, 0.04)
dst = cv2.dilate(dst,None)

plt.imshow(dst, cmap='gray')

thresh = 0.1*dst.max()
corner_image = np.copy(image_copy)
for j in range(0, dst.shape[0]):
    for i in range(0, dst.shape[1]):
        if(dst[j,i] > thresh):
            cv2.circle( corner_image, (i, j), 1, (0,255,0), 1)

print("Number of keypoints Detected In The Image: ", len(dst) )
plt.show()


import cv2
import imutils
import numpy as np
import specularity as spc  
import matplotlib.pyplot as plt
from imutils import contours
from imutils import perspective
from scipy.spatial.distance import euclidean


images = ("figs/figures1.jpeg")  
read = cv2.imread(images)
gray_img = spc.derive_graym(images)

r_img = m_img = np.array(gray_img)

rimg = spc.derive_m(read, r_img)
s_img = spc.derive_saturation(read, rimg)
spec_mask = spc.check_pixel_specularity(rimg, s_img)
enlarged_spec = spc.enlarge_specularity(spec_mask)
    
radius = 60
telea = cv2.inpaint(read, enlarged_spec, radius, cv2.INPAINT_TELEA)
ns = cv2.inpaint(read, enlarged_spec, radius, cv2.INPAINT_NS)
cv2.imwrite('figs/Impainted_telea.png',telea)
cv2.imwrite('figs/Impainted_ns.png',ns)
cv2.waitKey(0)

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[0] + ptB[0]) * 0.5)

def show_images(images): 
    for i, image in enumerate(images):
        cv2.imshow("Original" + str(i), image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
images = ("figs/Impainted_telea.png")  
read = cv2.imread(images)
read = cv2.resize(read, (600, 400), interpolation=cv2.INTER_AREA)

_, mask = cv2.threshold(read, 220, 220, cv2.THRESH_BINARY_INV)
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2)) 

gray = cv2.cvtColor(read, cv2.IMREAD_GRAYSCALE)
morh = cv2.cvtColor(read, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(blur, 100, 200)
dilate = cv2.dilate(edged, kernal, iterations=1)
erode = cv2.erode(edged, kernal, iterations=1)

counts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
counts = imutils.grab_contours(counts)

print("Total number of contours are: ", len(counts))

(counts, _) = contours.sort_contours(counts)
counts = [x for x in counts if cv2.contourArea(x) > 100]

objects =counts[0]
border = cv2.minAreaRect(objects)
border = cv2.boxPoints(border)
border = np.array(border, dtype="int")
border = perspective.order_points(border)
(tl, tr, br, bl) = border
dist_in_pixel = euclidean(tl, tr)
dist_in_cm = 2
pixel_per_cm = dist_in_pixel / dist_in_cm

for count in counts:
    border = cv2.minAreaRect(count)
    border = cv2.boxPoints(border)
    border = np.array(border, dtype="int")
    border = perspective.order_points(border)
    (tl, tr, br, bl) = border
    cv2.drawContours(morh, [border.astype("int")], -1, (0, 0, 255), 2)
    mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0]) / 2), tl[1] + int(abs(tr[1] - tl[1]) / 2))
    mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0]) / 2), tr[1] + int(abs(tr[1] - br[1]) / 2))
    width  = euclidean(tl, tr)
    length = euclidean(tr, br)

    cv2.line(border, (0,0), (150,150), (255,255,255), 15)
    cv2.rectangle(border, (15,25), (200, 150), (0,255,0), 5)
    cv2.circle(border, (100,63), 55, (0,0,255), -1)
    cv2.putText(morh, "{:.1f} px".format(width), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    cv2.putText(morh , "{:.1f} px".format(length), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2) 

    print("Total contours processed: ", counts)
    
    plt.subplot(121),plt.imshow(read),plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(blur),plt.title('Blurred')
    plt.xticks([]), plt.yticks([])
    cv2.imwrite("figs/output_telea.png", edged)
    cv2.imwrite("figs/output_ns.png", morh)
    cv2.imshow("Egded", edged)
    cv2.imshow("Morh", morh)
    cv2.waitKey(0)
    show_images([read])

    













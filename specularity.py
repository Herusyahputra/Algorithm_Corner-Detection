
import cv2
import numpy as np

def derive_graym(impath):
    return cv2.imread(impath, cv2.IMREAD_GRAYSCALE)

def derive_m(img, rimg):
    (rw, cl, ch) = img.shape
    for r in range(rw):
        for c in range(cl):
            rimg[r,c] = int(np.sum(img[r,c])/3.0)
            
    return rimg

def derive_saturation(img, rimg):
    s_img = np.array(rimg)
    (r, c) = s_img.shape
    for ri in range(r):
        for ci in range(c):
            s1 = img[ri,ci][0] + img[ri,ci][2]
            s2 = 2 * img[ri,ci][1] 
            if  s1 >=  s2:
                s_img[ri,ci] = 1.5*(img[ri,ci][2] - rimg[ri,ci])
            else:
                s_img[ri,ci] = 1.5*(rimg[ri,ci] - img[ri,ci][0])

    return s_img

def check_pixel_specularity(mimg, simg):
    m_max = np.max(mimg) * 0.5
    s_max = np.max(simg) * 0.33

    (rw, cl) = simg.shape
    spec_mask = np.zeros((rw,cl), dtype=np.uint8)
    for r in range(rw):
        for c in range(cl):
            if mimg[r,c] >= m_max and simg[r,c] <= s_max:
                spec_mask[r,c] = 255
    
    return spec_mask

def enlarge_specularity(spec_mask):
    win_size, step_size = (3,3), 1
    enlarged_spec = np.array(spec_mask)
    for r in range(0, spec_mask.shape[0], step_size):
        for c in range(0, spec_mask.shape[1], step_size):
            win = spec_mask[r:r + win_size[1], c:c + win_size[0]]
            
            if win.shape[0] == win_size[0] and win.shape[1] == win_size[1]:
                if win[1,1] !=0:
                    enlarged_spec[r:r + win_size[1], c:c + win_size[0]] = 255 * np.ones((3,3), dtype=np.uint8)

    return enlarged_spec 




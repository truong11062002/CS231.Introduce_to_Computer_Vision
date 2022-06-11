import cv2
import imageio
from seam import SeamCarve
from mask import Mask
img = cv2.imread("over9_2.jpg")

m = Mask(img)
m.Create_remove_mask()
cv2.imshow('remove_mask',m.mask_remove)
cv2.waitKey(0)
cv2.imwrite('maskr.jpg', m.mask_remove)

maskr = cv2.imread('maskr.jpg', 0) != 255
'''
m.Create_protect_mask()
cv2.imshow('protect_mask',m.mask_protect)
cv2.waitKey(0)
m.Delete_union()
cv2.imwrite('maskp.jpg',m.mask_protect)

maskp = cv2.imread('maskp.jpg', 0) != 255
'''
H,W = img.shape[:2]
sc_img = SeamCarve(img)
#sc_img.remove_mask(maskr,maskp)
sc_img.remove_mask(maskr)
cv2.destroyAllWindows()
cv2.imwrite('result_without_resize.jpg',sc_img.image())
sc_img.resize(H,W)
cv2.destroyAllWindows()
cv2.imwrite('result_resized.jpg',sc_img.image())
imageio.mimsave('over9_2.gif',sc_img.visual,fps = 60)




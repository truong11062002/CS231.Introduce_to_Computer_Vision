import cv2
import imageio
import os 
img1 = cv2.imread("messi-1488.jpg")
# img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

img2 = cv2.imread("images.jpg")
# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

# Lấy kích thước của ảnh
h1,w1,c1 = img1.shape
h2,w2,c2 = img2.shape

#Lưu vào h chiều cao, w chiều rộng nhỏ nhất giữa 2 ảnh

h = min(h1,h2)
w = min(w1,w2)

# Thay đổi kích thước ảnh theo w,h

img1 = cv2.resize(img1,(w,h))
img2 = cv2.resize(img2,(w,h))

cv2.imshow("Anh 1", img1)
cv2.imshow("Anh 2", img2)

results = []
line = 6 # chia ra thanh 6 line
h1 = h1 
speed = 6

for D in range(0, w+1, speed):
    result=img1.copy()
    for L in range(0, line, 2):
        result[h1*L:h1*(L+1), 0:D, :] = img1[h1*L:h1*(L+1), w - D:w, :]
        result[h1*L:h1*(L+1), D:w, :] = img2[h1*L:h1*(L+1), 0:w - D]
        result[h1*(L+1):h1*(L+2), 0:w - D, :] = img2[h1*(L+1):h1*(L+2), D:w, :]
        result[h1*(L+1):h1*(L+2), w - D:w, :] = img1[h1*(L+1):h1*(L+2), 0:D, :]
        results.append(result)
        
imageio.mimsave('Soccer_comb.gif', results)
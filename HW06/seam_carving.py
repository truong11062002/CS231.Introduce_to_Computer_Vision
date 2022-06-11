
import sys
import cv2
from matplotlib import scale
from matplotlib.pyplot import axis
import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve
from tqdm import trange

"""
Thuật toán sẽ thực hiện các bước sau:
1. Gán mỗi giá trị năng lượng cho mỗi pixel
2. Tìm một đường nối 8 điểm ảnh có ít năng lượng nhất
3. Xóa tất cả pixel trong đường nối
4. Lặp lại từ bước 1 -> 3 cho đến khi các dòng/ cột mong muốn bị xóa
"""

# Energy map
def calc_energy(img):
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])

    # Convert filter 2D thành filter 3D
    filter_du = np.stack([filter_du] * 3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])

    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # Sum the energies
    energy_map = convolved.sum(axis = 2)

    return energy_map
    
# Lặp lại cho mọi cột 

def crop_c(img, scale_c):
    r, c, _ = img.shape
    new_c = int(scale_c * c)

    for i in trange(c - new_c):
        img = carve_column(img)

    return img

def crop_r(img, scale_r):
    img = np.rot90(img, 1, (0, 1))
    img = crop_c(img, scale_r)
    img = np.rot90(img, 3, (0, 1))
    return img

# Xóa những pixels từ đường seem với mức năng lượng thấp nhất
def carve_column(img):
    r, c, _ = img.shape

    M, backtrack = minimum_seam(img)
    mask = np.ones((r, c), dtype=np.bool)

    j = np.argmin(M[-1])
    for i in reversed(range(r)):
        mask[i, j] = False
        j = backtrack[i, j]

    mask = np.stack([mask] * 3, axis=2)
    img = img[mask].reshape((r, c - 1, 3))
    return img

# Tìm đường seam ít tốn energy nhất
def minimum_seam(img):
    r, c, _ = img.shape
    energy_map = calc_energy(img)

    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype=np.int)

    for i in range(1, r):
        for j in range(0, c):
            # Giải quyết cạnh trái của ảnh
            if j == 0:
                idx = np.argmin(M[i - 1, j:j + 2])
                backtrack[i, j] = idx + j
                min_energy = M[i - 1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy

    return M, backtrack

scale = float(sys.argv[1])
in_filename = sys.argv[2]
out_filename = sys.argv[3]

# Kết quả đầu ra em lưu với tên cropped.png
img = imread(in_filename)
out = crop_c(img, scale)
imwrite(out_filename,out)

# Thể hiện kích thước ảnh ban đầu và lúc sau
first_img = cv2.imread('image.png', 1)
print("Kich thuoc anh ban dau: ",first_img.shape)

cropped_img = cv2.imread('cropped.png', 1)
print('Kich thuoc anh sau khi dung seam carving giam 50% kich thuoc chieu rong: ', cropped_img.shape)

# Show image
cv2.imshow("Image ban dau: ",first_img)
cv2.imshow("Image ban sau khi crop: ",cropped_img)
cv2.waitKey(0)

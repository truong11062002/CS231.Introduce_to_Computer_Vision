import cv2
import imageio
# đọc ảnh forground

fg = cv2.imread(r'C:\Users\WINDOWS 10\Desktop\image-processing\HW04\fg.jpg')
h_fg, w_fg, c_fg = fg.shape
fg = cv2.cvtColor(fg, cv2.COLOR_BGR2RGB)
# đọc ảnh mask
mask = cv2.imread(r'C:\Users\WINDOWS 10\Desktop\image-processing\HW04\mask.png', cv2.IMREAD_UNCHANGED)
mask = cv2.resize(mask, (w_fg,h_fg))
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

url = "https://media0.giphy.com/media/2vmiW6mcYgKst3QVDK/giphy.gif"
frames = imageio.mimread(imageio.core.urlopen(url).read(), '.gif')

# Chuẩn hóa background
fg_h, fg_w, fg_c = fg.shape
bg_h, bg_w, bg_c = frames[0].shape
top = int((bg_h-fg_h)/2)
left = int((bg_w-fg_w)/2)
bgs = [frame[top: top + fg_h, left:left + fg_w, 0:3] for frame in frames]

# Xử lí pha trộn ảnh với hiệu ứng 
results = []
alpha = 0.3
for i in range(len(bgs)):
    result = fg.copy()
    result[mask[:,:,0:3] != 0] = alpha * result[mask[:,:,0:3] != 0]
    bgs[i][mask[:,:,0:3] == 0] = 0
    bgs[i][mask[:,:,0:3] != 0] = (1-alpha)*bgs[i][mask[:,:,0:3] != 0]
    result = result + bgs[i]
    results.append(result)

imageio.mimsave('result_2.gif', results)
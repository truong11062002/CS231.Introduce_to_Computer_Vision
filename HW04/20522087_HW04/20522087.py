import cv2
import numpy as np
import glob
import os
import random
from cv2 import VideoWriter
class Image:
    def __init__(self, filename, time=500, size=500):
        self.size = size
        self.time = time
        self.shifted = 0.0
        self.img = cv2.imread(filename)
        self.height, self.width, _ = self.img.shape
        if self.width < self.height:
            self.height = int(self.height*size/self.width)
            self.width = size
            self.img = cv2.resize(self.img, (self.width, self.height))
            self.shift = self.height - size
            self.shift_height = True
        else:
            self.width = int(self.width*size/self.height)
            self.height = size
            self.shift = self.width - size
            self.img = cv2.resize(self.img, (self.width, self.height))
            self.shift_height = False
        self.delta_shift = self.shift/self.time

    def reset(self):
        if random.randint(0, 1) == 0:
            self.shifted = 0.0
            self.delta_shift = abs(self.delta_shift)
        else:
            self.shifted = self.shift
            self.delta_shift = -abs(self.delta_shift)

    def get_frame(self):
        if self.shift_height:
            roi = self.img[int(self.shifted):int(self.shifted) + self.size, :, :]
        else:
            roi = self.img[:, int(self.shifted):int(self.shifted) + self.size, :]
        self.shifted += self.delta_shift
        if self.shifted > self.shift:
            self.shifted = self.shift
        if self.shifted < 0:
            self.shifted = 0
        return roi

video=VideoWriter('video_2.avi',cv2.VideoWriter_fourcc('M','J','P','G'),90,(500,500)) 
def process():
    path = "image"
    filenames = glob.glob(os.path.join(path, "*"))

    cnt = 0
    images = []
    for filename in filenames:
        print(filename)

        img = Image(filename)

        images.append(img)
        if cnt > 300:
            break
        cnt += 1

    prev_image = images[random.randrange(0, len(images))]
    prev_image.reset()

    while True:
        while True:
            img = images[random.randrange(0, len(images))]
            if img != prev_image:
                break
        img.reset()

        for i in range(100):
            alpha = i/100
            beta = 1.0 - alpha
            dst = cv2.addWeighted(img.get_frame(), alpha, prev_image.get_frame(), beta, 0.0)
            video.write(dst)
            cv2.imshow("Slide", dst)
            if cv2.waitKey(1) == ord('q'):
                return

        prev_image = img
        for _ in range(300):
            frame = img.get_frame()
            cv2.imshow("Slide", frame)
            video.write(frame)
            if cv2.waitKey(1) == ord('q'):
                video.release()
                return


process()
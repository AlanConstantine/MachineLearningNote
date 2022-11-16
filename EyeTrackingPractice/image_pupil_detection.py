# -*- coding: utf-8 -*-
# @Author: Jennifer WU
# @Date: 2022-11-14 23:52:26

import os
import cv2
import operator
import numpy as np
from argparse import ArgumentParser
from PIL import Image


class pupil_detection():
    def __init__(self, image_path, if_show=True):
        '''
        initialize the class and set the class attributes
        '''
        self._img = None
        self._img_path = image_path
        self._pupil = None
        self._centroid = None
        self.center = None
        self.if_show = if_show
        
    def load_image(self):
        '''
        load the image based on the path passed to the class
        it should use the method cv2.imread to load the image
        it should also detect if the file exists
        '''
        self._img = cv2.imread(self._img_path)
        # If the image doesn't exists or is not valid then imread returns None
        if type(self._img) == None:
            return False
        else:
            return True
    
    def show_image (self, img):
        cv2.imshow("Result", img)
        cv2.waitKey(0)
    
    def centroid (self):
        # convert image to grayscale image
        gray_image = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # convert the grayscale image to binary image
        ret, thresh = cv2.threshold(gray_image,127,255,0)
        # calculate moments of binary image
        M = cv2.moments(thresh)
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        self._centroid = (cX,cY)
        #cv2.circle(self._img, (cX, cY), 5, (255, 255, 255), -1)
        
    def detect_pupil (self):
        dst = cv2.fastNlMeansDenoisingColored(self._img,None,10,10,7,21)
        blur = cv2.GaussianBlur(dst,(5,5),0)
        inv = cv2.bitwise_not(blur)
        thresh = cv2.cvtColor(inv, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((2,2),np.uint8)
        erosion = cv2.erode(thresh,kernel,iterations = 1)
        ret,thresh1 = cv2.threshold(erosion,210,255,cv2.THRESH_BINARY)
        cnts, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        flag = 10000
        final_cnt = None
        for cnt in cnts:
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            distance = abs(self._centroid[0]-x)+abs(self._centroid[1]-y)
            if distance < flag :
                flag = distance
                final_cnt = cnt
            else:
                continue
        (x,y),radius = cv2.minEnclosingCircle(final_cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(self._img, center, radius, (0, 255, 0), 2)
        cv2.circle(self._img, (0, 0), radius, (0, 0, 255), 2)

        self.center = (x ,y)
        
        self._pupil = (center[0],center[1],radius)
        if self.if_show:
            self.show_image(self._img)
        
    def start_detection(self):
        if(self.load_image()):
            self.centroid()
            self.detect_pupil()
            print(self.center)
        else:
            print('Image file "' + self._img_path + '" could not be loaded.')
        return self.center

 
def resize(img, size):
    # 先创建一个目标大小的幕布，然后将放缩好的图片贴到中央，这样就省去了两边填充留白的麻烦。
    canvas = Image.new("RGB", size=size, color="#7777")  
    
    target_width, target_height = size
    width, height = img.size
    offset_x = 0
    offset_y = 0
    if height > width:              # 高 是 长边
        height_ = target_height     # 直接将高调整为目标尺寸
        scale = height_ / height    # 计算高具体调整了多少，得出一个放缩比例
        width_ = int(width * scale) # 宽以相同的比例放缩
        offset_x = (target_width - width_) // 2     # 计算x方向单侧留白的距离
    else:   # 同上
        width_ = target_width
        scale = width_ / width
        height_ = int(height * scale)
        offset_y = (target_height - height_) // 2
 
    img = img.resize((width_, height_), Image.BILINEAR) # 将高和宽放缩
    canvas.paste(img, box=(offset_x, offset_y))         # 将放缩后的图片粘贴到幕布上
    # box参数用来确定要粘贴的图片左上角的位置。offset_x是x轴单侧留白，offset_y是y轴单侧留白，这样就能保证能将图片填充在幕布的中央
    
    return canvas

def distance_bearing(x, y):
    x1 = x / 10
    y1 = y / 10
    return x1, y1

def main():
    img_folder = r'D:/Desktop/'
    parser = ArgumentParser(description='')
    parser.add_argument('--img', type=str, required=True,
                        help='image path', default='4.jpg')
    parser.add_argument('--show', type=bool, help='if show result image',
                        default=True)

    args = parser.parse_args()

    img_path = Image.open(os.path.join(img_folder, args.img))
 
    target__size=(1000, 1000)  # 目标尺寸：宽为500，高为300
    res = resize(img_path, target__size)

    resize_path = os.path.join(img_folder, 'tmp.jpg')
    
    res.save(resize_path)

    img_path = args.img
    if_show = args.show
    id = pupil_detection(resize_path, if_show)
    x, y = id.start_detection()
    x1, y1 = distance_bearing(x, y)
    print(x1, y1)
    try:
        os.remove(resize_path)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()


# In[ ]:


# return x and y
# check 10 pix 


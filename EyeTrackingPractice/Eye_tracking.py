# -*- coding: utf-8 -*-
# @Author: Jennifer WU
# @Date: 2022-11-15 07:29:56


# https://blog.csdn.net/HC_wood/article/details/107060689
# https://www.bilibili.com/video/av333798098/



import cv2
import numpy as np


# In[2]:


# cap = cv2.VideoCapture('J:/吴恭俭/实验/eye tracking/WIN_20221107_16_58_41_Pro.mp4')


# In[5]:


# import cv2
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    exit()

# import cv2
# cap = cv2.VideoCapture(r"C:/Users/ngkk0/OneDrive/Desktop/实验/eye tracking/Christopher's eyes/WIN_20221107_16_58_41_Pro.mp4")
# import cv2
# cap = cv2.VideoCapture(1)
# if not cap.isOpened():
#     exit()  

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame,(800, 800))
    rows,cols,_ = frame.shape
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame,(7,7),0)#高斯滤波
    # _, threshold = cv2.threshold(gray_frame, 28, 255, cv2.THRESH_BINARY_INV)#设置灰度值
    _, threshold = cv2.threshold(gray_frame, 50, 255, cv2.THRESH_BINARY_INV)#设置灰度值

    
    # threshold = cv2.adaptiveThreshold(gray_frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2) 
#     _,threshold = cv2.adaptiveThreshold(gray_frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    
    contours,_ = cv2.findContours(threshold, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse = True)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        # cv2.circle(frame, (x, y), 30, (0, 0,255), 2)
        cv2.circle(frame, (x+int(w/2), y+int(h/2)), 30, (0, 0, 255), 2)
        cv2.circle(frame, (0+int(w/2), 0+int(h/2)), 30, (0, 0, 255), 2)
        cv2.circle(frame, (0, 0), 30, (0, 255, 0), 2)


        cv2.line(frame, (x+int(w/2), 0), (x+int(w/2), rows), (0, 255, 0), 2)# (255, 0, 0) -> Blue (0,0,255)-> red
        cv2.line(frame,(0, y+int(h/2)), (cols,y+int(h/2)), (0, 255, 0), 2)
        print(x, y)
        break
        
    cv2.imshow('gray_frame', gray_frame)
    cv2.imshow('threshold', threshold)
    cv2.imshow('frame',frame)
        
    k = cv2.waitKey(10)&0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
        
def main():
    pass

if __name__ == '__main__':
    main()


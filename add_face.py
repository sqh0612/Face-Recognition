import base64
import os
import time

import cv2
from PIL import Image, ImageTk
import numpy as np
import db


def makeDir():
    if not os.path.exists("face_trainer"):
        os.mkdir("face_trainer")
    if not os.path.exists("FaceData"):
        os.mkdir("FaceData")
    if not os.path.exists("zhuce"):
        os.mkdir("zhuce")


def getFace(name):
    cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    count = 0
    sucess, img1 = cam.read()  # 从摄像头读取图片
    if sucess is True:
        cv2.imshow('image', img1)
        cv2.imwrite("zhuce/" + name.get() + '.jpg', img1)
        print('记录注册时人脸！')

    while True:
        sucess, img = cam.read()  # 从摄像头读取图片
        if sucess is True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            print('没有检测到人脸！')
            break
        # 检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸
        # 其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        # 框选人脸，for循环保证一个能检测的实时动态视频流
        for (x, y, w, h) in faces:
            # xy为左上角的坐标,w为宽，h为高，用rectangle为人脸标记画框
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0))
            # 成功框选则样本数增加
            count += 1
            cv2.imshow('image', img)
            cv2.imwrite("FaceData/User." + name.get() + '.' + str(count) + '.jpg', gray[y: y + h, x: x + w])
        # 保持画面的持续。
        k = cv2.waitKey(1)
        if k == 27:  # 通过esc键退出摄像
            break
        elif count == 20:  # 得到1000个样本后退出摄像
            print("5s后请摇头晃脑，多角度采集")
            count += 1
            time.sleep(5)
        elif count == 41:
            break
        else:
            print(count)

    cam.release()
    cv2.destroyAllWindows()

# 查找注册人脸
def check_reg_face(name):
    try:
        lena = cv2.imread('./zhuce/{}.jpg'.format(name.get()))
        cv2.imshow('image', lena)
        k = cv2.waitKey(1)
        if k == 27:  # 通过esc键退出摄像
            cv2.destroyAllWindows()
    except:
        print('该学生未注册！')

# 查找签到人脸
def check_sign_face(name):
    try:
        lena = cv2.imread('./Qiandao/{}.jpg'.format(name.get()))
        cv2.imshow('image', lena)
        k = cv2.waitKey(1)
        if k == 27:  # 通过esc键退出摄像
            cv2.destroyAllWindows()
    except:
        print('该学生未签到！')

# 删除注册学生记录
def del_name(name):
    user = db.record()
    user.del_name(name.get())
    print('删除记录成功！')

# 该函数用于从数据集文件夹中获取训练图片和id
def get_Images_And_Labels(path, detector, usernames):
    image_Paths = [os.path.join(path, f) for f in os.listdir(path)]
    # 新建两个list用于存放
    face_Samples = []
    ids = []
    # 遍历图片路径，导入图片和id添加到list中
    for image_Path in image_Paths:
        # 通过图片路径将其转换为灰度图片
        PIL_img = Image.open(image_Path).convert('L')
        # 将图片转化为数组
        img_numpy = np.array(PIL_img, 'uint8')
        username = os.path.split(image_Path)[-1].split(".")[1]
        id = 1
        for x in usernames:
            if username == x:
                break
            else:
                id += 1

        faces = detector.detectMultiScale(img_numpy)
        # 将获取的图片和id添加到list中
        for (x, y, w, h) in faces:
            face_Samples.append(img_numpy[y:y + h, x: x + w])
            ids.append(id)
    return face_Samples, ids


def trainFace(names):
    # 人脸数据路径
    path = 'FaceData'
    # 初始化识别的方法
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # 调用人脸分类器
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # 获得处理好的图片和图片标签
    faces, ids = get_Images_And_Labels(path, detector, names)
    # 将采集的图片路径和标签传参，训练人脸模型
    recognizer.train(faces, np.array(ids))
    # 保存训练模型
    recognizer.write(r'face_trainer\trainer.yml')


def add_face(name, names):
    makeDir()
    getFace(name)
    print("获取{}人脸成功".format(name.get()))
    trainFace(names)
    print("训练{}人脸成功".format(name.get()))
    user = db.record()
    user.insert_name(name.get())
    print("录入{}人脸成功".format(name.get()))
    print("重新进入系统新人脸生效！！")

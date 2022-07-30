import time

import cv2

import db


def check(names):
    # 调用摄像头
    cam = cv2.VideoCapture(0)
    # 使用LBPH识别方法
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # 使用之前训练好的模型
    recognizer.read('face_trainer/trainer.yml')
    # 再次调用人脸分类器
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    # 加载一个字体，用于识别后，在图片上标注出对象的名字
    font = cv2.FONT_HERSHEY_COMPLEX
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    while True:
        sucess, img = cam.read()  # 从摄像头读取图片
        if sucess is True:
            cv2.imshow('camera', img)
            cv2.waitKey(100)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            print('没有匹配到人脸！')
            break

        # 识别人脸
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )
        # 进行校验
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            # print(idnum)
            if confidence < 50:
                username = names[idnum - 1]
                print('识别到：'+username)
                confidence = "{0}%".format(round(100 - confidence))
                # 输出检验结果
                cv2.putText(img, str(username), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                #cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)

                x = img.tobytes()
                #cv2.imshow('camera', img)
                cv2.imwrite("Qiandao/"+username+".jpg", img)

                time.sleep(2)
                db.record().insert_record(username, x, str(img.shape))  # 签到信息插入数据库
                cam.release()
                cv2.destroyAllWindows()
                return
            else:
                idnum = "unknown"
                confidence = "{0}%".format(round(100 - confidence))
                cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)

        cv2.imshow('camera', img)
        k = cv2.waitKey(10)
        if k == 27:
            return
        cam.release()
        cv2.destroyAllWindows()

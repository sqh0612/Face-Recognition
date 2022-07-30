from tkinter import *
from tkinter import ttk

import cv2
from PIL import Image as PIL_Image, ImageTk
import numpy as np
import add_face
import db
import detect


class APP:
    def __init__(self):
        self.root = Tk()
        self.root.title('实验室人脸识别考勤系统')
        self.root.geometry('%dx%d' % (400, 350))
        # 数据库实例创建
        self.mydb = db.record()
        self.createFirstPage()
        # 新录入的人的姓名
        self.name = StringVar()
        mainloop()

    def Showimage(self, imgCV_in, canva, layout="null"):
        """
        Showimage()是一个用于在tkinter的canvas控件中显示OpenCV图像的函数。
        使用前需要先导入库
        import cv2 as cv
        from PIL import Image,ImageTktkinter
        并注意由于响应函数的需要，本函数定义了一个全局变量 imgTK，请不要在其他地方使用这个变量名!
        参数：
        imgCV_in：待显示的OpenCV图像变量
        canva：用于显示的tkinter canvas画布变量
        layout：显示的格式。可选项为：
            "fill"：图像自动适应画布大小，并完全填充，可能会造成画面拉伸
            "fit"：根据画布大小，在不拉伸图像的情况下最大程度显示图像，可能会造成边缘空白
            给定其他参数或者不给参数将按原图像大小显示，可能会显示不全或者留空
        """
        global imgTK
        canvawidth = int(canva.winfo_reqwidth())
        canvaheight = int(canva.winfo_reqheight())
        sp = imgCV_in.shape
        cvheight = sp[0]  # height(rows) of image
        cvwidth = sp[1]  # width(colums) of image
        if layout == "fill":
            imgCV = cv2.resize(imgCV_in, (canvawidth, canvaheight), interpolation=cv2.INTER_AREA)
        elif layout == "fit":
            if float(cvwidth / cvheight) > float(canvawidth / canvaheight):
                imgCV = cv2.resize(imgCV_in, (canvawidth, int(canvawidth * cvheight / cvwidth)),
                                   interpolation=cv2.INTER_AREA)
            else:
                imgCV = cv2.resize(imgCV_in, (int(canvaheight * cvwidth / cvheight), canvaheight),
                                   interpolation=cv2.INTER_AREA)
        else:
            imgCV = imgCV_in
        imgCV2 = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
        current_image = PIL_Image.fromarray(imgCV2)  # 将图像转换成Image对象
        imgTK = ImageTk.PhotoImage(image=current_image)  # 将image对象转换为imageTK对象
        canva.create_image(0, 0, anchor=NW, image=imgTK, tags=('r1',))

    def createFirstPage(self):
        self.page1 = Frame(self.root)
        self.page1.grid()
        Label(self.page1, height=4, text='实验室人脸识别考勤系统', font=('粗体', 20)).grid(columnspan=2)
        # self.usernames 是用户名字组成的列表
        self.usernames = []
        self.usernames = self.mydb.query_name()

        self.button11 = Button(self.page1, width=18, height=2, text="签到打卡", bg='white', font=("宋", 12),
                               relief='raise', command=lambda: detect.check(self.usernames))
        self.button11.grid(row=1, column=1, padx=25, pady=10)
        self.button12 = Button(self.page1, width=18, height=2, text="录入新人脸", bg='white', font=("宋", 12),
                               relief='raise', command=self.createSecondPage)
        self.button12.grid(row=1, column=0, padx=25, pady=10)
        self.button13 = Button(self.page1, width=18, height=2, text="已录入学生", bg='white', font=("宋", 12),
                               relief='raise', command=self.checksuccess)
        self.button13.grid(row=2, column=0, padx=25, pady=10)
        self.button14 = Button(self.page1, width=18, height=2, text="签到信息浏览", bg='white', font=("宋", 12),
                               relief='raise', command=self.checkDataView)
        self.button14.grid(row=2, column=1, padx=25, pady=10)
        self.button15 = Button(self.page1, width=18, height=2, text="考勤记录查询", bg='white', font=("宋", 12),
                               relief='raise', command=self.checklist)
        self.button15.grid(row=3, column=0, padx=25, pady=10)
        self.button16 = Button(self.page1, width=18, height=2, text="退出系统", bg='gray', font=("宋", 12),
                               relief='raise', command=self.quitMain)
        self.button16.grid(row=3, column=1, padx=25, pady=10)

    def createSecondPage(self):
        # self.camera = cv2.VideoCapture(0)
        self.page1.grid_forget()
        self.page2 = Frame(self.root)
        self.root.geometry('600x300')
        self.page2.pack()
        Label(self.page2, text='欢迎使用人脸识别考勤系统', font=('粗体', 20)).pack()

        # 输入姓名的文本框
        font1 = ('宋', 18)
        # self.name = StringVar()
        self.text = Entry(self.page2, textvariable=self.name, width=20, font=font1).pack(side=LEFT)
        self.name.set('请输入学号姓名')

        # 确认名字的按钮
        self.button21 = Button(self.page2, text='确认', bg='white', font=("宋", 12),
                               relief='raise', command=lambda: add_face.add_face(self.name, self.usernames))
        self.button21.pack(side=LEFT, padx=5, pady=10)

        # 返回按钮
        self.button22 = Button(self.page2, text="返回", bg='white', font=("宋", 12),
                               relief='raise', command=self.backFirst)
        self.button22.pack(side=LEFT, padx=10, pady=10)

        # 查看录入人脸
        self.button24 = Button(self.page2, width=20, height=2, text="查看录入人脸", bg='gray', font=("宋", 12),
                               relief='raise', command=lambda: add_face.check_reg_face(self.name))
        self.button24.pack(side=TOP, padx=10, pady=10)
        # 不满意重拍
        self.button25 = Button(self.page2, width=20, height=2, text="重新录入人脸", bg='gray', font=("宋", 12),
                               relief='raise', command=lambda: add_face.add_face(self.name, self.usernames))
        self.button25.pack(side=BOTTOM, padx=10, pady=10)
        # 删除记录
        self.button23 = Button(self.page2, width=20, height=2, text="删除记录", bg='gray', font=("宋", 12),
                               relief='raise', command=lambda: add_face.del_name(self.name))
        self.button23.pack(side=BOTTOM, padx=10, pady=10)


    def checkDataView(self):
        self.imgTK = None
        self.records_index = 0
        self.page1.grid_forget()
        self.page3 = Frame(self.root)
        self.root.geometry('500x850')
        self.page3.pack()
        Label(self.page3, text='签到信息浏览', bg='white', fg='black', font=('宋体', 25)).pack(side=TOP, fill='x')
        # 签到信息查看视图
        canva = Canvas(self.page3, width=400, height=400)
        self.canva = canva
        canva.pack()

        # 插入数据
        self.records = self.mydb.query_record()
        canvawidth = int(canva.winfo_reqwidth())
        canvaheight = int(canva.winfo_reqheight())
        i = self.records[self.records_index]

        x = i[3]
        img = np.frombuffer(x, np.uint8).reshape(eval(i[4]))
        imgCV_in = img

        imgCV = cv2.resize(imgCV_in, (canvawidth, canvaheight), interpolation=cv2.INTER_AREA)
        imgCV2 = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGBA)

        current_image = PIL_Image.fromarray(imgCV2)  # 将图像转换成Image对象
        # current_image.show()
        imgTK = ImageTk.PhotoImage(image=current_image)  # 将image对象转换为imageTK对象
        self.imgTK = imgTK
        canva.create_image(0, 0, anchor=NW, image=imgTK, tags=('r',))

        self.la = Label(self.page3, text=f'签到时间：{i[2]}', bg='white', fg='black', font=('宋体', 25))
        self.la.pack(side=TOP, fill='x')
        self.la_1 = Label(self.page3, text=f'签到人：{i[1]}', bg='white', fg='black', font=('宋体', 25))
        self.la_1.pack(side=TOP, fill='x')
        self.la_2 = Label(self.page3, text=f'序号：{i[0]}', bg='white', fg='black', font=('宋体', 25))
        self.la_2.pack(side=TOP, fill='x')
        # 返回按钮
        Button(self.page3, width=20, height=2, text="上一条记录", bg='gray', font=("宋", 12),
               relief='raise', command=self.shang).pack(padx=20, pady=20)
        Button(self.page3, width=20, height=2, text="下一条记录", bg='gray', font=("宋", 12),
               relief='raise', command=self.xia).pack(padx=20, pady=20)
        Button(self.page3, width=20, height=2, text="返回", bg='gray', font=("宋", 12),
               relief='raise', command=self.backMain3).pack(padx=20, pady=20)

    def checklist(self):
        self.page4 = Frame(self.root)
        self.page1.grid_forget()
        self.root.geometry('900x360')
        self.page4.pack()
        Label(self.page4, text='签到信息列表', fg='black', font=('宋体', 25)).pack(side=TOP, fill='x')

        # 确认名字的按钮
        self.button21 = Button(self.page4, text='查询', bg='white', font=("宋", 12),
                               relief='raise', command=lambda: add_face.check_sign_face(self.name))
        self.button21.pack(side=RIGHT, padx=5, pady=10)

        # 输入姓名的文本框
        font1 = ('宋', 18)
        # self.name = StringVar()
        self.text = Entry(self.page4, textvariable=self.name, width=20, font=font1).pack(side=RIGHT)
        self.name.set('请输入学号姓名')

        # 签到信息查看视图
        self.checkDate = ttk.Treeview(self.page4, show='headings', column=('sid', 'name', 'check_time'))
        self.checkDate.column('sid', width=100, anchor="center")
        self.checkDate.column('name', width=200, anchor="center")
        self.checkDate.column('check_time', width=300, anchor="center")

        self.checkDate.heading('sid', text='签到序号')
        self.checkDate.heading('name', text='名字')
        self.checkDate.heading('check_time', text='签到时间')

        # 显示页面插入数据
        self.records = self.mydb.query_simple_record()
        for i in self.records:
            self.checkDate.insert('', 'end', values=i)

        # y滚动条
        yscrollbar = Scrollbar(self.page4, orient=VERTICAL, command=self.checkDate.yview)
        self.checkDate.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side=RIGHT, fill=Y)

        self.checkDate.pack(expand=1, fill=BOTH)

        # 返回按钮
        Button(self.page4, width=20, height=2, text="返回", bg='gray', font=("宋", 12),
               relief='raise', command=self.backMain4).pack(side=BOTTOM, padx=20, pady=20)

    def checksuccess(self):
        self.page5 = Frame(self.root)
        self.page1.grid_forget()
        self.root.geometry('900x360')
        self.page5.pack()
        Label(self.page5, text='已录入学生信息', fg='black', font=('宋体', 25)).pack(side=TOP, fill='x')

        # 确认名字的按钮
        self.button21 = Button(self.page5, text='查询', bg='white', font=("宋", 12),
                               relief='raise', command=lambda: add_face.check_reg_face(self.name))
        self.button21.pack(side=RIGHT, padx=5, pady=10)

        # 输入姓名的文本框
        font1 = ('宋', 18)
        # self.name = StringVar()
        self.text = Entry(self.page5, textvariable=self.name, width=20, font=font1).pack(side=RIGHT)
        self.name.set('请输入学号姓名')

        # 签到信息查看视图
        self.checkDate = ttk.Treeview(self.page5, show='headings', column=('sid', 'name', 'check_time'))
        self.checkDate.column('sid', width=100, anchor="center")
        self.checkDate.column('name', width=200, anchor="center")
        self.checkDate.column('check_time', width=300, anchor="center")

        self.checkDate.heading('sid', text='序号')
        self.checkDate.heading('name', text='学号姓名')
        self.checkDate.heading('check_time', text='注册时间')

        # 显示页面插入数据
        self.records = self.mydb.query_nametable()
        for i in self.records:
            self.checkDate.insert('', 'end', values=i)

        # y滚动条
        yscrollbar = Scrollbar(self.page5, orient=VERTICAL, command=self.checkDate.yview)
        self.checkDate.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side=RIGHT, fill=Y)

        self.checkDate.pack(expand=1, fill=BOTH)

        # 返回按钮
        Button(self.page5, width=20, height=2, text="返回", bg='gray', font=("宋", 12),
               relief='raise', command=self.backMain5).pack(padx=20, pady=20)

    def shang(self):
        if self.records_index == 0:
            return
        else:
            self.records_index -= 1
            self.canv()

    def xia(self):
        # print(len(self.records),len(self.records),111111)
        if self.records_index == len(self.records) - 1:
            return
        else:
            self.records_index += 1
            self.canv()

    def canv(self):
        self.canva.delete('r')
        canvawidth = int(self.canva.winfo_reqwidth())
        canvaheight = int(self.canva.winfo_reqheight())
        i = self.records[self.records_index]
        x = i[3]
        img = np.frombuffer(x, np.uint8).reshape(eval(i[4]))
        imgCV_in = img

        imgCV = cv2.resize(imgCV_in, (canvawidth, canvaheight), interpolation=cv2.INTER_AREA)
        imgCV2 = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGBA)
        # cv2.imshow('camera', imgCV2)
        # cv2.waitKey(0)
        current_image = PIL_Image.fromarray(imgCV2)  # 将图像转换成Image对象
        # current_image.show()
        imgTK = ImageTk.PhotoImage(image=current_image)  # 将image对象转换为imageTK对象
        self.imgTK = imgTK
        self.canva.create_image(0, 0, anchor=NW, image=imgTK, tags=('r',))
        self.la['text'] = f'签到时间：{i[2]}'
        self.la_1['text'] = f'签到人：{i[1]}'
        self.la_2['text'] = f'序号：{i[0]}'

    def backFirst(self):
        self.page2.pack_forget()
        self.root.geometry('400x300')
        self.page1.grid()

    def backMain3(self):
        self.root.geometry('400x300')
        self.page3.pack_forget()
        self.page1.grid()

    def backMain4(self):
        self.root.geometry('400x300')
        self.page4.pack_forget()
        self.page1.grid()

    def backMain5(self):
        self.root.geometry('400x300')
        self.page5.pack_forget()
        self.page1.grid()

    def quitMain(self):
        sys.exit(0)


if __name__ == '__main__':
    demo = APP()

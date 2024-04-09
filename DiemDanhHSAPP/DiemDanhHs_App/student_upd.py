from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
import numpy as np
import random
from tkinter import messagebox
import mysql.connector
from tkcalendar import Calendar, DateEntry
from time import strftime
import cv2
import os
import re
from database_str import Database_str
from search_image import student_id
from search_image import StdImage

mydata=[]
class Student:
    def __init__(self,root):
        self.root=root
        w = 1350  # chiều dài giao diện
        h = 700  # chiều rộng giao diện

        ws = self.root.winfo_screenwidth()  # độ dài màn hình
        hs = self.root.winfo_screenheight()  # độ rộng màn
        x = (ws / 2) - (w / 2)  # vị trí cách lề trái x px
        y = (hs / 2) - (h / 2)  # vị trí cách lề trên y px

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # kích thước và vị trí hiển thị giao diện
        self.root.title("Hệ thống quản lý điểm danh")
        today = strftime("%d-%m-%Y")

        # thông tin kết nối database
        self.db = Database_str()
        
        #=================Khai báo biến================

        self.var_year = StringVar()#khóa học
        self.var_semester = StringVar()#học kỳ
        self.var_std_id = StringVar()#id_hoc sinh
        self.var_std_name = StringVar()#tên hoc sinh
        self.var_div = StringVar()#lớp
        self.var_roll = StringVar()#CMND
        self.var_gender = StringVar()#giới tính
        self.var_dob = StringVar()#ngày sinh
        self.var_email = StringVar()#email
        self.var_phone = StringVar()#SDT
        self.var_address = StringVar()#Địa chỉ

        #==================Biến lớp học================
        self.var_class=StringVar()#biến chứa lớp học
        self.var_nameclass=StringVar()# biến tên lớp học
        #Lấy thông tin lớp học
        class_array = [] # Mảng thông tin lớp học
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()
        my_cursor.execute("Select Class from class")#truy vấn tất cả lớp trong bảng class
        data_class = my_cursor.fetchall()
        for i in data_class:#Với mỗi lớp trong mảng lớp học : truyền thông tin lớp vào mảng lớp học
            class_array.append(i)

        img3 = PIL.Image.open(r"ImageFaceDetect\bgnt.png")#Ảnh nền
        img3 = img3.resize((1350, 700), PIL.Image.ANTIALIAS)#resize ảnh nền
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)#label chứa ảnh nền
        bg_img.place(x=0, y=0, width=1350, height=700)

        # ==================================heading====================================
        # ====time====
        img_time = PIL.Image.open(r"ImageFaceDetect\timsearch50.png")#Ảnh icon thời gian
        img_time = img_time.resize((27, 27), PIL.Image.ANTIALIAS)
        self.photoimgtime = ImageTk.PhotoImage(img_time)
        time_img = Label(self.root, image=self.photoimgtime, bg="white")
        time_img.place(x=43, y=40, width=27, height=27)

        def time():#Hàm thời gian thay đổi mỗi giây
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = Label(self.root, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl.place(x=80, y=35, width=100, height=18)
        time()#chạy hàm time
        lbl1 = Label(self.root, text=today, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl1.place(x=80, y=60, width=100, height=18)

        # ====Tiêu đề=========
        self.txt = "Quản lý thông tin sinh viên"
        self.heading = Label(self.root, text=self.txt, font=("times new roman", 22, "bold"), bg="white", fg="black",
                             bd=5, relief=FLAT)
        self.heading.place(x=400, y=22, width=650)


        main_frame = Frame(bg_img, bd=2, bg="white")#main frame
        main_frame.place(x=24, y=90, width=1293, height=586)

        #Khung bên trái
        self.getNextid()#chạy hàm nextid để lấy ra id tiếp theo trong bảng
        Left_frame=LabelFrame(main_frame,bd=2,bg="white",font=("times new roman",12,"bold"))
        Left_frame.place(x=7,y=10,width=655, height=565)

        label_Update_att = Label(Left_frame, bg="white", fg="red2", text="Thông tin sinh viên",
                                 font=("times new roman", 13, "bold"))
        label_Update_att.place(x=0, y=1, width=640, height=35)


        #Frame thông tin khóa học
        current_course_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin khoá học",
                                font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=35, width=640, height=100)



        #khóa học
        year_label = Label(current_course_frame, text="Khóa học", font=("times new roman", 11, "bold"), bg="white")
        year_label.grid(row=1, column=0, padx=15, sticky=W)

        year_combo = ttk.Combobox(current_course_frame,textvariable=self.var_year, font=("times new roman", 11, "normal"), state="readonly",
                                    width=20)
        year_combo["values"] = ("Chọn khóa học", "2021", "2022", "2023")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=15, pady=10, sticky=W)

        #học kỳ
        semester_label = Label(current_course_frame, text="Học kỳ", font=("times new roman", 11, "bold"), bg="white")
        semester_label.grid(row=1, column=2, padx=15, sticky=W)

        semester_combo = ttk.Combobox(current_course_frame,textvariable=self.var_semester ,font=("times new roman", 11, "normal"), state="readonly",width=20)
        semester_combo["values"] = ("Chọn học kỳ", "1", "2")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=15, pady=10, sticky=W)

        #frame thông tin lớp học
        class_student_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin lớp học",
                                          font=("times new roman", 11, "bold"))
        class_student_frame.place(x=5, y=145, width=640, height=400)

        # Nhập Id sinh viên
        studentID_label = Label(class_student_frame, text="ID sinh viên:", font=("times new roman", 11, "bold"), bg="white")
        studentID_label.grid(row=0, column=0, padx=10,pady=10, sticky=W)

        self.studentID_entry=Entry(class_student_frame,width=21,textvariable=self.var_std_id,font=("times new roman", 11, "normal"),state="disabled",
                                 )
        self.studentID_entry.grid(row=0,column=1,padx=10,pady=10,sticky=W)

        #Tên sinh viên
        studentName_label = Label(class_student_frame, text="Tên sinh viên:", font=("times new roman", 11, "bold"),
                                bg="white")
        studentName_label.grid(row=0, column=2, padx=10,pady=10, sticky=W)

        studentName_entry = ttk.Entry(class_student_frame, width=23,textvariable=self.var_std_name, font=("times new roman", 11, "normal"))
        studentName_entry.grid(row=0, column=3, padx=10,pady=10, sticky=W)

        #Lớp học
        class_div_label = Label(class_student_frame, text="Lớp học:", font=("times new roman", 11, "bold"), bg="white")
        class_div_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        class_div_entry = ttk.Combobox(class_student_frame, width=18,textvariable=self.var_div, font=("times new roman", 11, "normal"))
        class_div_entry["values"] = class_array
        class_div_entry.current()
        class_div_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)


        #CMND
        roll_no_label = Label(class_student_frame, text="CMND", font=("times new roman", 11, "bold"),
                                  bg="white")
        roll_no_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        roll_no_entry = ttk.Entry(class_student_frame, width=23,textvariable=self.var_roll ,font=("times new roman", 11, "normal"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        #giới tính
        gender_label = Label(class_student_frame, text="Giới tính:", font=("times new roman", 11, "bold"),
                                bg="white")
        gender_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender,
                                  font=("times new roman", 11, "normal"), state="readonly",
                                  width=18)
        gender_combo["values"] = ("Nam", "Nữ", "Khác")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        #Ngày sinh
        dob_label = Label(class_student_frame, text="Ngày sinh:", font=("times new roman", 11, "bold"),
                              bg="white")
        dob_label.grid(row=2, column=2, padx=10, pady=10, sticky=W)

        self.dob_entry = DateEntry(class_student_frame, width=18, bd=3,selectmode='day',
                       year=2023, month=11,font=("times new roman", 12),
                       day=22,date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=2, column=3, padx=10, pady=10, sticky=W)

        #email
        email_label = Label(class_student_frame, text="Email:", font=("times new roman", 11, "bold"),
                             bg="white")
        email_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        email_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_email, font=("times new roman", 11, "normal"))
        email_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)


        #SĐT
        phone_label = Label(class_student_frame, text="SĐT:", font=("times new roman", 11, "bold"),
                          bg="white")
        phone_label.grid(row=3, column=2, padx=10, pady=10, sticky=W)

        phone_entry = ttk.Entry(class_student_frame, width=23,textvariable=self.var_phone, font=("times new roman", 11, "normal"))
        phone_entry.grid(row=3, column=3, padx=10, pady=10, sticky=W)


        #Địa chỉ
        address_label = Label(class_student_frame, text="Địa chỉ:", font=("times new roman", 11, "bold"),
                            bg="white")
        address_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)

        address_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_address ,font=("times new roman", 11, "normal"))
        address_entry.grid(row=4, column=1, padx=10, pady=10, sticky=W)


        #radioBtn
        self.var_radio1=StringVar()
        radionbtn1=ttk.Radiobutton(class_student_frame,variable=self.var_radio1,text="Có ảnh",value="Yes")
        radionbtn1.grid(row=6,column=0)


        radionbtn2 = ttk.Radiobutton(class_student_frame,variable=self.var_radio1, text="Không ảnh", value="No")
        radionbtn2.grid(row=6, column=1)

        #----------btn_frame----------------
        btn_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=260,width=635,height=50)

        #nút lưu thông tin sinh viên
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")#ảnh nút màu đỏ
        img_btn1 = img_btn1.resize((120, 35), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        save_btn=Button(btn_frame,text="Lưu",command=self.add_data,font=("times new roman",11,"bold"),bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=115,image=self.photobtn1,fg="white",compound="center")
        save_btn.place(x=30,y=3)

        # nút sửa thông tin sinh viên
        update_btn = Button(btn_frame, text="Sửa",command=self.update_data, font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=115,image=self.photobtn1,fg="white",compound="center")
        update_btn.place(x=180, y=3)

        # nút xóa thông tin sinh viên
        delete_btn = Button(btn_frame, text="Xóa",command=self.delete_data, font=("times new roman", 11, "bold"),bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=115,image=self.photobtn1,fg="white",compound="center")
        delete_btn.place(x=330, y=3)

        #nút làm mới
        reset_btn = Button(btn_frame, text="Làm mới",command=self.reset_data, font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=115,image=self.photobtn1,fg="white",compound="center")
        reset_btn.place(x=480, y=3)

        #----------btn_frame1--------------
        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=320, width=635, height=50)

        #nút chụp ảnh sinh viên
        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn2 = img_btn2.resize((170, 35), PIL.Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        take_photo_btn = Button(btn_frame1, text="Lấy ảnh sinh viên",command=self.generate_dataset, font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=170,image=self.photobtn2,fg="white", compound="center")
        take_photo_btn.place(x=30, y=3)

        #nút train data từ các ảnh đã chụp
        update_photo_btn = Button(btn_frame1, text="Training Data",command=self.train_classifier, font=("times new roman", 11, "bold"),bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=170,image=self.photobtn2,fg="white",compound="center")
        update_photo_btn.place(x=230, y=3)

        #Nút xem các ảnh đã chụp của sinh viên
        show_photo_btn = Button(btn_frame1, text="Xem ảnh", command=self.student_image,
                                font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=170,image=self.photobtn2,fg="white",compound="center")
        show_photo_btn.place(x=430, y=3)


        # Frame bên phải chứa bảng dữ liệu và chức năng tìm kiếm
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                font=("times new roman", 12, "bold"))
        Right_frame.place(x=675, y=10, width=610, height=290)


        #Tìm kiếm
        search_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE, text="Hệ Thống Tìm kiếm",
                                         font=("times new roman", 11, "bold"))
        search_frame.place(x=5, y=5, width=600, height=70)

        self.var_com_search= StringVar()#Loại tìm kiếm
        search_label = Label(search_frame, text="Tìm kiếm theo :", font=("times new roman", 10, "bold"),
                            bg="white",fg="red2")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        search_combo = ttk.Combobox(search_frame, font=("times new roman", 10, "bold"), state="readonly",
                                      width=10,textvariable=self.var_com_search)
        search_combo["values"] = ("ID sinh viên", "Tên sinh viên", "Lớp")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        #
        self.var_search = StringVar()#Khung nhập tìm kiếm
        search_entry = ttk.Entry(search_frame, width=15, font=("times new roman", 11, "bold"),textvariable=self.var_search)
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)


        #Nút tìm kiếm
        img_btn3 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")#ảnh nền màu đỏ
        img_btn3 = img_btn3.resize((105, 35), PIL.Image.ANTIALIAS)#resize ảnh
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)#convert ảnh dạng ImageTk để truyền vào Button
        #nút tìm kiếm
        search_btn = Button(search_frame, text="Tìm kiếm", font=("times new roman", 11, "bold"),command=self.search_data,bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=105,image=self.photobtn3,fg="white",compound="center")
        search_btn.grid(row=0, column=3,padx=4)

        #nút xem tất cả
        showAll_btn = Button(search_frame, text="Xem tất cả", font=("times new roman", 11, "bold"), command=self.fetch_data,bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=105,image=self.photobtn3,fg="white",compound="center")
        showAll_btn.grid(row=0, column=4,padx=4)


        #Bảng dữ liệu
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=85, width=600, height=195)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        #các trường dữ liệu
        self.student_table=ttk.Treeview(table_frame,column=("id","year","sem","name","div","roll","gender","dob","email","phone","address","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        #đặt tên các cột dữ liệu
        self.student_table.heading("id", text="ID sinh viên")
        self.student_table.heading("name", text="Họ tên")
        self.student_table.heading("div", text="Lớp học")
        self.student_table.heading("year", text="Khóa")
        self.student_table.heading("sem", text="Học kỳ")
        self.student_table.heading("roll", text="CMND")
        self.student_table.heading("gender", text="Giới tính")
        self.student_table.heading("dob", text="Ngày sinh")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Số điện thoại")
        self.student_table.heading("address",text="Địa chỉ")

        self.student_table.heading("photo", text="Trạng thái ảnh")
        self.student_table["show"]="headings"

        #độ dài các cột
        self.student_table.column("id", width=70)
        self.student_table.column("name", width=100)
        self.student_table.column("year", width=70)
        self.student_table.column("sem", width=60)
        self.student_table.column("div", width=60)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("photo", width=150)

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)#sự kiện khi click vào bảng các thông tin in ra các txtbox
        self.fetch_data()#load du lieu len bảng
        self.getNextid()#Lấy id tiếp theo

        #Thông tin lớp học và các chức năng thêm ,sửa ,xóa ,.....
        Underright_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                      font=("times new roman", 11, "bold"))
        Underright_frame.place(x=675, y=305, width=610, height=270)

        label_studentsb = Label(Underright_frame, bg="white", fg="red2", text="Quản lý lớp học",
                                font=("times new roman", 12, "bold"))
        label_studentsb.place(x=0, y=1, width=600, height=35)

        # search
        self.var_com_searchclass = StringVar()#Loại tìm kiếm lớp (theo lớp, tên lớp)
        search_combo = ttk.Combobox(Underright_frame, font=("times new roman", 11, "bold"),
                                    textvariable=self.var_com_searchclass,
                                    state="readonly",
                                    width=11)
        search_combo["values"] = ("Lớp", "Tên lớp")
        search_combo.current(0)
        search_combo.grid(row=0, column=0, padx=10, pady=40, sticky=W)

        self.var_searchclass = StringVar()#Khung nhập tìm kiếm lớp
        searchstd_entry = ttk.Entry(Underright_frame, textvariable=self.var_searchclass, width=13,
                                    font=("times new roman", 10, "bold"))
        searchstd_entry.grid(row=0, column=1, padx=5, pady=35, sticky=W)

        #Các nút
        img_btn4 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")#ảnh nút màu đỏ
        img_btn4 = img_btn4.resize((80, 25), PIL.Image.ANTIALIAS)
        self.photobtn4 = ImageTk.PhotoImage(img_btn4)

        #nút tìm kiếm
        searchstd_btn = Button(Underright_frame, command=self.search_Classdata, text="Tìm kiếm",
                               font=("times new roman", 10, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=80,image=self.photobtn4,fg="white",compound="center")
        searchstd_btn.grid(row=0, column=2, padx=3)

        #nút xem tất cả
        showAllstd_btn = Button(Underright_frame, text="Xem tất cả", command=self.fetch_Classdata,
                                font=("times new roman", 10, "bold"),bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=80,image=self.photobtn4,fg="white",compound="center")
        showAllstd_btn.grid(row=0, column=3, padx=3)

        # Lớp học
        studentid_label = Label(Underright_frame, text="Lớp học:", font=("times new roman", 12, "bold"),
                                bg="white", width=12)
        studentid_label.place(x=20, y=100, width=100)

        studentid_entry = ttk.Entry(Underright_frame, textvariable=self.var_class,
                                    font=("times new roman", 12, "bold"), width=20)
        studentid_entry.place(x=135, y=100, width=200)

        # Tên lớp học
        subsub_label = Label(Underright_frame, text="Tên lớp học:", font=("times new roman", 12, "bold"),
                             bg="white")
        subsub_label.place(x=20, y=145, width=80)

        subsub_entry = ttk.Entry(Underright_frame, width=22, textvariable=self.var_nameclass,
                                 font=("times new roman", 12, "bold"))
        subsub_entry.place(x=135, y=145, width=200)

        # btn_frame
        btn_framestd = Frame(Underright_frame, bg="white", bd=2, relief=RIDGE)
        btn_framestd.place(x=10, y=200, width=400, height=55)

        img_btn5 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn5 = img_btn5.resize((90, 30), PIL.Image.ANTIALIAS)
        self.photobtn5 = ImageTk.PhotoImage(img_btn5)

        #nút thêm lớp học
        addTc_btn = Button(btn_framestd, text="Thêm", command=self.add_Classdata,
                           font=("times new roman", 11, "bold"),
                           bd=0, bg="white", cursor='hand2', activebackground='white',
                           width=90, image=self.photobtn5, fg="white", compound="center"
                           )
        addTc_btn.place(x=5,y=7)

        #nút xóa lớp học
        deleteTc_btn = Button(btn_framestd, text="Xóa", command=self.delete_Classdata,
                              font=("times new roman", 11, "bold"),
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=90, image=self.photobtn5, fg="white", compound="center"
                              )
        deleteTc_btn.place(x=103, y=7)

        #nút cập nhật thông tin lớp học
        updateTc_btn = Button(btn_framestd, text="Cập nhật", command=self.update_Classdata,
                              font=("times new roman", 11, "bold"),
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=90, image=self.photobtn5, fg="white", compound="center")
        updateTc_btn.place(x=201,y=7)

        #nút làm mới
        resetTc_btn = Button(btn_framestd, text="Làm mới", command=self.reset_Classdata,
                             font=("times new roman", 11, "bold"),
                             bd=0, bg="white", cursor='hand2', activebackground='white',
                             width=90, image=self.photobtn5, fg="white", compound="center")
        resetTc_btn.place(x=299,y=7)

        # bảng dữ liệu lớp học
        tablestd_frame = Frame(Underright_frame, bd=2, relief=RIDGE, bg="white")
        tablestd_frame.place(x=420, y=35, width=180, height=220)

        # scroll bar
        scroll_x = ttk.Scrollbar(tablestd_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tablestd_frame, orient=VERTICAL)

        self.StudentTable = ttk.Treeview(tablestd_frame, column=("class", "name"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.StudentTable.xview)
        scroll_y.config(command=self.StudentTable.yview)

        self.StudentTable.heading("class", text="Lớp học")
        self.StudentTable.heading("name", text="Tên")

        self.StudentTable["show"] = "headings"
        self.StudentTable.column("class", width=80)
        self.StudentTable.column("name", width=80)

        self.StudentTable.pack(fill=BOTH, expand=1)
        #Đổ dữ liệu vào khung nhập liệu khu nhấp vào row ở table
        self.StudentTable.bind("<ButtonRelease>", self.get_cursorClass)
        self.fetch_Classdata()

    #============function decration===============
    def student_image(self):#Xem ảnh của sinh viên
        if self.var_std_name.get()=="" or self.var_std_id.get()=="":#Nếu txt tên hs hoặc id sinh viên trống thì báo lỗi
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        else:
            student_id(self.var_std_id.get())#truyền id sinh viên vào form thông tin ảnh
            self.new_window=Toplevel(self.root)#cửa sổ mới
            self.app=StdImage(self.new_window)#Hiện thị giao diện xem ảnh


    

    def getNextid(self):#Lấy ra id tiếp theo
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()
        my_cursor.execute(
            "SELECT  Student_id from student ORDER BY Student_id DESC limit 1")#câu lệnh truy vấn ra id tiếp theo(Vd: id cuối trong bảng là 5-> id tiếp theo=6)
        lastid = my_cursor.fetchone()
        if (lastid == None):
            self.var_std_id.set("1")#Nếu ko có dữ liệu -> id tiếp theo=1
        else:#Nếu có id tiếp theo bằng id cũ +1
            nextid = int(lastid[0]) + 1
            self.var_std_id.set(str(nextid))

        conn.commit()
        conn.close()

    def add_data(self):#Thêm dữ liệu
        # ========check class================
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #để Check xem email nhập vào có đúng định dạng email ko

        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)

        my_cursor = conn.cursor()
        my_cursor.execute("select Class from `class` ")
        ckclass = my_cursor.fetchall()
        arrayClass = []
        for chc in ckclass:
            arrayClass.append(str(chc[0]))
        if  self.var_std_name.get()=="" or self.var_std_id.get()=="" or self.var_div.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        elif (self.var_div.get() not in arrayClass):#Lớp ko tồn tại thì thông báo
            messagebox.showerror("Error", "Tên lớp học không tồn tại ! Vui lòng kiểm tra lại", parent=self.root)
        elif(re.search(regex, self.var_email.get())==None):#check email nhập vào đúng định dạng
            messagebox.showerror("Error", "Vui lòng nhập email đúng định dạng", parent=self.root)
        elif(self.var_phone.get().isnumeric()!=True):#SDT nhạp vào đúng dạng số ko
            messagebox.showerror("Error", "Vui lòng nhập số điện thoại đúng", parent=self.root)
        elif(self.var_roll.get().isnumeric()!=True):#CMND đúng dạng số ko
            messagebox.showerror("Error", "Vui lòng nhập số CMND đúng", parent=self.root)
        else:#Thêm thông tin sinh viên
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)

                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                    self.var_std_id.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.dob_entry.get_date().strftime('%d/%m/%Y'),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_radio1.get()
                ))

                conn.commit()#xác thực câu lệnh
                self.fetch_data()#In dữ liệu mới lên bảng sau khi thêm
                self.reset_data()#reset lại các txtbox để nhập dữ liệu mới
                conn.close()#Đóng kết nối DataBase
                messagebox.showinfo("Thành công","Thêm thông tin sinh viên thành công",parent=self.root)#thêm thành công
            except Exception as es:#Nếu có lỗi -> in ra màn hình
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    #=======================fetch-data========================
    def fetch_data(self):#Lấy tất cả thông tin sinh viên
        conn=mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)

        my_cursor = conn.cursor()
        #câu lệnh sql truy vấn tất cả thông tin sinh viên
        my_cursor.execute("Select * from student")
        data=my_cursor.fetchall()

        if len(data)!=0:#Nếu có dữ liệu hoc sinh thì hiện thị lên bảng
            self.student_table.delete(*self.student_table.get_children())#Xóa những dữ liệu cũ ở bảng
            for i in data:#Thêm tất cả thông tin vừa truy vấn đc lên bảng
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    #======================get-cursor==============================
    def get_cursor(self,event=""):#Sự kiện khi click vào bảng thì hiện chi tiết thông tin ra các txtbox
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]
        self.var_std_id.set(data[0]),
        self.var_year.set(data[1]),
        self.var_semester.set(data[2]),
        self.var_std_name.set(data[3]),
        self.var_div.set(data[4]),
        self.var_roll.set(data[5]),
        self.var_gender.set(data[6]),
        self.dob_entry.set_date(data[7]),
        self.var_email.set(data[8]),
        self.var_phone.set(data[9]),
        self.var_address.set(data[10]),
        self.var_radio1.set(data[11]),

    def update_data(self):#Cập nhật thông tin sinh viên
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # check email
        if  self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        elif (re.search(regex, self.var_email.get()) == None):
            messagebox.showerror("Error", "Vui lòng nhập email đúng định dạng", parent=self.root)
        elif (self.var_phone.get().isnumeric() != True):
            messagebox.showerror("Error", "Vui lòng nhập số điện thoại đúng", parent=self.root)
        elif (self.var_roll.get().isnumeric() != True):
            messagebox.showerror("Error", "Vui lòng nhập số CMND đúng", parent=self.root)
        else:
            try:
            	#Hỏi trước khi cập nhật
                Update=messagebox.askyesno("Update","Bạn có muốn cập nhật thông tin sinh viên này không?",parent=self.root)
                if Update>0:#nếu bấm yes
                    conn=mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                    my_cursor = conn.cursor()
                    #câu lệnh sql update các thong tin sinh viên
                    my_cursor.execute("update student set Year=%s,Semester=%s,Name=%s,Class=%s,"
                                      "Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,PhotoSample=%s where Student_id=%s",(

                                            self.var_year.get(),
                                            self.var_semester.get(),
                                            self.var_std_name.get(),
                                            self.var_div.get(),
                                            self.var_roll.get(),
                                            self.var_gender.get(),
                                            self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                            self.var_email.get(),
                                            self.var_phone.get(),
                                            self.var_address.get(),
                                            self.var_radio1.get(),
                                            self.var_std_id.get()
                                        ))
                else:
                    if not Update:#Nếu bấm no trở lại
                        return
                messagebox.showinfo("Thành công","Cập nhật thông tin sinh viên thành công",parent=self.root)
                conn.commit()#xác thực câu lệnh
                self.fetch_data()#Hiện thị dữ liệu sau update
                self.reset_data()#Lám mới các txtbox
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    #Delete Function
    def delete_data(self):#Xóa thông tin sinh viên theo mã id
        if self.var_std_id.get()=="":
            messagebox.showerror("Lỗi","Không được bỏ trống ID sinh viên",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Xoá sinh viên","Bạn có muốn xóa sinh viên này?",parent=self.root)
                if delete>0:
                        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                        my_cursor = conn.cursor()
                        sql="delete from student where Student_id=%s"#Câu lệnh xóa sinh viên theo id sinh viên
                        val=(self.var_std_id.get(),)
                        my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Xóa","Xóa sinh viên thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)


    #===================Reset function====================
    def reset_data(self):#Hàm rest cấc thong tin  txtbox
        self.var_year.set("Chọn khóa học"),
        self.var_semester.set("Chọn học kỳ"),
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_div.set(""),
        self.var_roll.set(""),
        self.var_gender.set("Nam"),
        self.dob_entry.set_date(strftime("%d/%m/%Y")),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_address.set(""),

        self.var_radio1.set(""),
        self.getNextid()
    def search_data(self):#Hàm tìm kiếm
            if self.var_com_search.get() == "" or self.var_search.get() == "":
                messagebox.showerror("Lỗi !", "Vui lòng nhập thông tin đầy đủ",parent=self.root)

            else:
                try:
                    conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                    my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID sinh viên"
                    #convert loại tìm kiếm về tên các côt trọng mysql
                    if (self.var_com_search.get() == "ID sinh viên"):
                        self.var_com_search.set("Student_id")
                    elif (self.var_com_search.get() == "Tên sinh viên"):
                        self.var_com_search.set("Name")
                    elif (self.var_com_search.get() == "Lớp biên chế"):
                        self.var_com_search.set("Class")
                    #câu lệnh tìm kiếm
                    my_cursor.execute("select * from student where " + str(
                        self.var_com_search.get()) + " Like '%" + str(self.var_search.get()) + "%'")
                    data = my_cursor.fetchall()
                    if (len(data) != 0):#Nếu có dữ liệu thì in lên bảng
                        self.student_table.delete(*self.student_table.get_children())
                        for i in data:
                            self.student_table.insert("", END, values=i)
                        #thông báo có bao nhiêu dữ liệu tìm kiếm đc
                        messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi thỏa mãn điều kiện",parent=self.root)
                        conn.commit()
                    else:#nếu ko có dữ liệu thông báo ko có bản ghi 
                        self.student_table.delete(*self.student_table.get_children())
                        messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    #=============generate dataset and take photo=================
    def generate_dataset(self):#Chụp ảnh sinh viên
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # check email
        if  self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        elif (re.search(regex, self.var_email.get()) == None):
            messagebox.showerror("Error", "Vui lòng nhập email đúng định dạng", parent=self.root)
        elif (self.var_phone.get().isnumeric() != True):
            messagebox.showerror("Error", "Vui lòng nhập số điện thoại đúng", parent=self.root)
        elif (self.var_roll.get().isnumeric() != True):
            messagebox.showerror("Error", "Vui lòng nhập số CMND đúng", parent=self.root)
        else:
            try:#update thông tin sinh viên
                conn=mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)

                my_cursor = conn.cursor()
                id=self.var_std_id.get()
                my_cursor.execute("update student set Year=%s,Semester=%s,Name=%s,Class=%s,"
                              "Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,PhotoSample=%s where Student_id=%s",
                              (

                                  self.var_year.get(),
                                  self.var_semester.get(),
                                  self.var_std_name.get(),
                                  self.var_div.get(),
                                  self.var_roll.get(),
                                  self.var_gender.get(),
                                  self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                  self.var_email.get(),
                                  self.var_phone.get(),
                                  self.var_address.get(),
                                  self.var_radio1.get(),
                                  self.var_std_id.get()
                              ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                #=========load haar===================
                face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")#Model phát hiện khuôn mặt trong màn hình
                def face_cropped(img):#Cắt khuôn mặt đã phát hiện theo hình ô vuông
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#chuyển ảnh về dạng gray để phát hiện khuôn mặt
                    faces=face_classifier.detectMultiScale(gray,1.3,5)#tỉ lệ của thuật toán phát hiện khuôn mặt
                    #1.3 hệ số thu nhỏ
                    #Số khuôn mặt tối đa có thể nhận diện
                    for(x,y,w,h) in faces:#với mỗi khuôn mặt phát hiện trên khung hình, cắt khuôn mặt ra
                        face_cropped=img[y:y+h,x:x+w]
                        return  face_cropped
                cap=cv2.VideoCapture(0)#Mở camera webcam(=0) bằng thư viện xử lý ảnh opencv
                img_id=0#Số ảnh chụp
                while True:#Nếu ko có lỗi mở cam
                    net,my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1#với mỗi ảnh chụp đc tăng số ảnh lên 1
                        face=cv2.resize(face_cropped(my_frame),(190,190))
                        face=cv2.cvtColor(face_cropped(my_frame),cv2.COLOR_BGR2GRAY)
                        fill_name_path="data/user."+str(id)+"."+str(img_id)+".jpg"#tên ảnh lưu vào thư mục

                        cv2.imwrite(fill_name_path,face)#Lưu ảnh khuôn mặt vào folder data
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)#in số ảnh đã chụp lên giao diện cam
                        cv2.imshow("Cropped Face",face)#Hiện thị các ảnh đã cắt

                    if cv2.waitKey(1)==13 or int(img_id)==120:#Nếu số ảnh đã chụp =120 thì dừng lại
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Kết quả","Tạo dữ liệu khuôn mặt thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    #==========================TrainDataSet=======================
    def train_classifier(self):#Hàm train model nhận diện
        data_dir=("data")#Thư mục chứa các ảnh chụp sinh viên
        #Lấy danh sách đường dẫn đến tất cả các tệp tin trong một thư mục chứa các ảnh chụp sinh viên
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]
        faces=[]
        ids=[]
        for image in path:#với từng ảnh trong thư mục
            img=PIL.Image.open(image).convert('L')#convert ảnh về dạng pil
            imageNp=np.array(img,'uint8') # chuyển đổi một đối tượng ảnh PIL sang một mảng NumPy với kiểu dữ liệu là số nguyên không dấu 8-bit
            id=int(os.path.split(image)[1].split('.')[1])#Lấy ra id sinh viên từ tên của ảnh( ví dụ: user.1.19.jpg -> id sinh viên=1)
            faces.append(imageNp)#truyền các ảnh vào mảng
            ids.append(id)#truyền các id vào mảng
            cv2.imshow("Training",imageNp)#In ra các ảnh đã chụp
            cv2.waitKey(1)==13
        ids=np.array(ids)#convert dạng mảng

        #=================Train data classifier and save============
        clf=cv2.face.LBPHFaceRecognizer_create()#Tạo model
        clf.train(faces,ids)#Tiến hành train model
        clf.write("classifier.xml")#Lưu model đã train đc ra file classifier.xml
        cv2.destroyAllWindows()#Hủy các cửa sổ opencv
        messagebox.showinfo("Kết quả","Training dataset Completed",parent=self.root)#thông báo train thành công

    # ========================================Function Student======================================

    def get_cursorClass(self, event=""):#sự kiện ckick vào bảng lớp học
            cursor_row = self.StudentTable.focus()
            content = self.StudentTable.item(cursor_row)
            rows = content['values']
            self.var_class.set(rows[0])
            self.var_nameclass.set(rows[1])


    def add_Classdata(self):#Thêm lớp học
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()


            # =========check class=================
            my_cursor.execute("select Class from `class` ")#Danh sách lớp
            ckClass = my_cursor.fetchall()
            arrayClass = []
            for chs in ckClass:
                # print(chs[0])
                arrayClass.append(str(chs[0]))
            conn.commit()
            conn.close()
            if self.var_class.get() == "" or self.var_nameclass.get() == "":
                messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)

            elif (self.var_class.get()  in arrayClass):#Kiểm tra xem lớp nhập vào đã tồn tại chưa
                messagebox.showerror("Error", "Class đã tồn tại! Vui lòng kiểm tra lại", parent=self.root)
            else:
                try:
                    conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                    my_cursor = conn.cursor()
                    my_cursor.execute("insert into class values(%s,%s)", (
                        self.var_class.get(),
                        self.var_nameclass.get(),
                    ))
                    conn.commit()
                    self.fetch_Classdata()
                    self.reset_Classdata()
                    conn.close()
                    messagebox.showinfo("Thành công", "Thêm thông tin lớp học thành công",
                                        parent=self.root)
                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def reset_Classdata(self):#làm mới
            self.var_class.set("")
            self.var_nameclass.set("")

    def fetch_Classdata(self):#Hiện thị các lớp học
            # global mydata
            # mydata.clear()
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            my_cursor.execute("Select * from class")#Lấy tất cả thông tin trong class
            data = my_cursor.fetchall()#truyền dữ liệu vừa lấy đc vào biến data
            if len(data) != 0:#nếu có dữ liệu thì in lên bảng
                self.StudentTable.delete(*self.StudentTable.get_children())
                for i in data:
                    self.StudentTable.insert("", END, values=i)
                    mydata.append(i)
                conn.commit()
            conn.close()

    def update_Classdata(self):#Cập nhật thông tin lớp học
            if self.var_class == "" or self.var_nameclass.get() == "":
                messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)

            else:
                try:
                    Update = messagebox.askyesno("Update", "Bạn có muốn cập nhật bản ghi này không?", parent=self.root)
                    if Update > 0:
                        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                        my_cursor = conn.cursor()
                        #Câu lệnh cập nhật lớp học
                        my_cursor.execute("UPDATE `class` SET Name = %s  WHERE "
                                          "`Class` = %s",
                                          (
                                              self.var_nameclass.get(),
                                              self.var_class.get(),
                                          ))
                    else:
                        if not Update:
                            return
                    messagebox.showinfo("Thành công", "Cập nhật thông tin lớp học thành công",
                                        parent=self.root)
                    conn.commit()
                    self.reset_Classdata()
                    self.fetch_Classdata()
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

            # Delete Function

    def delete_Classdata(self):#Xóa lớp học
            if self.var_class== "" or self.var_nameclass.get() == "":
                messagebox.showerror("Lỗi", "Không được bỏ trống thông tin! ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Xoá bản ghi", "Bạn có muốn xóa bản ghi này ?", parent=self.root)
                    if delete > 0:
                        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                        my_cursor = conn.cursor()
                        sql = "delete from class where Class=%s "#Xóa lớp học với class=
                        val = (self.var_class.get(),)
                        my_cursor.execute(sql, val)
                    else:
                        if not delete:
                            return
                    conn.commit()
                    # self.fetch_data()p
                    conn.close()
                    messagebox.showinfo("Xóa", "Xóa bản ghi thành công", parent=self.root)
                    self.reset_Classdata()
                    self.fetch_Classdata()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    def search_Classdata(self):#Tìm thông tin lớp học
            if self.var_com_searchclass.get() == "" or self.var_searchclass.get() == "":
                messagebox.showerror("Lỗi !", "Vui lòng nhập thông tin đầy đủ",parent=self.root)

            else:
                try:
                    conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                    my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID sinh viên"
                    if (self.var_com_searchclass.get() == "Lớp"):
                        self.var_com_searchclass.set("Class")
                    elif (self.var_com_searchclass.get() == "Tên lớp"):
                        self.var_com_searchclass.set("Name")

                    my_cursor.execute("select * from class where " + str(
                        self.var_com_searchclass.get()) + " Like '%" + str(self.var_searchclass.get()) + "%'")
                    data = my_cursor.fetchall()
                    if (len(data) != 0):
                        self.StudentTable.delete(*self.StudentTable.get_children())
                        for i in data:
                            self.StudentTable.insert("", END, values=i)
                        messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi thỏa mãn điều kiện",parent=self.root)
                        conn.commit()
                    else:
                        self.StudentTable.delete(*self.StudentTable.get_children())
                        messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao

    obj=Student(root)
    root.mainloop()# cua so hien len

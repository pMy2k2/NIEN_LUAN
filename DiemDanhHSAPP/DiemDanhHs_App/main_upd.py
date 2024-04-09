from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from datetime import *
import time
import smtplib
import random
import PIL.Image
from tkinter import messagebox
from student_upd import Student
from teacher import Teacher
#
from face_recognition import Face_Recognition
from attendance import Attendance
from face_recognition import new_tcid


from lesson import Lesson
from import_csv import InsertData
from report_attendance import Report
from database_str import Database_str
import mysql.connector

value_from_p1 = None
def new_print(value):
    global value_from_p1
    value_from_p1 = value
    print(value_from_p1)

class Face_Recognition_System(Toplevel):
    def __init__(self, window):
        Toplevel.__init__(self)
        self.window = window
        self.geometry("1366x720+100+40")
        self.title("Hệ thống quản lý điểm danh sinh viên")
        self.resizable(False, False) # Không cho thay đổi khích thước
        self.admin_dashboard_frame = ImageTk.PhotoImage(file='ImageFaceDetect\\admin_frame.png') #Mở ảnh nền
        self.image_panel = Label(self, image=self.admin_dashboard_frame)
        self.image_panel.pack(fill='both', expand='yes') # Đặt ảnh nền làm trung tâm
        self.user_name = StringVar()  # Biến mới để lưu trữ tên người dùng
        new_tcid(value_from_p1) #Truyền id giáo viên cho face_recongnition.py khi đăng nhập vào form main_upd.py

        # thông tin kết nối database
        self.db = Database_str()

        self.txt = "Hệ thống nhận diện khuôn mặt"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self, text=self.txt, font=('times new roman', 20, "bold"), bg="white",fg='black', bd=5)
        self.heading.place(x=350, y=26, width=550)
        self.slider()
        self.heading_color()
        # =========account===========
        # ===lấy thông tin tài khoản=============
        self.account = StringVar()
        self.p_password=StringVar()
        self.n_password=StringVar()
        self.c_password=StringVar()

        if (value_from_p1 == "0"):#Nếu thông tin truyền từ form login là 0 -> tài khoản admin
            self.account.set("admin")
            self.user_name.set("Admin")
        elif (value_from_p1 == None):#Nếu chạy riêng file main thì coi như tài khoản admin
            self.account.set("admin")
            self.user_name.set("Admin")
        else:
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()
                my_cursor.execute("select Email from teacher where Teacher_id=%s", (
                    value_from_p1,
                ))
                row = my_cursor.fetchone()
                if row is not None:
                    self.user_name.set(row[0])  # Cập nhật tên người dùng
                    self.account.set(str(row[0])) #Cập nhật account cho phần đổi mật khẩu
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self)

        # ============================Ngày và giờ hệ thống==============================

        self.clock_image = ImageTk.PhotoImage(file="ImageFaceDetect/time.png")
        self.date_time_image = Label(self, image=self.clock_image, bg="white")
        self.date_time_image.place(x=35, y=45)

        self.date_time = Label(self)
        self.date_time.place(x=65, y=35)
        self.time_running()

        # ============================Icon user================================

        self.current_user_image = ImageTk.PhotoImage(file="ImageFaceDetect/current_user.png")
        self.current_user_label = Label(self, image=self.current_user_image, bg="white")
        self.current_user_label.place(x=1000, y=47)
        #Cập nhật tên người dùng đang nhập
        self.name_user = Label(self, textvariable=self.user_name, bg="white", fg="blue",  font=("times new roman", 15, "bold"))
        self.name_user.place(x=1040, y=46)
        # ============================Nút Trang chủ====================================

        self.home = ImageTk.PhotoImage(file="ImageFaceDetect/home.png")
        self.home_button = Button(self, image=self.home,font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2", command=self.click_home)
        self.home_button.place(x=43, y=113)
        self.click_home()

        # ============================Nút Quản lý===============================

        self.manage = ImageTk.PhotoImage(file="ImageFaceDetect/manage.png")
        self.manage_button = Button(self, image=self.manage,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.click_manage)
        self.manage_button.place(x=41, y=233)

        # ============================Nút Nhận diện===============================

        self.view = ImageTk.PhotoImage(file="ImageFaceDetect/view.png")
        self.view_button = Button(self, image=self.view,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2", command=self.face_recognition)
        self.view_button.place(x=41, y=353)

        # ============================Nút đổi MK===============================

        self.setting = ImageTk.PhotoImage(file="ImageFaceDetect/setting.png")
        self.setting_button = Button(self, image=self.setting,
                                     font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                     , borderwidth=0, background="white", cursor="hand2", command=self.click_setting)
        self.setting_button.place(x=41, y=473)

        # ============================Nút thoát===============================

        self.exit = ImageTk.PhotoImage(file="ImageFaceDetect/exit_button.png")
        self.exit_button = Button(self, image=self.exit,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2", command=self.click_exit)
        self.exit_button.place(x=41, y=593)

        # ============================Nút đăng xuất===============================

        self.logout = ImageTk.PhotoImage(file="ImageFaceDetect/logout.png")
        self.logout_button = Button(self, image=self.logout,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.click_logout)
        self.logout_button.place(x=1241, y=50)



    def click_home(self):
        # ===========variable============
        self.student = StringVar()
        self.teacher = StringVar()
        self.classCount = StringVar()


        home_frame = Frame(self)
        home_frame.place(x=145, y=105, height=576, width=1181)

        self.home_dashboard_frame = ImageTk.PhotoImage(file="ImageFaceDetect/home_frame.png")
        self.home_panel = Label(home_frame, image=self.home_dashboard_frame, bg="white")
        self.home_panel.pack(fill='both', expand='yes')

        try:
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            # ======== Đếm số lượn SV==========
            my_cursor.execute("select count(*) from student")
            count_st = my_cursor.fetchone()
            self.student.set(count_st[0])
            # =======Đếm số lượng lớp========
            my_cursor.execute("select count(*) from class")
            count_class = my_cursor.fetchone()
            self.classCount.set(count_class[0])
            # =======Đếm số lượng GV=============
            my_cursor.execute("select  count(*) from teacher")
            count_tc = my_cursor.fetchone()
            self.teacher.set(count_tc[0])
            conn.commit()
            conn.close()



        except BaseException as msg:
            print(msg)
        total_students = Label(home_frame, text=f" TỔNG \n {self.student.get()}\n SINH VIÊN",
                               font=("times new roman", 30, "bold"),
                               background="white", fg='#e67c0b')
        total_students.place(x=230, y=90)

        total_teacher = Label(home_frame, text=f" TỔNG \n {self.teacher.get()}\n GIÁO VIÊN",
                                font=("times new roman", 30, "bold"),
                                background="white", fg='#e67c0b')
        total_teacher.place(x=720, y=90)

        total_class = Label(home_frame, text=f" TỔNG \n {self.classCount.get()}\n LỚP HỌC",
                                 font=("times new roman", 30, "bold"),
                                 background="white", fg='#e67c0b')
        total_class.place(x=230, y=330)
        #Nút nhập file ex
        self.img_ex = ImageTk.PhotoImage(file="ImageFaceDetect/excel.png")
        self.ex_button = Button(home_frame, image=self.img_ex,
                                    relief=FLAT, activebackground="white",
                                    borderwidth=0, background="white", cursor="hand2", command=self.excel_data)
        self.ex_button.place(x=670,y=310,width=260,height=180)

    def click_manage(self):
        manage_frame = Frame(self, bg="white")
        manage_frame.place(x=145, y=105, height=576, width=1181)

        self.manage_dashboard_frame = ImageTk.PhotoImage(file="ImageFaceDetect/manage_frame.png")
        self.manage_panel = Label(manage_frame, image=self.manage_dashboard_frame, bg="white")
        self.manage_panel.pack(fill='both', expand='yes')

        #Nút quản lý Sinh viên
        img_btn1 = Image.open(r"ImageFaceDetect\student2.png")
        img_btn1 = img_btn1.resize((60, 88), Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        button_student = Button(manage_frame, text="Sinh viên", font=("times new roman", 14, "bold"), command=self.student_details,
                    image=self.photobtn1, cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        button_student.place(x=340, y=117, width=127, height=127)

        #Nút quản lý Giáo viên
        img_btn5 = Image.open(r"ImageFaceDetect\teacher.png")
        img_btn5 = img_btn5.resize((60, 88), Image.ANTIALIAS)
        self.photobtn5 = ImageTk.PhotoImage(img_btn5)
        button_att = Button(manage_frame, text="Giáo viên", font=("times new roman", 14, "bold"),
                            command=self.teacher_details,
                            image=self.photobtn5, cursor="hand2",
                            activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=535, y=117, width=127, height=127)

        #Nút thống kê các bản điểm danh
        img_btn2 = Image.open(r"ImageFaceDetect\ghichu.png")
        img_btn2 = img_btn2.resize((60, 88), Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        button_att = Button(manage_frame, text="Điểm danh", font=("times new roman", 14, "bold"),
                                command=self.attendance_data,
                                image=self.photobtn2, cursor="hand2",
                                activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=725, y=117, width=127, height=127)

        #Nút quản lý buổi học
        img_btn3 = Image.open(r"ImageFaceDetect\lesson.png")
        img_btn3 = img_btn3.resize((60, 88), Image.ANTIALIAS)
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)
        button_att = Button(manage_frame, text="Buổi học", font=("times new roman", 14, "bold"),
                            command=self.lesson_data,
                            image=self.photobtn3, cursor="hand2",
                            activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=625, y=314, width=127, height=127)

        #Nút thống kê hệ thống
        img_btn4 = Image.open(r"ImageFaceDetect\report.png")
        img_btn4 = img_btn4.resize((60, 88), Image.ANTIALIAS)
        self.photobtn4 = ImageTk.PhotoImage(img_btn4)
        button_att = Button(manage_frame, text="Thống kê", font=("times new roman", 14, "bold"),
                            command=self.report_data,
                            image=self.photobtn4, cursor="hand2",
                            activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=430, y=314, width=127, height=127)

    def click_setting(self):

        setting_frame = Frame(self, bg="white")
        setting_frame.place(x=145, y=105, height=576, width=1181)
        self.setting_dashboard_frame = ImageTk.PhotoImage(file="ImageFaceDetect/setting_frame.png")
        self.setting_panel = Label(setting_frame, image=self.setting_dashboard_frame, bg="white")
        self.setting_panel.pack(fill='both', expand='yes')

        heading = Label(setting_frame, text="Đổi mật khẩu", font=('times new roman', 20, "bold"), bg="white",
                        fg='black', bd=5, relief=FLAT)
        heading.place(x=410, y=27, width=350)

        # ============================Tên đăng nhập====================================

        self.username_label = Label(setting_frame, text="Tài khoản ", bg="white", fg="#4f4e4d",font=("times new roman", 13, "bold"))
        self.username_label.place(x=415, y=90)

        self.username_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.account,
                                    font=("times new roman ", 11), state="disabled",)
        self.username_entry.place(x=450, y=118, width=300)

        # ============================Mật khẩu củ============================

        self.p_password_label = Label(setting_frame, text="Mật khẩu cũ ", bg="white", fg="#4f4e4d",font=("times new roman", 13, "bold"))
        self.p_password_label.place(x=415, y=180)
        self.p_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.p_password,
                                      font=("times new roman ", 12), show='*')
        self.p_password_entry.place(x=450, y=207, width=300)

        # ============================Mật khẩu mới============================

        self.n_password_label = Label(setting_frame, text="Mật khẩu mới ", bg="white", fg="#4f4e4d", font=("times new roman", 13, "bold"))
        self.n_password_label.place(x=415, y=270)

        self.n_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.n_password,
                                      font=("times new roman ", 12), show='*')
        self.n_password_entry.place(x=450, y=298, width=300)

        # ============================Xác nhận lại MK============================

        self.c_password_label = Label(setting_frame, text="Nhập lại mật khẩu ", bg="white", fg="#4f4e4d",font=("times new roman", 13, "bold"))
        self.c_password_label.place(x=415, y=360)

        self.c_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.c_password,
                                      font=("times new roman ", 12), show='*')
        self.c_password_entry.place(x=450, y=388, width=300)

        # ============================Nút Xác nhận đổi MK================================

        self.submit = ImageTk.PhotoImage(file="ImageFaceDetect/submit.png")
        self.submit_button = Button(setting_frame, image=self.submit,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2",
                                    command=self.reset_pass)
        self.submit_button.place(x=520, y=450)

    def reset_pass(self):
        if self.p_password_entry.get()=="":
            messagebox.showerror("Error","Vui lòng nhập mật khẩu cũ",parent=self)
        elif self.n_password_entry.get()=="":
            messagebox.showerror("Error","Vui lòng nhập mật khẩu mới",parent=self)
        elif self.c_password_entry.get()=="":
            messagebox.showerror("Error", "Hãy nhập lại mật khẩu",parent=self)
        elif self.n_password_entry.get()!="" and self.n_password_entry.get()!=self.c_password_entry.get():
            messagebox.showerror("Error", "Xác nhận lại mật khẩu không đúng!!", parent=self)
        elif self.p_password_entry.get()==self.n_password_entry.get():
            messagebox.showerror("Error", "Mật khẩu mới trùng với mật khẩu mới", parent=self)
        else:
            if(self.username_entry.get()=="admin"):
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "SELECT  Password from admin where Account=%s ",
                    (self.username_entry.get(),))
                row = my_cursor.fetchone()
                if str(row[0])!=self.p_password_entry.get():
                    messagebox.showerror("Error","Mật khẩu cũ không đúng !!! ",parent=self)
                else:
                    my_cursor.execute("update admin set Password=%s where Account=%s",(self.n_password_entry.get(),self.username_entry.get(),))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thông báo","Đổi mật khẩu thành công",parent=self)
                    self.p_password.set("")
                    self.n_password.set("")
                    self.c_password.set("")
            else:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "SELECT  Password from teacher where Teacher_id=%s ",
                    (str(value_from_p1),))
                row = my_cursor.fetchone()
                if str(row[0])!=self.p_password_entry.get():
                    messagebox.showerror("Error", "Mật khẩu cũ không đúng !!! ", parent=self)
                else:
                    my_cursor.execute("update teacher set Password=%s where Teacher_id=%s",
                                      (self.n_password_entry.get(), str(value_from_p1),))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thông báo", "Đổi mật khẩu thành công", parent=self)
                    self.p_password.set("")
                    self.n_password.set("")
                    self.c_password.set("")


    def face_recognition(self):
        self.new_window=Toplevel(self)
        self.app=Face_Recognition(self.new_window)
    def student_details(self):
        self.new_window=Toplevel(self)
        self.app=Student(self.new_window)

    def teacher_details(self):
        self.new_window = Toplevel(self)
        self.app = Teacher(self.new_window)
    def attendance_data(self):
        self.new_window=Toplevel(self)
        self.app=Attendance(self.new_window)

    def lesson_data(self):
        self.new_window = Toplevel(self)
        self.app = Lesson(self.new_window)
    def report_data(self):
        self.new_window=Toplevel(self)
        # self.app=Report(self.new_window)

    def excel_data(self):
        self.new_window = Toplevel(self)
        self.app = InsertData(self.new_window)


    def click_exit(self):

        self.deiconify()
        ask = messagebox.askyesnocancel("Xác nhận thoát", "Bạn chắc chắn muốn đóng chương trình?", parent=self)
        if ask is True:
            self.quit()

    def click_logout(self):

        Exit = messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?", parent=self)
        if (Exit > 0):
            self.destroy()
            self.window.show()
        else:
            if not Exit:
                return

    def slider(self):
        if self.count >= len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)
        else:
            self.text = self.text + self.txt[self.count]
            self.heading.config(text=self.text)
        self.count += 1
        self.heading.after(100, self.slider)

    def heading_color(self):
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)

    def time_running(self):

        self.time = time.strftime("%H:%M:%S")
        self.date = time.strftime('%d/%m/%Y')
        concated_text = f"  {self.time} \n {self.date}"
        self.date_time.configure(text=concated_text, font=("times new roman", 13, "bold"), relief=FLAT
                                 , borderwidth=0, bg="white", fg="black")
        self.date_time.after(100, self.time_running)

if __name__ == '__main__':
    window = Tk()  # khoi tao cua so va gan root vao
    obj = Face_Recognition_System(window)
    window.mainloop()  # cua so hien len


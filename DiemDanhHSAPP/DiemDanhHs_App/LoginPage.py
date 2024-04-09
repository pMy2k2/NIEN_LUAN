from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
from tkinter import messagebox
from datetime import *
import time
from time import strftime
from main_upd import Face_Recognition_System
from main_upd import new_print
from teacher import check_user

class LoginPage(object):
    # hàm khởi tạo giao diện
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')  # kích thước giao diện
        self.window.resizable(0, 0)  # ko cho giao diện thu nhỏ
        # self.window.state('zoomed') #giao diện hiển thị toàn màn hình
        self.window.title('Đăng nhập hệ thống')  # tiêu đề của cửa sổ app
        today = strftime("%d-%m-%Y")  # thời gian ngày-tháng-năm

        # =============biến kiểu string email,password============
        self.var_email = StringVar()
        self.var_password = StringVar()

        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('ImageFaceDetect\\background1.png')  # khai báo biến bg_frame là ảnh background trong thư mục ImageFaceDetect\\background1.png
        photo = ImageTk.PhotoImage(self.bg_frame)  # chuyển ảnh về lớp ImageTk
        self.bg_panel = Label(self.window, image=photo)  # Khai báo biến bg_panel chứa ảnh photo
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')  # Vị trí của lớp Label : chính giữa giao diện
        # ====== Login Frame =========================

        self.lgn_frame = Frame(self.window, bg='#15233c', width=900, height=600)
        self.lgn_frame.place(x=265, y=70)


        # ======Hiện thị ngày====
        self.txt = today
        self.heading = Label(self.lgn_frame, text=self.txt, font=('times new roman', 25, "bold"), bg="#15233c", fg='white',bd=5)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ============Ảnh bên trái================================================

        self.side_image = Image.open('ImageFaceDetect\\vector.png')
        photo = ImageTk.PhotoImage(self.side_image) # chuyển ảnh về lớp ImageTk
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#15233c')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ============ Icon đăng nhập =============================================

        self.sign_in_image = Image.open('ImageFaceDetect\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image) # chuyển ảnh về lớp ImageTk
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#15233c')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ============ Label Đăng nhập =============================================

        self.sign_in_label = Label(self.lgn_frame, text="Đăng nhập", bg="#15233c", fg="white",
                                   font=("times new roman", 17, "bold"))
        self.sign_in_label.place(x=630, y=240)


        # ============================tài khoản====================================
        # ===== Lable Tài khoản =========
        self.username_label = Label(self.lgn_frame, text="Tài khoản", bg="#15233c", fg="white", font=("times new roman", 13, "bold"))
        self.username_label.place(x=550, y=300)
        # ===== Khung nhập Tài khoản =========
        self.txtuser = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#15233c", fg="white", insertbackground='white', font=("times new roman ", 13, ), textvariable=self.var_email)
        self.txtuser.place(x=580, y=335, width=270)
        # ===== Đường line =========
        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # =====  icon tài khoản =========
        self.username_icon = Image.open('ImageFaceDetect\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#15233c')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ============================Mật khẩu====================================
        # ===== Lable Mật khẩu =========
        self.password_label = Label(self.lgn_frame, text="Mật khẩu", bg="#15233c", fg="white", font=("times new roman", 13, "bold"))
        self.password_label.place(x=550, y=380)
        # ===== Khung nhập mật khẩu =========
        self.txtpass = Entry(self.lgn_frame,  relief=FLAT, bg="#15233c", fg="white", insertbackground='white', font=("times new roman", 12, "bold"), show="*", textvariable=self.var_password)
        self.txtpass.place(x=580, y=416, width=244)
        # ===== Đường line =========
        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)

        # ======== icon mật khẩu ================
        self.password_icon = Image.open('ImageFaceDetect\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#15233c')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)

        # ============================Nút đăng nhập================================

        self.lgn_button = Image.open('ImageFaceDetect\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#15233c')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='Đăng nhập', command=self.login,
                            font=("times new roman", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3057ff', fg='white')
        self.login.place(x=20, y=15)

        # =============Kiểm tra admin=============
        self.varcheck = IntVar()
        checkbtn = Checkbutton(self.lgn_frame, variable=self.varcheck,
                               font=("times new roman", 12), onvalue=1, offvalue=0, bg="#15233c")
        checkbtn.place(x=550, y=510)

        self.check_label = Label(self.lgn_frame, text="Đăng nhập bằng tài khoản admin", bg="#15233c", fg="white", font=("times new roman", 12, "bold"))
        self.check_label.place(x=580, y=513)

        # ========= show/hide password ==================================================================
        # ảnh nút hiển thị password
        self.show_image = ImageTk.PhotoImage(file='ImageFaceDetect\show.png')

        # ảnh  nút ẩn password
        self.hide_image = ImageTk.PhotoImage(file='ImageFaceDetect\hide.png')

        # nút hiển thị password
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.showpass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def showpass(self):  # hàm hiển thị mật khẩu
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.txtpass.config(show='')

    def show(self):
        self.window.update()
        self.window.deiconify()

    def hide(self):  # hàm ẩn mật khẩu dưới dạng ***
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.showpass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.txtpass.config(show='*')

    # reset thông tin password_tài khoản
    def reset(self):
        self.var_email.set("")
        self.var_password.set("")
        self.varcheck.set(0)

    # hàm đăng nhập
    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Lỗi !!", "Vui lòng nhập đầy đủ thông tin")
        elif (self.varcheck.get() == 1):
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',port='3306')
                my_cursor = conn.cursor()
                my_cursor.execute("select * from admin where Account=%s and Password=%s", (
                    self.var_email.get(),
                    self.var_password.get()
                ))
                row = my_cursor.fetchone()
                if row == None:
                    messagebox.showerror("Lỗi", "Sai tên đăng nhập, mật khẩu hoặc quyền đăng nhập")
                else:
                    new_print(str(0))
                    check_user(0)
                    self.reset()
                    messagebox.showinfo("Thông báo", "Bạn đã đăng nhập thành công với quyền Admin")
                    self.window.withdraw()
                    self.app = Face_Recognition_System(self)
                conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self)
        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')
                my_cursor = conn.cursor()
                my_cursor.execute("select Teacher_id from teacher where Email=%s and Password=%s", (
                    self.var_email.get(),
                    self.var_password.get()
                ))
                row = my_cursor.fetchone()

                if row == None:
                    messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")
                else:
                    new_print(str(row[0]))
                    check_user(1)
                    self.reset()
                    self.window.withdraw()
                    self.app = Face_Recognition_System(self)
                conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self)


if __name__ == '__main__':
    window = Tk()  # tạo giao diện tkinter Tk() và gán nó vào biến window
    obj = LoginPage(window)
    window.mainloop()  # hiển thị giao diện và bắt đầu nhận các sự kiện để xử lý.

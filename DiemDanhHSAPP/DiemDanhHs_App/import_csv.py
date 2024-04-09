from PIL import Image, ImageTk,ImageDraw
from tkinter import *
from tkinter import ttk
import PIL.Image ,PIL.ImageDraw
import csv
from tkinter import filedialog
import os
import mysql.connector
from tkinter import messagebox
import pandas as pd
from database_str import Database_str
mydata=[]
class InsertData:
    def __init__(self,root):
        self.root=root
        self.root.title("Quản lý thông tin")#tiêu đề
        self.root.geometry("900x550+0+0")
        self.root.config(bg="#021e2f")
        left_lbl = Label(self.root, bg="#08A3D2", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=400)
        right_lbl = Label(self.root, bg="white", bd=2)
        right_lbl.place(x=200, y=0, relheight=1, relwidth=1)

        # ===========Frame===========
        # thông tin kết nối database
        self.db = Database_str()

        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn1 = img_btn1.resize((120, 30), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)

        title = Label(right_lbl, text="Thêm danh sách sinh viên: ", font=("times new roman", 12, "bold"), bg="white", fg="black").place(x=50, y=240)

        #chọn file danh sách hoc sinh
        btn_choose = Button(right_lbl, text="Choose File...", command=self.insert_stu, font=("times new roman", 11, "normal"),
                           bd=0,image=self.photobtn1,fg="white", compound="center",
                            cursor="hand2").place(x=280, y=240, width=120, height=30)


    #thêm danh sách sinh viên từ file csv
    def insert_stu(self):
        try:
            global mydata
            mydata.clear()
            fln = filedialog.askopenfilename(initialdir=os.getcwd() + "/ListCSV", title="Open CSV",
                                             filetypes=(("Excel File", ".xlsx"), ("ALL File", "*.*")), parent=self.root)
            print(fln)

            df = pd.read_excel(fln)#đọc file excel đã chọn

            for index, row in df.iterrows():#truyền dữ liệu trong file excel ra biến mydata
                mydata.append((row[0], row[1], row[2],row[3], row[4], row[5],row[6], row[7].replace("'",""), row[8],row[9], row[10],row[11]))

            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()

            #câu lệnh thêm danh sách sinh viên
            sql_insert_query = "insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            my_cursor.executemany(sql_insert_query, mydata)
            conn.commit()
            messagebox.showinfo("Thông báo", "Thêm danh sách sinh viên!!!")
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()  # khoi tao cua so va gan root vao
    obj = InsertData(root)
    root.mainloop()  # cua so hien len
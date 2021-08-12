import socket
import sys
import tkinter as tk
from tkinter import Frame, Label, messagebox
from tkinter import ttk
import tkinter
from tkinter.constants import RAISED 
from tkinter import *

Payload = 2048

LOGIN = "login"
LOGOUT = "logout"
SIGNUP = "signup"
EXIT = "out"
SEARCH = "search"
FONT = ("Calibri", 15, "bold")
idx = 0

class GUILogin(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("500x250")
        self.iconbitmap('a.ico')
        self.title("TRA CỨU COVID-19")
        self.protocol("WM_DELETE_WINDOW", self.quitClose)
        self.resizable(width = False, height = False)

        box = tk.Frame(self)
        box.pack(side = "top", fill = "both", expand = True)
        
        box.grid_columnconfigure(0, weight = 1)
        box.grid_rowconfigure(0, weight = 1)

        self.frames = {}
        for F in (LoginStart, MainPage):
            frame = F(box, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky= "nsew")

        self.nowSlide(LoginStart)
    
    def nowSlide(self, box):
        frame = self.frames[box]
        if box == MainPage:
            self.geometry("900x600")
        else:
            self.geometry("500x250")
        frame.tkraise()

    def quitClose(self):
        if messagebox.askyesno("THOÁT CHƯƠNG TRÌNH", "BẠN CÓ MUỐN THOÁT KHÔNG?"):
            try:
                choice = EXIT
                client.sendall(choice.encode('utf-8'))
                print("Đã thoát!")
                client.close()
            except: 
                window = tkinter.Tk()
                window.wm_withdraw()
                window.geometry("1x1+200+200")
                messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
                client.close()
                sys.exit(0)

            self.destroy()

    def LoginIn(self, nowFrame, sock):
        try:
            UserName = nowFrame.boxUser.get()
            Password = nowFrame.boxPassword.get()

            print ("Username: ", UserName)
            print ("Password: ", Password)

            if Password == "":
                nowFrame.Notice["text"] = "Mật khẩu không thể để trống!"
                return
            elif UserName == "":
                nowFrame.Notice["text"] = "Tài khoản không thể để trống!"
                return
            elif UserName == "" and Password == "":
                nowFrame.Notice["text"] = "Tài khoản và mật khẩu trống"
                return

            choice = LOGIN
            sock.sendall(choice.encode('utf-8'))
            
            # Sock send user
            sock.sendall(UserName.encode('utf-8'))
            sock.recv(Payload)
            print ("Has responded")

            # Sock send Password
            sock.sendall(Password.encode('utf-8'))
            sock.recv(Payload)
            print ("Has responded")

            check = sock.recv(Payload).decode('utf-8')
            if check == '1':
                self.nowSlide(MainPage)
            elif check == '2':
                nowFrame.Notice["text"] = "Mật khẩu và tài khoản có thể sai"
            elif check == '0':
                nowFrame.Notice["text"] = "Bạn đã đăng nhập sẵn rồi!"

        except: 
            nowFrame.Notice["text"] = "Server không thể phản hồi!"
            print("Lỗi server không phản hồi!")
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            sock.close()
            sys.exit(0)

    def SignUp(self, nowFrame, sock):
        try:
            UserName = nowFrame.boxUser.get()
            Password = nowFrame.boxPassword.get()

            if Password == "":
                nowFrame.Notice["text"] = "Mật khẩu không thể để trống!"
                return
            elif UserName == "":
                nowFrame.Notice["text"] = "Tài khoản không thể để trống!"
                return
            elif UserName == "" and Password == "":
                nowFrame.Notice["text"] = "Tài khoản và mật khẩu trống"
                return

            choice = SIGNUP
            sock.sendall(choice.encode('utf-8'))

            sock.sendall(UserName.encode('utf-8'))
            sock.recv(Payload)
            print ("Has responded")

            sock.sendall(Password.encode('utf-8'))
            sock.recv(Payload)
            print ("Has responded")
            
            check = sock.recv(Payload).decode('utf-8')
            if check == "True":
                self.nowSlide(MainPage)
            elif check == "Already":
                nowFrame.Notice["text"] = "Tài khoản đã đăng ký và có người sử dụng"
            elif check == "False":
                nowFrame.Notice["text"] = "Tài khoản đã đăng ký"
            
        except:
            nowFrame.Notice["text"] = "Server không phản hồi, ngắt kết nối"
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            client.close()
            sys.exit(0)

    def LogOut(self, nowFrame, sock):
        try: 
            choice = LOGOUT
            sock.sendall(choice.encode('utf-8'))

            check = sock.recv(Payload).decode('utf-8')
            if check == "True":
                self.nowSlide(LoginStart)
                for i in nowFrame.tree.get_children():
                    nowFrame.tree.delete(i)
                nowFrame.update()
                sock.sendall("Thoát tài khoản thành công!".encode('utf-8'))
            else:
                print("Server không phản hồi!")
        except:
            nowFrame.Notice["text"] = "Server Không phản hồi"
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            sock.close()
            sys.exit(0)

class LoginStart(tk.Frame):

    def __init__(self, home, control):
        tk.Frame.__init__(self, home)
        self.configure(bg = "#e1dcfd")

        Title = tk.Label(self, text= "\nĐĂNG NHẬP THÔNG TIN\n", font = FONT, fg = '#5a5865', bg = "#e1dcfd").grid(row = 3, column = 1)
        User = tk.Label(self, text = "\tTÀI KHOẢN", fg = '#5a5865', bg = "#e1dcfd", font='Calibri 12 bold').grid(row = 4, column = 0)
        Passw = tk.Label(self, text = "\tMẬT KHẨU ", fg = '#5a5865', bg = "#e1dcfd", font='Calibri 12 bold').grid(row = 5, column = 0)

        self.Notice = tk.Label(self, text = "", bg = "#e1dcfd", fg = 'red')
        self.boxUser = tk.Entry(self, width = 35, bg = '#dff0ee')
        self.boxPassword = tk.Entry(self, width = 35, bg = '#dff0ee')

        ButtLog = tk.Button(self, text = "Đăng Nhập", bg = "#5a5865", fg = '#dff0ee', command = lambda: control.LoginIn(self, client))
        ButtLog.configure(width = 14)
        ButtSign = tk.Button(self, text = "Đăng ký", bg = "#5a5865", fg = '#dff0ee', command = lambda: control.SignUp(self, client))
        ButtSign.configure(width = 14)

        self.boxUser.grid(row = 4, column = 1)
        self.boxPassword.grid(row = 5, column = 1)
        IPaddress = tk.Label(self, text = "\tIP server: " + str(add), fg = '#5a5865', bg = "#e1dcfd", font='Calibri 10 bold').grid(row = 6, column = 1, sticky = "W")
        self.Notice.grid(row = 7, column = 1)

        ButtLog.grid(row = 8, column =  1, sticky = "E")
        ButtSign.grid(row = 8, column = 1, sticky = "W") 

class MainPage(tk.Frame):
    
    def __init__(self, home, control):
        tk.Frame.__init__(self, home)
        self.configure(bg = "#e1dcfd")

        left_frame = Frame(self, width = 400, height = 500, bg = '#DDC488')
        left_frame.grid(row = 0, column = 0, padx = 10, pady = 5)
        
        right_frame = Frame(self, width = 400, height = 300, bg = '#999966')
        right_frame.grid(row = 1, column = 0, padx = 10, pady = 5)
        
        Label(left_frame, text = "TRA CỨU DỮ LIỆU COVID-19", font = FONT, relief = RAISED).grid(row = 0, column = 0, padx = 5, pady = 5)

        tool_bar = Frame(left_frame, width = 180, height= 185, bg = '#DDC488')
        tool_bar.grid(row = 3, column = 0, padx = 5, pady = 5)

        self.Notice = tk.Label(left_frame, text = "", bg = "#DDC488")
        self.Notice.grid(column = 0, row = 2)

        self.tree = ttk.Treeview(right_frame)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background = "white", foreground = "black", rowheight = 25, fieldbackground = "white")
        style.map("Treeview", background = [('selected', 'blue')])
        
        self.tree["column"] = ("Tên nước", "Số ca hôm nay", "Ca nhiễm", "Tử vong", "Hồi phục", "Nguy kịch", "Đang nhiễm")
        self.tree.column('#0', width = 0, stretch = tk.NO)
        self.tree.column("Tên nước", anchor = 'c', width = 120)
        self.tree.column("Số ca hôm nay", anchor = 'c', width = 120)
        self.tree.column("Ca nhiễm", anchor = 'c', width = 150)
        self.tree.column("Tử vong", anchor = 'c', width = 120)
        self.tree.column("Hồi phục", anchor = 'c', width = 120)
        self.tree.column("Nguy kịch", anchor = 'c', width = 120)
        self.tree.column("Đang nhiễm", anchor = 'c', width = 120)

        self.tree.heading("0", text = "", anchor = 'c')
        self.tree.heading("Tên nước", text = "TÊN NƯỚC", anchor = 'c')
        self.tree.heading("Số ca hôm nay", text = "CA HÔM NAY", anchor = 'c')
        self.tree.heading("Ca nhiễm", text = "TỔNG CA NHIỄM", anchor = 'c')
        self.tree.heading("Tử vong", text = "TỬ VONG", anchor = 'c')
        self.tree.heading("Hồi phục", text = "HỒI PHỤC", anchor = 'c')
        self.tree.heading("Nguy kịch", text = "NGUY KỊCH", anchor = 'c')
        self.tree.heading("Đang nhiễm", text = "ĐANG NHIỄM" , anchor = 'c')
        self.tree.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.EntrySearch = tk.Entry(left_frame, width = 25, font = ("Calibri", 15, "bold"), bg = 'light yellow')
        self.EntrySearch.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
        self.LabelEntry = tk.Label(left_frame, text = "     NHẬP TÊN NƯỚC", font = ("Calibri", 15, "bold"), bg = '#DDC488').grid(row = 1, column = 0, sticky = "W")
        self.table = self.tree

        Button(tool_bar, text ="TÌM KIẾM", command = self.searchBox, width = 15).grid(row = 0, column = 1, padx = 5, pady = 3, ipadx = 10)
        Button(tool_bar, text = "XÓA LIST", command = self.clearRow, width = 15).grid(row = 0, column = 0, padx = 5, pady = 3, ipadx = 10)
        Button(tool_bar, text ="ĐĂNG XUẤT", command = lambda: control.LogOut(self, client), width = 15).grid(row = 0, column = 2, padx = 5, pady = 3, ipadx = 10)

    def searchBox(self):
        try:
            choice = SEARCH
            client.sendall(choice.encode('utf-8'))

            boxData = []
            #boxData: [Tên nước, số ca hôm nay, ca nhiễm, tử vong, hồi phục, nguy kịch, đang nhiễm]
            self.Notice["text"] = ""

            countryName = self.EntrySearch.get()
            if (countryName == ""):
                self.Notice["text"] = "Không được bỏ trống"
                return

            client.sendall(countryName.encode('utf-8'))
            checkRes = client.recv(Payload).decode('utf-8')
            print(checkRes)

            checkIsTrue = client.recv(Payload).decode('utf-8')
            if (checkIsTrue == "-1"):
                print("Nhập sai dữ liệu")
                self.Notice["text"] = "Nhập dữ liệu sai, nhập lại!"
                return

            boxData.append(countryName)

            client.sendall("Client tiến hành gửi lại phản hồi lần 1".encode('utf-8'))
            todaycase = client.recv(Payload).decode('utf-8')
            boxData.append(todaycase)

            client.sendall("Client tiến hành gửi lại phản hồi lần 2".encode('utf-8'))
            cases = client.recv(Payload).decode('utf-8')
            boxData.append(cases)

            client.sendall("Client tiến hành gửi lại phản hồi lần 3".encode('utf-8'))
            deaths = client.recv(Payload).decode('utf-8')
            boxData.append(deaths)

            client.sendall("Client tiến hành gửi lại phản hồi lần 4".encode('utf-8'))
            recovered = client.recv(Payload).decode('utf-8')
            boxData.append(recovered)

            client.sendall("Client tiến hành gửi lại phản hồi lần 5".encode('utf-8'))
            critical = client.recv(Payload).decode('utf-8')
            boxData.append(critical)

            client.sendall("Client tiến hành gửi lại phản hồi lần 6".encode('utf-8'))
            active = client.recv(Payload).decode('utf-8')
            boxData.append(active)

            self.tree.tag_configure('odd', background = 'white')
            self.tree.tag_configure('even', background = '#CCCCFF')

            global idx
            if idx % 2 == 0:
                self.table.insert(parent = "", index = "end", iid = idx, values = (boxData[0], boxData[1], boxData[2], boxData[3], boxData[4], boxData[5], boxData[6]), tags = ('even',))
            else:
                self.table.insert(parent = "", index = "end", iid = idx, values = (boxData[0], boxData[1], boxData[2], boxData[3], boxData[4], boxData[5], boxData[6]), tags = ('odd',))
            idx += 1

        except:
            print("Server không phản hồi!")
            self.Notice["text"] = "Server không phản hồi, ngắt kết nối!"
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            client.close()
            sys.exit(0)

    def clearRow(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.update()

if __name__ == '__main__':

    add = input("Nhập địa chỉ IP: ")
    port = input("Nhập số port của Server (Server tra cứu là 65432): ")

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as er:
        print("Error creating socket: ", er)
        sys.exit(1)
    try:
        serverAdrr = add, int(port)
        client.connect(serverAdrr)
    except socket.gaierror as e:
        print("Address-related error connecting to server: ", e)
        sys.exit(1)
    except socket.error as e:
        print("Error: ", e)
        sys.exit(1)
    try:
        app = GUILogin()
        app.mainloop()
    except:
        print("Server không phản hồi!")
        client.close()
        sys.exit(1)
    finally:
        client.close()

import tkinter as tk
import tkinter
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import *
import threading
import json
import socket
from urllib.request import urlopen
import sys

PORT = 65432

LOGIN = "login"
LOGOUT = "logout"
SIGNUP = "signup"
EXIT = "out"
SEARCH = "search"
FONT = ("Calibri", 25, "bold")

Payload = 2048

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOSTNAME = socket.gethostname()
    ADDRESS = socket.gethostbyname(HOSTNAME)
    print(ADDRESS)
    
except socket.error as er:
    print("Lỗi khi tạo socket: ", er)
    sys.exit(1)
try:
    sock.bind((ADDRESS, PORT))
    sock.listen(10)
except socket.gaierror as e:
    print("Address-related error connecting to server: ", e)
    sys.exit(1)
except socket.error as e:
    print("Lỗi kết nối: ", e)
    sys.exit(1)

def handleClient(Client_Sock, Client_Address):
        try:
            while True:
                choice = Client_Sock.recv(Payload).decode('utf-8')
                print("Client muốn: ", choice)

                if choice == LOGIN:
                    LoginIn_Client(Client_Sock, Client_Address)
                elif choice == SIGNUP:
                    SignUp_Client(Client_Sock, Client_Address)
                elif choice == LOGOUT:
                    LogOut_Client(Client_Sock, Client_Address)
                elif choice == EXIT:
                    Exit_Client(Client_Address)
                    break
                elif choice == SEARCH:
                    SendData_Client(Client_Sock)
                else:
                    break

            Client_Sock.close()
            print("Kết thúc phiên làm việc của client", str(Client_Address))

        except OSError as e:
            print(str(e))
        finally:
            Client_Sock.close()

def handleServer():
    try:
        print ("...Đợi kết nối từ server...")
        while True:
            print ("...Kết nối...")
            Client_Sock, Client_Address = sock.accept()
            threading.Thread(target = handleClient, daemon = True, args = (Client_Sock, Client_Address)).start()

    except KeyboardInterrupt:
        print("Lỗi xử lý!!")
        sock.close()
    finally:
        print("Kết thúc tiến trình!")
        sock.close()

def getData(filename):
    url = "https://coronavirus-19-api.herokuapp.com/countries"
    response = urlopen(url)
    data = json.loads(response.read())

    json_object = json.dumps(data, indent = 4)

    with open(filename, "w") as outfile:
        outfile.write(json_object)

class manageAccount:

    def __init__(self, username, password):
        self.user =  username
        self.password = password

    def createAccount(self):
        if self.checkAccount() == "2":
            with open('Account.json','r+') as file:
                file_data = json.load(file)
                file_data["Account"].append(self.user)
                file_data["Password"].append(self.password)

                file.seek(0)
                json.dump(file_data, file, indent = 4)
            print ("Tạo tài khoản thành công")
        else: 
            print ("Tạo tài khoản thất bại")

    def checkAccount(self):
        with open('Account.json') as file:
            file_data = json.load(file)

        if self.checkAlreadyAccount() == True:
            return "0"

        if self.user in file_data["Account"]:
            i = file_data["Account"].index(self.user)
            if self.password in file_data["Password"]:
                j = file_data["Password"].index(self.password)
                if i == j:
                    return "1"
                return "2"
            else:
                return "2"
        else: 
            return "2"

    def saveAlreadyAccount(self, addr):
        with open('AccountLive.json', 'r+') as file:
            file_data = json.load(file)
            file_data["Account"].append(self.user)
            file_data["Password"].append(self.password)
            file_data["Address"].append(addr)

            file.seek(0)
            json.dump(file_data, file, indent = 4)
            
            print ("Insert now user to server success!")
    
    def checkAlreadyAccount(self):
        with open('AccountLive.json') as file:
            file_data = json.load(file)

        if self.user in file_data["Account"]:
            i = file_data["Account"].index(self.user)
            if self.password in file_data["Password"]:
                j = file_data["Password"].index(self.password)
                if i == j:
                    return True
                return False
            else:
                return False
        else: 
            return False
    
def removeExitAccount(addr):
    with open('AccountLive.json') as file: 
        file_data = json.load(file)
    try:
        i = 0
        for element in file_data["Address"]:
            if str(addr) in element:
                file_data["Address"].remove(str(addr))
                break
            i = i + 1
        
        del file_data["Password"][i]
        del file_data["Account"][i]

        with open('AccountLive.json', 'w') as data_file:
            data = json.dump(file_data, data_file, indent = 4)
            print("Xóa xong!")
    except:
        print("Không xóa được!")
        
def LoginIn_Client(sock, addr):

    # Sock receive User
    UserName = sock.recv(Payload).decode('utf-8')
    print("USERNAME: ", UserName)
    sock.sendall(UserName.encode('utf-8'))

    # Sock receive Password from user
    Password = sock.recv(Payload).decode('utf-8')
    print("PASSWORD: ", Password)
    sock.sendall(Password.encode('utf-8'))

    Check = manageAccount(UserName, Password).checkAccount()

    if Check == '1':
        manageAccount(UserName, Password).saveAlreadyAccount(str(addr))
        print ("ACCEPT!")

    sock.sendall(Check.encode('utf-8'))
    print ("End Login Process")

def SignUp_Client(sock, addr):

    UserName = sock.recv(Payload).decode('utf-8')
    print("USERNAME: ", UserName)
    sock.sendall(UserName.encode('utf-8'))

    Password = sock.recv(Payload).decode('utf-8')
    print("PASSWORD: ", Password)
    sock.sendall(Password.encode('utf-8'))

    Account = manageAccount(UserName, Password)
    Check = Account.checkAccount()

    if Check == "2":
        Account.createAccount()
        Account.saveAlreadyAccount(str(addr))
        sock.sendall("True".encode('utf8'))
    elif Check == "0":
        sock.sendall("Already".encode('utf-8'))
    elif Check == "1":
        sock.sendall("False".encode('utf-8'))

    print("End Sign Up")

def LogOut_Client(sock, addr):
    removeExitAccount(addr)
    try:
        sock.sendall("True".encode('utf-8'))
        ok = sock.recv(Payload).decode('utf-8')
        print(ok)
    except:
        print("Lỗi về mật khẩu/Tài khoản!")

def Exit_Client(addr):
    removeExitAccount(str(addr))
    window = tkinter.Tk()
    window.wm_withdraw()
    window.geometry("1x1+200+200")
    messagebox.showwarning('CLIENT ĐÃ THOÁT','MỘT CLIENT ĐÃ THOÁT')

class handleData:
    def __init__(self, name, filename):
        self.nameC = name
        self.file = filename
            
    def indexCountry(self):
        with open(self.file) as file:
            file_data = json.load(file)

        for i in range(len(file_data)):
            for key in file_data[i]:
                if file_data[i][key] == self.nameC:
                    return i
        return "-1"
    
    def cases(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["cases"]

    def todayCases(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["todayCases"]

    def deaths(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["deaths"]

    def todaydeaths(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["todayDeaths"]

    def recovered(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["recovered"]

    def active(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["active"]

    def critical(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["critical"]

    def casesPerOneMilion(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["casesPerOneMillion"]

    def deathsPerOneMillion(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["deathsPerOneMillion"]

    def totalTests(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["totalTests"]   
    
    def testsPerOneMillion(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["testsPerOneMillion"]

def SendData_Client(sock):
    try:
        countryBox = sock.recv(Payload).decode('utf-8')
        sock.sendall("Nhận được phản hồi".encode('utf-8'))

        nameCountry = countryBox
        dataCovid = handleData(nameCountry, "covid19.json")
        checkName = dataCovid.indexCountry()

        sock.sendall(str(checkName).encode('utf-8'))
        if (checkName == "-1"):
            print("Server đặt tên sai!")
            return

        todayCases = dataCovid.todayCases()
        Announcement1 = sock.recv(Payload).decode('utf-8')
        print (Announcement1)
        sock.sendall(str(todayCases).encode('utf-8'))
        print("Đã tải về cho client số ca hôm nay!")
                
        cases = dataCovid.cases()
        Announcement2 = sock.recv(Payload).decode('utf-8')
        print (Announcement2)
        sock.sendall(str(cases).encode('utf-8'))
        print("Đã tải về cho client số ca!")

        deaths = dataCovid.deaths()
        Announcement3 = sock.recv(Payload).decode('utf-8')
        print (Announcement3)
        sock.sendall(str(deaths).encode('utf-8'))
        print("Đã tải về cho client số người chết!")
        
        recovered = dataCovid.recovered()
        Announcement4 = sock.recv(Payload).decode('utf-8')
        print (Announcement4)
        sock.sendall(str(recovered).encode('utf-8'))
        print("Đã tải về cho client số ca hồi phục!")
                
        critical = dataCovid.critical()
        Announcement5 = sock.recv(Payload).decode('utf-8')
        print (Announcement5)
        sock.sendall(str(critical).encode('utf-8'))
        print("Đã tải về cho client số ca có dấu hiệu nguy kịch!")
                
        active = dataCovid.active()
        Announcement6 = sock.recv(Payload).decode('utf-8')
        print (Announcement6)
        sock.sendall(str(active).encode('utf-8'))
        print("Đã tải về cho client số người đang nhiễm!")
    
    except OSError as e:
        print(str(e))

class GUISERVER(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        getData("covid19.json")

        self.iconbitmap("a.ico")
        self.title("TRA CỨU DỮ LIỆU COVID-19")
        self.maxsize(900, 600)
        self.protocol("WM_DELETE_WINDOW", self.quitClose)
        self.config(bg = "#e1dcfd")

        # Create left and right frames
        left_frame = Frame(self, width = 200, height = 400, bg = '#6699CC')
        left_frame.grid(row = 0, column = 0, padx = 10, pady = 5)
        
        right_frame = Frame(self, width = 650, height = 400, bg = '#6699CC')
        right_frame.grid(row = 0, column= 1, padx=10, pady=5)
        
        Label(left_frame, text = "TRA CỨU DỮ LIỆU COVID", font = FONT, relief = RAISED).grid(row = 0, column = 0, padx = 5, pady = 5)
        
        image = PhotoImage(file = "covid2.gif")
        original_image = image.subsample(3,3)
        Label(left_frame, image = original_image).grid(row = 1, column = 0, padx = 5, pady = 5)
        
        Label(right_frame, image = image, bg='grey').grid(row = 0, column = 0, padx = 5, pady = 5)
        
        tool_bar = Frame(left_frame, width = 180, height = 185, bg = 'grey')
        tool_bar.grid(row = 2, column = 0, padx = 5, pady = 5)
        
        self.listBox = Listbox(left_frame, height = 10, width = 30, bg = "white", activestyle = 'dotbox', font = 'Calibri', fg = "black")
        self.listBox.grid(column = 0, row = 0, sticky='w'+'e'+'n'+'s')
        Button(tool_bar, text = "LÀM MỚI", command = self.ClientUpdate, width = 20).grid(row = 0, column = 0, padx = 5, pady = 3, ipadx = 10)
        Button(tool_bar, text = "THOÁT", command = self.quitClose, width = 20).grid(row = 0, column = 1, padx = 5, pady = 3, ipadx = 10)

        self.refresh()
        self.mainloop()
        
    def ClientUpdate(self):
        with open('AccountLive.json') as file:
            file_data = json.load(file)
        self.listBox.delete(0, len(file_data["Address"]))
        for i in range(len(file_data["Address"])):
            self.listBox.insert(i, "Client đang truy cập: " + file_data["Address"][i])

    def quitClose(self):
        if messagebox.askokcancel("THOÁT CHƯƠNG TRÌNH?", "BẠN MUỐN THOÁT ỨNG DỤNG?"):
            with open('AccountLive.json') as file: 
                file_data = json.load(file)
            try:
                i = 0
                while i < len(file_data["Password"]):  
                    file_data["Password"].remove(file_data["Password"][i])
                    file_data["Account"].remove(file_data["Account"][i])
                    file_data["Address"].remove(file_data["Address"][i])
                    i = i + 1
                
                file_data["Password"].remove(file_data["Password"][0])
                file_data["Account"].remove(file_data["Account"][0])
                file_data["Address"].remove(file_data["Address"][0])
                with open('AccountLive.json', 'w') as data_file:
                    json.dump(file_data, data_file, indent = 4)

                print("Xóa xong!")
                self.destroy()
            except:
                print("Không xóa được!")
                self.destroy()

    def refresh(self):
        self.after(3600000, self.refresh)

if __name__ == '__main__':
    threading.Thread(target = handleServer, daemon = True).start()
    app = GUISERVER()

    

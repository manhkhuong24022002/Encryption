import tkinter as tk
from tkinter import filedialog, messagebox
import os
import Function
import sys 

input_file_encrypt = ""
input_file_encrypt_decrypt=""
file_Kprivate=""
file_HKprivate=""
def Encrypt_form():
    root.withdraw()
        
    def choose_file():
        global input_file_encrypt
        input_file_encrypt = filedialog.askopenfilename()
        entry_path.delete(0, tk.END)
        entry_path.insert(0, input_file_encrypt)

    def get_file_path():
        global input_file_encrypt
        input_file_encrypt = entry_path.get()
        if os.path.isfile(input_file_encrypt):
            return True
        else:
            return False
    def button_ok_callback():
        if get_file_path():  
            # successfully file path
            messagebox.showinfo("SUCCESSFULLY", "Đường dẫn hợp lệ!")
            # windows.withdraw()
            windows.destroy()
            root.destroy()

        else:
            # error file path
            messagebox.showerror("ERROR", "Đường dẫn không hợp lệ!")    

    windows = tk.Toplevel(root)
    windows.title("ENCRYPT")
    windows.geometry("500x150+550+250")
    windows.resizable(False, False) 

    label_path = tk.Label(windows, text="Đường dẫn file cần mã hóa:", font=0)
    label_path.pack()

    entry_path = tk.Entry(windows, width=60)
    entry_path.pack()

    icon = tk.PhotoImage(file="icondown.png").subsample(10)

    button_browse = tk.Button(windows, image=icon, command=choose_file)
    button_browse.place(x=432, y=25)

    button_open = tk.Button(windows, text="OK", command=button_ok_callback, font=0)
    button_open.place(x=425, y=50)

    windows.mainloop()
    #Thực hiện mã hóa file và sinh ra chuỗi Kx
    Function.encrypt_file_Kx(input_file_encrypt)
    messagebox.showinfo("SUCESSFULLY", "Mã hóa thành công")

    sys.exit()


def Decrypt_form():
    root.withdraw()
    def choose_file_decrypt():
        global input_file_encrypt_decrypt
        input_file_encrypt_decrypt = filedialog.askopenfilename()
        entry_path_decrypt.delete(0, tk.END)
        entry_path_decrypt.insert(0, input_file_encrypt_decrypt)
    # Hàm khi người dùng nhập vào đường dẫn file
    def get_file_decrypt():
        global input_file_encrypt_decrypt
        input_file_encrypt_decrypt = entry_path_decrypt.get()
        if os.path.isfile(input_file_encrypt_decrypt):
            return True
        else:
            return False

    # Hàm lấy Kprivate
    def choose_Kprivate():
        global file_Kprivate
        # Mở hộp thoại chọn file để lấy khóa Kprivate
        file_Kprivate = filedialog.askopenfilename()
        entry_Kprivate.delete(0, tk.END)
        entry_Kprivate.insert(0, file_Kprivate)

    def get_file_Kprivate():
        global file_Kprivate
        file_Kprivate = entry_Kprivate.get()
        if os.path.isfile(file_Kprivate):
            return True
        else:
            return False
        
    # Hàm lấy HKprivate
    def choose_HKprivate():
        global file_HKprivate
        # Mở hộp thoại chọn file để lấy khóa Kprivate
        file_HKprivate = filedialog.askopenfilename()
        entry_HKprivate.delete(0,tk.END)
        entry_HKprivate.insert(0, file_HKprivate)

    def get_file_HKprivate():
        global file_HKprivate
        file_HKprivate = entry_HKprivate.get()
        if os.path.isfile(file_HKprivate):
            return True
        else:
            return False    

    # Hàm dùng để thông báo người dùng nhập/chọn đúng đường dẫn file hay chưa
    def button_ok_callback():
        if get_file_Kprivate() and get_file_decrypt() and get_file_HKprivate():  
            # sucessfully file path
            messagebox.showinfo("SUCESSFULLY", "Đường dẫn hợp lệ!")
            windows.withdraw()
            windows.destroy()
            root.destroy()
        else:
            if get_file_Kprivate()==False and get_file_decrypt()==False and get_file_HKprivate==False:
                messagebox.showerror("ERROR","Vui lòng nhập đường dẫn")
            # error file kprivate
            elif get_file_Kprivate()==False:
                messagebox.showerror("ERROR", "Đường dẫn file kprivate không hợp lệ!")
            elif get_file_decrypt()==False:
                # error file path
                messagebox.showerror("ERROR", "Đường dẫn file cần mã hóa không hợp lệ!")
            else:
                messagebox.showerror("ERROR", "Đường dẫn file Hkprivate không hợp lệ!")
    windows = tk.Toplevel(root)
    windows.title("DECRYPT")
    windows.geometry("500x230+550+250")
    windows.resizable(False, False) 

    label_path = tk.Label(windows, text="Đường dẫn file cần giải mã:", font=0)
    label_path.pack()

    entry_path_decrypt = tk.Entry(windows,width=60)
    entry_path_decrypt.pack()

    spacer =tk.Label(windows, text="", width=10)
    spacer.pack()

    label_Kprivate = tk.Label(windows, text="Đường dẫn file Kprivate:", font=0)
    label_Kprivate.pack()

    entry_Kprivate = tk.Entry(windows,width=60)
    entry_Kprivate.pack()


    spacer =tk.Label(windows, text="", width=10)
    spacer.pack()

    label_HKprivate = tk.Label(windows, text="Đường dẫn file HKprivate:", font=0)
    label_HKprivate.pack()

    entry_HKprivate = tk.Entry(windows,width=60)
    entry_HKprivate.pack()

    icon=tk.PhotoImage(file="icondown.png").subsample(10)

    button_browse = tk.Button(windows,image=icon, command=choose_file_decrypt)
    button_browse.place(x=432,y=24)

    button_Kprivate = tk.Button(windows,image=icon, command=choose_Kprivate)
    button_Kprivate.place(x=432,y=88)

    button_Kprivate = tk.Button(windows,image=icon, command=choose_HKprivate)
    button_Kprivate.place(x=432,y=151)


    button_open = tk.Button(windows, text="OK", command=button_ok_callback, font=0)
    button_open.place(x=250,y=180)
    windows.mainloop()
    # Thực hiện quá kiểm tra giá trị HKprivate và giải mã
    check=Function.check_value_hash(file_Kprivate,file_HKprivate)
    if check==True:
        Ks=Function.Decrypt_Kx(file_Kprivate,file_HKprivate)
        Function.decrypt_file(Ks, input_file_encrypt_decrypt)
        messagebox.showinfo("SUCESSFULLY", "Giải mã thành công")
        sys.exit()
        
    else:
        messagebox.showerror("ERROR", "SHA-1 của Kprivate không trùng với HKprivate")
        sys.exit()
        
root = tk.Tk()
root.title("An Ninh Máy Tính")

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Tạo form
form = tk.Frame(root, width=350, height=150)
form.pack()

# Tính toán vị trí để căn giữa form
x = (screen_width - form.winfo_reqwidth()) // 2
y = (screen_height - form.winfo_reqheight()) // 2

# Đặt vị trí cho form
root.geometry(f"+{x}+{y-100}")
root.resizable(False, False) 
label_menu=tk.Label(root, text="Bạn Muốn Mã Hóa Hay Giải Mã", font=14)
label_menu.place(x=60, y=20)
button_encrypt = tk.Button(root, text="Mã Hóa File", command=Encrypt_form, font=12)
button_encrypt.place(x=30,y=60)

button_decrypt = tk.Button(root, text="Giải Mã File", command=Decrypt_form, font=12)
button_decrypt.place(x=220,y=60)

root.mainloop()




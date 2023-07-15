from tkinter import *
from tkinter import filedialog, messagebox
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import hashlib
import binascii
import json


def generate_aes_key():
    # Phát sinh khoá bí mật Ks 32 bytes
    return get_random_bytes(32)
def encrypt_file(key, input_file, output_file):
    # Đọc dữ liệu từ tập tin gốc
    with open(input_file, 'rb') as file:
        plaintext = file.read()

    # Tạo một khoá iv ngẫu nhiên
    iv = get_random_bytes(16)  # 16 bytes = 128 bits

    # Tạo đối tượng AES cipher với khoá và iv
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Áp dụng đệm PKCS7 cho dữ liệu
    padded_data = pad(plaintext, AES.block_size)

    # Mã hoá dữ liệu
    ciphertext = cipher.encrypt(padded_data)

    # Ghi dữ liệu đã mã hoá và iv vào tập tin đích
    with open(output_file, 'wb') as file:
        file.write(iv)
        file.write(ciphertext)
    os.remove(input_file)    

def generate_rsa_key():
    # Phát sinh cặp khóa RSA
    key_pair = RSA.generate(2048)

    # Lấy khóa Kpublic RSA 
    Kpublic = key_pair.publickey()

    # Lấy khóa Kprivate RSA
    Kprivate = key_pair.export_key()
    return Kpublic,Kprivate      

def encrypt_file_Kx(input_file):
    # Tạo khóa Ks ASE
    Ks_key=generate_aes_key()
    # Tạo tên tập tin đích
    output_file =  input_file + '.encrypted'
    # Mã hoá tập tin
    encrypt_file(Ks_key, input_file, output_file)
    Kpublic, Kprivate=generate_rsa_key()
    
    # Mã hóa khóa Ks bằng khóa công khai
    cipher = PKCS1_OAEP.new(Kpublic)
    encrypted_ks = cipher.encrypt(Ks_key)

    # In ra chuỗi Kx (khóa Ks đã được mã hóa)
    Kx = encrypted_ks.hex()
    # Xác định thư mục gốc
    root_directory = os.path.dirname(os.path.abspath(__file__))
   # Tính giá trị hash SHA-1 của Kprivate
    HKprivate = hashlib.sha1(Kprivate.hex().encode()).hexdigest()
    # Tên tập tin C
    file_name = "C"
    metadata_file = f"{file_name}.metadata"

    # Dữ liệu metadata
    metadata = {
        "Kx": Kx,
        "HKprivate": HKprivate
    }
    # Lưu metadata vào tập tin
    with open(metadata_file, "w") as file:
        json.dump(metadata, file,indent=0)
    output_Kprivatefile = os.path.join(root_directory, "Kprivate.txt")
    with open(output_Kprivatefile, "w") as file:
        file.write(Kprivate.hex())


# Mở file HKprivate và Kx
def open_file_Kx(file_HKprivate):
        with open(file_HKprivate,"r") as file:
            content=json.load(file)
        HKprivate=content["HKprivate"]
        Kx=content["Kx"]
        return Kx, HKprivate

def open_file_Kprivate(file_Kprivate):
    with open (file_Kprivate,"r") as file:
        Kprivate=file.read()
    return Kprivate

def check_value_hash(file_Kprivate,file_HKprivate):
    # Mở và đọc file kprivate để lấy kprivate
    Kprivate=open_file_Kprivate(file_Kprivate)

    # Mở và đọc file hkprivate để lấy hkprivate
    Kx,HKprivate=open_file_Kx(file_HKprivate)
    # Tính giá trị SHA-1 và kiểm tra có trùng với HKprivate không 
    hash_value=hashlib.sha1(Kprivate.encode()).hexdigest()
    if hash_value==HKprivate:
        return True
    else:
        return False

# Giải mã Ks từ Kx thông qua Kprivate    
def Decrypt_Kx(file_Kprivate,file_HKprivate):
    # Chuyển đổi chuỗi Kprivate từ hex sang dạng bytes
    Kprivate=open_file_Kprivate(file_Kprivate)
    Kprivate_bytes = binascii.unhexlify(Kprivate)
        
    # Tạo đối tượng RSA private key từ chuỗi Kprivate
    private_key = RSA.import_key(Kprivate_bytes)
        
    # Giải mã chuỗi Kx sử dụng khóa private key
    Kx, Hkprivate=open_file_Kx(file_HKprivate)

    # Chuyển đổi chuỗi Kx từ hex sang dạng bytes
    Kx_bytes = binascii.unhexlify(Kx)

    # Tạo đối tượng cipher PKCS1_OAEP với khóa private key
    cipher = PKCS1_OAEP.new(private_key)
    # Giải mã chuỗi Kx
    Ks_bytes = cipher.decrypt(Kx_bytes)
    # Chuyển đổi Ks từ dạng bytes sang hex
    Ks = binascii.hexlify(Ks_bytes).decode()
    return Ks
  

def decrypt_file(Ks, file_encrypt):
    # Chuyển đổi Ks từ dạng hex sang dạng byte
    Ks_byte = bytes.fromhex(Ks)

    # Đọc iv từ tập tin đầu vào
    with open(file_encrypt, 'rb') as encrypted_file:
        iv = encrypted_file.read(16)  
        ciphertext = encrypted_file.read()
    # Sử dụng chế độ CBC với IV
    cipher = AES.new(Ks_byte, AES.MODE_CBC, iv)  

    # Giải mã dữ liệu
    decrypted_data = cipher.decrypt(ciphertext)

    # Loại bỏ byte padding
    decrypted_data = unpad(decrypted_data, AES.block_size)

    output_file = os.path.splitext(os.path.basename(file_encrypt))[0]

    with open(output_file, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    os.remove(file_encrypt)

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def pad_data(data: bytes) -> bytes:
    """Hàm đệm dữ liệu chuẩn PKCS7 cho vừa đủ bội số 16 bytes (128 bits)."""
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

def unpad_data(padded_data: bytes) -> bytes:
    """Hàm gỡ đệm PKCS7 sau khi giải mã dữ liệu."""
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

def ma_hoa_aes_256(van_ban_goc: str, khoa_bi_mat: bytes):
    """Mã hóa chuỗi văn bản rõ bằng AES-256-CBC."""
    iv = os.urandom(16)  # Vector khởi tạo IV 16 bytes ngẫu nhiên
    cipher = Cipher(algorithms.AES(khoa_bi_mat), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    du_lieu_dem = pad_data(van_ban_goc.encode('utf-8'))
    van_ban_ma_hoa = encryptor.update(du_lieu_dem) + encryptor.finalize()
    return iv, van_ban_ma_hoa

def giai_ma_aes_256(van_ban_ma_hoa: bytes, khoa_bi_mat: bytes, iv: bytes) -> str:
    """Giải mã chuỗi mã hóa AES-256-CBC về văn bản ban đầu."""
    cipher = Cipher(algorithms.AES(khoa_bi_mat), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    du_lieu_giai_ma = decryptor.update(van_ban_ma_hoa) + decryptor.finalize()
    du_lieu_goc = unpad_data(du_lieu_giai_ma)
    return du_lieu_goc.decode('utf-8')

if __name__ == "__main__":
    # Khóa 256-bit (32 bytes) ngẫu nhiên
    khoa_khoi_tao = os.urandom(32)
    thong_diep = "Bai tap thuc hanh An toan va Bao mat thong tin - K235480106060"

    print("=== DEMO THUẬT TOÁN MÃ HÓA AES-256 ===")
    print("Văn bản gốc:", thong_diep)
    
    # Mã hóa
    iv_vector, du_lieu_ma_hoa = ma_hoa_aes_256(thong_diep, khoa_khoi_tao)
    print("\n[+] Dữ liệu mã hóa (Hex):", du_lieu_ma_hoa.hex())
    print("[+] IV Vector (Hex):", iv_vector.hex())
    
    # Giải mã
    van_ban_giai_ma = giai_ma_aes_256(du_lieu_ma_hoa, khoa_khoi_tao, iv_vector)
    print("\n[+] Dữ liệu sau giải mã:", van_ban_giai_ma)

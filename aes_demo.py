import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def pad_data(data: bytes) -> bytes:
    """Hàm đệm dữ liệu theo chuẩn PKCS7 để đảm bảo đủ bội số 16 bytes (128 bits)."""
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

def unpad_data(padded_data: bytes) -> bytes:
    """Hàm gỡ đệm PKCS7 sau khi giải mã dữ liệu xong."""
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

def ma_hoa_aes_256(van_ban_goc: str, khoa_bi_mat: bytes):
    """Hàm thực hiện mã hóa văn bản rõ sử dụng thuật toán AES-256-CBC."""
    # Sinh ngẫu nhiên Vector khởi tạo IV (16 bytes)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(khoa_bi_mat), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Chuyển văn bản sang bytes và đệm PKCS7
    du_lieu_dem = pad_data(van_ban_goc.encode('utf-8'))
    van_ban_ma_hoa = encryptor.update(du_lieu_dem) + encryptor.finalize()
    return iv, van_ban_ma_hoa

def giai_ma_aes_256(van_ban_ma_hoa: bytes, khoa_bi_mat: bytes, iv: bytes) -> str:
    """Hàm giải mã chuỗi mã hóa AES-256-CBC trở lại văn bản gốc."""
    cipher = Cipher(algorithms.AES(khoa_bi_mat), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    du_lieu_giai_ma = decryptor.update(van_ban_ma_hoa) + decryptor.finalize()
    du_lieu_goc = unpad_data(du_lieu_giai_ma)
    return du_lieu_goc.decode('utf-8')

if __name__ == "__main__":
    # Khai báo khóa bí mật 256-bit (32 bytes)
    khoa_khoi_tao = os.urandom(32)
    thong_diep_can_bao_mat = "Bài tập thực hành An toàn và Bảo mật thông tin - K235480106060"

    print("=== CHƯƠNG TRÌNH DEMO MÃ HÓA VÀ GIẢI MÃ AES-256 ===")
    print("Thông điệp ban đầu:", thong_diep_can_bao_mat)
    
    # Chạy thử mã hóa
    iv_vector, du_lieu_ma_hoa = ma_hoa_aes_256(thong_diep_can_bao_mat, khoa_khoi_tao)
    print("\n[+] Dữ liệu sau khi mã hóa (Hex):", du_lieu_ma_hoa.hex())
    print("[+] Vector IV (Hex):", iv_vector.hex())
    
    # Chạy thử giải mã
    van_ban_giai_ma = giai_ma_aes_256(du_lieu_ma_hoa, khoa_khoi_tao, iv_vector)
    print("\n[+] Dữ liệu sau khi giải mã:", van_ban_giai_ma)

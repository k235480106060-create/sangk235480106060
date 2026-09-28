# BÀI TẬP VỀ NHÀ: AN TOÀN VÀ BẢO MẬT THÔNG TIN


**Sinh viên thực hiện:** Nguyễn Văn Sang  

**Mã sinh viên:** K235480106060   

**Lớp:** K59.KMT.K01  

**Khoa:** Điện tử  

## 1. Thuật toán mã hóa đối xứng (DES & AES)

### a. Mã hóa DES (Data Encryption Standard)
- **Tổng quan:** DES là chuẩn mã hóa khối (Block Cipher) ra đời từ những năm 1970. Nền tảng cấu trúc của DES dựa trên mạng Feistel 16 vòng (round).
- **Thông số kỹ thuật:**
  Kích thước khối dữ liệu mã hóa: 64 bit.
  Kích thước khóa (Key): 64 bit (trên thực tế chỉ dùng 56 bit để làm khóa thực sự, 8 bit còn lại dùng kiểm tra lỗi parity).
- **Quy trình xử lý:**
1. **Hoán vị ban đầu (IP - Initial Permutation):** Khối 64-bit đầu vào được xáo trộn thứ tự các bit.
2. **Tách khối:** Khối dữ liệu sau hoán vị tách làm 2 nửa 32-bit: Trái ($L_0$) và Phải ($R_0$).
3. **Vòng lặp Feistel (16 vòng):** Tại mỗi vòng $i$ (từ 1 đến 16):
- Sinh khóa con $K_i$ (48 bit) từ khóa chính 56 bit.
- $L_i = R_{i-1}$
- $R_i = L_{i-1} \oplus f(R_{i-1}, K_i)$
- Trong đó hàm $f$ thực hiện: Mở rộng $R_{i-1}$ từ 32 bit lên 48 bit $\rightarrow$ XOR với $K_i$ $\rightarrow$ Đưa qua các hộp S-Box để nén lại thành 32 bit $\rightarrow$ Cho qua hộp P-Box hoán vị.
4. **Hoán vị kết thúc ($IP^{-1}$):** Ghép $R_{16}$ và $L_{16}$ lại với nhau rồi qua bảng hoán vị ngược $IP^{-1}$ để thu được ciphertext 64 bit.
- **Quy trình giải mã:** Giống hệt quá trình mã hóa, chỉ cần đảo ngược thứ tự các khóa con $K_{16} \rightarrow K_1$.

---

### b. Mã hóa AES (Advanced Encryption Standard)
- **Tổng quan:** AES ra đời để thay thế DES vì độ dài khóa 56-bit của DES đã quá yếu trước các đòn tấn công vét cạn (brute-force). AES dùng cấu trúc SPN (Substitution-Permutation Network) thay vì Feistel.
- **Thông số kỹ thuật:**
- Kích thước khối dữ liệu: Cố định 128 bit (xếp thành ma trận $4 \times 4$ byte, gọi là State matrix).
- Độ dài khóa hỗ trợ: 128 bit (10 vòng), 192 bit (12 vòng), hoặc 256 bit (14 vòng).
- **Quy trình mã hóa (ví dụ dòng AES-128):**
1. **Khởi tạo (Key Expansion & AddRoundKey):** Mở rộng khóa ban đầu thành các khóa con. Thực hiện XOR dữ liệu đầu vào với khóa vòng 0.
2. **Thực hiện 9 vòng lặp chuẩn (từ vòng 1 đến 9):**
- `SubBytes`: Thay thế từng byte trong ma trận State qua bảng S-Box (biến đổi phi tuyến).
- `ShiftRows`: Dịch hàng theo chu kỳ (hàng 0 giữ nguyên, hàng 1 dịch 1 byte, hàng 2 dịch 2 bytes, hàng 3 dịch 3 bytes).
- `AddRoundKey`: XOR kết quả ma trận State với khóa con của vòng đó.
3. **Vòng 10 (Vòng cuối):** Thực hiện tương tự nhưng **bỏ qua bước MixColumns** (`SubBytes` $\rightarrow$ `ShiftRows` $\rightarrow$ `AddRoundKey`).
- **Quy trình giải mã:** Áp dụng các thao tác ngược lại theo chu trình: `InvAddRoundKey` $\rightarrow$ `InvShiftRows` $\rightarrow$ `InvSubBytes` $\rightarrow$ `InvMixColumns`.

---

### c. Demo cài đặt AES bằng Python
Code triển khai thuật toán **AES-256 (chế độ CBC)** sử dụng thư viện `cryptography`:
> **Lưu ý cài thư viện:** `pip install cryptography`
```python
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def pad(data: bytes) -> bytes:
"""Đệm dữ liệu chuẩn PKCS7 cho vừa đủ bội số 16 bytes (128 bits)."""
padder = padding.PKCS7(128).padder()
return padder.update(data) + padder.finalize()

def unpad(padded_data: bytes) -> bytes:
"""Gỡ đệm PKCS7 sau khi giải mã."""
unpadder = padding.PKCS7(128).unpadder()
return unpadder.update(padded_data) + unpadder.finalize()

def aes_encrypt(plain_text: str, secret_key: bytes):
"""Mã hóa văn bản bằng AES-256-CBC."""
# Tạo ngẫu nhiên Vector khởi tạo IV (16 bytes)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
padded_bytes = pad(plain_text.encode('utf-8'))
cipher_text = encryptor.update(padded_bytes) + encryptor.finalize()
return iv, cipher_text

def aes_decrypt(cipher_text: bytes, secret_key: bytes, iv: bytes) -> str:
"""Giải mã văn bản bằng AES-256-CBC."""
cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()

padded_plain = decryptor.update(cipher_text) + decryptor.finalize()
plain_bytes = unpad(padded_plain)
return plain_bytes.decode('utf-8')

# Running Test
if __name__ == "__main__":
key_256 = os.urandom(32)  # Khóa 256-bit
raw_text = "Thử nghiệm mã hóa dữ liệu với AES-256 CBC Mode"

print("Văn bản gốc:", raw_text)

# Mã hóa
iv, encrypted_data = aes_encrypt(raw_text, key_256)
print("Dữ liệu sau mã hóa (Hex):", encrypted_data.hex())

# Giải mã
decrypted_text = aes_decrypt(encrypted_data, key_256, iv)
print("Dữ liệu sau giải mã:", decrypted_text)

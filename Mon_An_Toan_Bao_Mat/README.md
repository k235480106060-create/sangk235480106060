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

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1c541e12-16dc-45a9-aaae-9b46817a8622" />

### Kết quả thực thi chương trình AES-256 (`aes_demo.py`)

Sau khi khởi chạy file `aes_demo.py`, chương trình đã thực hiện thành công chu trình mã hóa và giải mã dữ liệu với kết quả đầu ra như sau:

#### 1. Dữ liệu đầu vào:
- **Thông điệp ban đầu (Plaintext):** `Bai tap thuc hanh An toan va Bao mat thong tin`

#### 2. Kết quả Mã hóa (Encryption):
- **Dữ liệu mã hóa (Ciphertext - dạng Hex):**
`b21ea1a38e2663e35b452299c69dd97aad1a5c92ed96b527d81764f04e58f9f6a49d2c96b9634a1a89677447e184512f`
- **Vector khởi tạo IV (Initialization Vector - dạng Hex):**
`3e3928569989768a41a287e97fd07794`

#### 3. Kết quả Giải mã (Decryption):
- **Dữ liệu sau khi giải mã (Decrypted Text):** `Bai tap thuc hanh An toan va Bao mat thong tin`

#### 4. Đánh giá kết quả:
- Dữ liệu sau khi giải mã trùng khớp hoàn toàn 100% với thông điệp ban đầu.
- Chuỗi ciphertext thu được hoàn toàn là ký tự hex ngẫu nhiên, đảm bảo tính bảo mật khi truyền qua môi trường mạng không an toàn.
- Mã thoát chương trình: `Process finished with exit code 0` (Thực thi thành công, không phát sinh lỗi).


## 2. Tìm hiểu thuật toán mã hóa bất đối xứng RSA

### a. Giới thiệu thuật toán RSA
RSA (Rivest–Shamir–Adleman) là thuật toán mã hóa bất đối xứng phổ biến nhất hiện nay, dựa trên độ khó của bài toán phân tích một số nguyên lớn thành tích của các số nguyên tố.

### b. Nguyên lý sinh cặp khóa (Key Generation)
Quy trình sinh cặp khóa công khai $(e, n)$ và khóa bí mật $(d, n)$:
1. **Chọn 2 số nguyên tố lớn:** $p$ và $q$ ($p \neq q$).
2. **Tính tích:** $n = p \times q$ (Độ dài $n$ chính là độ dài khóa, ví dụ 2048-bit).
3. **Tính hàm số Euler:** $\phi(n) = (p - 1) \times (q - 1)$.
4. **Chọn số $e$ (Khóa công khai):** Chọn $e$ sao cho $1 < e < \phi(n)$ và $gcd(e, \phi(n)) = 1$ (thường chọn $e = 65537$).
5. **Tính số $d$ (Khóa bí mật):** Tìm $d$ sao cho $(d \times e) \equiv 1 \pmod{\phi(n)}$ (tức $d$ là nghịch đảo nhân modular của $e$).

- **Public Key (Khóa công khai):** $(e, n)$ — Dùng để mã hóa hoặc kiểm tra chữ ký.
- **Private Key (Khóa bí mật):** $(d, n)$ — Dùng để giải mã hoặc tạo chữ ký.

---

## 3. Các mô hình áp dụng RSA, So sánh và Kết hợp RSA với AES
### a. Các mô hình ứng dụng RSA
1. **Mô hình Xác thực người nhận (Bảo mật dữ liệu):**
- **Người gửi:** Dùng **Khóa công khai của người nhận** để mã hóa thông điệp.
- **Người nhận:** Dùng **Khóa bí mật của chính mình** để giải mã.
- *Mục đích:* Chỉ duy nhất người nhận sở hữu khóa bí mật mới đọc được nội dung.

2. **Mô hình Xác thực người gửi (Chữ ký số - Digital Signature):**
- **Người gửi:** Dùng **Khóa bí mật của chính mình** để ký (mã hóa) vào bản băm của thông điệp.
- **Người nhận:** Dùng **Khóa công khai của người gửi** để xác thực chữ ký.
- *Mục đích:* Đảm bảo tính chống chối bỏ và xác nhận đúng danh tính người gửi.

3. **Mô hình Xác thực cả hai (Mã hóa + Chữ ký số):**
- **Người gửi:** Lấy thông điệp $\rightarrow$ Ký bằng **Khóa bí mật người gửi** $\rightarrow$ Mã hóa tiếp bằng **Khóa công khai người nhận**.
- **Người nhận:** Giải mã bằng **Khóa bí mật người nhận** $\rightarrow$ Kiểm tra chữ ký bằng **Khóa công khai người gửi**.
- *Mục đích:* Đảm bảo vừa bảo mật nội dung vừa xác thực danh tính 2 chiều.

### b. So sánh thời gian và tốc độ giữa RSA và AES

| Tiêu chí | AES (Mã hóa đối xứng) | RSA (Mã hóa bất đối xứng) |
| :--- | :--- | :--- |
| **Kích thước khóa** | 128, 192, 256 bits | 2048, 3072, 4096 bits |
| **Tốc độ mã hóa/giải mã** | Cực nhanh (hàng nghìn đến hàng triệu phép tính/giây) | Rất chậm (chậm hơn AES từ 1000 đến 10.000 lần) |
| **Tài nguyên tính toán** | Thấp, tối ưu tốt trên phần cứng | Cao, đòi hỏi tính toán số nguyên lớn |
| **Khả năng xử lý dữ liệu** | Mã hóa khối dữ liệu dung lượng lớn bất kỳ | Chỉ mã hóa được dữ liệu ngắn (nhỏ hơn kích thước khóa) |
| **Quản lý khóa** | Khó khăn trong việc phân phối khóa an toàn | Dễ dàng chia sẻ khóa công khai |

  
### c. Giải pháp kết hợp sức mạnh của RSA và AES (Mã hóa lai - Hybrid Encryption)

```text
[Dữ liệu lớn] -----( Mã hóa bằng AES )-----> [Ciphertext]
                          ^
                          |
                   [Khóa Session AES]
                          |
                   ( Mã hóa bằng RSA )
                          |
                          v
                 [Khóa Session đã mã hóa]
```

Vì **AES mã hóa cực nhanh** nhưng gặp khó khăn khi chia sẻ khóa bí mật, còn **RSA truyền khóa an toàn** nhưng tốc độ quá chậm, mô hình **Mã hóa lai (Hybrid Encryption)** ra đời để kết hợp ưu điểm của cả hai:

1. **Quy trình gửi dữ liệu:**
- Tạo ra một **Khóa phiên ngẫu nhiên (Session Key)** dùng thuật toán AES.
- Sử dụng **AES + Khóa phiên** để mã hóa toàn bộ dữ liệu dung lượng lớn (Nhanh chóng).
- Sử dụng **RSA + Khóa công khai của người nhận** để mã hóa chính **Khóa phiên AES** này (An toàn).
- Gửi cả *Dữ liệu đã mã hóa AES* và *Khóa phiên đã mã hóa RSA* cho người nhận.

2. **Quy trình nhận dữ liệu:**
- Người nhận dùng **Khóa bí mật RSA** của mình để giải mã lấy lại **Khóa phiên AES**.
- Dùng **Khóa phiên AES** vừa lấy được để giải mã toàn bộ dữ liệu gốc.
> **Ứng dụng thực tế:** Đây chính là cơ chế đang được sử dụng trong các giao thức bảo mật hàng ngày như **HTTPS (TLS/SSL)**, **SSH**, và **PGP Email**.

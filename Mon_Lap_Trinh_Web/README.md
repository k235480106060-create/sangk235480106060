# Báo cáo Thực hành Môn Lập trình Web

Báo cáo chi tiết quá trình triển khai hệ thống dịch vụ web đa container bằng Docker Compose, cấu hình Nginx Virtual Host và tích hợp API từ Node-RED.

---

## BÀI TẬP 1: Triển khai Hạ tầng Web & Docker Compose
### 1. Cấu trúc hệ thống & Môi trường
Trong bài tập này, hệ thống sử dụng **WSL2 (Ubuntu)** làm môi trường giả lập Linux trên Windows để chạy Docker. Hệ thống bao gồm 5 dịch vụ chính chạy riêng biệt trong các container:
- **Nginx**: Đóng vai trò làm Web Server chính và Reverse Proxy.
- **Node-RED**: Công cụ xử lý logic backend và tạo API.
- **MariaDB**: Hệ quản trị cơ sở dữ liệu quan hệ.
- **phpMyAdmin**: Giao diện web quản lý cơ sở dữ liệu MariaDB (chạy port 8080).
- **Cloudflared**: Dịch vụ Cloudflare Tunnel kết nối domain ra internet không cần mở port router.

### 2. Các bước thực hành
#### Bước 1: Cài đặt Docker trên WSL2
Thực hiện cập nhật hệ thống và cài đặt Docker Compose:
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable --now docker

```
#### Bước 2: Khởi tạo file `docker-compose.yml`
Tạo file cấu hình điều phối cả 5 dịch vụ với cổng và volume tương ứng.

#### Bước 3: Khởi chạy container
Chạy lệnh khởi động toàn bộ dịch vụ dưới dạng ngầm (detached mode):
```bash
docker-compose up -d

```

### 3. Minh chứng & Kết quả cần đạt
- **Minh chứng 1 (Trạng thái Container):** Kết quả lệnh `docker ps` hiển thị đầy đủ 5 container đang ở trạng thái `Up` (chạy thành công).
- **Minh chứng 2 (Giao diện Quản trị DB):** Truy cập địa chỉ `http://localhost:8080` hiển thị trang đăng nhập của **phpMyAdmin** kết nối thành công tới MariaDB.
- **Minh chứng 3 (Cấu hình Nginx):** Truy cập `http://localhost` nhận phản hồi từ Nginx web server.

---

## BÀI TẬP 2: Dựng API với Node-RED & Tích hợp Website
### 1. Cấu trúc xử lý & Cấu hình Nginx
- **API Backend:** Được dựng bằng Node-RED qua cụm node `http in` -> `function` -> `http response`.
- **Nginx Virtual Host:** Điều hướng 2 trang web độc lập (`web1` và `web2`) trên cùng port 80 dựa theo `server_name`.
- **Cấu hình CORS / Proxy:** Nginx chuyển hướng các request từ đường dẫn `/api/` sang container Node-RED port 1880 để xử lý lỗi Chặn truy cập nguồn gốc chéo (CORS) trên trình duyệt.

### 2. Các bước thực hành

#### Bước 1: Tạo API trên Node-RED
1. Truy cập giao diện Node-RED tại `http://localhost:1880`.
2. Tạo node `http in` (Method: `GET`, URL: `/api/tacke`).
3. Tạo node `function` trả về dữ liệu chuẩn JSON:
```json
{
     "ok": 1,
     "msg": "thành công",
     "dssv": [
       {"name": "Cốp", "money": 123},
       {"name": "David", "money": 456}
     ]
   }

```
4. Nối sang node `http response` và bấm **Deploy**.

#### Bước 2: Viết giao diện Web & Gọi API
Trong file `nginx/web2/index.html`, sử dụng hàm `fetch('/api/tacke')` của JavaScript để gửi yêu cầu lấy dữ liệu JSON và bóc tách hiển thị danh sách lên giao diện HTML.

### 3. Minh chứng & Kết quả cần đạt
- **Minh chứng 1 (Kiểm tra API trực tiếp):** Truy cập URL `https://tnut.cuong.id.vn/api/tacke` (hoặc `http://localhost/api/tacke`) trên trình duyệt trả về đúng chuỗi JSON dữ liệu danh sách sinh viên.
- **Minh chứng 2 (Giao diện Website gọi API):** Khi mở trang `web2` và bấm nút **"Tải dữ liệu API"**, dữ liệu tên sinh viên (`Cốp`, `David`) và số tiền tương ứng hiển thị trực quan trên trang web mà không phát sinh lỗi CORS trong mục Console của trình duyệt.
---

## Tổng kết & Đánh giá kết quả
Sau khi hoàn thành cả 2 bài tập thực hành, hệ thống đã đạt được các yêu cầu đặt ra:
1. **Hạ tầng Docker Compose:**
- Vận hành mượt mà cả 5 dịch vụ (`Nginx`, `Node-RED`, `MariaDB`, `phpMyAdmin`, `Cloudflared`) trên cùng một mạng container nội bộ.
- Giảm thiểu xung đột tài nguyên và dễ dàng quản lý/mở rộng hệ thống.

2. **Khả năng điều hướng & Tích hợp:**
- Nginx xử lý tốt việc chia Virtual Host cho nhiều Domain/Website chạy song song.
- Giải quyết triệt để vấn đề Chặn truy cập nguồn gốc chéo (**CORS**) bằng giải pháp Reverse Proxy đường dẫn `/api/` về Node-RED.
- Giao diện Frontend (HTML/JS) tương tác realtime và hiển thị dữ liệu linh hoạt từ backend API.

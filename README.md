# 📘 HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

Tài liệu này cung cấp các bước chi tiết để **giảng viên** cài đặt và chạy **PROJECT 2 - FUTOSHIKI SOLVER & AI METHODS** trên máy tính cá nhân bằng **VS Code**.

---

## 1️⃣ Yêu cầu hệ thống

Vui lòng đảm bảo hệ thống có:

- **Python** ≥ 3.10  
- **pip** (trình quản lý gói của Python)  
- **Git** (khuyến nghị, không bắt buộc)

Kiểm tra phiên bản:

```bash
python --version
pip --version
```

---

## 2️⃣ Cấu trúc thư mục của Project

```text
FUTOSHIKI/
│
├── benchmark/          # Script benchmark các thuật toán
├── cnf/                # Biểu diễn logic CNF
├── csp/                # Constraint Satisfaction Problem
├── fol/                # First Order Logic
├── heuristics/         # Heuristic cho A*
├── horn_clauses/       # Horn clauses
├── inference/          # Forward / Backward chaining
├── input/              # Dữ liệu đầu vào (input_01 → input_10)
├── model/              # Định nghĩa FutoshikiData
├── output/             # Kết quả (solution + benchmark)
├── solver/             # Các solver (Backtracking, BruteForce, A*, FC)
├── ui/                 # Giao diện PyQt6
├── utils/              # Các hàm hỗ trợ (parse, random, write file)
├── worker/             # Thread xử lý nền
│
├── feature.ipynb       # Notebook: ground, query, benchmark
├── main.py             # Chạy ứng dụng UI
├── README.md           # Tài liệu hướng dẫn
└── requirements.txt    # Thư viện cần cài
```

---

## 3️⃣ Tạo và kích hoạt môi trường ảo (Khuyến nghị)

### ▶️ Trên Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### ▶️ Trên macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

Sau khi kích hoạt, `(venv)` sẽ xuất hiện ở đầu dòng trong terminal.

---

## 4️⃣ Cài đặt các thư viện cần thiết

Tất cả các thư viện cần thiết được liệt kê trong file **`requirements.txt`**.

Chạy lệnh sau:

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Chạy Project (Ứng dụng giao diện)

Chạy file:

```bash
python main.py
```
Ứng dụng sẽ mở giao diện giải bài toán Futoshiki bằng các thuật toán AI.

### Bước 1: Khởi động Jupyter Notebook

Mở terminal trong thư mục project và chạy:

```bash
jupyter notebook
```

Một cửa sổ trình duyệt sẽ tự động mở.

---

### Bước 2: Mở Notebook 

Trong giao diện Jupyter, mở file:

```
feature.ipynb
```

---

### Bước 3: Chạy Notebook

Chạy các cell theo thứ tự bằng cách chọn:

```
Cell → Run All
```

hoặc nhấn:

```
Shift + Enter
```

cho từng cell.

---

### Bước 4: Nội dung trong Notebook

 - Ground & Query:
   - Kiểm tra tri thức
   - Thực hiện truy vấn bằng Backward Chaining
 - Benchmark
   - Chạy các input từ **`input_01 → input_10`**
   - So sánh các thuật toán:
      - Backtracking
      - Brute Force
      - Forward Chaining
      - A* (Heuristic 1, Heuristic 2)

---

### Bước 5: Xem kết quả

- Kết quả lời giải được lưu trong thư mục **`output/`**.
- Kết quả benchmark sẽ được hiển thị trực tiếp trong notebook.
# 🚀 Hướng Dẫn Chạy AI Cố Vấn Học Tập

Hướng dẫn từng bước để setup và chạy ứng dụng AI Cố Vấn Học Tập trên máy của bạn.

---

## 📋 Yêu Cầu Hệ Thống

- **Python**: 3.9 trở lên
- **RAM**: Tối thiểu 4GB (khuyến nghị 8GB)
- **Disk**: 2GB trống để lưu vector database
- **Google Account**: Để setup email notifications
- **Internet**: Kết nối ổn định (LLM gọi API Groq)

---

## ⚙️ Bước 1: Setup Ban Đầu

### 1.1 Clone Repository

```bash
git clone https://github.com/quanghuy25w/AI-academic-advisor.git
cd Agent_AI_Levelup
```

### 1.2 Tạo Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 1.3 Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

Quá trình cài đặt mất khoảng 2-5 phút tùy tốc độ internet.

---

## 🔑 Bước 2: Cấu Hình API Keys

### 2.1 Lấy Groq API Key

1. Truy cập: https://console.groq.com/keys
2. Đăng nhập/Tạo tài khoản (miễn phí)
3. Nhấn **"Create API Key"**
4. Copy key vừa tạo

### 2.2 Cấu Hình File `.env`

```bash
# Copy file mẫu
cp .env.example .env

# Chỉnh sửa .env (mở bằng text editor)
```

**Nội dung `.env`:**
```env
# API Keys Groq (dùng nhiều key để tránh rate limiting)
GROQ_KEYS=gsk_your_key_1,gsk_your_key_2,gsk_your_key_3

# Email (optional - nếu muốn dùng tính năng email reminder)
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_16_char_app_password
```

**Nếu không có App Password:**
1. Truy cập: https://myaccount.google.com/security
2. Bật 2-Step Verification (nếu chưa)
3. Vào: https://myaccount.google.com/apppasswords
4. Chọn "Mail" → "Máy tính" → Copy password 16 ký tự

---

## 📊 Bước 3: Xích Nhập Dữ Liệu

Lần đầu chạy, cần xích nhập chương trình học từ `data_raw/` vào vector database.

```bash
# Tự động xích nhập dữ liệu
python src/ingestion/ingest.py

# Hoặc chạy full pipeline
python src/ingestion/ingest_pipeline.py
```

**Thời gian chờ**: ~2-5 phút (tùy kích thước dữ liệu)

**Xác nhận thành công:**
- Thư mục `vector_store/` sẽ có file `chroma.sqlite3` mới
- Không có error trong console

---

## 🎮 Bước 4: Chạy Ứng Dụng

### **Cách 1: Streamlit UI (Giao diện Web - Khuyên dùng)**

```bash
streamlit run app.py
```

✅ Ứng dụng mở tự động ở: `http://localhost:8501`

**Tính năng:**
- Đăng ký / Đăng nhập sinh viên
- Nhập thông tin profile (năm học, khóa học yêu thích, ràng buộc thời gian)
- Chat với AI để nhận gợi ý khóa học
- Xem lịch sử trò chuyện
- Nhận email nhắc nhở (nếu cấu hình email)

---

### **Cách 2: Chạy Script Python**

```python
from src.agent.graph import build_graph

# Khởi tạo
graph = build_graph()

# Gửi truy vấn
response = graph.invoke({
    "user_id": "student_001",
    "query": "Tôi muốn học AI nhưng chỉ có 10 tiếng/tuần"
})

# In kết quả
print(response["response"])
```

---

### **Cách 3: Chạy Test Suite**

```bash
# Test toàn bộ RAG pipeline
python src/rag/test_full_pipeline.py

# Test agent logic
python test_router_upgrade.py

# Kiểm tra vector collections
python src/ingestion/check_collections.py

# Kiểm tra vector store
python src/ingestion/check_vector.py
```

---

## ⚡ Bước 5: Xác Nhận Setup Thành Công

Kiểm tra từng phần:

```bash
# 1. Kiểm tra Python environment
python --version  # Phải >= 3.9

# 2. Kiểm tra .env
cat .env

# 3. Kiểm tra dependencies
pip list | grep -E "langchain|groq|chroma|pydantic"

# 4. Kiểm tra vector database
ls -la vector_store/

# 5. Test LLM connection
python -c "from src.config.groq_gateway import invoke_llm; print(invoke_llm('Hello!'))"
```

## 📈 Performance Tips

| Tính năng | Làm sao tối ưu |
|----------|-----------------|
| **Chậm lần đầu** | Cache vector database sau xích nhập |
| **Rate limiting** | Thêm nhiều API keys vào GROQ_KEYS |
| **Streamlit lag** | Chạy ở server khác (không localhost) |
| **Memory cao** | Giảm chunk_size trong `ingest_pipeline.py` |

---

## 🚀 Production Deployment

Khi muốn deploy lên server thực:

```bash
# 1. Setup environment này trên server
# 2. Cài đặt Gunicorn (ASGI server)
pip install gunicorn

# 3. Run app
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Hoặc dùng Docker (file Dockerfile sắp thêm)
docker build -t ai-advisor .
docker run -p 8000:8000 ai-advisor
```

---

## 📞 Support & Debug

**Có vấn đề gì?**
- Xem logs: `tail -f debug-logs/`
- Enable debug mode: `DEBUG=1 streamlit run app.py`
- Check project issues: [GitHub Issues](https://github.com/quanghuy25w/AI-academic-advisor/issues)

---

## ✅ Checklist Hoàn Thành

- [ ] Python >= 3.9 cài đặt
- [ ] Virtual environment activate
- [ ] Dependencies cài xong
- [ ] `.env` file cấu hình
- [ ] Groq API key hoạt động
- [ ] Dữ liệu xích nhập xong
- [ ] Streamlit chạy OK
- [ ] Test queries hoạt động

**Nếu checkmark hết → Bạn đã sẵn sàng!** 🎉
- [ ] Ứng dụng chạy bình thường

---

## 📝 Notes:

- Không cần restart server, chỉ cần reload ứng dụng
- Force push sẽ ghi đè history trên remote
- Đảm bảo không ai khác đang work trên branch này

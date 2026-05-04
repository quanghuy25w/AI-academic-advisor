# AI Cố Vấn Học Tập

Một hệ thống gợi ý khóa học thông minh sử dụng AI agents và RAG để cung cấp hướng dẫn học tập được cá nhân hóa cho sinh viên đại học.

## Tổng Quan

Quy trình đa-agent kết hợp dữ liệu chương trình đào tạo với hồ sơ học tập của sinh viên để tạo ra các gợi ý thích hợp theo ngữ cảnh, bổ sung bởi hệ thống thông báo email tự động và quản lý lịch sử trò chuyện bền vững.

---

## Tính Năng Chính

- **Kiến Trúc Đa-Agent**: Quy trình suy luận nhiều bước sử dụng LangGraph để phân tích chương trình, phân loại ý định và tạo phản hồi
- **RAG (Retrieval-Augmented Generation)**: Tìm kiếm lai ghép kết hợp semantic + exact matching để tránh AI hallucination và đảm bảo độ chính xác dữ liệu
- **Hồ Sơ Sinh Viên**: Tự động trích xuất và lưu trữ các ưu tiên học tập, ràng buộc và lịch sử học tập của sinh viên
- **Bộ Nhớ Đa Tầng**: Giảm các lệnh gọi LLM không cần thiết thông qua chiến lược cache semantic, exact match và bộ nhớ
- **Tích Hợp Email**: Hệ thống nhắc nhở theo lịch trình với các gợi ý khóa học và cảnh báo hạn chót
- **Cấu Hình Dựa Trên Môi Trường**: Quản lý an toàn các khóa API và thông tin đăng nhập thông qua biến môi trường

---

## Công Nghệ Sử Dụng

**Ngôn Ngữ**: Python 3.9+  
**LLM & Orchestration**: LangChain, LangGraph, Groq (llama-3.1-8b)  
**Vector Database**: Chroma với tìm kiếm cosine similarity  
**Xử Lý Dữ Liệu**: Các loader tùy chỉnh cho CSV, PDF với chunking có thể cấu hình  
**Công Cụ Hỗ Trợ**: python-dotenv, Pydantic cho xác thực

---

## Cài Đặt Nhanh

### Yêu Cầu
- Python 3.9+
- API key Groq (https://console.groq.com)

### Hướng Dẫn Cài Đặt

```bash
# 1. Clone repository
git clone <repo_url>
cd Agent_AI_Levelup

# 2. Tạo virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# hoặc: source venv/bin/activate  (macOS/Linux)

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Thiết lập biến môi trường
cp .env.example .env
# Chỉnh sửa .env và thêm GROQ_KEYS của bạn
```

### Cấu Hình

**Cấu trúc file `.env`:**
```env
GROQ_KEYS=gsk_xxxxx,gsk_yyyyy,gsk_zzzzz
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_app_password
```

Các key sẽ được tự động xoay vòng để quản lý rate limits.

**Hướng Dẫn Lấy API Key Groq:**

1. Truy cập: https://console.groq.com/keys
2. Đăng nhập hoặc tạo tài khoản Groq (free)
3. Nhấn "Create API Key" 
4. Copy API key vừa tạo
5. Thêm vào `.env`:
   ```env
   GROQ_KEYS=gsk_your_key_here
   ```
   
   **Lưu ý**: Bạn có thể thêm nhiều key cách nhau bằng dấu phẩy:
   ```env
   GROQ_KEYS=gsk_key1,gsk_key2,gsk_key3
   ```
   Điều này giúp tránh rate limiting khi có lượng request lớn.

**Hướng Dẫn Cấu Hình Email:**

1. Bật **2-Step Verification** trên Google Account: https://myaccount.google.com/security
2. Tạo **App Password**:
   - Vào: https://myaccount.google.com/apppasswords
   - Chọn "Mail" → "Windows Computer" (hoặc thiết bị của bạn)
   - Google sẽ tạo một password 16 ký tự
   - Copy password này vào `.env` (`APP_PASSWORD=xxxxx`)
3. Thêm email của bạn vào `.env` (`SENDER_EMAIL=your_email@gmail.com`)

### Sử Dụng

```python
from src.config.groq_gateway import invoke_llm
from src.agent.graph import build_graph

# Chạy quy trình agent
graph = build_graph()
result = graph.invoke({
    "query": "Tôi muốn học data science nhưng có hạn thời gian"
})

print(result["response"])
```

### Chạy Ứng Dụng

Ứng dụng có hai cách chạy:

**Cách 1: Chạy qua Streamlit UI (Giao diện Web)**

```bash
streamlit run app.py
```

Ứng dụng sẽ mở ở: `http://localhost:8501`

Tính năng:
- Login/Register sinh viên
- Nhập profile học tập (năm học, yêu cầu, ràng buộc)
- Chat với AI để nhận gợi ý khóa học
- Xem lịch sử trò chuyện
- Nhận email nhắc nhở

**Cách 2: Chạy qua API/Python Script**

```python
from src.agent.graph import build_graph
from src.config.groq_gateway import invoke_llm

# Khởi tạo graph
graph = build_graph()

# Gửi truy vấn
response = graph.invoke({
    "user_id": "student_123",
    "query": "Khóa học nào tốt cho lập trình web?",
})

print(f"Gợi ý: {response['response']}")
```

**Cách 3: Chạy các script test**

```bash
# Test toàn bộ RAG pipeline
python src/rag/test_full_pipeline.py

# Test router/agent logic
python test_router_upgrade.py

# Check vector store collections
python src/ingestion/check_collections.py
```

**Lưu ý:**
- Lần đầu chạy sẽ cần xích nhập dữ liệu (chương trình học từ `data_raw/`)
- Quá trình xích nhập mất ~2-5 phút tùy kích thước dữ liệu
- Sau đó, vector database sẽ được cache trong `vector_store/`

---

## Cấu Trúc Dự Án

```
Agent_AI_Levelup/
├── src/
│   ├── agent/              # Quy trình suy luận đa-node
│   │   ├── graph.py        # Orchestration quy trình LangGraph
│   │   ├── nodes.py        # Các bước suy luận riêng lẻ
│   │   └── state.py        # Định nghĩa schema & kiểu state
│   │
│   ├── rag/                # Retrieval-Augmented Generation
│   │   ├── hybrid_retriever.py   # Tìm kiếm semantic + exact
│   │   ├── rag_pipeline.py       # Quy trình RAG toàn bộ
│   │   ├── reranker.py           # Xếp hạng lại cross-encoder
│   │   └── response_generator.py # Tổng hợp phản hồi LLM
│   │
│   ├── cache/              # Cache đa chiến lược
│   │   ├── semantic_cache.py     # Cache dựa trên similarity vector
│   │   ├── exact_cache.py        # Cache khớp chính xác
│   │   └── memory_cache.py       # Cache LRU trong bộ nhớ
│   │
│   ├── memory/             # Hồ sơ sinh viên & lịch sử trò chuyện
│   │   ├── student_memory.py     # Trích xuất hồ sơ học tập
│   │   ├── chat_memory.py        # Lưu trữ trò chuyện
│   │   └── vector_memory/        # Kho vector Chroma
│   │
│   ├── ingestion/          # Quy trình dữ liệu
│   │   ├── loaders.py            # Loader CSV, PDF, tài liệu
│   │   ├── chunkers.py           # Chia nhỏ text có thể cấu hình
│   │   ├── ingest_pipeline.py    # Quy trình xích nhập toàn bộ
│   │   └── vector_store.py       # Khởi tạo Chroma
│   │
│   ├── prompts/            # Mẫu prompt
│   │   ├── intent_prompt.py      # Phân loại ý định
│   │   ├── answer_prompt.py      # Tạo phản hồi
│   │   └── validation_prompt.py  # Xác thực đầu ra
│   │
│   ├── tools/              # Tích hợp bên ngoài
│   │   ├── email_sender.py       # Gửi email
│   │   ├── search_tool.py        # Tìm kiếm web
│   │   └── response_tool.py      # Công cụ hậu xử lý
│   │
│   └── config/             # Quản lý cấu hình
│       ├── groq_gateway.py       # Client LLM với xoay key
│       └── email_config.py       # Thiết lập email service
│
├── data_raw/               # Dữ liệu chương trình & quy định thô
├── vector_store/           # File database vector Chroma
├── requirements.txt        # Các dependencies Python
└── README.md              # File này
```

---

## Quyết Định Thiết Kế

### Tại Sao LangGraph?

Prompt tuần tự truyền thống thường thất bại ở suy luận phức tạp. LangGraph cho phép chúng ta cấu trúc vấn đề như một máy trạng thái với các bước suy luận riêng biệt:
1. **Phân Loại Ý Định** → Sinh viên muốn gì?
2. **Tìm Kiếm Chương Trình** → Những khóa học nào phù hợp?
3. **Xác Thực Ràng Buộc** → Có đủ điều kiện tiên quyết không? Có thời gian không?
4. **Tạo Phản Hồi** → Tổng hợp gợi ý với giải thích

### Tìm Kiếm Lai (Semantic + Exact)

Tìm kiếm semantic thuần túy có thể bị dương tính giả (các khóa học giống nhưng yêu cầu khác). Matching chính xác bắt lại các code khóa học và yêu cầu có cấu trúc. Chúng ta kết hợp cả hai:
- **Semantic**: Bắt ý định và chủ đề khóa học
- **Exact**: Đảm bảo tìm thấy khóa học theo code, phòng ban hoặc từ khóa cụ thể

### Cache Đa Tầng

Các lệnh gọi LLM rất đắt tiền. Chúng ta cache ở ba mức:
- **Memory Cache**: Nhanh cho truy vấn lặp lại trong cùng một phiên
- **Exact Cache**: Tái sử dụng phản hồi cho truy vấn giống hệt nhau qua các phiên
- **Semantic Cache**: Truy vấn tương tự (trong khoảng cách embedding) bỏ qua LLM hoàn toàn

---

## Hiệu Suất

- **Độ trễ trung bình**: ~2-3 giây (bao gồm tìm kiếm vector + suy luận LLM)
- **Tỷ lệ cache hit**: ~35-45% trên các yêu cầu học sinh điển hình
- **Tìm kiếm vector**: Dưới 100ms cho 10k+ course vectors

---

## Mở Rộng Hệ Thống

### Thêm Dữ Liệu Tùy Chỉnh
```python
from src.ingestion.ingest_pipeline import IngestPipeline

pipeline = IngestPipeline(
    data_source="curriculum.csv",
    chunk_size=500,
    chunk_overlap=50
)
pipeline.run()
```

### Tạo Node Suy Luận Mới
```python
from src.agent.nodes import BaseNode

class MyAnalysisNode(BaseNode):
    def invoke(self, state):
        # Logic tùy chỉnh của bạn ở đây
        return {"analysis": result}
```

---

## Các Hạn Chế Đã Biết & Kế Hoạch Tương Lai

- **Context Window**: Bị giới hạn bởi context của model Groq (8K tokens) → Kế hoạch triển khai tóm tắt đệ quy
- **Dữ Liệu Thực Tế**: Cập nhật chương trình cần xích nhập lại → Xem xét pipeline CDC
- **Đa Ngôn Ngữ**: Hiện tại tập trung vào tiếng Việt → Có thể mở rộng với lớp dịch
- **Triển Khai**: Chỉ kiểm tra cuc bộ → Docker + triển khai đám mây đang chờ xử lý

---

## Bảo Mật

- API keys lưu trữ trong `.env` (không bao giờ được commit vào git)
- Cấu hình dựa trên môi trường cho các giai đoạn triển khai khác nhau
- Xem [SECURITY_SETUP.md](./SECURITY_SETUP.md) để biết thủ tục xoay key

---

## Đóng Góp

Tìm thấy lỗi hoặc muốn cải thiện độ chính xác? Mở một issue hoặc gửi PR. Tất cả các đóng góp đều được hoan nghênh.

---

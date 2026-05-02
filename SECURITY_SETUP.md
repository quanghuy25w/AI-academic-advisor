# 🔐 Hướng dẫn Bảo mật Dự án - Security Setup Guide

## ✅ Các bước đã hoàn thành:

1. ✓ Tạo file `.env` với các API Keys
2. ✓ Cập nhật `src/config/groq_gateway.py` để đọc từ biến môi trường
3. ✓ Cập nhật `.gitignore` để chứa `.env` và thư mục rác Python

---

## 🚨 QUAN TRỌNG: Xóa API Keys khỏi Git History

Vì các commit cũ đã chứa API Key trong `groq_gateway.py`, bạn cần xóa chúng khỏi Git history.

### **Phương pháp 1: Sử dụng BFG Repo-Cleaner (Khuyên dùng - Nhanh & Dễ)**

#### Cài đặt BFG:
```bash
# Trên Windows (PowerShell - chạy quyền Admin)
choco install bfg  # Nếu dùng Chocolatey

# Hoặc download từ: https://rtyley.github.io/bfg-repo-cleaner/
# Sau đó thêm vào PATH
```

#### Xóa API Keys khỏi history:
```bash
# 1. Tạo một bản sao lưu của dự án (nếu cần)
cp -r Agent_AI_Levelup Agent_AI_Levelup.backup

# 2. Chạy BFG để xóa patterns từ tất cả các commit
bfg --replace-text groq-keys.txt Agent_AI_Levelup/

# Tạo file groq-keys.txt chứa các API Key cần xóa:
cat > groq-keys.txt << 'EOF'
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
gsk_***REDACTED***
EOF

# 3. Chạy BFG
bfg --replace-text groq-keys.txt

# 4. Cleanup
cd Agent_AI_Levelup
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Force push lên GitHub
git push -f origin main
```

---

### **Phương pháp 2: Sử dụng git-filter-branch (Nếu không có BFG)**

```bash
# ⚠️ CẢNH BÁO: Phương pháp này sẽ viết lại tất cả commits
# Nên backup lại dự án trước

cd Agent_AI_Levelup

# 1. Xóa API Keys từ tất cả commits
git filter-branch --rewrite-map-commit $(cat << 'EOF'
#!/bin/bash
# Thay thế tất cả API Keys bằng placeholder
# ⚠️ Thay gsk_... bằng actual keys bạn muốn xóa
sed -i 's/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g; s/***REMOVED***/***REMOVED***/g' "$@"
EOF
) -f -- src/config/groq_gateway.py src/tools/system_prompt.py

# 2. Cleanup
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 3. Force push (⚠️ CẦN THẬN!)
git push -f origin main
```

---

### **Phương pháp 3: Đơn giản - Xóa hết và tạo lại (Nếu commit quá cũ hoặc không quan trọng)**

```bash
cd Agent_AI_Levelup

# ⚠️ CẦN THẬN: Phương pháp này xóa tất cả lịch sử commit!

# 1. Tạo một branch mới từ commit hiện tại
git checkout --orphan new_branch

# 2. Thêm tất cả file
git add .

# 3. Commit
git commit -m "chore: remove sensitive data and restructure history"

# 4. Xóa branch main cũ
git branch -D main

# 5. Đổi tên branch
git branch -m main

# 6. Force push lên GitHub
git push -f origin main
```

---

## 🔄 Các bước tiếp theo:

### 1. **Cài đặt python-dotenv** (nếu chưa có):
```bash
pip install python-dotenv
```

### 2. **Cập nhật requirements.txt**:
```bash
# Thêm vào requirements.txt
echo "python-dotenv>=0.19.0" >> requirements.txt

# Hoặc chạy
pip freeze > requirements.txt
```

### 3. **Kiểm tra setup hiện tại**:
```bash
# 1. Xác nhận .env được tạo
ls -la .env

# 2. Xác nhận groq_gateway.py đã cập nhật
cat src/config/groq_gateway.py | head -20

# 3. Xác nhận .gitignore đã cập nhật
cat .gitignore

# 4. Kiểm tra git status
git status
```

### 4. **Commit các thay đổi mới**:
```bash
git add .env .gitignore src/config/groq_gateway.py requirements.txt
git commit -m "security: migrate API keys to environment variables"
git push origin main
```

---

## 🛡️ Checklist Bảo mật:

- [ ] File `.env` được tạo với các API Keys
- [ ] `src/config/groq_gateway.py` đã cập nhật để đọc từ `.env`  
- [ ] `.gitignore` chứa `.env` và thư mục rác Python
- [ ] Commit cũ có API Keys đã được xóa khỏi Git history
- [ ] Đã push lên GitHub với flag `-f` (force push)
- [ ] Xác nhận GitHub không còn hiển thị API Keys
- [ ] `requirements.txt` đã cập nhật với `python-dotenv`
- [ ] Tất cả team members đã được thông báo về thay đổi

---

## ⚠️ LƯU Ý Quan Trọng:

1. **GitHub Secret Scanning**: GitHub sẽ tự động quét Git history để phát hiện API Keys. Nếu phát hiện, bạn cần:
   - Regenerate tất cả các API Keys trên Groq dashboard
   - Xóa khỏi Git history
   - Push lên GitHub

2. **Force Push**: Các lệnh `-f` (force push) sẽ ghi đè lịch sử commit. Đảm bảo tất cả team members đã sync trước khi làm điều này.

3. **Backup**: Luôn tạo backup trước khi chạy các lệnh xóa lịch sử Git.

4. **Kiểm tra localhost**: Trước khi push, hãy test ứng dụng nó có thể đọc từ `.env` bình thường.

---

## 📝 Thêm Notes:

- API Keys nên được rotate định kỳ (ví dụ: hàng tháng)
- Sử dụng Environment Variables cho staging và production
- Không commit bất kỳ secrets nào vào Git

# 🚀 Quick Fix: GitHub Push Protection - Xóa Secrets & Push Lại

## ❌ Vấn đề:
GitHub phát hiện API Keys trong:
- `src/tools/system_prompt.py` (commit cũ)
- `SECURITY_SETUP.md` (vừa upload - chứa ví dụ keys)

---

## ✅ Giải pháp: 4 bước đơn giản

### **Bước 1: Cài git-filter-repo (Khuyên dùng - Nhanh nhất)**

```bash
pip install git-filter-repo
```

### **Bước 2: Xóa Secrets khỏi Git History**

```bash
# Tạo file danh sách API Keys cần xóa
@"
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
"@ | Out-File -Encoding ASCII groq-keys.txt

# Chạy git-filter-repo để xóa tất cả secrets
git filter-repo --replace-text groq-keys.txt

# Cleanup
Remove-Item groq-keys.txt
```

### **Bước 3: Commit lại các file đã sửa**

```bash
# Xóa backup từ git-filter-repo
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Commit lại
git add .
git commit -m "security: remove API keys from git history and SECURITY_SETUP.md"
```

### **Bước 4: Force Push lên GitHub**

```bash
git push -u origin main --force
```

---

## ⚠️ Nếu vẫn bị reject:

**Phương pháp 2 - Dùng git filter-branch (Nếu không có git-filter-repo):**

```bash
# Windows PowerShell - Tạo batch script
$script = @"
`$FILTER_BRANCH_SQUELCH_WARNING=1
git filter-branch -f --tree-filter 'powershell -Command "
  `$file = 'src/config/groq_gateway.py'
  if (Test-Path `$file) {
    `$(Get-Content `$file) `
      -replace '***REMOVED***', '***REMOVED***' `
      -replace '***REMOVED***', '***REMOVED***' `
      | Set-Content `$file
  }
"' -- --all
```

---

## 🔄 Sau khi push thành công:

1. **Regenerate tất cả API Keys trên Groq Dashboard** (vì đã bị expose)
2. **Update .env** với những keys mới
3. **Test ứng dụng**
4. **Commit & push**

---

## ✅ Checklist:

- [ ] `git-filter-repo` được cài đặt
- [ ] Chạy lệnh xóa secrets
- [ ] Force push thành công
- [ ] GitHub không còn cảnh báo secrets
- [ ] API Keys đã được regenerate
- [ ] .env được update
- [ ] Ứng dụng chạy bình thường

---

## 📝 Notes:

- Không cần restart server, chỉ cần reload ứng dụng
- Force push sẽ ghi đè history trên remote
- Đảm bảo không ai khác đang work trên branch này

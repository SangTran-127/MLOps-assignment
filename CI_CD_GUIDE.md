# 🔄 Hướng Dẫn CI/CD - GitHub Actions

## 📋 Tổng Quan

Dự án này sử dụng **GitHub Actions** để tự động hóa quy trình kiểm thử và triển khai (CI/CD).

## ✅ Các Tính Năng CI/CD Đã Cài Đặt

### 1. Automated Testing

- ✅ Tự động chạy tests khi push code
- ✅ Kiểm tra syntax và code quality (flake8)
- ✅ Validate data generation và model training
- ✅ Chạy full experiments để đảm bảo pipeline hoạt động

### 2. Build & Package

- ✅ Tự động đóng gói ứng dụng
- ✅ Upload artifacts (MLflow tracking data)
- ✅ Tạo release package

### 3. Docker Support

- ✅ Dockerfile để containerize ứng dụng
- ✅ Docker Compose để chạy cả MLflow UI và Flask app
- ✅ Health checks và auto-restart

## 🚀 Cách Sử Dụng

### Xem Kết Quả CI/CD

1. Truy cập: https://github.com/SangTran-127/MLOps-assignment
2. Click tab **Actions**
3. Xem workflow runs và logs

### Workflow Tự Động Chạy Khi:

- ✅ Push code lên branch `main`
- ✅ Push code lên branch `develop`
- ✅ Tạo Pull Request vào branch `main`

## 🐳 Docker Deployment

### Cách 1: Docker Compose (Khuyên Dùng)

```bash
# Chạy tất cả services (MLflow UI + Flask App)
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng services
docker-compose down
```

Sau khi chạy:

- **MLflow UI**: http://localhost:5000
- **Flask App**: http://localhost:5001

### Cách 2: Chỉ Chạy Flask App

```bash
# Build Docker image
docker build -t mlops-app .

# Chạy container
docker run -d -p 5001:5001 --name mlops-flask mlops-app

# Xem logs
docker logs -f mlops-flask

# Dừng container
docker stop mlops-flask
```

## 🧪 Testing

### Chạy Tests Locally

```bash
# Cài đặt pytest
pip install pytest pytest-cov

# Chạy tất cả tests
pytest test_models.py -v

# Chạy với coverage report
pytest test_models.py --cov=. --cov-report=html
```

### Tests Bao Gồm:

1. **Data Generation Tests**

   - Kiểm tra shape của dữ liệu
   - Kiểm tra số lượng classes
   - Kiểm tra data scaling

2. **Model Training Tests**

   - Test SVM training
   - Test Logistic Regression training
   - Test Neural Network training

3. **Prediction Tests**
   - Kiểm tra output predictions

## 📊 Pipeline Workflow

```
┌─────────────────┐
│   Push Code     │
│   to GitHub     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Checkout Code  │
│  Setup Python   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Install Deps    │
│ Run Linting     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Run Tests      │
│  Validate       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Run Experiments │
│ Upload Artifacts│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build & Package │
│ Create Release  │
└─────────────────┘
```

## 📁 Files Liên Quan CI/CD

```
MLOps-assignment/
├── .github/
│   └── workflows/
│       └── mlops-pipeline.yml    ← GitHub Actions workflow
│
├── Dockerfile                    ← Docker image definition
├── docker-compose.yml            ← Multi-container setup
├── .dockerignore                 ← Docker ignore rules
│
├── test_models.py                ← Unit tests
├── .gitignore                    ← Git ignore rules
│
├── DEPLOYMENT.md                 ← Deployment guide (English)
└── CI_CD_GUIDE.md               ← This file (Tiếng Việt)
```

## 🔧 Cấu Hình

### GitHub Actions Variables

Không cần setup thêm variables, pipeline chạy tự động với:

- Python 3.9
- Ubuntu latest runner
- Cached pip dependencies

### Customize Pipeline

Chỉnh sửa file `.github/workflows/mlops-pipeline.yml` để:

- Thêm/bớt testing steps
- Thay đổi Python version
- Thêm deployment steps
- Configure notifications

## 📝 Best Practices

### 1. Code Quality

- ✅ Chạy `flake8` trước khi commit
- ✅ Viết tests cho code mới
- ✅ Đảm bảo tests pass trước khi push

### 2. Commits

- ✅ Commit messages rõ ràng
- ✅ Commit nhỏ, tập trung vào một feature
- ✅ Không commit sensitive data

### 3. Branches

- ✅ `main`: Production code
- ✅ `develop`: Development code
- ✅ Feature branches: `feature/tên-feature`

### 4. Testing

- ✅ Test locally trước khi push
- ✅ Xem CI logs nếu tests fail
- ✅ Fix tests trước khi merge

## 🎯 Lợi Ích CI/CD

### 1. Tự Động Hóa

- Không cần chạy tests thủ công
- Tự động validate code mỗi lần push
- Phát hiện lỗi sớm

### 2. Chất Lượng Code

- Code review tự động
- Đảm bảo standards
- Duy trì test coverage

### 3. Deployment Nhanh

- Package tự động
- Artifacts sẵn sàng deploy
- Rollback dễ dàng

### 4. Collaboration

- Team biết code status
- Review PRs dễ hơn
- Transparency trong development

## 🚨 Troubleshooting

### Pipeline Fails

**Kiểm tra:**

1. Xem logs trong Actions tab
2. Run tests locally để reproduce
3. Kiểm tra dependencies trong requirements.txt

**Common Issues:**

**❌ Flake8 errors**

```bash
# Fix locally
flake8 . --max-line-length=127
```

**❌ Test failures**

```bash
# Run tests locally
pytest test_models.py -v
```

**❌ Dependency issues**

```bash
# Update requirements
pip freeze > requirements.txt
```

## 📚 Tài Liệu Tham Khảo

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [Pytest Documentation](https://docs.pytest.org/)

## 🎓 Điểm Cộng Cho Bài Tập

Setup CI/CD này đáp ứng yêu cầu:

- ✅ **Automated Testing**: Tests tự động chạy
- ✅ **Code Quality**: Linting và validation
- ✅ **Containerization**: Docker support
- ✅ **Documentation**: Đầy đủ hướng dẫn
- ✅ **Best Practices**: Follow MLOps standards

---

**Tạo bởi**: MLOps Assignment  
**Ngày**: 12/2025  
**GitHub**: https://github.com/SangTran-127/MLOps-assignment

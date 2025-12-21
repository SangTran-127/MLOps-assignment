# BÁO CÁO DỰ ÁN MLOPS

**Môn học:** MLOps  
**Sinh viên:** [Điền tên sinh viên]  
**MSSV:** [Điền MSSV]  
**Ngày nộp:** Tháng 12/2025

---

## TỔNG QUAN DỰ ÁN

Dự án này thực hiện đầy đủ 2 câu hỏi trong đề bài:
- Câu 1: Tạo dự án MLflow cho bài toán phân loại (8 điểm)
- Câu 2: Thiết lập CI/CD với GitHub và Docker

**Repository:** https://github.com/SangTran-127/MLOps-assignment

---

## CÂU 1: TẠO DỰ ÁN MLFLOW (8 ĐIỂM)

### Bước 1.1: Chuẩn bị môi trường

Đầu tiên, tôi tạo thư mục dự án và cài đặt các thư viện cần thiết.

File requirements.txt chứa các thư viện:
- mlflow: Theo dõi thí nghiệm và quản lý mô hình
- scikit-learn: Thư viện học máy
- numpy, pandas: Xử lý dữ liệu
- matplotlib, seaborn: Vẽ biểu đồ
- Flask: Tạo ứng dụng web

Lệnh cài đặt:
```
python3 -m pip install -r requirements.txt
```

**[Thuộc Câu 1]**

---

### Bước 1.2: Tạo dữ liệu phân loại

Tôi sử dụng hàm make_classification của sklearn để tạo dữ liệu tổng hợp cho bài toán phân loại.

File: data_generator.py

Cấu hình dữ liệu:
- Số lượng mẫu: 2000
- Số đặc trưng: 20 (15 đặc trưng thông tin, 5 đặc trưng dư thừa)
- Số lớp phân loại: 3
- Tỷ lệ chia: 80% train, 20% test
- Dữ liệu được chuẩn hóa bằng StandardScaler

Hàm generate_synthetic_data nhận các tham số và trả về dữ liệu đã được chia và chuẩn hóa.

**[Thuộc Câu 1]**

---

### Bước 1.3: Xây dựng module huấn luyện với MLflow

File: train.py

Module này chứa 3 hàm huấn luyện chính:

1. train_svm: Huấn luyện mô hình Support Vector Machine
   - Hỗ trợ các kernel: RBF, Linear, Poly
   - Tham số điều chỉnh: C, gamma

2. train_logistic_regression: Huấn luyện mô hình Logistic Regression
   - Tham số điều chỉnh: C (regularization), solver

3. train_neural_network: Huấn luyện mạng Neural Network (MLP)
   - Tham số điều chỉnh: hidden_layers, alpha, learning_rate

Mỗi hàm đều tích hợp MLflow để:
- Ghi lại tham số mô hình (mlflow.log_param)
- Ghi lại các metric: accuracy, precision, recall, f1-score (mlflow.log_metric)
- Lưu confusion matrix dưới dạng artifact (mlflow.log_artifact)
- Lưu mô hình đã huấn luyện (mlflow.sklearn.log_model)

**[Thuộc Câu 1]**

---

### Bước 1.4: Thực hiện 8 thí nghiệm với các siêu tham số khác nhau

File: run_experiments.py

Tôi thực hiện 8 thí nghiệm với lý do rõ ràng cho mỗi lần điều chỉnh siêu tham số:

**Thí nghiệm 1: SVM RBF Baseline (C=1.0)**
- Lý do: Bắt đầu với cấu hình mặc định của RBF kernel làm baseline. RBF kernel phù hợp với dữ liệu phi tuyến tính.
- Kết quả: Accuracy = 82.25%, F1 = 82.17%

**Thí nghiệm 2: SVM RBF với C=10.0**
- Lý do: Tăng C lên 10 để giảm regularization, cho phép mô hình học các pattern phức tạp hơn từ dữ liệu huấn luyện.
- Kết quả: Accuracy = 82.25%, F1 = 82.19% (Tốt nhất)

**Thí nghiệm 3: SVM Linear**
- Lý do: Thử kernel tuyến tính để kiểm tra xem dữ liệu có thể phân tách tuyến tính không. Mô hình tuyến tính đơn giản hơn và nhanh hơn.
- Kết quả: Accuracy = 71.00%, F1 = 70.64%

**Thí nghiệm 4: Logistic Regression Baseline (C=1.0)**
- Lý do: So sánh SVM với Logistic Regression, một mô hình tuyến tính đơn giản thường được dùng làm baseline.
- Kết quả: Accuracy = 69.00%, F1 = 68.62%

**Thí nghiệm 5: Logistic Regression với C=0.1**
- Lý do: Giảm C xuống 0.1 để tăng cường regularization, giúp tránh overfitting và cải thiện khả năng tổng quát hóa.
- Kết quả: Accuracy = 69.25%, F1 = 68.86%

**Thí nghiệm 6: Neural Network 1 lớp ẩn (100 neurons)**
- Lý do: Thử nghiệm mạng neural đơn giản với 1 lớp ẩn để nắm bắt các pattern phi tuyến nhưng vẫn giữ mô hình tương đối đơn giản.
- Kết quả: Accuracy = 79.75%, F1 = 79.59%

**Thí nghiệm 7: Neural Network sâu (100, 50 neurons)**
- Lý do: Sử dụng mạng sâu hơn với 2 lớp ẩn để học các đặc trưng phân cấp phức tạp hơn, kết hợp với regularization mạnh hơn (alpha=0.001).
- Kết quả: Accuracy = 78.00%, F1 = 77.87%

**Thí nghiệm 8: Neural Network rộng (200 neurons)**
- Lý do: Sử dụng lớp ẩn rộng hơn (200 neurons) để tăng khả năng biểu diễn của mô hình.
- Kết quả: Accuracy = 80.00%, F1 = 79.88%

**[Thuộc Câu 1]**

---

### Bước 1.5: So sánh kết quả các mô hình

Bảng so sánh kết quả:

| Thứ hạng | Mô hình | Accuracy | F1 Score |
|----------|---------|----------|----------|
| 1 | SVM RBF C=10.0 | 82.25% | 82.19% |
| 2 | SVM RBF Baseline | 82.25% | 82.17% |
| 3 | NN Wide (200) | 80.00% | 79.88% |
| 4 | NN Single Layer | 79.75% | 79.59% |
| 5 | NN Deep | 78.00% | 77.87% |
| 6 | SVM Linear | 71.00% | 70.64% |
| 7 | LogReg C=0.1 | 69.25% | 68.86% |
| 8 | LogReg Baseline | 69.00% | 68.62% |

Nhận xét:
- SVM với RBF kernel cho kết quả tốt nhất, chứng tỏ dữ liệu có tính phi tuyến
- Neural Network cho kết quả khá tốt nhưng không vượt qua SVM
- Các mô hình tuyến tính (SVM Linear, Logistic Regression) cho kết quả thấp hơn

**[Thuộc Câu 1]**

---

### Bước 1.6: Đăng ký mô hình tốt nhất vào Model Registry

Mô hình SVM RBF với C=10.0 được chọn là mô hình tốt nhất dựa trên F1 Score.

Các bước thực hiện:
1. Lấy run_id của mô hình tốt nhất từ MLflow
2. Đăng ký mô hình vào Model Registry với tên "BestClassifier"
3. Chuyển trạng thái mô hình sang "Production"

Code thực hiện trong hàm register_best_model:
```python
model_uri = f"runs:/{best_run_id}/model"
model_version = mlflow.register_model(model_uri, "BestClassifier")
client.transition_model_version_stage(
    name="BestClassifier",
    version=model_version.version,
    stage="Production"
)
```

**[Thuộc Câu 1]**

---

### Bước 1.7: Xem kết quả trong MLflow UI

Để xem kết quả thí nghiệm, chạy lệnh:
```
python3 -m mlflow ui
```

Sau đó truy cập http://localhost:5000

Trong MLflow UI có thể xem:
- Tất cả 8 thí nghiệm với metrics chi tiết
- So sánh giữa các runs
- Confusion matrix của mỗi mô hình
- Model Registry với mô hình đã đăng ký

**[Thuộc Câu 1]**

---

### Bước 1.8: Tạo ứng dụng Flask

File: app.py
File giao diện: templates/index.html

Ứng dụng Flask có các tính năng:
- Tự động load mô hình tốt nhất từ Model Registry
- Giao diện web cho phép nhập 20 đặc trưng
- Nút "Random Example" để tạo dữ liệu mẫu ngẫu nhiên
- Hiển thị kết quả dự đoán và xác suất của từng lớp

Các API endpoint:
- GET /: Trang chủ với form nhập liệu
- POST /predict: Thực hiện dự đoán
- GET /info: Thông tin về mô hình
- GET /health: Kiểm tra trạng thái server

Chạy ứng dụng:
```
python3 app.py
```

Truy cập http://localhost:5001

**[Thuộc Câu 1]**

---

## CÂU 2: CI/CD VỚI GITHUB

### Bước 2.1: Tạo GitHub Repository

Tôi đã tạo repository trên GitHub và push toàn bộ code lên.

Repository: https://github.com/SangTran-127/MLOps-assignment

Các lệnh thực hiện:
```
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:SangTran-127/MLOps-assignment.git
git push -u origin main
```

**[Thuộc Câu 2]**

---

### Bước 2.2: Tạo GitHub Actions Workflow

File: .github/workflows/mlops-pipeline.yml

Pipeline CI/CD gồm 2 jobs:

**Job 1: Test & Validate**
- Checkout code từ repository
- Cài đặt Python 3.9
- Cài đặt dependencies từ requirements.txt
- Chạy linting với flake8
- Validate module data_generator
- Validate module train
- Chạy toàn bộ 8 thí nghiệm
- Upload MLflow artifacts

**Job 2: Build & Package**
- Chỉ chạy sau khi Job 1 thành công
- Đóng gói ứng dụng thành file tar.gz
- Upload package artifact

Pipeline tự động chạy khi:
- Push code vào branch main hoặc develop
- Tạo Pull Request vào branch main

**[Thuộc Câu 2]**

---

### Bước 2.3: Tạo Unit Tests

File: test_models.py

Các test case bao gồm:

1. TestDataGeneration:
   - test_generate_synthetic_data_shape: Kiểm tra kích thước dữ liệu
   - test_generate_synthetic_data_classes: Kiểm tra số lượng lớp
   - test_data_scaling: Kiểm tra dữ liệu đã được chuẩn hóa

2. TestModelTraining:
   - test_svm_training: Kiểm tra huấn luyện SVM
   - test_logistic_regression_training: Kiểm tra huấn luyện Logistic Regression
   - test_neural_network_training: Kiểm tra huấn luyện Neural Network

3. TestModelPrediction:
   - test_svm_prediction_shape: Kiểm tra output dự đoán

Chạy tests:
```
pytest test_models.py -v
```

**[Thuộc Câu 2]**

---

### Bước 2.4: Tạo Docker Configuration

**Dockerfile:**
- Base image: python:3.9-slim
- Cài đặt dependencies
- Copy code ứng dụng
- Expose port 5001
- Cấu hình health check

**docker-compose.yml:**
Định nghĩa 2 services:
1. mlflow-server (port 5000): Chạy MLflow UI
2. flask-app (port 5001): Chạy Flask application

Chạy với Docker Compose:
```
docker-compose up -d
```

**[Thuộc Câu 2]**

---

### Bước 2.5: Xem kết quả CI/CD

Truy cập: https://github.com/SangTran-127/MLOps-assignment/actions

Tại đây có thể xem:
- Lịch sử các workflow runs
- Log chi tiết của từng step
- Artifacts đã upload (mlflow-artifacts, mlops-package)
- Trạng thái pass/fail của pipeline

**[Thuộc Câu 2]**

---

## CẤU TRÚC THƯ MỤC DỰ ÁN

```
MLOps-assignment/
|-- .github/
|   |-- workflows/
|       |-- mlops-pipeline.yml    # CI/CD workflow
|
|-- templates/
|   |-- index.html                # Giao diện web
|
|-- app.py                        # Flask application
|-- data_generator.py             # Module tạo dữ liệu
|-- train.py                      # Module huấn luyện
|-- run_experiments.py            # Script chạy thí nghiệm
|-- test_models.py                # Unit tests
|-- verify_model.py               # Kiểm tra mô hình
|
|-- Dockerfile                    # Docker image
|-- docker-compose.yml            # Docker services
|-- .dockerignore                 # Docker ignore
|
|-- requirements.txt              # Dependencies
|-- .gitignore                    # Git ignore
|
|-- README.md                     # Tài liệu hướng dẫn
|-- SUMMARY.md                    # Tóm tắt dự án
|-- BAO_CAO_DU_AN.md             # File báo cáo này
|
|-- mlruns/                       # Dữ liệu MLflow (tự động tạo)
```

---

## HƯỚNG DẪN CHẠY DỰ ÁN

### Cách 1: Chạy trực tiếp

1. Cài đặt dependencies:
```
python3 -m pip install -r requirements.txt
```

2. Chạy thí nghiệm:
```
python3 run_experiments.py
```

3. Xem MLflow UI (Terminal 1):
```
python3 -m mlflow ui
```
Truy cập: http://localhost:5000

4. Chạy Flask app (Terminal 2):
```
python3 app.py
```
Truy cập: http://localhost:5001

### Cách 2: Chạy với Docker

```
docker-compose up -d
```

Truy cập:
- MLflow UI: http://localhost:5000
- Flask App: http://localhost:5001

---

## KẾT LUẬN

Dự án đã hoàn thành đầy đủ các yêu cầu:

**Câu 1 (MLflow Project):**
- Sử dụng make_classification của sklearn để tạo dữ liệu
- Xây dựng 3 loại mô hình: SVM, Logistic Regression, Neural Network
- Thực hiện 8 thí nghiệm với lý do rõ ràng cho mỗi lần tuning
- So sánh kết quả và chọn mô hình tốt nhất (SVM RBF C=10.0, F1=82.19%)
- Đăng ký mô hình vào MLflow Model Registry
- Tạo ứng dụng Flask với giao diện web

**Câu 2 (CI/CD):**
- Push code lên GitHub repository
- Tạo GitHub Actions workflow với 2 jobs
- Viết unit tests cho các module
- Tạo Docker và Docker Compose configuration
- Pipeline tự động chạy khi push code

---

## LINK THAM KHẢO

- GitHub Repository: https://github.com/SangTran-127/MLOps-assignment
- GitHub Actions: https://github.com/SangTran-127/MLOps-assignment/actions

---

**Ngày hoàn thành:** Tháng 12/2025

# TÀI LIỆU TRIỂN KHAI PIPELINE PHÂN TÍCH DỮ LIỆU CHẤT LƯỢNG KHÔNG KHÍ

Tài liệu này cung cấp toàn bộ kiến thức lý thuyết, mô tả luồng công việc (pipeline), và giải thích chi tiết các đoạn mã nguồn (code) được áp dụng trong project phân tích mức độ ô nhiễm không khí.

---

## 1. Giới Thiệu Bài Toán và Dữ Liệu
* **Bài toán:** Phân tích, đánh giá biến động và dự đoán nồng độ ô nhiễm dựa trên các chỉ số không khí và khí tượng.
* **Nguồn dữ liệu:** Dựa trên bộ dữ liệu **Air Quality UCI Dataset** thu thập từ một trạm cảm biến chất lượng không khí nằm trong khu vực thành phố.
* **Đặc trưng dữ liệu:**
  * Dữ liệu thời gian chuỗi (Time Series): Bao gồm biến ngày (`Date`) và giờ (`Time`).
  * Chỉ số nồng độ các chất: `CO(GT)`, `NO2(GT)`, `NOx(GT)`, `C6H6(GT)`, `PT08.S1`...
  * Chỉ số khí tượng: Nhiệt độ (`T`), Độ ẩm tương đối (`RH`), Độ ẩm tuyệt đối (`AH`).
  * Nhiễu (Missing value): Bộ dữ liệu quy ước các giá trị không thu thập được bằng số **`-200`**.

---

## 2. Kiến Trúc Pipeline 

Quá trình phân tích dữ liệu được triển khai theo quy trình Data Science tiêu chuẩn gồm 5 bước chính:
1. **Tiền xử lý dữ liệu (Data Preprocessing):** Làm sạch, xử lý missing value, định dạng thời gian.
2. **Thống kê mô tả (Descriptive Statistics):** Trích xuất thông tin tổng quan, phát hiện ngoại lai (Outliers).
3. **Trực quan hóa (Data Visualization):** Nhận diện xu hướng và phân bố.
4. **Phân tích suy diễn (Hypothesis Testing):** Đánh giá mức độ ý nghĩa thống kê của các giả thuyết.
5. **Mô hình hóa (Machine Learning - Linear Regression):** Xây dựng hệ thống dự báo.

---

## 3. Giải Thích Mã Nguồn và Lý Thuyết Triển Khai

### Bước 1: Thu thập và Tiền xử lý dữ liệu
**Lý thuyết:** 
Dữ liệu thực tế thường chứa nhiều lỗi như cột rỗng, dòng trống, đặc biệt là dữ liệu khuyết. Nếu mang trực tiếp vào mô hình sẽ gây sai lệch kết quả nghiêm trọng. Kỹ thuật nội suy (Interpolation) rất phù hợp cho dữ liệu chuỗi thời gian vì các biến như nhiệt độ, khí gas thường thay đổi tuyến tính và liên tục.

**Giải thích Code:**
- `pd.read_csv(..., sep=';', decimal=',')`: File có định dạng theo chuẩn châu âu nên dấu cách cột là `;` và dấu thập phân là `,`.
- `df.replace(-200, np.nan, inplace=True)`: Chuyển các giá trị nhiễu `-200` thành dạng giá trị rỗng (`NaN`) chuẩn của Numpy để thư viện Pandas có thể hiểu được.
- `pd.to_datetime(...)`: Ghép 2 cột Ngày và Giờ thành 1 trục thời gian duy nhất (`Datetime`) nhằm hỗ trợ index cho bài toán chuỗi thời gian.
- `df.interpolate(method='time', inplace=True)`: Hàm tự động điền các giá trị `NaN` dựa trên thời gian. Ví dụ: Nếu 8h00 là 20 độ, 10h00 là 24 độ, thì máy sẽ tự động tính nội suy 9h00 (nếu bị khuyết) là 22 độ.

### Bước 2: Phân tích thống kê & Phát hiện ngoại lai (Outliers)
**Lý thuyết:**
- Ngoại lai là những điểm dữ liệu "đột biến", quá cao hoặc quá thấp so với phần lớn dữ liệu còn lại (có thể do cảm biến hỏng).
- **Phương pháp IQR (Interquartile Range - Khoảng Tứ Phân Vị):**
  - Q1 (Tứ phân vị thứ nhất): Điểm cắt 25% dữ liệu thấp nhất.
  - Q3 (Tứ phân vị thứ ba): Điểm cắt 75% dữ liệu thấp nhất.
  - IQR = Q3 - Q1.
  - Cận dưới: $Q1 - 1.5 \times IQR$
  - Cận trên: $Q3 + 1.5 \times IQR$
  - Các giá trị vượt qua hai cận này được phân loại là Outliers.

**Giải thích Code:**
- `df.describe().T`: Trả về các thông số nền tảng như Mean (Trung bình), Std (Độ lệch chuẩn đại diện cho độ phân tán dữ liệu), Min, Max.
- `detect_outliers_iqr()`: Hàm tuân theo đúng công thức Toán học của IQR để lọc ra những giá trị ngoại lai.

### Bước 3: Trực quan hóa dữ liệu
**Lý thuyết:**
- **Line Chart (Biểu đồ đường):** Giúp nhìn rõ xu hướng dao động theo thời gian (chu kỳ ngày/đêm, mùa). Ở đây dùng `.resample('W').mean()` để gộp dữ liệu theo từng tuần (Weekly), giúp đồ thị bớt bị "nhiễu răng cưa".
- **Scatter Plot (Biểu đồ phân tán):** Quan sát tương quan trực tiếp giữa 2 biến liên tục (Ví dụ: Nhiệt độ tăng thì độ ẩm có giảm không?).
- **Histogram (Biểu đồ tần suất):** Đánh giá mức độ phân bố của 1 biến (xem có tuân theo phân phối chuẩn Gaussian hay bị lệch).
- **Boxplot (Biểu đồ hộp):** Hiển thị rõ ràng các điểm ngoại lai thông qua các "dấu chấm" nằm ngoài vùng Box và Whiskers.

### Bước 4: Kiểm định giả thuyết (Hypothesis Testing)
**Lý thuyết:**
- Sử dụng **Independent T-Test (Kiểm định T độc lập hai mẫu)** để xét xem hai tập mẫu riêng biệt có trung bình tổng thể bằng nhau hay không.
- **Giả thuyết H0 (Null Hypothesis):** Nồng độ CO ban ngày = Nồng độ CO ban đêm.
- **P-value:** Xác suất để xảy ra kết quả hiện tại nếu H0 là đúng. Nếu $P \text{-value} < 0.05$ (mức ý nghĩa 5%), ta có đủ cơ sở để bác bỏ H0.

**Giải thích Code:**
- `df.index.hour`: Lấy ra phần giờ từ trục thời gian để phân nhóm Ban ngày (06-18h) và Ban đêm (18h-06h).
- `stats.ttest_ind(daytime_co, nighttime_co, equal_var=False)`: Chạy kiểm định T-test (đặt `equal_var=False` cho bài toán biến phương sai không đồng nhất - Welch's t-test).

### Bước 5: Mô hình Hồi quy Tuyến tính (Linear Regression)
**Lý thuyết:**
Đây là phương pháp tìm ra một đường thẳng siêu phẳng (Hyperplane) tốt nhất phù hợp với dữ liệu để dự đoán kết quả.
Công thức: $Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_n X_n + \epsilon$
- Y: Nồng độ Benzen (`C6H6(GT)`) (Biến mục tiêu / Target).
- X: Các đặc trưng (Features) như Nhiệt độ, Độ ẩm, Cảm biến khí khác.
- $\beta$: Các hệ số (Coefficients) thể hiện tác động của từng X lên Y.

**Đánh giá Mô hình:**
- **MSE (Mean Squared Error):** Trung bình bình phương sai số. Phạt rất nặng các dự đoán bị sai lệch lớn (Outliers).
- **MAE (Mean Absolute Error):** Trung bình sai số tuyệt đối. Sai số trung bình cơ bản tính bằng đơn vị gốc của Y.
- **R-squared ($R^2$):** Hệ số xác định. Nằm trong khoảng $0 \to 1$. $R^2 = 0.8$ có nghĩa là 80% sự thay đổi của nồng độ Benzen có thể được giải thích bằng các biến X đầu vào.

**Giải thích Code:**
- `train_test_split(..., test_size=0.2)`: Chia bộ dữ liệu theo tỷ lệ Vàng: 80% (Học mô hình) - 20% (Làm bài kiểm tra đánh giá độ chính xác).
- `LinearRegression().fit(X_train, y_train)`: Quá trình Training, thuật toán tối ưu hóa Gradient Descent (hoặc OLS) để tìm ra các $\beta$ tốt nhất.
- `lr_model.coef_`: Gọi ra danh sách các hệ số tác động. Biến nào có hệ số tuyệt đối lớn chứng tỏ nó có ảnh hưởng mạnh lên nồng độ của Benzen.

---

## 4. Kết luận
Tài liệu này cung cấp đầy đủ các góc nhìn từ cơ sở toán học thống kê cho đến logic triển khai lập trình bằng Python. Bạn có thể sử dụng các nội dung trong này để điền trực tiếp vào Báo cáo Tiểu luận, cũng như làm Slide để bảo vệ trước Hội đồng một cách tự tin nhất vì bạn nắm rõ mọi chi tiết của bài toán!

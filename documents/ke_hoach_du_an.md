# KẾ HOẠCH DỰ ÁN: DỰ BÁO NỒNG ĐỘ PM2.5 TẠI TRẠM AOTIZHONGXIN

**Bộ dữ liệu:** `Aotizhongxin_Raw.csv`
**Loại bài toán:** Hồi quy (Regression)

---

## 1. Giới thiệu bài toán thực tế
- Ô nhiễm không khí, đặc biệt là bụi mịn PM2.5, ảnh hưởng nghiêm trọng đến sức khỏe cộng đồng và chất lượng cuộc sống.
- Việc theo dõi và dự báo nồng độ PM2.5 giúp người dân có biện pháp phòng ngừa và các cơ quan quản lý đưa ra cảnh báo sớm.
- **Bài toán đặt ra:** Dựa vào các thông số khí tượng (nhiệt độ, áp suất, độ ẩm, sức gió...) và các chất ô nhiễm khác (SO2, NO2, CO, O3) để dự đoán giá trị nồng độ bụi mịn PM2.5 tại trạm quan trắc Aotizhongxin, Bắc Kinh.

## 2. Mục tiêu và câu hỏi phân tích
- **Mục tiêu:** Xây dựng mô hình học máy (Machine Learning) để dự báo nồng độ PM2.5 một cách chính xác.
- **Câu hỏi phân tích:**
    1. Yếu tố khí tượng nào (nhiệt độ, lượng mưa, tốc độ gió) có tác động mạnh nhất đến việc làm giảm hoặc tăng nồng độ PM2.5?
    2. Nồng độ PM2.5 thay đổi như thế nào theo thời gian (theo giờ trong ngày, tháng trong năm, hoặc các mùa)?
    3. Các chất gây ô nhiễm khác (như CO, NO2) có mối tương quan đồng biến hay nghịch biến với PM2.5?

## 3. Mô tả dữ liệu
- Dữ liệu đầu vào lấy từ file: `Aotizhongxin_Raw.csv`.
- Tập dữ liệu bao gồm các nhóm biến chính:
    - **Biến thời gian:** `year`, `month`, `day`, `hour`.
    - **Biến mục tiêu (Target):** `PM2.5` (Nồng độ bụi mịn PM2.5).
    - **Biến đặc trưng - Chất ô nhiễm:** `PM10`, `SO2`, `NO2`, `CO`, `O3`.
    - **Biến đặc trưng - Khí tượng:** `TEMP` (Nhiệt độ), `PRES` (Áp suất), `DEWP` (Điểm sương), `RAIN` (Lượng mưa), `wd` (Hướng gió), `WSPM` (Tốc độ gió).

## 4. Thu thập dữ liệu / Nguồn dữ liệu
- Nguồn dữ liệu có sẵn thông qua file `.csv` (`Aotizhongxin_Raw.csv`). Đây là một phần của bộ dữ liệu "Beijing Multi-Site Air-Quality Data" bao gồm thông tin theo giờ từ các trạm quan trắc.

## 5. Làm sạch và tiền xử lý dữ liệu
*(Đáp ứng Yêu cầu kỹ thuật: Xử lý dữ liệu thiếu hoặc không nhất quán)*
- **Xử lý dữ liệu thiếu (Missing Values):**
    - Kiểm tra tỷ lệ dữ liệu bị thiếu (NaN/Null) trên từng biến.
    - Phương pháp xử lý: Sử dụng nội suy tuyến tính (Linear Interpolation) theo chuỗi thời gian hoặc điền bằng giá trị trung bình/trung vị của ngày đó để không làm gãy cấu trúc chuỗi thời gian.
- **Biến đổi dữ liệu:**
    - Gộp các cột `year`, `month`, `day`, `hour` thành một cột kiểu `datetime` làm Index.
    - Mã hóa (Encoding) biến phân loại hướng gió (`wd`) sang dạng số học (ví dụ sử dụng One-Hot Encoding).

## 6. Phân tích thống kê mô tả
- Tính toán và hiển thị các đại lượng thống kê cơ bản: Trung bình (Mean), Trung vị (Median), Min, Max, Độ lệch chuẩn cho `PM2.5` và các biến độc lập.
- Quan sát độ lệch (Skewness) để xem phân phối của mức PM2.5 có bị nghiêng mạnh (ví dụ nhiều ngày mức PM thấp và ít ngày mức PM cực cao) hay không.

## 7. Phát hiện ngoại lai (Outlier Detection)
*(Đáp ứng Yêu cầu kỹ thuật: Kiểm tra/phân tích ngoại lai)*
- Khảo sát sự tồn tại của các giá trị ngoại lai trong dữ liệu khí tượng (ví dụ: nhiệt độ quá cao/thấp bất thường) và dữ liệu ô nhiễm (nồng độ PM2.5 tăng vọt đột biến).
- **Phương pháp:** Sử dụng Boxplot hoặc IQR (Interquartile Range) để cô lập các ngoại lai. Cân nhắc giữ lại các giá trị PM2.5 cao vì đây có thể là các "cơn bão bụi" thực tế thay vì lỗi đo lường.

## 8. Trực quan hóa dữ liệu
*(Đáp ứng Yêu cầu kỹ thuật: Ít nhất 03 biểu đồ trực quan)*
Sẽ triển khai các biểu đồ bao gồm:
1. **Line Chart (Biểu đồ đường):** Thể hiện xu hướng biến động của nồng độ PM2.5 theo một khoảng thời gian nhất định (tháng/năm).
2. **Scatter Plot (Biểu đồ phân tán):** Phân tích tương quan giữa một biến khí tượng (VD: Tốc độ gió `WSPM` hoặc Nhiệt độ `TEMP`) so với biến `PM2.5`.
3. **Correlation Heatmap (Bản đồ nhiệt tương quan):** Thể hiện hệ số tương quan (Pearson) giữa tất cả các đặc trưng số để trực quan hóa đa biến.
4. **Histogram / Bar Chart (Tùy chọn thêm):** Biểu diễn phân phối tần suất của PM2.5.

## 9. Xây dựng mô hình / thuật toán
*(Đáp ứng Yêu cầu kỹ thuật: Ít nhất 01 bài toán mô hình hóa hoặc dự đoán)*
- **Xác định bài toán:** Dự báo/Hồi quy (Regression).
- **Chia tập dữ liệu:** Sử dụng kỹ thuật chia Train/Test phù hợp với chuỗi thời gian (ví dụ: dùng 80% dữ liệu ở các năm đầu làm Train, 20% dữ liệu ở năm cuối làm Test).
- **Thuật toán áp dụng:**
    - *Baseline Model:* Hồi quy tuyến tính (Linear Regression).
    - *Advanced Model:* Random Forest Regressor hoặc XGBoost Regressor nhằm xử lý tốt hơn mối quan hệ phi tuyến giữa thời tiết và chất ô nhiễm.

## 10. Đánh giá kết quả
*(Đáp ứng Yêu cầu kỹ thuật: Có đánh giá bằng độ đo phù hợp & Giải thích kết quả)*
- **Độ đo đánh giá (Metrics):** Sử dụng các độ đo chuẩn cho bài toán hồi quy:
    - **MAE (Mean Absolute Error):** Đo lường sai số tuyệt đối trung bình.
    - **MSE (Mean Squared Error) / RMSE:** Ưu tiên trừng phạt các sai số lớn.
    - **$R^2$ Score:** Xác định mô hình giải thích được bao nhiêu phần trăm sự biến thiên của dữ liệu.
- **Giải thích kết quả:** 
    - Phân tích "Feature Importance" (Mức độ quan trọng của đặc trưng) sinh ra từ mô hình Random Forest/XGBoost để lý giải nguyên nhân vật lý (ví dụ: Tốc độ gió cao thì bụi giảm, nồng độ CO cao thì PM2.5 tăng,...).
    - Không chỉ báo cáo các chỉ số MAE, MSE mà giải thích ý nghĩa thực tế (sai số này tương đương với lệch bao nhiêu $\mu g/m^3$).

## 11. Kết luận và hướng phát triển
- Đúc kết lại các yếu tố quan trọng nhất ảnh hưởng tới chất lượng không khí tại Aotizhongxin. Đánh giá ưu nhược điểm của mô hình được xây dựng.
- **Hướng phát triển:** 
    - Mở rộng phân tích kết hợp dữ liệu từ các trạm quan trắc khác trong khu vực Bắc Kinh.
    - Thử nghiệm các kiến trúc Deep Learning chuyên biệt cho chuỗi thời gian như LSTM (Long Short-Term Memory) hoặc GRU.

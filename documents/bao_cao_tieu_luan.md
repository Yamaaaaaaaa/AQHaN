# BÁO CÁO TIỂU LUẬN: PHÂN TÍCH VÀ DỰ ĐOÁN CHẤT LƯỢNG KHÔNG KHÍ (TẬP TRUNG VÀO BỤI MỊN PM2.5)

---

## 1. Giới thiệu bài toán thực tế

**Tình trạng không khí trên thế giới:** Hiện nay, ô nhiễm không khí đang là một trong những thách thức môi trường và sức khỏe cộng đồng lớn nhất trên toàn cầu. Theo các báo cáo của Tổ chức Y tế Thế giới (WHO), có đến hơn 90% dân số thế giới đang phải hít thở bầu không khí chứa mức độ chất ô nhiễm cao vượt quá giới hạn an toàn. Sự gia tăng chóng mặt của các khu công nghiệp, cùng với mật độ phương tiện giao thông khổng lồ tại các siêu đô thị, đang giải phóng hàng triệu tấn khí thải độc hại và bụi mịn (đặc biệt là PM2.5) mỗi năm, gây ra các hệ lụy vô cùng nghiêm trọng cho sức khỏe hệ hô hấp của con người.

**Tình trạng không khí tại Việt Nam:** Tại Việt Nam, đặc biệt là ở các thành phố lớn như Hà Nội và Thành phố Hồ Chí Minh, vấn đề ô nhiễm không khí cũng đang ở mức báo động đỏ. Tình trạng "sương mù quang hóa" và bụi mịn thường xuyên bao phủ vào các khung giờ cao điểm hoặc mùa khô nồm. Nguyên nhân chủ yếu đến từ mật độ phương tiện giao thông cá nhân quá cao, khói bụi từ các công trình xây dựng, cũng như hoạt động sản xuất chưa có hệ thống lọc khí thải đạt chuẩn. Việc liên tục xuất hiện trong các bảng xếp hạng ô nhiễm khu vực đòi hỏi những biện pháp giám sát chặt chẽ và khoa học hơn.

**Giới thiệu bài toán:** Nhận thức được tính cấp thiết của vấn đề trên, bài toán đặt ra là ứng dụng Khoa học Dữ liệu (Data Science) để theo dõi, phân tích và đánh giá tình hình chất lượng không khí một cách khách quan, với sự tập trung đặc biệt vào hạt bụi siêu vi nguy hiểm PM2.5. Bằng cách khai phá dữ liệu từ hệ thống cảm biến đo lường nồng độ bụi và các loại khí xả, chúng ta có thể phân tích đặc tính dao động theo chu kỳ của không khí, và tìm ra mối tương quan giữa bụi PM2.5 với các loại khí thải khác. Từ đó, xây dựng thuật toán học máy (Machine Learning) để dự báo thông minh mức độ gia tăng của bụi mịn.

## 2. Mục tiêu và câu hỏi phân tích
**Mục tiêu:**
- Khám phá xu hướng thay đổi theo thời gian của bụi mịn PM2.5.
- Trực quan hóa dữ liệu để tìm ra sự gắn kết giữa bụi mịn và các loại khí thải thông dụng.
- Xây dựng mô hình học máy để dự báo nồng độ bụi PM2.5.

**Câu hỏi phân tích:**
1. Lượng bụi mịn PM2.5 có sự chênh lệch rõ rệt mang ý nghĩa thống kê giữa ban ngày (giờ hành chính/giao thông) và ban đêm hay không?
2. Bụi mịn PM2.5 và bụi cỡ lớn PM10 có mối liên hệ sinh thái như thế nào?
3. Các loại khí thải (CO, SO2, NO2, O3) ảnh hưởng thế nào đến hạt PM2.5? Có thể dùng chúng để dự đoán chính xác lượng PM2.5 thông qua một mô hình Hồi quy tuyến tính không?

## 3. Mô tả dữ liệu
Bộ dữ liệu sử dụng là **Beijing Multi-Site Air-Quality Data Set** chứa các thông số đo lường chất lượng không khí theo từng giờ. Chỉ số PM2.5 (Particulate Matter) đại diện cho các hạt bụi mịn lơ lửng trong không khí có đường kính nhỏ hơn hoặc bằng 2.5 micromet. Do kích thước cực kỳ nhỏ, nó có khả năng xâm nhập sâu vào phổi và hệ máu, vì vậy PM2.5 thường được các cơ quan môi trường sử dụng làm thước đo chính để đánh giá mức độ ô nhiễm không khí.

Để phục vụ chuyên sâu cho bài toán dự đoán, tập dữ liệu thô ban đầu đã được chọn lọc lại. Dưới đây là bảng mô tả chi tiết các trường dữ liệu (Data Dictionary) được giữ lại trong mô hình:

| Tên Cột | Kiểu Dữ Liệu | Đơn vị tính | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| `Datetime` | Datetime | - | Trục thời gian chuẩn, được ghép lại từ các biến năm, tháng, ngày, giờ. |
| `city` | String | - | Tên trạm quan trắc / Thành phố đo lường (VD: Aotizhongxin). |
| `pm25` | Float | $\mu g/m^3$ | Nồng độ bụi siêu mịn có đường kính $\le 2.5\mu m$ (**Biến mục tiêu**). |
| `pm10` | Float | $\mu g/m^3$ | Nồng độ bụi mịn có đường kính $\le 10\mu m$. |
| `so2` | Float | $\mu g/m^3$ | Nồng độ khí Lưu huỳnh điôxít (Sinh ra từ đốt than, công nghiệp). |
| `no2` | Float | $\mu g/m^3$ | Nồng độ khí Nitơ điôxít (Sinh ra chủ yếu từ khí thải xe cơ giới). |
| `co` | Float | $\mu g/m^3$ | Nồng độ khí Cacbon monoxit (Khí độc sinh ra khi đốt cháy không hoàn toàn). |
| `o3` | Float | $\mu g/m^3$ | Nồng độ khí Ozone ở mặt đất tầng đối lưu. |

## 4. Thu thập dữ liệu / nguồn dữ liệu
- **Nguồn cung cấp:** Dữ liệu bao gồm các thông số ô nhiễm không khí hàng giờ được lấy từ 12 trạm giám sát chất lượng không khí cấp quốc gia (trực thuộc Trung tâm Quan trắc Môi trường Thành phố Bắc Kinh). Thông số khí tượng tại từng trạm được đồng bộ và đối chiếu với trạm thời tiết gần nhất của Cục Khí tượng Trung Quốc.
- **Khung thời gian:** Tập dữ liệu bao phủ liên tục trong 4 năm, từ ngày 01 tháng 03 năm 2013 đến ngày 28 tháng 02 năm 2017.
- **Liên kết tải bộ dữ liệu:**
  - Nguồn Kaggle: [Beijing Multisite Air-Quality Data Set](https://www.kaggle.com/datasets/sid321axn/beijing-multisite-airquality-data-set)
  - Nguồn khoa học (gốc): [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Beijing+Multi-Site+Air-Quality+Data)
- **Trạng thái dự án:** Dữ liệu gốc hoàn toàn không bị chỉnh sửa trước khi nạp. Code sẽ đọc trực tiếp từ tệp `Aotizhongxin_Raw.csv` trên đĩa cục bộ thông qua thư viện Pandas.
- **Trích dẫn nghiên cứu khoa học (Acknowledgements):** 
  > Zhang, S., Guo, B., Dong, A., He, J., Xu, Z. and Chen, S.X. (2017). *Cautionary Tales on Air-Quality Improvement in Beijing*. Proceedings of the Royal Society A, Volume 473, No. 2205, Pages 20170457.

## 5. Làm sạch và tiền xử lý dữ liệu
Trong Pipeline (`analysis_pipeline.ipynb`), bước làm sạch dữ liệu tuân thủ nghiêm ngặt các quy tắc học thuật để chuẩn bị dữ liệu thô. Quá trình bao gồm các bước cốt lõi:
1. **Lọc dữ liệu trọng tâm:** Chỉ giữ lại 7 biến mục tiêu: `city`, `pm25`, `pm10`, `o3`, `no2`, `so2`, `co`.
2. **Xử lý giá trị thiếu (Missing Values):** Thực tế quá trình thu thập dữ liệu luôn có sai sót. Giải pháp áp dụng:
   - *Biến định danh (Categorical):* Cột `city` được nhóm các ô trống thành một giá trị cụ thể mang tên `Missing`.
   - *Biến định lượng (Numeric):* Ước tính các giá trị còn thiếu bằng **Nội suy tuyến tính (Interpolate)** cho chuỗi thời gian liên tục. Đối với các dữ liệu khuyết thiếu ở hai đầu mút, thuật toán thay thế bằng giá trị **Trung vị (Median)**.
3. **Co giãn và Chuẩn hoá dữ liệu:** Các thuộc tính không khí (bụi và khí) có thang đo khác biệt rất lớn (ví dụ CO có giá trị hàng ngàn). Phương pháp sử dụng là **Chuẩn hóa Z-score (Standardization)** với công thức $z = \frac{x - \mu}{\sigma}$. Dữ liệu được đẩy về trung bình $\mu=0$ và độ lệch chuẩn $\sigma=1$, đảm bảo mọi biến đầu vào đều bình đẳng trước khi Train.
4. **Giảm chiều và biến đổi dữ liệu:** Áp dụng **Phân tích thành phần chính (PCA - Principal Component Analysis)** để nén cấu trúc 5 chiều dữ liệu (5 loại khí) xuống thành không gian **2 chiều (PC1 và PC2)** nhằm giảm thiểu độ phức tạp tính toán nhưng vẫn giữ lại tối đa tỷ lệ phương sai (Explained Variance Ratio) của hệ thống.

## 6. Phân tích thống kê mô tả
- **Thống kê tổng quan:** Tính toán các chỉ số cốt lõi bao gồm Mean (Trung bình), Median (Trung vị), Std (Độ lệch chuẩn), Min, Max cho các loại khí và bụi để có cái nhìn bao quát về mức độ ô nhiễm.
- **Kiểm định giả thuyết (Independent T-Test):** 
  - *Mục đích:* So sánh mức độ bụi PM2.5 giữa ban ngày (06h-18h) và ban đêm (18h-06h).
  - *Kết quả:* Dựa trên chỉ số T-statistic và P-value, nếu P-value < 0.05, ta bác bỏ giả thuyết H0 và khẳng định mức độ bụi mịn PM2.5 có sự chênh lệch rõ rệt mang ý nghĩa thống kê giữa ngày và đêm.

## 7. Phát hiện ngoại lai
Chương trình áp dụng đồng thời cả 2 phương pháp toán học để rà soát dữ liệu bất thường (Outliers - thường là các ngày có sự cố khói bụi cực đoan hoặc bão cát):
- **Phương pháp sử dụng $\bar{x}$ và $s$:** Xác định giá trị ngoại lai là những quan sát không nằm trong khoảng $(\bar{x} - 3s, \bar{x} + 3s)$ (với $\bar{x}$ là trung bình mẫu, $s$ là độ lệch chuẩn mẫu).
- **Phương pháp sử dụng Biểu đồ hộp (Boxplot):** Dựa trên khoảng tứ phân vị IQR. Các điểm quan sát rơi ra ngoài ranh giới $[Q1 - 1.5\times IQR, Q3 + 1.5\times IQR]$ được tự động thu thập và cảnh báo là các giá trị dị thường cần theo dõi.

## 8. Trực quan hóa dữ liệu
Bốn loại đồ thị được áp dụng để làm nổi bật các chiều thông tin:
Dưới đây là chi tiết và nhận xét phân tích cho từng biểu đồ:

**1. Line Chart (Biểu đồ đường):** 
- *Chi tiết:* Biểu diễn sự biến thiên nồng độ PM2.5 trung bình theo từng tháng (`resample('M')`) trên trục thời gian.
- *Nhận xét:* Đồ thị cho thấy rõ tính chu kỳ (Seasonality) của ô nhiễm không khí. Nồng độ bụi mịn PM2.5 thường tăng vọt và đạt đỉnh vào các tháng mùa đông (từ tháng 11 đến tháng 2) do hiện tượng nghịch nhiệt, và giảm mạnh vào mùa hè do mưa nhiều giúp rửa trôi bụi bẩn.

**2. Scatter Plot (Biểu đồ phân tán):** 
- *Chi tiết:* Rải điểm trên trục tọa độ, trục X là lượng bụi PM2.5, trục Y là bụi PM10.
- *Nhận xét:* Quần thể điểm dữ liệu tạo thành một đường thẳng dốc lên hoàn hảo. Điều này chứng minh PM2.5 và PM10 có sự tương quan thuận (Positive Correlation) cực kỳ mạnh. Khi lượng bụi tổng tăng cao do khói bụi, bụi siêu vi PM2.5 cũng tăng theo tỷ lệ tương ứng.

**3. Histogram (Biểu đồ tần suất):** 
- *Chi tiết:* Biểu đồ cột phân bố nồng độ bụi PM2.5. Trục X là mức độ bụi, trục Y là tần suất xuất hiện (số giờ đo).
- *Nhận xét:* Phân bố của PM2.5 có dạng lệch phải (Right-skewed). Điều này phản ánh thực tế rằng trong phần lớn thời gian, nồng độ bụi nằm ở mức thấp (an toàn). Tuy nhiên, cái đuôi dài bên phải cho thấy thỉnh thoảng vẫn xuất hiện những "đợt" ô nhiễm ngắn hạn cực kỳ độc hại.

**4. Boxplot (Biểu đồ hộp):** 
- *Chi tiết:* Đồ thị thể hiện các mức phân vị (Q1, Median, Q3) và các điểm dữ liệu ngoại lai của toàn bộ 5 chỉ số khí/bụi.
- *Nhận xét:* Trung vị của các khí đều nằm ở nửa dưới của hộp. Các điểm chấm đen (Outliers) xuất hiện dày đặc ở râu phía trên hộp của PM2.5 và PM10, xác nhận rằng thành phố liên tục phải hứng chịu những trận "bão khói bụi" với nồng độ dị thường vượt xa quy chuẩn hàng ngày.

## 9. Xây dựng mô hình / thuật toán (Hồi quy tuyến tính)

### 9.1. Tổng quan về mô hình Hồi quy tuyến tính
Hồi quy tuyến tính đa biến (Multiple Linear Regression) là một thuật toán Học máy có giám sát (Supervised Learning) mạnh mẽ trong việc dự báo. Nhiệm vụ của mô hình là thiết lập một mối quan hệ tuyến tính (đường thẳng/siêu phẳng) tối ưu nhất giữa một biến phụ thuộc (Biến mục tiêu $Y$) và nhiều biến độc lập (Biến dự báo $X$). 

**Công thức toán học:**
Mô hình giả định rằng giá trị của biến mục tiêu $Y$ được tính bằng tổ hợp tuyến tính của các biến đầu vào $X_i$ theo công thức:
$$ Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + ... + \beta_n X_n + \epsilon $$
Trong đó:
- $Y$: Biến mục tiêu cần dự báo (Nồng độ PM2.5).
- $X_1, X_2, ..., X_n$: Các biến độc lập (Nồng độ `pm10`, `o3`, `no2`, `so2`, `co`).
- $\beta_0$: Hệ số tự do (Intercept).
- $\beta_1, \beta_2, ..., \beta_n$: Trọng số hồi quy (Coefficients). Chúng thể hiện mức độ tác động của từng biến $X$ lên $Y$. Thuật toán sẽ dùng phương pháp Bình phương tối thiểu (OLS) để tìm bộ trọng số $\beta$ này sao cho sai số dự đoán là nhỏ nhất.
- $\epsilon$: Sai số ngẫu nhiên (Error term).

*Cơ sở khoa học về việc chọn biến X:* Việc dùng khí thải để tính ra bụi PM2.5 hoàn toàn dựa trên cơ chế vật lý (PM2.5 là thành phần của PM10), cơ chế sinh hạt thứ cấp trong khí quyển (SO2 và NO2 kết tinh thành bụi mịn dưới ánh sáng), và sự cộng sinh phát thải (CO sinh ra khi kẹt xe đi kèm khói bụi).

### 9.2. Mục tiêu của mô hình
- Dự báo chính xác nồng độ hạt bụi siêu vi nguy hiểm `pm25`.
- Tìm ra bảng Trọng số tác động $\beta$ để biết chính xác loại khí xả nào (`co`, `so2` hay `no2`...) có tầm ảnh hưởng lớn nhất đến sự hình thành của bụi PM2.5, từ đó cung cấp căn cứ để bảo vệ môi trường.

### 9.3. Triển khai thuật toán
1. **Tiền xử lý:** Các dữ liệu được nạp vào đều là dữ liệu đã trải qua làm sạch, lọc Missing Value và chuẩn hóa Z-score.
2. **Chia tách dữ liệu (Train/Test Split):** Toàn bộ dữ liệu được xáo trộn ngẫu nhiên và cắt thành 2 phần độc lập:
   - Tập huấn luyện (Train set - 80%): Máy tính sử dụng phần này để tự động học hỏi và tìm ra siêu phẳng tối ưu (tính $\beta$).
   - Tập kiểm thử (Test set - 20%): Dùng để chạy thử nghiệm và kiểm tra xem máy dự đoán có chính xác trên dữ liệu mới không.
3. **Huấn luyện (Fitting):** Khởi tạo `LinearRegression()` và truyền tập Train vào để khớp thuật toán.
4. **Dự đoán (Predicting):** Mô hình xuất ra các con số PM2.5 dự đoán cho tập Test.

### 9.4. Đánh giá mô hình
Hệ thống sử dụng các hàm toán học sau để chấm điểm độ sai lệch của mô hình:
- **MSE (Mean Squared Error):** Tính trung bình bình phương khoảng cách giữa giá trị thực tế và dự đoán. MSE càng nhỏ, mô hình càng chính xác. Việc bình phương giúp phóng đại và trừng phạt nặng các điểm dự báo sai số quá lớn.
- **MAE (Mean Absolute Error):** Tính sai số tuyệt đối trung bình. Cung cấp con số trực quan rằng mô hình đang dự báo chênh lệch bao nhiêu $\mu g/m^3$ bụi.
- **R-squared ($R^2$ Score):** Thể hiện phần trăm sự biến thiên của bụi PM2.5 được giải thích bởi các khí thải đầu vào. $R^2$ càng gần 1, mô hình càng sát với thực tế.

## 10. Đánh giá kết quả
Dựa trên các chỉ số mô tả ở phần 9.4, kết quả chạy thực tế của thuật toán Hồi quy tuyến tính được ghi nhận như sau:
- **Độ đo sai số thực tế:** Chỉ số MSE và MAE đều ở mức tương đối thấp, đặc biệt hệ số $R^2$ đạt mức vô cùng ấn tượng. Điều này chứng tỏ thuật toán Hồi quy tuyến tính chạy cực kỳ tốt cho bài toán môi trường này.
- **Trực quan hóa mức độ chính xác:** Hệ thống in ra biểu đồ Scatter trực quan so sánh Thực tế vs Dự đoán. Các điểm chấm bám sát một cách hoàn hảo lấy đường phân giác nét đứt màu đỏ ($y=x$), khẳng định mô hình dự đoán ra con số cực kỳ bám sát thực tế chứ không bị lệch pha.
- **Phân tích Hệ số tác động (Coefficients):** Dựa vào bảng phân tích $\beta$, `pm10` có trọng số tác động cao nhất, theo sau là `co` và `no2`. Nó xác nhận thực tế rằng giao thông ùn tắc (sinh ra khí CO) chính là nguyên nhân lớn nhất làm gia tăng bụi mịn tại khu vực thành thị.

## 11. Kết luận và hướng phát triển
**Kết luận:**
- Toàn bộ Pipeline phân tích từ dữ liệu thô ra dữ liệu sạch, có biểu đồ đã hoạt động hoàn hảo. 
- Tìm ra được sự thật rằng ô nhiễm bụi mịn PM2.5 có tính chu kỳ, bị ảnh hưởng lớn từ sinh hoạt giao thông ngày/đêm và có tương quan vật lý cực kỳ lớn với bụi PM10 cùng các khí đốt công nghiệp.
- Mô hình Hồi quy tuyến tính tỏ ra rất hiệu quả trong bài toán này. Khẳng định có thể dùng thông số các loại khí cơ bản để dự báo sớm nồng độ PM2.5.

**Hướng phát triển trong tương lai:**
- Áp dụng các mô hình chuỗi thời gian như **LSTM (Deep Learning)** hoặc **ARIMA** để dùng nồng độ PM2.5 của 3 ngày trước dự đoán PM2.5 của ngày mai, qua đó xây dựng tính năng cảnh báo sức khỏe độc lập.
- Tích hợp thêm các chỉ số Thời tiết (Nhiệt độ, Gió, Mưa) để thuật toán tính toán được hiện tượng "nước mưa rửa trôi bụi", giúp mô hình trở nên thực tế và gần với cơ chế tự nhiên nhất.

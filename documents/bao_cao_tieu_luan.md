# BÁO CÁO TIỂU LUẬN: MÔ HÌNH HỌC MÁY DỰ BÁO NỒNG ĐỘ BỤI MỊN PM2.5 TẠI TRẠM AOTIZHONGXIN

**Học phần:** Nhập môn Khoa học Dữ liệu  
**Dữ liệu sử dụng:** `Aotizhongxin_Raw.csv`  
**Bài toán:** Hồi quy (Regression)

---

## 1. Giới thiệu bài toán thực tế
**Về ô nhiễm không khí nói chung:**
Ô nhiễm không khí, đặc biệt là sự gia tăng nồng độ bụi mịn PM2.5, đang là một trong những hiểm họa môi trường nguy hiểm nhất. Những hạt bụi này có đường kính cực nhỏ ($\le 2.5 \mu m$), có khả năng xâm nhập sâu vào hệ hô hấp và đi thẳng vào mạch máu, gây ra hàng loạt các bệnh lý nghiêm trọng về tim mạch, phổi và làm giảm tuổi thọ con người.

**Tình trạng không khí trên thế giới:**
Hiện nay, ô nhiễm không khí đang là một trong những thách thức môi trường và sức khỏe cộng đồng lớn nhất trên toàn cầu. Theo các báo cáo của Tổ chức Y tế Thế giới (WHO), có đến hơn 90% dân số thế giới đang phải hít thở bầu không khí chứa mức độ chất ô nhiễm cao vượt quá giới hạn an toàn. Sự gia tăng chóng mặt của các khu công nghiệp, cùng với mật độ phương tiện giao thông khổng lồ tại các siêu đô thị, đang giải phóng hàng triệu tấn khí thải độc hại và bụi mịn (đặc biệt là PM2.5) mỗi năm, gây ra các hệ lụy vô cùng nghiêm trọng cho sức khỏe hệ hô hấp của con người.

**Tình trạng không khí tại Việt Nam:**
Tại Việt Nam, đặc biệt là ở các thành phố lớn như Hà Nội và Thành phố Hồ Chí Minh, vấn đề ô nhiễm không khí cũng đang ở mức báo động đỏ. Tình trạng "sương mù quang hóa" và bụi mịn thường xuyên bao phủ vào các khung giờ cao điểm hoặc mùa khô nồm. Nguyên nhân chủ yếu đến từ mật độ phương tiện giao thông cá nhân quá cao, khói bụi từ các công trình xây dựng, cũng như hoạt động sản xuất chưa có hệ thống lọc khí thải đạt chuẩn. Việc liên tục xuất hiện trong các bảng xếp hạng ô nhiễm khu vực đòi hỏi những biện pháp giám sát chặt chẽ và khoa học hơn.

**Bài toán đặt ra:**
Nhận thức được tính cấp thiết của vấn đề trên, bài toán đặt ra là ứng dụng Khoa học Dữ liệu (Data Science) để theo dõi, phân tích và đánh giá tình hình chất lượng không khí một cách khách quan, với sự tập trung đặc biệt vào hạt bụi siêu vi nguy hiểm PM2.5. Bằng cách khai phá dữ liệu từ hệ thống cảm biến đo lường nồng độ bụi và các loại khí xả, chúng ta có thể phân tích đặc tính dao động theo chu kỳ của không khí, và tìm ra mối tương quan giữa bụi PM2.5 với các loại khí thải khác. Từ đó, xây dựng thuật toán học máy (Machine Learning) để dự báo thông minh mức độ gia tăng của bụi mịn.

Lấy cảm hứng từ thực trạng trên, đồ án này sử dụng tập dữ liệu tại trạm quan trắc Aotizhongxin (Bắc Kinh - một trong những siêu đô thị từng ô nhiễm nhất thế giới) làm trường hợp nghiên cứu (Case study) điển hình. Dựa vào các thông số khí tượng (nhiệt độ, áp suất, độ ẩm, sức gió...) và nồng độ các chất ô nhiễm khác (SO2, NO2, CO, O3), bài toán yêu cầu xây dựng mô hình học máy để dự báo chính xác nồng độ bụi mịn PM2.5. Việc giải quyết bài toán này không chỉ hỗ trợ thiết lập hệ thống cảnh báo y tế sớm để bảo vệ sức khỏe cộng đồng ở các ngày "bão bụi", mà phương pháp học máy này còn hoàn toàn có thể ứng dụng trực tiếp vào việc dự báo tình trạng ô nhiễm không khí đang rất nhức nhối tại các thành phố lớn của Việt Nam hiện nay.

## 2. Mục tiêu và câu hỏi phân tích
- **Mục tiêu tổng quát:** Áp dụng toàn diện quy trình Khoa học Dữ liệu (Data Science Pipeline) để trích xuất tri thức từ bộ dữ liệu thô. Các mục tiêu cụ thể bao gồm:
  1. **Làm sạch và tiền xử lý dữ liệu:** Xử lý triệt để các giá trị khuyết thiếu bằng phương pháp nội suy, phát hiện và xử lý các điểm dữ liệu ngoại lai (outliers) nhằm chuẩn bị một tập dữ liệu chất lượng cao.
  2. **Phân tích Khám phá Dữ liệu (EDA):** Sử dụng các kỹ thuật thống kê và trực quan hóa (biểu đồ) để tìm ra quy luật phân bố, tính chu kỳ và đo lường mức độ tương quan giữa các yếu tố khí hậu với sự biến động của PM2.5.
  3. **Xây dựng Mô hình Học máy (Machine Learning):** Huấn luyện các thuật toán Hồi quy (Regression) từ cơ bản đến nâng cao để dự báo mức độ ô nhiễm, qua đó đánh giá độ tin cậy và trích xuất ra các đặc trưng quan trọng nhất (Feature Importance) quyết định nồng độ bụi mịn.
- **Câu hỏi phân tích:**
  1. Nồng độ PM2.5 có tính chu kỳ và thay đổi như thế nào theo thời gian (tháng/năm)?
  2. Các yếu tố khí tượng (nhiệt độ, lượng mưa, tốc độ gió) tác động ra sao đến việc gia tăng hay suy giảm PM2.5?
  3. Các loại khí thải công nghiệp/giao thông (CO, NO2, SO2) có mối tương quan như thế nào với bụi mịn?

## 3. Mô tả dữ liệu
Tập dữ liệu đầu vào chứa toàn bộ các thông số môi trường được quan trắc tại trạm Aotizhongxin trong giai đoạn 4 năm, kéo dài từ **ngày 01/03/2013 đến hết ngày 28/02/2017**. Dữ liệu được thu thập liên tục với tần suất **1 giờ/lần** (mỗi giờ hệ thống sẽ đo đạc và lưu lại 1 bản ghi mới). Tổng cộng, bộ dữ liệu bao gồm 35,064 bản ghi và 18 biến đặc trưng như sau:
| Nhóm Đặc Trưng | Tên Biến | Ý Nghĩa / Mô Tả | Đơn vị / Phân loại |
| :--- | :--- | :--- | :--- |
| **Thời gian** | `year`, `month`, `day`, `hour` | Thời điểm ghi nhận dữ liệu | Thời gian |
| **Biến mục tiêu** | `PM2.5` | Nồng độ hạt bụi mịn (kích thước $\le 2.5 \mu m$) | $\mu g/m^3$ |
| **Chất ô nhiễm** | `PM10` | Nồng độ hạt bụi (kích thước $\le 10 \mu m$) | $\mu g/m^3$ |
| **Chất ô nhiễm** | `SO2` | Nồng độ Lưu huỳnh Đioxit | $\mu g/m^3$ |
| **Chất ô nhiễm** | `NO2` | Nồng độ Nitơ Đioxit | $\mu g/m^3$ |
| **Chất ô nhiễm** | `CO` | Nồng độ Carbon Monoxit | $\mu g/m^3$ |
| **Chất ô nhiễm** | `O3` | Nồng độ Ozone | $\mu g/m^3$ |
| **Khí tượng** | `TEMP` | Nhiệt độ môi trường | $^\circ C$ |
| **Khí tượng** | `PRES` | Áp suất khí quyển | hPa |
| **Khí tượng** | `DEWP` | Điểm sương (Dew Point) | $^\circ C$ |
| **Khí tượng** | `RAIN` | Lượng mưa | mm |
| **Khí tượng** | `wd` | Hướng gió | Biến phân loại |
| **Khí tượng** | `WSPM` | Tốc độ gió | m/s |

## 4. Thu thập dữ liệu / Nguồn dữ liệu
- **Nguồn dữ liệu:** Được lấy từ nền tảng Kaggle, bộ dữ liệu công khai "Beijing Multi-Site Air-Quality Data" (tổng hợp từ Đại học Bắc Kinh / UCI Machine Learning Repository).
- **Đường dẫn (URL):** [https://www.kaggle.com/datasets/sid321axn/beijing-multisite-airquality-data-set](https://www.kaggle.com/datasets/sid321axn/beijing-multisite-airquality-data-set)
- **Cách thức:** Tải trực tiếp dưới dạng tệp tin `Aotizhongxin_Raw.csv` chứa dữ liệu thô (raw data) và lưu trữ nguyên bản trên ổ đĩa nội bộ để tiến hành phân tích.

## 5. Làm sạch và tiền xử lý dữ liệu

### 5.1. Xử lý giá trị thiếu (Missing Values)
- **Cơ sở lý thuyết:** Dữ liệu cảm biến đo theo thời gian thực thường bị khuyết (NaN) do sự cố máy móc. Với dữ liệu dạng chuỗi thời gian (Time-series), nếu xóa bỏ dòng bị thiếu sẽ làm gãy tính liên tục của thời gian. Phương pháp tối ưu là **Nội suy tuyến tính (Linear Interpolation)**.
- **Công thức nội suy tuyến tính:** 
  Dự đoán giá trị $y$ tại thời điểm $x$ dựa trên hai điểm liền kề $(x_1, y_1)$ và $(x_2, y_2)$:
  $$ y = y_1 + (x - x_1) \frac{y_2 - y_1}{x_2 - x_1} $$
- **Triển khai:** 
  - Gộp 4 cột `year, month, day, hour` thành cột `datetime` và gán làm Index.
  - Biến phân loại `wd` (hướng gió) có khuyết thiếu được điền bằng giá trị xuất hiện nhiều nhất (Mode).
  - Các biến số (TEMP, PRES, PM2.5...) sử dụng hàm `df.interpolate(method='time')`.
- **Kết quả:** Xử lý triệt để hàng ngàn giá trị khuyết (ví dụ: PM2.5 thiếu 925 dòng, CO thiếu 1776 dòng) đưa tập dữ liệu về trạng thái sạch (0 null) mà vẫn giữ được xu hướng tự nhiên.

### 5.2. Chuẩn hóa dữ liệu (Feature Scaling)
- **Cơ sở lý thuyết:** Các biến như Áp suất (PRES ~ 1000) và Tốc độ gió (WSPM ~ 1.5) có thang đo hoàn toàn khác biệt. Các mô hình dựa trên khoảng cách hoặc hồi quy tuyến tính sẽ bị hội tụ chậm và sai lệch nếu không chuẩn hóa.
- **Công thức (Standard Scaler / Z-score Normalization):**
  $$ z = \frac{x - \mu}{\sigma} $$
  *(Trong đó $\mu$ là trung bình và $\sigma$ là độ lệch chuẩn của tập dữ liệu).*
- **Triển khai:** Sử dụng `StandardScaler` của thư viện `scikit-learn` để chuẩn hóa toàn bộ tập `X_train` và `X_test` cho mô hình Linear Regression.

## 6. Phân tích thống kê mô tả
- **Cơ sở lý thuyết:** Sử dụng các độ đo xu hướng tập trung (Mean, Median) và phân tán (Std, Min, Max) để có cái nhìn tổng quan về đặc tính phân phối của dữ liệu.
- **Công thức:**
  - Trung bình (Mean): $\mu = \frac{1}{N} \sum_{i=1}^{N} x_i$
  - Phương sai (Variance): $\sigma^2 = \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \mu)^2$
- **Triển khai:** Do yêu cầu không sử dụng hàm `df.describe()`, một vòng lặp `for` duyệt qua từng cột số học đã được viết để tính toán thủ công từng đại lượng `mean(), median(), min(), max(), std()` và lưu vào một DataFrame thống kê.
- **Kết quả:** Thống kê cho thấy PM2.5 có mức trung bình $\approx 82.5 \mu g/m^3$, nhưng giá trị lớn nhất (Max) lên tới $898 \mu g/m^3$. Độ lệch chuẩn $\sigma \approx 81.9$ cực lớn cho thấy sự biến động dữ dội của bụi mịn và sự tồn tại của các đợt ô nhiễm khốc liệt.

## 7. Phát hiện ngoại lai (Outliers)
- **Cơ sở lý thuyết:** 
  - **Khái niệm Ngoại lai (Outliers):** Ngoại lai là những điểm dữ liệu có giá trị chênh lệch một cách cực đoan (cao bất thường hoặc thấp bất thường) so với phần lớn các quan sát còn lại trong cùng một tập dữ liệu.
  - **Vì sao cần phát hiện ngoại lai?** Ngoại lai có thể xuất phát từ sai số đo lường (như cảm biến lỗi) hoặc từ các sự kiện vật lý có thật nhưng hiếm gặp (như đợt bão bụi khốc liệt). Việc để lọt ngoại lai có thể làm méo mó nghiêm trọng các tham số thống kê cơ bản (như giá trị trung bình) và đặc biệt làm suy giảm hiệu năng của các mô hình học máy nhạy cảm với nhiễu (ví dụ: Hồi quy tuyến tính), do thuật toán sẽ cố gắng "bẻ cong" đường dự báo để khớp với các điểm bất thường này. Do đó, bước phát hiện ngoại lai là vô cùng quan trọng để hiểu đặc tính tập dữ liệu và quyết định phương pháp xử lý phù hợp nhằm tối ưu chất lượng mô hình.
  - **Phương pháp sử dụng IQR:** Để định lượng và cô lập một cách toán học các điểm ngoại lai này, phương pháp trực quan và hiệu quả nhất là sử dụng biểu đồ Hộp (Boxplot) kết hợp với dải phân vị (Interquartile Range - IQR).
- **Công thức IQR:**
  $$ IQR = Q_3 - Q_1 $$
  $$ \text{Upper Bound} = Q_3 + 1.5 \times IQR $$
- **Triển khai:** 
  Tính toán $Q_1 = 22.0$, $Q_3 = 114.0 \Rightarrow IQR = 92.0$.
  Ngưỡng bất thường (Upper Bound) $= 114 + 1.5 \times 92 = 252.0 \mu g/m^3$.
  Có $1,653$ bản ghi vượt ngưỡng này.
- **Kết quả & Quyết định phân tách:** 
  Do PM2.5 tăng vọt là **hiện tượng vật lý có thật** (Bão bụi mùa đông) chứ không phải do lỗi máy đo, việc xóa ngoại lai sẽ làm mô hình "mù" trước các đợt ô nhiễm nặng. Hệ quả là tập dữ liệu được tách thành hai phần:
  1. **Tập loại bỏ ngoại lai ($PM2.5 \le 252.0$):** Dành để train mô hình Linear Regression (vốn nhạy cảm với nhiễu).
  2. **Tập giữ nguyên ngoại lai:** Dành để train Random Forest (thuật toán miễn nhiễm với ngoại lai).

## 8. Trực quan hóa dữ liệu
- **Cơ sở lý thuyết:** Sử dụng đồ thị để nhận dạng xu hướng (Trend) và sự tương quan (Correlation) giữa các biến. 
- **Công thức Hệ số tương quan Pearson:**
  $$ r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}} $$
- **Triển khai & Kết quả:**
  1. **Line Chart (Biểu đồ đường):** Thể hiện xu hướng nồng độ PM2.5 trung bình theo từng tháng. Quan sát biểu đồ, ta thấy rõ tính chu kỳ biến động theo mùa: Các đỉnh ô nhiễm tồi tệ nhất (lên tới $140 - 150 \mu g/m^3$) luôn rơi vào các tháng mùa đông (quanh mốc tháng 1 hàng năm). Ngược lại, vào mùa hè (tháng 6 đến tháng 8), nồng độ PM2.5 chạm "đáy". Điều này phản ánh thực tế nhu cầu đốt than sưởi ấm gia tăng mạnh vào mùa đông tại Bắc Kinh, kết hợp với hiện tượng nghịch nhiệt độ làm giam giữ khói bụi ở tầm thấp.
  2. **Scatter Plot (Biểu đồ phân tán):** Phân tích mối quan hệ giữa Nhiệt độ (`TEMP`) và nồng độ `PM2.5`. Biểu đồ biểu diễn một mây điểm tập trung rất dày đặc và vươn lên những đỉnh cực kỳ cao (có thể chạm tới $800-900 \mu g/m^3$) ở dải nhiệt độ thấp (từ $-10^\circ C$ đến $10^\circ C$). Ở chiều ngược lại, khi thời tiết nóng dần lên trên $20^\circ C$, nồng độ PM2.5 hiếm khi vượt quá $200 \mu g/m^3$. Điều này củng cố thêm nhận định rằng thời tiết giá rét tạo điều kiện cực kỳ thuận lợi cho sự tích tụ của hạt bụi mịn.
  3. **Correlation Heatmap (Ma trận tương quan):** Thể hiện hệ số tương quan Pearson giữa toàn bộ các biến số học. 
     - **Tương quan dương mạnh:** Nổi bật nhất là sự đồng biến rất cao giữa PM2.5 với PM10 ($r = 0.88$), CO ($r = 0.79$), và NO2 ($r = 0.68$). Bằng chứng này khẳng định bụi mịn và các khí thải này được sinh ra từ cùng một nguồn gốc phát thải (khí thải công nghiệp và phương tiện giao thông).
     - **Tương quan âm:** Tốc độ gió (`WSPM`) có tương quan nghịch lớn nhất với PM2.5 ($r = -0.28$). Xét về mặt vật lý, gió càng mạnh thì bụi mịn càng dễ bị thổi bay và khuếch tán ra xa, giúp làm sạch không khí tại trạm đo.

## 9. Xây dựng mô hình / Thuật toán

Trong đồ án này, chúng ta tiếp cận bài toán dự báo bằng hai phương pháp mang tính đối lập nhau để so sánh hiệu quả: một mô hình tham số cơ bản (Linear Regression) và một mô hình phi tham số phức tạp (Random Forest).

### 9.1. Mô hình Hồi quy Tuyến tính (Linear Regression)
- **Cơ sở lý thuyết:** Hồi quy tuyến tính là một thuật toán thống kê, giả định rằng tồn tại một mối quan hệ tuyến tính (đường thẳng hoặc siêu phẳng) giữa biến mục tiêu (PM2.5) và các biến đặc trưng đầu vào (Nhiệt độ, CO, Tốc độ gió,...). Thuật toán này sử dụng phương pháp **Bình phương tối thiểu thông thường (Ordinary Least Squares - OLS)**, cố gắng tìm ra một siêu phẳng sao cho tổng bình phương của các sai số (khoảng cách từ các điểm dữ liệu thực tế đến mặt phẳng dự báo) là nhỏ nhất.
- **Ưu và nhược điểm:** 
  - *Ưu điểm:* Thuật toán rất đơn giản, tốc độ huấn luyện nhanh và có tính diễn giải cao (hiểu rõ tác động của từng biến qua các hệ số trọng số).
  - *Nhược điểm:* Bị giới hạn bởi giả định quan hệ tuyến tính. Đặc biệt, phương pháp OLS cực kỳ nhạy cảm với các điểm ngoại lai (Outliers); một vài điểm nhiễu có độ lệch lớn có thể kéo lệch toàn bộ đường hồi quy làm sai số mô hình tăng vọt.
- **Công thức:** 
  $$ \hat{y} = w_0 + w_1 x_1 + w_2 x_2 + ... + w_n x_n $$
  *(Trong đó: $\hat{y}$ là giá trị dự báo, $w_0$ là hệ số chênh lệch/intercept, $w_1...w_n$ là các trọng số tương ứng với từng đặc trưng $x_1...x_n$)*
- **Triển khai:** 
  - Trước tiên, toàn bộ dữ liệu đầu vào được chuẩn hóa bằng `StandardScaler` để đưa các biến có thang đo hoàn toàn khác biệt (như Áp suất $\sim 1000$ hPa và Lượng mưa $\sim 0$ mm) về cùng một phân phối chuẩn, giúp hàm mục tiêu hội tụ mượt mà và chính xác.
  - Sau đó, mô hình được huấn luyện (Train) **chỉ trên Tập dữ liệu đã xóa ngoại lai** ($PM2.5 \le 252.0 \mu g/m^3$) nhằm đảm bảo mặt phẳng hồi quy không bị bóp méo bởi các đợt bão bụi dị biệt.

### 9.2. Mô hình Rừng Ngẫu nhiên (Random Forest Regressor)
- **Cơ sở lý thuyết:** Random Forest là một thuật toán **Học tập tập hợp (Ensemble Learning)** vô cùng mạnh mẽ. Thay vì chỉ phụ thuộc vào một mô hình duy nhất, nó xây dựng một "khu rừng" bao gồm hàng trăm **Cây quyết định (Decision Trees)** hoạt động độc lập. Thuật toán này ứng dụng kỹ thuật **Bagging (Bootstrap Aggregating)**, nghĩa là mỗi cây quyết định sẽ được huấn luyện trên một tập con dữ liệu lấy mẫu ngẫu nhiên (có hoàn lại) và một tập con các đặc trưng ngẫu nhiên. Khi dự báo, kết quả cuối cùng sẽ được tổng hợp lại từ tất cả các cây trong rừng đó.
- **Ưu và nhược điểm:**
  - *Ưu điểm:* Khả năng nắm bắt các mối quan hệ phi tuyến tính vô cùng phức tạp. Vì bản chất của cây quyết định là chia cắt không gian (splitting) dựa trên các ngưỡng, thuật toán này hoàn toàn **không cần bước chuẩn hóa dữ liệu (Scaling)** và **vô cùng miễn nhiễm (robust) trước các nhiễu hay điểm ngoại lai**. Ngoài ra, nó cung cấp sẵn thuộc tính Feature Importance để trích xuất độ quan trọng của từng biến.
  - *Nhược điểm:* Tốn nhiều tài nguyên RAM và thời gian huấn luyện hơn, đồng thời mang tính "hộp đen" (Black-box) nên rất khó diễn giải logic bên trong hơn Linear Regression.
- **Công thức:** Kết quả dự báo là trung bình cộng giá trị dự báo của $K$ cây quyết định:
  $$ \hat{y} = \frac{1}{K} \sum_{k=1}^{K} f_k(x) $$
- **Triển khai:** Khác biệt hoàn toàn với mô hình Hồi quy tuyến tính, Random Forest được đưa vào huấn luyện trên **Tập dữ liệu gốc (giữ nguyên 100% các điểm ngoại lai)**. Thuật toán được thiết lập tham số `n_estimators=100` (xây dựng 100 cây quyết định độc lập). Chiến lược triển khai này dựa trên các lập luận sau:
  1. **Bản chất của ngoại lai trong bài toán:** Nồng độ PM2.5 tăng đột biến lên mức hàng trăm $\mu g/m^3$ không phải là lỗi cảm biến, mà là các thảm họa môi trường có thật (như bão bụi, nghịch nhiệt mùa đông). Nếu xóa bỏ chúng, mô hình sẽ hoàn toàn "mù" trước các ngày ô nhiễm nặng nhất - thời điểm mà hệ thống cảnh báo y tế cần phát huy tác dụng nhất.
  2. **Cơ chế cô lập ngoại lai:** Nhờ nguyên lý chia nhánh (splitting) thay vì cố khớp một phương trình liên tục, các cây quyết định trong Random Forest sẽ tự động phân lập các điểm ô nhiễm cực đoan này vào những "nút lá" (leaf nodes) sâu riêng biệt, dựa trên các điều kiện thời tiết đặc thù lúc đó (ví dụ: nhiệt độ cực thấp kết hợp gió lặng). Nhờ đó, sự tồn tại của ngoại lai không hề làm kéo lệch (skew) hay méo mó dự báo của mô hình ở những ngày không khí trong lành.
  3. **Sức mạnh của số đông (`n_estimators=100`):** Việc tạo ra 100 cây quyết định trên các bộ dữ liệu lấy mẫu ngẫu nhiên (Bagging) giúp thuật toán triệt tiêu hiện tượng học vẹt (Overfitting). Trong khu rừng này, một số cây sẽ chuyên học quy luật của ngày bình thường, trong khi một số cây khác (do vô tình lấy mẫu trúng nhiều điểm ngoại lai) sẽ trở thành "chuyên gia" nhận diện bão bụi. Khi lấy trung bình cộng dự báo của cả 100 cây, ta thu được một mô hình có bức tranh toàn cảnh: vừa cực kỳ ổn định, vừa có sức mạnh nội tại để dự báo chính xác các đỉnh ô nhiễm tồi tệ nhất.

## 10. Đánh giá kết quả
Do đây là bài toán Hồi quy (Regression) nhằm dự báo một biến số liên tục (nồng độ PM2.5), chúng thực tế không thể sử dụng độ đo Accuracy (Độ chính xác) như trong bài toán Phân lớp. Thay vào đó, mô hình được đánh giá thông qua 4 độ đo chuyên dụng sau:

### 10.1. Mean Absolute Error (MAE) - Sai số tuyệt đối trung bình
- **Ý nghĩa:** MAE đo lường khoảng cách sai lệch trung bình giữa giá trị dự báo của mô hình và giá trị thực tế. Đơn vị của MAE cùng với đơn vị của biến mục tiêu ($\mu g/m^3$). MAE càng nhỏ chứng tỏ mô hình dự báo càng sát với thực tế. Điểm đặc trưng của MAE là nó đối xử công bằng với tất cả các sai số (không phạt nặng sai số lớn).
- **Công thức:**
  $$ MAE = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i| $$

### 10.2. Mean Squared Error (MSE) - Sai số toàn phương trung bình
- **Ý nghĩa:** MSE đo lường trung bình của bình phương các sai số. Việc bình phương này khiến cho các sai số lớn bị khuếch đại lên rất nhiều, do đó mô hình sẽ bị "phạt nặng" nếu có những dự báo trượt quá xa thực tế. Điểm yếu của MSE là đơn vị của nó cũng bị bình phương (ví dụ: $(\mu g/m^3)^2$), khiến nó khó diễn giải trực tiếp so với biến gốc.
- **Công thức:**
  $$ MSE = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2 $$

### 10.3. Root Mean Squared Error (RMSE) - Căn bậc hai sai số toàn phương trung bình
- **Ý nghĩa:** RMSE chính là căn bậc hai của MSE. Việc lấy căn bậc hai giúp đưa đơn vị của sai số về lại cùng hệ quy chiếu với biến mục tiêu ($\mu g/m^3$), giúp ta dễ hình dung mức độ sai lệch hơn. Tương tự MSE, RMSE cũng trừng phạt nặng các dự đoán sai lệch lớn. Việc so sánh giữa RMSE và MAE giúp ta biết được liệu mô hình có đang mắc phải những sai số cực đoan hay không.
- **Công thức:**
  $$ RMSE = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2} $$

### 10.4. R-squared ($R^2$) - Hệ số xác định
- **Ý nghĩa:** Khác với MAE, MSE và RMSE (nhằm đo lường sai số), $R^2$ đo lường mức độ "vừa vặn" (goodness-of-fit) của mô hình. Cụ thể, nó thể hiện bao nhiêu phần trăm sự biến thiên của biến mục tiêu (PM2.5) có thể được giải thích bởi các biến đầu vào. $R^2$ có giá trị tối đa là 1 (hoặc 100%), giá trị càng tiến gần về 1 chứng tỏ mô hình hoạt động càng xuất sắc.
- **Công thức:**
  $$ R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2} $$
  *(Trong đó: $y_i$ là giá trị thực, $\hat{y}_i$ là giá trị dự báo, và $\bar{y}$ là giá trị trung bình của toàn bộ dữ liệu thực tế).*

### 10.5. Triển khai & Kết quả
Dựa trên việc đánh giá tập thử nghiệm (Test set), ta thu được các kết quả cụ thể như sau:

- **Linear Regression (Huấn luyện trên tập KHÔNG có ngoại lai):**
  - **Kết quả:** $MAE = 16.3358$, $MSE = 524.0252$, $RMSE = 22.8916$, $R^2 = 0.8454$
  - **Nhận xét:** Mặc dù đã cố tình loại bỏ các điểm nhiễu lớn để ưu ái cho đường hồi quy, hệ số $R^2$ chỉ dừng lại ở mức $0.8454$. Sự chênh lệch đáng kể giữa MAE ($16.3$) và RMSE ($22.8$) cho thấy dù phần lớn dự báo bám sát thực tế, nhưng thỉnh thoảng mô hình vẫn mắc phải những sai số khá cao. Nguyên nhân cốt lõi là do mối quan hệ giữa các yếu tố thời tiết và hạt bụi mịn thực chất mang tính chất phi tuyến tính phức tạp, vượt qua giới hạn năng lực nội suy của một phương trình đường thẳng đơn giản.

- **Random Forest Regressor (Huấn luyện trên tập CÓ chứa ngoại lai):**
  - **Kết quả:** $MAE = 13.4999$, $MSE = 476.9945$, $RMSE = 21.8402$, $R^2 = 0.9318$
  - **Nhận xét:** Bất chấp việc phải đối mặt với một tập dữ liệu thô chứa đầy các đợt bão bụi kỷ lục, Rừng Ngẫu Nhiên đã chứng tỏ hiệu năng vượt trội một cách rõ rệt. $R^2$ vọt lên $0.9318$ chứng tỏ mô hình giải thích được tới hơn 93% sự biến thiên phức tạp của dữ liệu. Sai số tuyệt đối MAE được ép xuống mức rất thấp ($13.49$), và MSE/RMSE đều cải thiện đáng kể so với mô hình Linear Regression. Điều này khẳng định sức mạnh của thuật toán Ensemble trong việc "bắt bài" các đỉnh ô nhiễm cực đoan mà không để chúng phá hỏng bức tranh tổng thể.
  - **Feature Importance (Tầm quan trọng của đặc trưng):** Biểu đồ Barplot trích xuất từ mô hình chỉ ra một cách áp đảo rằng hạt bụi to **PM10** (đóng góp tới $\sim 80\%$ quyết định) chính là "chỉ báo" dự báo PM2.5 mạnh mẽ nhất. Xếp ở vị trí thứ hai là nồng độ khí **CO** ($\sim 12\%$). Về phía yếu tố khí tượng, yếu tố quan trọng nhất ảnh hưởng trực tiếp đến quá trình tích tụ bụi mịn trong không khí chính là **DEWP (Điểm sương)**. 

## 11. Kết luận và hướng phát triển
- **Kết luận:** Đồ án đã triển khai thành công quy trình hồi quy dự báo PM2.5. So sánh chứng minh rằng trong dữ liệu tự nhiên như khí hậu, các sự kiện cực đoan (ngoại lai) chứa rất nhiều thông tin giá trị. Việc chọn đúng thuật toán (Random Forest) để tận dụng các nhiễu này mang lại hiệu quả dự đoán tốt hơn hẳn so với việc xóa bỏ chúng để ép vừa vào mô hình tuyến tính (Linear Regression).
- **Hướng phát triển & Tính ứng dụng:** 
  1. **Nâng cấp thuật toán:** Ứng dụng các kiến trúc mạng nơ-ron chuyên sâu cho chuỗi thời gian như **LSTM (Long Short-Term Memory)** hoặc **GRU** để khai thác hiệu quả hơn yếu tố trễ (lag) của nồng độ khói bụi theo thời gian thực.
  2. **Mở rộng dữ liệu:** Bổ sung dữ liệu quan trắc từ các trạm lân cận nhằm thu thập thêm biến về xu hướng dịch chuyển không gian (Spatial dependencies) của luồng bụi.
  3. **Khả năng ứng dụng thực tiễn tại Việt Nam:** Quy trình phân tích và mô hình Random Forest trong đồ án này hoàn toàn có thể được chuyển giao và huấn luyện lại bằng bộ dữ liệu đo lường không khí tại các siêu đô thị như Hà Nội hay TP.HCM. Tương tự như Bắc Kinh, Hà Nội cũng thường xuyên đối mặt với hiện tượng "sương mù quang hóa" và nghịch nhiệt mùa đông làm giam giữ bụi mịn ở tầm thấp. Việc tích hợp mô hình dự báo này với mạng lưới cảm biến môi trường (IoT) của thành phố sẽ cung cấp một giải pháp cảnh báo y tế sớm với độ tin cậy cao. Điều này giúp các cơ quan quản lý chủ động điều tiết giao thông và phát đi khuyến cáo kịp thời để người dân có biện pháp phòng vệ (hạn chế ra đường, sử dụng khẩu trang chuyên dụng, bật máy lọc không khí) trước khi những đợt không khí độc hại đạt "đỉnh điểm".

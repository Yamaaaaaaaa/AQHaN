# Kịch bản Thuyết trình: Báo cáo Bài tập lớn Nhập môn Khoa học Dữ liệu
**Đề tài:** Mô hình học máy dự báo nồng độ bụi mịn PM2.5 tại trạm Aotizhongxin

---

## Slide 1: Tiêu đề
- **Tiêu đề Slide:** DỰ BÁO NỒNG ĐỘ BỤI MỊN PM2.5 BẰNG MÔ HÌNH HỌC MÁY
- **Nội dung hiển thị:**
  - Tên học phần: Nhập môn Khoa học Dữ liệu
  - Case study: Trạm quan trắc Aotizhongxin (Bắc Kinh)
  - Thông tin sinh viên thực hiện / Nhóm thực hiện.
- **Hình ảnh đề xuất:** Một bức ảnh minh họa sự đối lập giữa bầu trời trong xanh và bầu trời ô nhiễm khói bụi mù mịt để tạo ấn tượng thị giác.
- **Lời thoại (Speaker Notes):** "Xin chào thầy cô và các bạn. Hôm nay em/nhóm em xin trình bày về đồ án áp dụng Khoa học Dữ liệu để giải quyết một trong những vấn đề môi trường nhức nhối nhất hiện nay: Dự báo nồng độ bụi mịn PM2.5 thông qua case study tại trạm Aotizhongxin, Bắc Kinh."

---

## Slide 2: Đặt vấn đề & Mục tiêu
- **Tiêu đề Slide:** Vấn đề Ô nhiễm không khí & Mục tiêu đồ án
- **Nội dung hiển thị:**
  - **Vấn đề:** 
    - PM2.5 gây nguy hiểm nghiêm trọng đến sức khỏe hô hấp và tim mạch.
    - Hơn 90% dân số thế giới đang hít thở không khí vượt ngưỡng an toàn của WHO.
    - Tại Việt Nam, tình trạng "sương mù quang hóa" ở các đô thị lớn đang ở mức báo động đỏ.
  - **Mục tiêu:**
    1. Trực quan hóa dữ liệu để tìm ra chu kỳ và nguyên nhân ô nhiễm.
    2. Xây dựng mô hình học máy dự báo mức độ gia tăng PM2.5.
    3. Hỗ trợ cảnh báo y tế sớm.
- **Lời thoại (Speaker Notes):** "Bụi mịn PM2.5 có thể đi thẳng vào mạch máu, đe dọa trực tiếp tới tuổi thọ con người. Mục tiêu của đồ án không chỉ dừng lại ở việc phân tích dữ liệu khô khan, mà xa hơn là xây dựng một hệ thống cảnh báo sớm, giúp người dân chủ động phòng tránh trong các ngày ô nhiễm đỉnh điểm."

---

## Slide 3: Giới thiệu Tập dữ liệu (Dataset)
- **Tiêu đề Slide:** Tổng quan Tập dữ liệu
- **Nội dung hiển thị:**
  - **Nguồn:** "Beijing Multi-Site Air-Quality" (ĐH Bắc Kinh).
  - **Thời gian:** 01/03/2013 - 28/02/2017 (Tròn 4 năm).
  - **Quy mô:** 35,064 bản ghi (Tần suất đo: 1 giờ/lần).
  - **Đặc trưng chính (18 biến):** Bụi (PM2.5, PM10), Khí thải (SO2, NO2, CO), Thời tiết (Nhiệt độ, Độ ẩm, Gió...).
- **Hình ảnh đề xuất:** Cắt một đoạn nhỏ bảng dữ liệu (DataFrame) hiển thị vài dòng đầu tiên.
- **Lời thoại (Speaker Notes):** 
  - "Chúng em sử dụng bộ dữ liệu thu thập liên tục trong 4 năm, mỗi giờ một bản ghi. Bộ dữ liệu này rất giá trị vì nó kết hợp cả yếu tố chất thải công nghiệp (như CO, SO2) và yếu tố khí hậu (như gió, nhiệt độ), giúp mô hình có cái nhìn toàn diện nhất."
  - Bộ dữ liệu này là dữ liệu theo chuỗi thời gian
  - Đặc trưng gồm 18 đặc trưng chia làm 3 nhóm: Chất ô nhiễm, Khí tượng, Thời gian


---

## Slide 4: Tiền xử lý Dữ liệu
- **Tiêu đề Slide:** Làm sạch & Chuẩn hóa Dữ liệu
- **Nội dung hiển thị:**
  - **Xử lý khuyết thiếu (Missing values):**
    - Vấn đề: Cảm biến hỏng gây đứt gãy chuỗi thời gian.
    - Giải pháp: Dùng thuật toán **Nội suy tuyến tính (Linear Interpolation)**.
  - **Chuẩn hóa (Feature Scaling):**
    - Sử dụng **StandardScaler (Z-score)**.
    - Đưa tất cả biến (Nhiệt độ, Áp suất...) về trung bình 0, độ lệch chuẩn 1 để mô hình dễ hội tụ.
- **Lời thoại (Speaker Notes):** 
  - Dữ liệu khuyết thiếu trong Dataset là những dữ liệu NA do máy đo bị lỗi.
  - Vì đây là dữ liệu chuỗi thời gian, nếu xóa các dòng bị lỗi máy đo sẽ làm đứt gãy thời gian. Do đó, phương pháp tối ưu được chọn là Nội suy tuyến tính. Đồng thời, dữ liệu được chuẩn hóa Z-score để đưa các thang đo chênh lệch về cùng một vạch xuất phát.
  - Chuẩn hóa Z-score là lấy giá trị trừ đi trung bình rồi chia cho độ lệch chuẩn.

---

## Slide 5: Bài toán Ngoại lai (Outliers)
- **Tiêu đề Slide:** Phát hiện Ngoại lai bằng Boxplot & IQR
- **Nội dung hiển thị:**
  - **Lý do chọn IQR:** Dữ liệu PM2.5 có phân phối lệch (không phải phân phối chuẩn). IQR sử dụng trung vị và dải phân vị nên không bị bóp méo bởi chính các ngoại lai, ưu việt hơn phương pháp Z-score.
  - **Ngoại lai:** PM2.5 > $252.0 \mu g/m^3$ (Có tới 1,653 bản ghi).
  - **Bản chất:** Đây KHÔNG phải lỗi máy đo, mà là các **đợt bão bụi/nghịch nhiệt có thật**.
  - **Quyết định chia tập dữ liệu:**
    - Tập ĐÃ XÓA ngoại lai $\Rightarrow$ Dùng cho mô hình Hồi quy tuyến tính.
    - Tập GIỮ NGUYÊN 100% ngoại lai $\Rightarrow$ Dùng cho mô hình Rừng Ngẫu Nhiên (Random Forest).
- **Hình ảnh đề xuất:** Chèn biểu đồ Boxplot (nếu có) thể hiện các điểm đen dày đặc ở tít trên cao.
- **Lời thoại (Speaker Notes):** 
  - "Lý do nhóm không dùng phương pháp Z-score để tìm ngoại lai vì Z-score yêu cầu dữ liệu phải có phân phối chuẩn và dùng giá trị trung bình (mean). Trong khi đó, bụi PM2.5 lại có phân phối lệch phải. Phương pháp IQR dựa trên trung vị (Median) và dải phân vị nên nó bền vững và không bị bóp méo bởi chính các ngoại lai đó."
  - "Bằng IQR, ta phát hiện hơn 1600 điểm cực đoan. Tuy nhiên, ô nhiễm cao vọt là thảm họa có thật chứ không phải nhiễu máy đo. Nếu xóa hết đi, mô hình sẽ 'mù' trước bão bụi. Do đó, nhóm quyết định giữ nguyên tập gốc để huấn luyện Random Forest, và chỉ xóa ngoại lai khi chạy Linear Regression để bảo vệ đường hồi quy."

---

## Slide 6: Phân tích Khám phá Dữ liệu (EDA)
- **Tiêu đề Slide:** Khám phá & Trực quan hóa Dữ liệu
- **Nội dung hiển thị:**
  - **Theo thời gian:** Mùa đông ô nhiễm gấp nhiều lần mùa hè (Đỉnh điểm $>140 \mu g/m^3$).
  - **Tương quan khí hậu:** Nhiệt độ thấp sinh ra nồng độ bụi cao. Gió mạnh giúp thổi bay khói bụi ($r = -0.28$).
  - **Nguồn gốc phát thải:** PM2.5 đồng biến cực mạnh với PM10 ($0.88$) và CO ($0.79$).
- **Hình ảnh đề xuất:** Đưa 3 biểu đồ (Line chart, Scatter plot, Heatmap) vào slide này (thu nhỏ sắp xếp vừa vặn).
- **Lời thoại (Speaker Notes):** 
  - "Nhìn vào biểu đồ đường (Line Chart), chúng ta dễ dàng nhận thấy một chu kỳ rất rõ ràng: Nồng độ PM2.5 luôn chạm đáy vào mùa hè nhưng lại tăng vọt lên mức báo động vào các tháng mùa đông. Nguyên nhân chính là do sự gia tăng đột biến của việc đốt than sưởi ấm, kết hợp với hiện tượng nghịch nhiệt độ giam giữ khói bụi ở sát mặt đất."
  - "Chuyển sang biểu đồ phân tán (Scatter Plot), mây điểm tập trung dày đặc và vọt lên rất cao ở dải nhiệt độ lạnh (dưới 10 độ C). Điều này một lần nữa củng cố giả thuyết: thời tiết giá rét tạo môi trường lý tưởng cho sự tích tụ bụi mịn."
  - "Cuối cùng, ma trận tương quan (Heatmap) đã bóc trần bản chất nguồn phát thải. PM2.5 có sự đồng biến cực kỳ cao với hạt bụi to PM10 (0.88) và khí độc CO (0.79). Bằng chứng này khẳng định bụi mịn sinh ra cùng một 'lò' với các loại khí thải công nghiệp và giao thông. Ở chiều ngược lại, tốc độ gió là yếu tố khí tượng duy nhất có tương quan âm (-0.28), đóng vai trò như một 'chiếc quạt khổng lồ' thổi phân tán khói bụi, giúp làm sạch bầu không khí tại trạm đo."

---

## Slide 7: Phương pháp Học máy (Machine Learning)
- **Tiêu đề Slide:** Xây dựng Mô hình Thuật toán
- **Nội dung hiển thị:**
  - **Mô hình 1: Linear Regression (Hồi quy tuyến tính)**
    - Đơn giản, tìm siêu phẳng (OLS).
    - Dễ bị bẻ cong bởi nhiễu $\Rightarrow$ Chỉ train trên tập Không có ngoại lai.
  - **Mô hình 2: Random Forest (Rừng ngẫu nhiên)**
    - Ensemble Learning, sử dụng 100 cây quyết định (Bagging).
    - Chia cắt không gian (splitting) $\Rightarrow$ Hoàn toàn miễn nhiễm với ngoại lai.
    - Train trực tiếp trên tập gốc có bão bụi cực đoan.
- **Lời thoại (Speaker Notes):** "Chúng em đối đầu hai phương pháp: một mô hình cơ bản và một mô hình phức tạp. Random Forest tỏ ra cực kỳ phù hợp nhờ nguyên lý chia nhánh của cây quyết định, nó có thể tự động cô lập các đỉnh ô nhiễm vào các nút lá riêng biệt mà không làm sai lệch dự báo của những ngày bình thường."

---

## Slide 8: Đánh giá Hiệu năng Mô hình
- **Tiêu đề Slide:** Đánh giá & So sánh Kết quả
- **Nội dung hiển thị:**
  - **Linear Regression:**
    - RMSE: 22.89 | $R^2$: 84.54%
    - Hạn chế: Thời tiết là hệ thống phi tuyến tính phức tạp.
  - **Random Forest:**
    - RMSE: 21.84 | $R^2$: 93.18% 🏆
    - Sức mạnh: Thuật toán xuất sắc bắt được quy luật của các đợt bão bụi.
- **Hình ảnh đề xuất:** Một bảng (Table) đơn giản so sánh 4 chỉ số (MAE, MSE, RMSE, R2) của 2 mô hình.
- **Lời thoại (Speaker Notes):** "Nhìn vào bảng đánh giá, Random Forest hoàn toàn áp đảo với khả năng giải thích tới hơn 93% sự biến thiên của dữ liệu. Việc nó vượt trội cả về MAE và RMSE chứng tỏ rừng cây quyết định đã học thành công quy luật của các đợt ô nhiễm nặng nhất."

---

## Slide 9: Các Yếu tố Quyết định (Feature Importance)
- **Tiêu đề Slide:** Các yếu tố quyết định Ô nhiễm PM2.5
- **Nội dung hiển thị:**
  - Random Forest tự động trích xuất mức độ quan trọng:
  - **Top 1:** PM10 (~80%) $\Rightarrow$ Chỉ báo mạnh nhất.
  - **Top 2:** Khí CO (~12%) $\Rightarrow$ Cảnh báo từ khí thải công nghiệp/giao thông.
  - **Top 3:** Điểm sương DEWP $\Rightarrow$ Yếu tố khí hậu chi phối mạnh nhất.
- **Hình ảnh đề xuất:** Biểu đồ Barplot "Feature Importance" từ Random Forest.
- **Lời thoại (Speaker Notes):** "Khác với Linear Regression, Random Forest cung cấp cho chúng ta một tính năng tuyệt vời là Feature Importance. Mô hình đã tự học và chỉ ra rằng: cứ thấy bụi PM10 và khí CO tăng cao, chắc chắn nồng độ PM2.5 sẽ bùng phát ngay sau đó."

---

## Slide 10: Kết luận & Hướng phát triển
- **Tiêu đề Slide:** Tổng kết & Khả năng Ứng dụng
- **Nội dung hiển thị:**
  - **Kết luận:** Ngoại lai mang giá trị thông tin khổng lồ. Random Forest là thuật toán tối ưu nhất để cảnh báo thảm họa không khí.
  - **Hướng phát triển kỹ thuật:** Thử nghiệm Mạng nơ-ron chuỗi thời gian (LSTM / GRU) để khai thác tính trễ (lag) của khói bụi.
  - **Ứng dụng tại Việt Nam:** Chuyển giao mô hình, áp dụng dữ liệu IoT tại Hà Nội và TP.HCM để hỗ trợ Chính phủ phát đi cảnh báo y tế kịp thời.
- **Lời thoại (Speaker Notes):** "Để khép lại, đồ án chứng minh rằng đừng bao giờ vội vàng xóa bỏ các điểm ngoại lai trong dữ liệu môi trường. Hướng đi sắp tới, mô hình này hoàn toàn có thể được 'học chuyển giao' về áp dụng trực tiếp tại mạng lưới IoT của Hà Nội, góp phần xây dựng một hệ thống cảnh báo sớm giúp bảo vệ sức khỏe cho người dân Việt Nam. Xin cảm ơn thầy cô và các bạn đã lắng nghe!"

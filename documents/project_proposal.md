# 📊 Phân Tích Chất Lượng Không Khí tại Hà Nội

> **Môn học:** Nhập môn Khoa học Dữ liệu  
> **Nguồn dữ liệu:** OpenAQ API (Air Quality Open Data)  
> **Ngôn ngữ:** Python 3.x  
> **Loại bài toán:** Phân tích thống kê + Phân loại mức AQI

---

## 1. Giới thiệu bài toán thực tế

Hà Nội liên tục nằm trong danh sách các thành phố có chất lượng không khí ô nhiễm nhất Đông Nam Á. Các chất ô nhiễm chính như PM2.5, PM10, NO₂, CO và O₃ gây ra nhiều bệnh hô hấp, tim mạch và ảnh hưởng lâu dài đến sức khỏe cộng đồng, đặc biệt với trẻ em và người cao tuổi.

**Bài toán đặt ra:** Dựa trên dữ liệu chất lượng không khí lịch sử tại Hà Nội, hãy:
- Phân tích xu hướng biến động nồng độ các chất ô nhiễm theo thời gian;
- Phát hiện các thời điểm chất lượng không khí ở mức nguy hiểm (outlier);
- Xây dựng mô hình phân loại mức AQI (Tốt / Trung bình / Kém / Xấu);
- Trực quan hóa toàn bộ kết quả phân tích bằng Python.

---

## 2. Mục tiêu và câu hỏi phân tích

### 2.1 Mục tiêu tổng quát

Phân tích chuyên sâu chất lượng không khí tại Hà Nội, nhận diện các yếu tố ô nhiễm chính và xây dựng mô hình phân loại AQI để hỗ trợ cảnh báo sức khỏe cộng đồng.

### 2.2 Câu hỏi phân tích

| # | Câu hỏi | Loại phân tích |
|---|---------|----------------|
| Q1 | Nồng độ PM2.5 tại Hà Nội biến động như thế nào theo từng giờ/ngày? | Thống kê mô tả + Line chart |
| Q2 | PM2.5 và PM10 có tương quan chặt với nhau không? | Scatter plot + Pearson correlation |
| Q3 | Những thời điểm nào AQI vượt ngưỡng "Không tốt cho sức khỏe" (>150)? | Phát hiện ngoại lai (IQR) |
| Q4 | Chất lượng không khí có khác biệt đáng kể giữa ngày trong tuần và cuối tuần không? | Kiểm định t-test |
| Q5 | Có thể phân loại mức AQI dựa trên nồng độ các chất ô nhiễm không? | Random Forest Classifier |

---

## 3. Mô tả dữ liệu

### 3.1 Nguồn dữ liệu

Sử dụng **OpenAQ API** – nền tảng dữ liệu chất lượng không khí mở toàn cầu, miễn phí, không cần API key cho truy cập cơ bản. Dữ liệu được thu thập từ các trạm quan trắc thực tế tại Hà Nội.

**API endpoint sử dụng:**

| API | Endpoint | Mô tả |
|-----|----------|--------|
| Measurements | `GET /v2/measurements` | Đo lường các chất ô nhiễm theo giờ |
| Locations | `GET /v2/locations` | Danh sách trạm quan trắc tại Hà Nội |
| Latest | `GET /v2/latest` | Số liệu mới nhất |

**Tham số gọi API:**
```
city=Hanoi
country=VN
parameter=pm25,pm10,no2,co,o3,so2
limit=1000          # Số bản ghi mỗi trang
date_from=2024-01-01
date_to=2024-12-31
```

**URL ví dụ:**
```
https://api.openaq.org/v2/measurements?city=Hanoi&country=VN&parameter=pm25&limit=1000&page=1
```

> **Ưu điểm:** Tải về ngay lập tức, không cần chờ; lịch sử nhiều năm; miễn phí hoàn toàn; thuần dữ liệu không khí.

### 3.2 Bảng mô tả biến dữ liệu

| Biến | Kiểu | Đơn vị | Mô tả |
|------|------|--------|-------|
| `dt` | datetime | ISO 8601 | Thời điểm đo |
| `location` | str | — | Tên trạm quan trắc |
| `pm2_5` | float | μg/m³ | Bụi mịn PM2.5 |
| `pm10` | float | μg/m³ | Bụi PM10 |
| `no2` | float | μg/m³ | Nồng độ NO₂ |
| `co` | float | μg/m³ | Nồng độ CO |
| `o3` | float | μg/m³ | Nồng độ Ozone |
| `so2` | float | μg/m³ | Nồng độ SO₂ |
| `aqi_category` | str | — | Mức AQI (nhãn phân loại, tạo từ PM2.5) |
| `hour` | int | — | Giờ trong ngày (trích xuất từ `dt`) |
| `day_of_week` | int | 0–6 | Thứ trong tuần |
| `is_weekend` | int | 0/1 | Cuối tuần hay không |

**Quy đổi PM2.5 → AQI category (US-EPA):**

| PM2.5 (μg/m³) | Mức AQI | Nhãn |
|--------------|---------|------|
| 0 – 12 | 0–50 | Good |
| 12.1 – 35.4 | 51–100 | Moderate |
| 35.5 – 55.4 | 101–150 | Unhealthy for Sensitive |
| 55.5 – 150.4 | 151–200 | Unhealthy |
| > 150.4 | 201+ | Very Unhealthy / Hazardous |

**Quy mô dữ liệu dự kiến:** ~2000–5000 bản ghi (tùy số trạm và khoảng thời gian chọn).

---

## 4. Thu thập dữ liệu

### 4.1 Code thu thập từ OpenAQ API

```python
import requests
import pandas as pd
import time

BASE_URL = "https://api.openaq.org/v2/measurements"

def fetch_openaq(parameter, date_from, date_to, limit=1000):
    records = []
    page = 1
    while True:
        params = {
            "city": "Hanoi", "country": "VN",
            "parameter": parameter,
            "date_from": date_from, "date_to": date_to,
            "limit": limit, "page": page,
            "sort": "asc", "order_by": "datetime"
        }
        resp = requests.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json().get("results", [])
        if not data:
            break
        records.extend(data)
        print(f"[{parameter}] Trang {page}: +{len(data)} bản ghi")
        page += 1
        time.sleep(0.5)   # Tránh rate limit
    return records

# Thu thập các chất ô nhiễm chính
params = ["pm25", "pm10", "no2", "co", "o3", "so2"]
all_dfs = []

for param in params:
    raw = fetch_openaq(param, "2024-01-01", "2024-12-31")
    rows = [{
        "dt":       r["date"]["local"],
        "location": r["location"],
        "parameter": r["parameter"],
        "value":    r["value"],
        "unit":     r["unit"]
    } for r in raw if r["value"] >= 0]
    all_dfs.append(pd.DataFrame(rows))

df_long = pd.concat(all_dfs, ignore_index=True)

# Pivot thành dạng wide (mỗi hàng = 1 thời điểm × 1 trạm)
df = df_long.pivot_table(
    index=["dt", "location"], columns="parameter",
    values="value", aggfunc="mean"
).reset_index()
df.columns.name = None
df.rename(columns={"pm25": "pm2_5"}, inplace=True)
df["dt"] = pd.to_datetime(df["dt"])

df.to_csv("data/hanoi_airquality.csv", index=False)
print(f"✅ Đã lưu {len(df)} bản ghi.")
```

### 4.2 Cấu trúc thư mục dự án

```
BTL_NMKHDL/
├── data/
│   └── hanoi_airquality.csv
├── notebooks/
│   └── analysis.ipynb
├── charts/
│   ├── line_pm25.png
│   ├── scatter_pm25_pm10.png
│   ├── histogram_pm25.png
│   ├── boxplot_by_hour.png
│   ├── heatmap_corr.png
│   └── feature_importance.png
├── documents/
│   ├── rule_doc.md
│   ├── yeu_cau_de_bai.md
│   └── project_proposal.md
└── README.md
```

---

## 5. Làm sạch và tiền xử lý dữ liệu

### 5.1 Các bước xử lý

**1. Chuẩn hóa thời gian:**
```python
df["dt"] = pd.to_datetime(df["dt"], utc=True).dt.tz_convert("Asia/Bangkok")
df["hour"]        = df["dt"].dt.hour
df["day_of_week"] = df["dt"].dt.dayofweek    # 0=Thứ 2, 6=Chủ nhật
df["is_weekend"]  = (df["day_of_week"] >= 5).astype(int)
```

**2. Kiểm tra giá trị thiếu:**
```python
print(df.isnull().sum())
# Xử lý: nội suy tuyến tính cho cột thiếu ít (<10%)
df[["pm2_5","pm10","no2","co","o3","so2"]] = \
    df[["pm2_5","pm10","no2","co","o3","so2"]].interpolate(method="linear")
```

**3. Loại bỏ dữ liệu không hợp lệ:**
```python
# Ràng buộc vật lý: các chất ô nhiễm phải không âm
for col in ["pm2_5","pm10","no2","co","o3","so2"]:
    df.loc[df[col] < 0, col] = None

# PM2.5 tại Hà Nội: ngưỡng hợp lý < 500 μg/m³
df = df[df["pm2_5"] < 500]
```

**4. Tạo nhãn AQI category từ PM2.5:**
```python
def pm25_to_category(val):
    if   val <= 12:    return "Good"
    elif val <= 35.4:  return "Moderate"
    elif val <= 55.4:  return "Unhealthy for Sensitive"
    elif val <= 150.4: return "Unhealthy"
    else:              return "Very Unhealthy"

df["aqi_category"] = df["pm2_5"].apply(pm25_to_category)
```

---

## 6. Phân tích thống kê mô tả

```python
desc = df[["pm2_5","pm10","no2","co","o3","so2"]].describe()
print(desc.to_markdown())
```

**Phân tích theo nhóm:**
```python
# PM2.5 trung bình theo giờ trong ngày
df.groupby("hour")["pm2_5"].mean().plot(kind="bar", figsize=(12,4),
    title="PM2.5 trung bình theo giờ – Hà Nội")

# PM2.5 trung bình theo thứ trong tuần
day_names = ["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7","CN"]
df["day_name"] = df["day_of_week"].map(dict(enumerate(day_names)))
df.groupby("day_name")["pm2_5"].mean()
```

---

## 7. Phát hiện ngoại lai

### 7.1 Phương pháp IQR

```python
def detect_outliers_iqr(series):
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return series[(series < lower) | (series > upper)]

outliers_pm25 = detect_outliers_iqr(df["pm2_5"])
print(f"Số ngoại lai PM2.5: {len(outliers_pm25)} ({len(outliers_pm25)/len(df)*100:.1f}%)")
```

### 7.2 Trực quan hóa ngoại lai

- **Boxplot** cho PM2.5, PM10, NO₂;
- Đánh dấu các điểm ngoại lai màu đỏ trên **line chart** theo thời gian;
- Bảng tổng hợp thời điểm AQI vượt ngưỡng "Unhealthy".

---

## 8. Trực quan hóa dữ liệu

| # | Loại | Nội dung | Thư viện |
|---|------|---------|---------|
| 1 | **Line chart** | Diễn biến PM2.5 theo thời gian (toàn bộ dataset) | `matplotlib` |
| 2 | **Scatter plot** | Tương quan PM2.5 vs PM10 | `seaborn` |
| 3 | **Histogram** | Phân bố nồng độ PM2.5 và NO₂ | `matplotlib` |
| 4 | **Boxplot** | PM2.5 phân bố theo giờ trong ngày | `seaborn` |
| 5 | **Heatmap** | Ma trận tương quan giữa các chất ô nhiễm | `seaborn` |
| 6 | **Bar chart** | Tỷ lệ % các mức AQI (Good/Moderate/Unhealthy…) | `matplotlib` |

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Biểu đồ 1: Line chart PM2.5
fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(df["dt"], df["pm2_5"], color="tomato", linewidth=0.7, alpha=0.8)
ax.axhline(35.4, color="orange", linestyle="--", label="Ngưỡng Moderate (35.4)")
ax.axhline(55.4, color="red",    linestyle="--", label="Ngưỡng Unhealthy (55.4)")
ax.set_title("Diễn biến PM2.5 tại Hà Nội theo thời gian")
ax.set_xlabel("Thời gian"); ax.set_ylabel("PM2.5 (μg/m³)")
ax.legend(); fig.tight_layout()
plt.savefig("charts/line_pm25.png", dpi=150); plt.show()

# Biểu đồ 5: Heatmap tương quan
plt.figure(figsize=(7, 5))
corr = df[["pm2_5","pm10","no2","co","o3","so2"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn_r")
plt.title("Ma trận tương quan giữa các chất ô nhiễm")
plt.tight_layout(); plt.savefig("charts/heatmap_corr.png", dpi=150); plt.show()
```

---

## 9. Xây dựng mô hình / thuật toán

### 9.1 Bài toán: Phân loại mức AQI (Classification)

**Biến mục tiêu:** `aqi_category` (Good / Moderate / Unhealthy for Sensitive / Unhealthy / Very Unhealthy)  
**Biến đầu vào:** `pm10`, `no2`, `co`, `o3`, `so2`, `hour`, `day_of_week`, `is_weekend`

> **Lưu ý:** `pm2_5` không dùng làm feature vì `aqi_category` được tạo trực tiếp từ nó.

### 9.2 Mô hình áp dụng

| Mô hình | Lý do chọn |
|---------|-----------|
| **Decision Tree Classifier** | Dễ hiểu, dễ trực quan hóa cây quyết định, phù hợp giải thích kết quả |

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

features = ["pm10","no2","co","o3","so2","hour","day_of_week","is_weekend"]
target   = "aqi_category"

df_model = df[features + [target]].dropna()
X = df_model[features]
le = LabelEncoder()
y  = le.fit_transform(df_model[target])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Decision Tree
dt = DecisionTreeClassifier(max_depth=5, random_state=42, class_weight="balanced")
dt.fit(X_train, y_train)
print(f"Depth thực tế: {dt.get_depth()} | Số lá: {dt.get_n_leaves()}")
```

### 9.3 Giả thuyết thống kê

> **H₀:** Không có sự khác biệt đáng kể về nồng độ PM2.5 giữa ngày trong tuần và cuối tuần tại Hà Nội.  
> **H₁:** PM2.5 ngày trong tuần cao hơn cuối tuần do mật độ giao thông và hoạt động công nghiệp.

```python
from scipy import stats

weekday_pm25 = df[df["is_weekend"] == 0]["pm2_5"].dropna()
weekend_pm25 = df[df["is_weekend"] == 1]["pm2_5"].dropna()

t_stat, p_value = stats.ttest_ind(weekday_pm25, weekend_pm25, equal_var=False)
print(f"Trung bình ngày thường: {weekday_pm25.mean():.2f} μg/m³")
print(f"Trung bình cuối tuần:   {weekend_pm25.mean():.2f} μg/m³")
print(f"t = {t_stat:.4f}, p = {p_value:.4f}")
if p_value < 0.05:
    print("→ Bác bỏ H₀: Có sự khác biệt có ý nghĩa thống kê (p < 0.05).")
else:
    print("→ Không đủ cơ sở bác bỏ H₀.")
```

---

## 10. Đánh giá kết quả

### 10.1 Độ đo đánh giá (bài toán phân loại)

```python
y_pred = dt.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, target_names=le.classes_))
```

**Bảng kết quả (điền sau khi chạy):**

| Mô hình | Accuracy | Precision (macro) | Recall (macro) | F1-score (macro) |
|---------|----------|-------------------|----------------|-----------------|
| Decision Tree | — | — | — | — |

### 10.2 Confusion Matrix

```python
import seaborn as sns
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", xticklabels=le.classes_, yticklabels=le.classes_,
            cmap="Blues")
plt.title("Confusion Matrix – Decision Tree"); plt.tight_layout()
plt.savefig("charts/confusion_matrix.png", dpi=150); plt.show()
```

### 10.3 Feature Importance & Trực quan hóa cây quyết định

```python
# Feature importance
feat_imp = pd.Series(dt.feature_importances_, index=features).sort_values(ascending=False)
feat_imp.plot(kind="bar", figsize=(8,4), color="steelblue",
              title="Feature Importance – Decision Tree (AQI Classification)")
plt.tight_layout(); plt.savefig("charts/feature_importance.png", dpi=150); plt.show()

# Vẽ cây quyết định
plt.figure(figsize=(20, 8))
plot_tree(dt, feature_names=features, class_names=le.classes_,
          filled=True, rounded=True, fontsize=9)
plt.title("Decision Tree – Phân loại mức AQI tại Hà Nội")
plt.tight_layout(); plt.savefig("charts/decision_tree.png", dpi=120); plt.show()
```

### 10.4 Giải thích kết quả

- Đánh giá Accuracy và F1-score (macro) của Decision Tree;
- Phân tích các lớp bị nhầm lẫn nhiều nhất qua Confusion Matrix;
- Đọc cây quyết định: nút gốc và nhánh phân chia quan trọng nhất là gì?
- Xác định chất ô nhiễm nào đóng vai trò phân loại AQI quan trọng nhất qua feature importance;
- Giải thích kết quả kiểm định t-test: có hay không sự khác biệt PM2.5 giữa ngày thường và cuối tuần.

---

## 11. Kết luận và hướng phát triển

### 11.1 Kết luận dự kiến

- Hà Nội thường duy trì PM2.5 ở mức **Moderate – Unhealthy** (35–150 μg/m³), đặc biệt cao vào mùa đông (tháng 11–2) do hiện tượng nghịch nhiệt;
- PM2.5 và PM10 có tương quan dương mạnh (r > 0.8), trong khi O₃ thường tương quan âm với NO₂ (phản ứng quang hóa);
- Kết quả t-test xác nhận/bác bỏ giả thuyết về sự khác biệt PM2.5 ngày thường vs cuối tuần;
- Random Forest đạt accuracy cao hơn Decision Tree, đặc biệt với các lớp thiểu số (Very Unhealthy).

### 11.2 Hướng phát triển

| Hướng | Mô tả |
|-------|-------|
| Chuỗi thời gian | Dự báo PM2.5 theo giờ bằng ARIMA hoặc LSTM |
| Mở rộng địa lý | So sánh chất lượng không khí Hà Nội vs các tỉnh lân cận |
| Dashboard | Xây dựng giao diện thời gian thực với Streamlit |
| Cảnh báo | Gửi thông báo tự động khi AQI vượt ngưỡng nguy hiểm |

---

## 12. Thư viện cần cài đặt (Phụ lục kỹ thuật)

```bash
pip install requests pandas numpy matplotlib seaborn scikit-learn scipy jupyter
```

| Thư viện | Phiên bản | Mục đích |
|---------|-----------|---------|
| `requests` | ≥ 2.28 | Gọi OpenAQ API |
| `pandas` | ≥ 2.0 | Xử lý dữ liệu |
| `numpy` | ≥ 1.24 | Tính toán số học |
| `matplotlib` | ≥ 3.7 | Vẽ biểu đồ |
| `seaborn` | ≥ 0.12 | Biểu đồ thống kê |
| `scikit-learn` | ≥ 1.3 | Mô hình phân loại |
| `scipy` | ≥ 1.11 | Kiểm định thống kê |
| `jupyter` | ≥ 1.0 | Chạy notebook |

---

## 13. Checklist đáp ứng yêu cầu

### ✅ Yêu cầu đề bài (`yeu_cau_de_bai.md`)

| Yêu cầu | Đáp ứng |
|---------|---------|
| Phân tích chất lượng không khí | ✅ Toàn bộ dự án |
| Nhận diện xu hướng biến động | ✅ Mục 6, 11 |
| Phát hiện giá trị bất thường | ✅ Mục 7 (IQR + Boxplot) |
| Trực quan hóa theo thời gian | ✅ Mục 8, biểu đồ #1 |
| Thu thập & tiền xử lý dữ liệu | ✅ Mục 4, 5 |
| Chuẩn hóa dữ liệu thời gian | ✅ Mục 5.1 |
| Phát hiện giá trị thiếu & lỗi | ✅ Mục 5.1 |
| Thống kê Mean, Median, Std | ✅ Mục 6 |
| Ngoại lai: Boxplot + IQR | ✅ Mục 7 |
| Line chart theo thời gian | ✅ Mục 8, #1 |
| Scatter plot giữa hai biến | ✅ Mục 8, #2 |
| Histogram phân bố | ✅ Mục 8, #3 |
| Ít nhất 01 giả thuyết thống kê | ✅ Mục 9.3 |
| Kết luận xu hướng & so sánh nhóm | ✅ Mục 11 |

### ✅ Yêu cầu kỹ thuật tối thiểu (`rule_doc.md`)

| Yêu cầu | Đáp ứng |
|---------|---------|
| ≥ 01 bảng dữ liệu thực tế | ✅ OpenAQ: ~2000–5000 bản ghi |
| ≥ 03 biểu đồ trực quan | ✅ 6 biểu đồ (Mục 8) |
| Xử lý dữ liệu thiếu / không nhất quán | ✅ Mục 5.1 |
| Kiểm tra / phân tích ngoại lai | ✅ Mục 7 |
| ≥ 01 bài toán mô hình hóa | ✅ Phân loại AQI (Mục 9) |
| Đánh giá: Accuracy, Precision, Recall, F1 | ✅ Mục 10 |
| Giải thích kết quả | ✅ Mục 10.4, 11 |

---

*Tài liệu được xây dựng theo cấu trúc thống nhất quy định tại `rule_doc.md`, tập trung hoàn toàn vào phân tích chất lượng không khí tại Hà Nội.*

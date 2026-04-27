# # Phân Tích Dữ Liệu Chất Lượng Không Khí (Air Quality)
# Pipeline phân tích, xử lý, trực quan hoá dữ liệu và xây dựng mô hình dự đoán.
# Yêu cầu: Đọc dữ liệu `raw.csv`, tiền xử lý, phân tích thống kê, trực quan hóa, kiểm định giả thuyết và tạo mô hình học máy.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings

warnings.filterwarnings('ignore')
# Thiết lập style cho đồ thị
plt.style.use('seaborn-v0_8-whitegrid')

# %% [markdown]
# ## 1. Thu thập và Tiền xử lý dữ liệu

# %%
# Đọc dữ liệu từ file csv (Dữ liệu cách nhau bởi dấu chấm phẩy, dấu thập phân là phẩy)
data_path = r'../data/raw.csv'
print(f"Đang đọc dữ liệu từ: {data_path}")
df = pd.read_csv(data_path, sep=';', decimal=',')

# Xóa các cột trống (thường có tên 'Unnamed: ...' do có dấy ; dư ở cuối mỗi dòng)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Xóa các dòng trống hoàn toàn (thường ở cuối file)
df.dropna(how='all', inplace=True)

print("Kích thước dữ liệu ban đầu:", df.shape)
print("\nDữ liệu 5 dòng đầu:")
display(df.head())

# Xử lý giá trị bị khuyết: Trong Air Quality UCI dataset, missing value được ký hiệu là -200
print("\nSố lượng giá trị -200 (missing) trong mỗi cột:")
print((df == -200).sum())

# Thay thế -200 bằng NaN
df.replace(-200, np.nan, inplace=True)

# Kết hợp Date và Time thành cột Datetime kiểu chuẩn
if 'Date' in df.columns and 'Time' in df.columns:
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')
    df.drop(['Date', 'Time'], axis=1, inplace=True)
    df.set_index('Datetime', inplace=True)

print("\nThông tin dữ liệu sau khi định dạng lại thời gian:")
df.info()

# Nội suy dữ liệu thiếu (Interpolation) cho dữ liệu chuỗi thời gian
df.interpolate(method='time', inplace=True)

# Điền các giá trị NaN ở đầu hoặc cuối bằng bfill và ffill
df.bfill(inplace=True)
df.ffill(inplace=True)

print("\nTổng số missing values sau khi tiền xử lý:", df.isnull().sum().sum())

# %% [markdown]
# ## 2. Phân tích thống kê

# %%
# Thống kê mô tả (Mean, Standard Deviation, Min, Max)
desc_stats = df.describe().T
# Thêm cột Median (Trung vị)
desc_stats['median'] = df.median()

print("\n--- Bảng Thống Kê Mô Tả ---")
display(desc_stats[['mean', 'median', 'std', 'min', 'max']])

# Hàm phát hiện ngoại lai bằng phương pháp IQR (Interquartile Range)
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers

outliers_T = detect_outliers_iqr(df, 'T')
outliers_CO = detect_outliers_iqr(df, 'CO(GT)')

print(f"\nSố dòng chứa ngoại lai ở Nhiệt độ (T): {len(outliers_T)} dòng")
print(f"Số dòng chứa ngoại lai ở Nồng độ CO(GT): {len(outliers_CO)} dòng")

# %% [markdown]
# ## 3. Trực quan hóa dữ liệu

# %%
# 3.1. Line chart: Xu hướng nhiệt độ theo thời gian
# Resample theo tuần (W) để đường đồ thị mượt mà hơn
plt.figure(figsize=(14, 6))
df['T'].resample('W').mean().plot(color='crimson', linewidth=2, label='Nhiệt độ (T) - Trung bình Tuần')
plt.title('Biến Động Nhiệt Độ (T) Theo Thời Gian', fontsize=16)
plt.xlabel('Thời Gian (Năm-Tháng)', fontsize=12)
plt.ylabel('Nhiệt Độ (°C)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

# 3.2. Scatter plot: Mối quan hệ giữa Nhiệt độ và Độ ẩm
plt.figure(figsize=(8, 6))
sns.scatterplot(x='T', y='RH', data=df, alpha=0.3, color='steelblue')
plt.title('Mối Quan Hệ Giữa Nhiệt Độ (T) Và Độ Ẩm Tương Đối (RH)', fontsize=14)
plt.xlabel('Nhiệt Độ (°C)')
plt.ylabel('Độ Ẩm Tương Đối (RH %)')
plt.tight_layout()
plt.show()

# 3.3. Histogram: Phân bố của khí CO(GT)
plt.figure(figsize=(8, 6))
sns.histplot(df['CO(GT)'], bins=40, kde=True, color='forestgreen')
plt.title('Phân Bố Nồng Độ Khí CO(GT)', fontsize=14)
plt.xlabel('Nồng Độ CO(GT)')
plt.ylabel('Tần Suất')
plt.tight_layout()
plt.show()

# 3.4. Boxplot: Biểu diễn phân bố và ngoại lai của các biến chọn lọc
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['CO(GT)', 'NO2(GT)', 'T', 'RH']], palette='Set2')
plt.title('Boxplot Phát Hiện Ngoại Lai Các Chỉ Số Chính', fontsize=14)
plt.ylabel('Giá trị')
plt.tight_layout()
plt.show()


# %% [markdown]
# ## 4. Phân tích và Kiểm định giả thuyết

# %%
# Tạo cột 'Hour' để phân tích theo giờ
df['Hour'] = df.index.hour

# Chia làm 2 nhóm: Ban ngày (06:00 - 18:00) và Ban đêm (18:00 - 06:00)
daytime_co = df[(df['Hour'] >= 6) & (df['Hour'] < 18)]['CO(GT)']
nighttime_co = df[(df['Hour'] < 6) | (df['Hour'] >= 18)]['CO(GT)']

print("\n--- Kiểm Định Giả Thuyết (T-Test) ---")
print("H0 (Giả thuyết không): Không có sự khác biệt về lượng CO(GT) trung bình giữa ban ngày và ban đêm.")
print("H1 (Giả thuyết đối): Có sự khác biệt có ý nghĩa về lượng CO(GT) trung bình giữa ban ngày và ban đêm.")

# Thực hiện Independent T-test
t_stat, p_val = stats.ttest_ind(daytime_co, nighttime_co, equal_var=False)

print(f"\nKết quả:")
print(f"- T-statistic: {t_stat:.4f}")
print(f"- P-value:     {p_val:.4e}")

if p_val < 0.05:
    print("=> Kết luận: Bác bỏ H0. Nồng độ CO(GT) ban ngày và ban đêm CÓ sự khác biệt mang ý nghĩa thống kê.")
else:
    print("=> Kết luận: Chưa đủ bằng chứng để bác bỏ H0.")


# %% [markdown]
# ## 5. Xây dựng Mô Hình Thuật Toán

# %%
# Bài toán: Dự báo nồng độ C6H6(GT) (Benzen) dựa trên thông số các cảm biến khí khác và thời tiết.
# Đây là bài toán Hồi quy tuyến tính (Linear Regression) đơn giản nhưng hiệu quả.

features = ['PT08.S1(CO)', 'PT08.S2(NMHC)', 'PT08.S3(NOx)', 'PT08.S4(NO2)', 'PT08.S5(O3)', 'T', 'RH', 'AH']
target = 'C6H6(GT)'

# Loại bỏ các dòng mà target hoặc features vẫn bị rỗng (nếu có)
df_model = df.dropna(subset=[target] + features)

X = df_model[features]
y = df_model[target]

# Chia tách tập huấn luyện (Train) và tập kiểm tra (Test) theo tỉ lệ 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\n--- Xây Dựng Mô Hình Hồi Quy Tuyến Tính (Linear Regression) ---")
print(f"Kích thước tập huấn luyện: {X_train.shape}")
print(f"Kích thước tập kiểm tra:   {X_test.shape}")

# Khởi tạo và huấn luyện mô hình Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = lr_model.predict(X_test)

# Đánh giá mô hình bằng các độ đo MSE, MAE, R2-Score
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nKết quả Đánh giá Mô hình:")
print(f"- Mean Squared Error (MSE):  {mse:.4f}")
print(f"- Mean Absolute Error (MAE): {mae:.4f}")
print(f"- R-squared (R2 Score):      {r2:.4f}")

# Vẽ đồ thị so sánh giá trị Thực tế và Dự đoán
plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, alpha=0.3, color='darkorange')
# Đường chéo y = x (hoàn hảo)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title('Đánh Giá Hồi Quy Tuyến Tính: C6H6(GT) Thực Tế vs Dự Đoán', fontsize=14)
plt.xlabel('Giá Trị Thực Tế C6H6(GT)')
plt.ylabel('Giá Trị Dự Đoán C6H6(GT)')
plt.tight_layout()
plt.show()

# Hiển thị các hệ số (Coefficients) để xem ảnh hưởng của từng biến
coefficients = pd.DataFrame({'Biến': features, 'Hệ số': lr_model.coef_})
print("\nHệ số tác động của từng đặc trưng (Coefficients):")
display(coefficients.sort_values(by='Hệ số', ascending=False))

# %% [markdown]
# ## 6. Kết luận
# 
# 1. **Xu hướng và Dữ liệu:** 
#    - Đã tiền xử lý thành công bằng nội suy để thay thế các giá trị nhiễu `-200`. 
#    - Dữ liệu Nhiệt độ và CO có sự dao động mạnh và mang tính chu kỳ ngày/đêm.
# 2. **Kiểm định:** 
#    - Chứng minh được bằng xác suất thống kê rằng nồng độ ô nhiễm ban ngày và ban đêm có sự khác biệt rõ rệt.
# 3. **Mô hình học máy:** 
#    - Mô hình Hồi quy tuyến tính (Linear Regression) cơ bản đã cho kết quả tương đối tốt (đánh giá qua R2).
#    - Điều này cho thấy các cảm biến khí (như PT08) và nhiệt độ có mối liên hệ tuyến tính tỷ lệ thuận tương đối rõ ràng với nồng độ chất Benzen (C6H6).

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os

API_KEY = 'ad501790141d4bf19445aecfc44e1da6' # Thay bằng API Key của bạn
LAT = 21.0285  # Vĩ độ (ví dụ: Hà Nội)
LON = 105.8542 # Kinh độ (ví dụ: Hà Nội)
DAYS_TO_FETCH = 200
CHUNK_DAYS = 5 # Weatherbit tính phí theo từng chunk 5 ngày, nên chia nhỏ request để an toàn và tránh timeout
OUTPUT_CSV = 'weatherbit_historical_aq_200days.csv'

def get_historical_aq(lat, lon, start_date, end_date, api_key):
    url = f"https://api.weatherbit.io/v2.0/forecast/airquality"
    params = {
        'lat': lat,
        'lon': lon,
        'start_date': start_date,
        'end_date': end_date,
        'key': api_key,
        'tz': 'local' # Để trả về giờ địa phương
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {start_date} to {end_date}: {e}")
        # Nếu in ra lỗi 403 Forbidden, có thể key của bạn không có quyền truy cập History API.
        if response is not None:
             print("Response content:", response.text)
        return None

def main():
    if API_KEY == 'YOUR_WEATHERBIT_API_KEY':
        print("Vui lòng thay 'YOUR_WEATHERBIT_API_KEY' bằng API key thực tế của bạn!")
        return

    end_date_obj = datetime.now()
    start_date_obj = end_date_obj - timedelta(days=DAYS_TO_FETCH)
    
    current_start = start_date_obj
    all_data = []

    print(f"Đang lấy dữ liệu chất lượng không khí từ {start_date_obj.strftime('%Y-%m-%d')} đến {end_date_obj.strftime('%Y-%m-%d')}")

    while current_start < end_date_obj:
        current_end = current_start + timedelta(days=CHUNK_DAYS)
        if current_end > end_date_obj:
            current_end = end_date_obj

        str_start = current_start.strftime('%Y-%m-%d')
        str_end = current_end.strftime('%Y-%m-%d')
        
        print(f"Đang lấy khoảng: {str_start} đến {str_end}...")
        
        data = get_historical_aq(LAT, LON, str_start, str_end, API_KEY)
        
        if data and 'data' in data:
            for entry in data['data']:
                # Lọc ra các trường cần thiết
                row = {
                    'timestamp_local': entry.get('timestamp_local'),
                    'timestamp_utc': entry.get('timestamp_utc'),
                    'aqi': entry.get('aqi'),
                    'pm25': entry.get('pm25'),
                    'pm10': entry.get('pm10'),
                    'o3': entry.get('o3'),
                    'no2': entry.get('no2'),
                    'so2': entry.get('so2'),
                    'co': entry.get('co'),
                }
                all_data.append(row)
                
        # Tạm nghỉ 1s giữa các request để tránh rate limit
        time.sleep(1)
        
        current_start = current_end

    if all_data:
        df = pd.DataFrame(all_data)
        # Xóa các dòng trùng lặp (nếu có) do trùng lặp ở biên của các ngày
        df.drop_duplicates(subset=['timestamp_utc'], inplace=True)
        # Sắp xếp theo thời gian
        df.sort_values('timestamp_utc', inplace=True)
        
        # Lưu ra CSV
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\nThành công! Đã lưu {len(df)} bản ghi vào file {OUTPUT_CSV}")
    else:
        print("\nKhông có dữ liệu nào được thu thập. Vui lòng kiểm tra lại API Key hoặc giới hạn của tài khoản.")

if __name__ == "__main__":
    main()

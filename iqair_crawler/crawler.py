import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import os

def crawl_iqair():
    url = "https://www.iqair.com/vietnam/ha-noi/hanoi"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Sửa lỗi encoding để đọc đúng các ký tự O₃ và µ
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        patterns = {
            "pm25": r"PM2\.5.*?([\d.]+)\s*µg/m³",
            "pm10": r"PM10.*?([\d.]+)\s*µg/m³",
            "o3": r"O₃.*?([\d.]+)\s*µg/m³",
            "no2": r"NO₂.*?([\d.]+)\s*µg/m³",
            "so2": r"SO₂.*?([\d.]+)\s*µg/m³",
            "co": r"CO.*?([\d.]+)\s*µg/m³",
        }

        data = {
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": "Hanoi"
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            data[key] = float(match.group(1)) if match else None

        df = pd.DataFrame([data])
        print("Data scraped:")
        print(df)
        
        file_name = "../data/hanoi_iqair.csv"
        
        try:
            old_df = pd.read_csv(file_name)
            df = pd.concat([old_df, df], ignore_index=True)
        except FileNotFoundError:
            pass

        df.to_csv(file_name, index=False, encoding="utf-8-sig")
        print(f"\nSuccessfully saved data to {file_name}. Total records: {len(df)}")
        return len(df)

    except Exception as e:
        print(f"Error occurred during crawl: {e}")
        return -1

if __name__ == "__main__":
    import time
    
    print("Bắt đầu crawler. Sẽ thu thập cho đến khi đạt 2000 bản ghi...")
    while True:
        num_records = crawl_iqair()
        
        # Nếu lấy thành công và đạt đủ 2000 bản ghi
        if num_records >= 2000:
            print(f"Đã đạt {num_records} bản ghi. Dừng chương trình.")
            break
            
        print("Đang đợi 30 giây trước lần lấy tiếp theo...")
        time.sleep(30)

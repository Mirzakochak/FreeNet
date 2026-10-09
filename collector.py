import requests
import base64

# بهترین و معتبرترین منابع گیت‌هاب که مرتب آپدیت می‌شوند
sources = [
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/main/v2ray_sub.txt",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray"
]

# استفاده از set برای حذف خودکار کانفیگ‌های تکراری
configs = set()

print("Starting to collect configs...")

for url in sources:
    try:
        print(f"Fetching from: {url}")
        # گرفتن اطلاعات از لینک با محدودیت زمانی 15 ثانیه
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            # بررسی اینکه آیا متن خودش از قبل Base64 است یا متن ساده
            try:
                decoded_text = base64.b64decode(response.text).decode('utf-8')
                lines = decoded_text.splitlines()
            except Exception:
                lines = response.text.splitlines()
            
            # پیدا کردن کانفیگ‌های Vless و Vmess
            count = 0
            for line in lines:
                line = line.strip()
                if line.startswith("vless://") or line.startswith("vmess://"):
                    configs.add(line)
                    count += 1
            print(f"Found {count} configs in this source.")
        else:
            print(f"Error: Server returned status code {response.status_code}")
            
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

# اگر حداقل یک کانفیگ پیدا شد، فایل رو بساز
if configs:
    print(f"\nTotal unique configs collected: {len(configs)}")
    
    # چسباندن تمام کانفیگ‌ها به هم (هر کدام در یک خط)
    final_content = "\n".join(configs).encode("utf-8")
    
    # تبدیل کل لیست به فرمت استاندارد Base64 برای ساب‌لینک
    encoded_sub = base64.b64encode(final_content).decode("utf-8")

    # ذخیره اطلاعات داخل فایل sub.txt
    with open("sub.txt", "w") as f:
        f.write(encoded_sub)
        
    print("sub.txt updated successfully!")
else:
    print("\nNo vless/vmess configs found. File not updated.")

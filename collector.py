import requests
import base64
import random
import re

sources = [
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/main/v2ray_sub.txt",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/ts-sf/fly/main/v2",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2"
]

configs = set()

def decode_base64(text):
    # حذف تمام فاصله‌ها و اینترهای مخرب از رشته
    text = re.sub(r'\s+', '', text)
    # اضافه کردن پدینگ مساوی (=) برای جلوگیری از ارور دیکود
    missing_padding = len(text) % 4
    if missing_padding:
        text += '=' * (4 - missing_padding)
    try:
        return base64.b64decode(text).decode('utf-8', errors='ignore')
    except:
        return ""

print("شروع جمع‌آوری کانفیگ‌ها...")

for url in sources:
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            raw_text = response.text.strip()
            
            # تشخیص هوشمندانه: اگر متن ساده است یا Base64
            if "vless://" in raw_text or "vmess://" in raw_text:
                lines = raw_text.splitlines()
            else:
                decoded = decode_base64(raw_text)
                lines = decoded.splitlines()
            
            count = 0
            for line in lines:
                line = line.strip()
                if line.startswith("vless://") or line.startswith("vmess://"):
                    configs.add(line)
                    count += 1
            print(f"منبع {url.split('/')[-2]} -> پیدا شد: {count}")
    except Exception as e:
        print(f"خطا در منبع {url}: {e}")

# تبدیل مجموعه به لیست
configs_list = list(configs)
print(f"\nتعداد کل کانفیگ‌های بدون تکرار: {len(configs_list)}")

# به هم ریختن لیست برای میکس شدن منابع
random.shuffle(configs_list)

# جدا کردن دقیق 200 کانفیگ
final_configs = configs_list[:200]

if final_configs:
    final_content = "\n".join(final_configs).encode("utf-8")
    encoded_sub = base64.b64encode(final_content).decode("utf-8")

    with open("sub.txt", "w") as f:
        f.write(encoded_sub)
        
    print(f"فایل با موفقیت با {len(final_configs)} کانفیگ ساخته شد!")
else:
    print("هیچ کانفیگی پیدا نشد!")

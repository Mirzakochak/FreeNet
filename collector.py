import requests
import base64
import random
import re

# لیست منابع جدید با آپدیت‌های ساعتی و کیفیت بالاتر
sources = [
    "https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt",
    "https://raw.githubusercontent.com/pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/yebekhe/V2Hub/main/Split/Normal/vless",
    "https://raw.githubusercontent.com/yebekhe/V2Hub/main/Split/Normal/vmess",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vmess",
    "https://raw.githubusercontent.com/w17star/V2ray-Configs/main/Sub3.txt"
]

configs = set()

def decode_base64(text):
    text = re.sub(r'\s+', '', text)
    missing_padding = len(text) % 4
    if missing_padding:
        text += '=' * (4 - missing_padding)
    try:
        return base64.b64decode(text).decode('utf-8', errors='ignore')
    except:
        return ""

print("شروع جمع‌آوری کانفیگ‌ها از منابع جدید...")

for url in sources:
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            raw_text = response.text.strip()
            
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
            print(f"منبع {url.split('/')[-1]} -> پیدا شد: {count}")
    except Exception as e:
        print(f"خطا در منبع {url}")

configs_list = list(configs)
print(f"\nتعداد کل کانفیگ‌های بدون تکرار: {len(configs_list)}")

random.shuffle(configs_list)
final_configs = configs_list[:200]

if final_configs:
    final_content = "\n".join(final_configs).encode("utf-8")
    encoded_sub = base64.b64encode(final_content).decode("utf-8")

    with open("sub.txt", "w") as f:
        f.write(encoded_sub)
        
    print(f"فایل با موفقیت با {len(final_configs)} کانفیگ ساخته شد!")
else:
    print("هیچ کانفیگی پیدا نشد!")

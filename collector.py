import requests
import base64
import random

sources = [
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/main/v2ray_sub.txt",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray"
]

configs = set()

print("Starting to collect configs...")

for url in sources:
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            raw_text = response.text.strip()
            
            # برطرف کردن مشکل فاصله‌ها و فرمت در کدهای Base64 منابع
            clean_text = raw_text.replace('\n', '').replace('\r', '')
            clean_text += "=" * ((4 - len(clean_text) % 4) % 4) 
            
            try:
                decoded_text = base64.b64decode(clean_text).decode('utf-8')
                lines = decoded_text.splitlines()
            except Exception:
                # اگر سورس Base64 نبود، به صورت متن ساده بخوان
                lines = raw_text.splitlines()
            
            for line in lines:
                line = line.strip()
                if line.startswith("vless://") or line.startswith("vmess://"):
                    configs.add(line)
    except Exception as e:
        print(f"Failed to fetch: {url}")

# تبدیل به لیست برای انجام برش و انتخاب
configs_list = list(configs)
print(f"Total unique configs found: {len(configs_list)}")

# بُر زدن (مخلوط کردن) لیست تا کانفیگ‌های منابع مختلف ترکیب شوند
random.shuffle(configs_list)

# انتخاب دقیق ۲۰۰ کانفیگ اول از لیست مخلوط شده
final_configs = configs_list[:200]

if final_configs:
    print(f"Saving exactly {len(final_configs)} configs to sub.txt...")
    
    final_content = "\n".join(final_configs).encode("utf-8")
    encoded_sub = base64.b64encode(final_content).decode("utf-8")

    with open("sub.txt", "w") as f:
        f.write(encoded_sub)
        
    print("sub.txt updated successfully with 200 configs!")
else:
    print("No configs found!")

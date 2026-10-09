import requests
import base64

# لینک‌های خام (Raw) منابع معتبر را اینجا قرار بده
sources = [
    "https://raw.githubusercontent.com/example1/sub/main/sub.txt",
    "https://raw.githubusercontent.com/example2/sub/main/v2ray.txt"
]

configs = set()

for url in sources:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # بررسی اینکه آیا متن خودش از قبل Base64 است یا خیر
            try:
                decoded_text = base64.b64decode(response.text).decode('utf-8')
                lines = decoded_text.splitlines()
            except:
                lines = response.text.splitlines()
            
            for line in lines:
                # فیلتر کردن فقط کانفیگ‌های vless و vmess
                if line.startswith("vless://") or line.startswith("vmess://"):
                    configs.add(line.strip())
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

# تبدیل مجدد لیست کانفیگ‌های یکتا به فرمت Base64
final_content = "\n".join(configs).encode("utf-8")
encoded_sub = base64.b64encode(final_content).decode("utf-8")

# ذخیره در فایل متنی
with open("sub.txt", "w") as f:
    f.write(encoded_sub)

import time
import requests

def bark(title, content, is_url=False, is_critical=False):
    url = f"https://api.day.app/xxxxxxxx"
    headers = {"Content-Type": "application/json"}
    data = {"title": title, "body": content}
    if is_url:
        data["url"] = content
    if is_critical:
        data["level"] = "critical"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Bark sent successfully!")
    else:
        print("Failed to send bark. Waiting for retry...")
        time.sleep(2)  # 等待 5 秒后重试
        bark(title, content)

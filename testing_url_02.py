import requests

url = "https://www.hul.co.in/files/hul-integrated-annual-report-2024-25.pdf"

r = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
)

print(r.status_code)
print(r.headers.get("Content-Type"))
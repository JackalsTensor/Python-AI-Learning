import requests

def ip_location(ip=""):
    # 如果不填 IP，就是查自己当前公网 IP
    url = f"http://ip-api.com/json/{ip}?lang=zh-CN"

    try:
        res = requests.get(url, timeout=5)
        data = res.json()

        if data["status"] != "success":
            print("查询失败")
            return

        print("=" * 40)
        print("IP定位结果")
        print("=" * 40)
        print("IP地址:", data["query"])
        print("国家:", data["country"])
        print("地区:", data["regionName"])
        print("城市:", data["city"])
        print("运营商:", data["isp"])
        print("经纬度:", data["lat"], data["lon"])
        print("时区:", data["timezone"])
        print("=" * 40)

        # Google Maps 链接
        print("地图查看:")
        print(f"https://www.google.com/maps?q={data['lat']},{data['lon']}")

    except Exception as e:
        print("请求失败:", e)


# ======================
# 使用方式
# ======================

# 查自己公网 IP
ip_location()

# 查指定 IP（示例）
# ip_location("8.8.8.8")
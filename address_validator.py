import requests

url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Tresalonspa 718 Sutter St., Suite 105 Folsom California USA 95630&inputtype=textquery&key=AIzaSyDAe5M-G_DekBt1t52eauZY9zI14JZwSGU"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

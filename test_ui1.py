import urllib.request
try:
    res = urllib.request.urlopen('http://localhost:8000/ui1.html')
    print("ui1.html loaded")
except Exception as e:
    print(e)

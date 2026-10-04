import urllib.request
import urllib.error
import sys

req = urllib.request.Request('http://localhost:8000/api/evidence')
try:
    response = urllib.request.urlopen(req, timeout=5)
    print("Success:", response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Error body:", e.read().decode())
except Exception as e:
    print("Other error:", e)

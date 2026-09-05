import httpx
import datetime
start = "2023-01-01"
end = "2023-01-10"
# Agra
url = f"https://archive-api.open-meteo.com/v1/archive?latitude=27.1751&longitude=78.0421&start_date={start}&end_date={end}&daily=weathercode,temperature_2m_max,precipitation_sum&timezone=Asia/Kolkata"
r = httpx.get(url).json()
print(r)

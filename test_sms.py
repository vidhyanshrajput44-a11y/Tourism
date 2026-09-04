import httpx

FAST2SMS_API_KEY = "SKqTIuHbGPfVBDdZYcpOXeCsjNywmo7vMAgLt9F10z3RWhJ6iaOUfZTdXLM6tni0Ym8KuqV3GFNaBx2P"
phone = "9999999999" # Placeholder
otp_code = "123456"

url = "https://www.fast2sms.com/dev/bulkV2"
payload = f"variables_values={otp_code}&route=otp&numbers={phone}"
headers = {
    'authorization': FAST2SMS_API_KEY,
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
}

print("Sending request...")
response = httpx.post(url, data=payload, headers=headers)
print("Status:", response.status_code)
print("Response:", response.text)

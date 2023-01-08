from asyncio import tasks
import requests
import sys
import threading
import asyncio
import base64
import schedule
import time
import urllib.parse
import html

# Add support for testing different injection points, HTTP methods, and payload encodings
def test_xss(url, injection_point, payload, vuln_type, http_method, encoding):
  injection_point = injection_point
  headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Custom-Header": "custom value"
  }
  cookies = {
    "session_id": "abcdef123456"
  }
  proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
  }
  
  # Modify the request based on the injection point and HTTP method
  if injection_point == "url":
    if http_method == "get":
# Test for XSS vulnerability in URL parameter
      r = requests.get(url, params={injection_point: payload}, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
    elif http_method == "post":
      # Test for XSS vulnerability in URL parameter
      r = requests.post(url, data={injection_point: payload}, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
  elif injection_point == "header":
    if http_method == "get":

      if http_method == "get":
      # Test for XSS vulnerability in HTTP header
       headers["X-Custom-Header"] = payload
      r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
    elif http_method == "post":
      # Test for XSS vulnerability in HTTP header
      headers["X-Custom-Header"] = payload
      r = requests.post(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
  elif injection_point == "Cookie":
    if http_method == "get":
      # Test for XSS vulnerability in cookie
      cookies["X-Custom-Cookie"] = payload
      r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
    elif http_method == "post":
      # Test for XSS vulnerability in cookie
      cookies["X-Custom-Cookie"] = payload
      r = requests.post(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
  elif injection_point == "javascript":
    if http_method == "get":
      # Test for XSS vulnerability in JavaScript code
      if encoding == "base64":
        payload = base64.b64encode(payload.encode("utf-8")).decode("utf-8")
      elif encoding == "url":
        payload = urllib.parse.quote(payload)
      elif encoding == "html":
        payload = html.escape(payload)
      else:
        print(f"Invalid encoding: {encoding}")
      r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, auth=("user", "pass"))
  
  # Check the response for the payload
  if vuln_type == "reflected":
    if payload in r.text:
      print(f"XSS VULNERABILITY FOUND at {url} with payload {payload}")
    else:
      print(f"No XSS vulnerability found at {url} with payload {payload}")
  elif vuln_type == "persistent":
    # Check for persistent XSS vulnerability
    # TODO: Implement persistent XSS check
    pass
  else:
    print(f"Invalid vulnerability type: {vuln_type}")
  
  return r

async def scan(url, payloads, vuln_type, injection_point, http_method, encoding):
  tasks = []
  for payload in payloads:
    task = asyncio.ensure_future(test_xss(url, injection_point, payload, vuln_type, http_method, encoding))
    tasks.append(task)
  responses = await asyncio.gather(*tasks)
  return responses

def main(url, payloads_file, vuln_type, injection_point, http_method, encoding):
  with open(payloads_file, "r") as f:
    payloads = f.read().splitlines()
  loop = asyncio.get_event_loop()
  responses = loop.run_until_complete(scan(url, payloads, vuln_type, injection_point, http_method, encoding))
  return responses

if __name__ == "__main__":
  url = sys.argv[1]
  payloads_file = sys.argv[2]
  vuln_type = sys.argv[3]
  injection_point = sys.argv[4]
  http_method = sys.argv[5]
  encoding = sys.argv[6]
  main(url, payloads_file, vuln_type, injection_point, http_method, encoding)

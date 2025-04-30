import os

# Load SMTP accounts from smtp-credentials.txt
smtp_credentials_file = os.path.join(os.path.dirname(__file__), "smtp.txt")
smtp = []
with open(smtp_credentials_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line or ',' not in line:
            continue
        user, passwd = line.split(",", 1)
        smtp.append({
            "host": "smtp-relay.gmail.com",
            "port": 587,
            "auth": True,
            "user": user,
            "pass": passwd
        })

message = [
    {
        "fromName": "test",
        "fromEmail": "test",
        "subject": "‍test CASE#{random_number_4}",
    }
]

shortlink = [
    'http://ow.ly/y0vn50KNmxk',
    'http://ow.ly/UUXz50KNmxG',
    'http://ow.ly/jn4h50KNmy1',
]

send = {
    "delay": 3,           # seconds
    "pauseAfter": 10,     # pause after how many emails
    "pauseFor": 10,       # pause for how many seconds
    "useAmazonSES": False,
    "useHeader": False,
    "useAttach": False,
    "useHttpProxy": False,
    "text": "",           # plain text version of the email
    "letter": "letter.html",# HTML template file
    "list": "your-list.txt"
}

proxy = {
    "http": "87.228.103.111:8080"
}

attach = {
    "file": "letterms3.pdf"
}

custom_headers = {
    "KONTOL": "KONTOL"
}
import smtplib
import ssl
import time
import re
from email.message import EmailMessage
from colorama import Fore, Style, init
from datetime import datetime
import config
import random
import random_data

init(autoreset=True)
LIME = Fore.LIGHTGREEN_EX

banner = f"""{LIME}{Style.BRIGHT}
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║                   Python Sender By Bob Marley                      ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
print(banner)

print(f"{LIME}{Style.BRIGHT}How To Use:")
print(f"{LIME}{Style.BRIGHT}1. Prepare a text file with your target emails, one per line (see config.py for the filename).")
print(f"{LIME}{Style.BRIGHT}2. Prepare your HTML letter and set the filename in config.py.")
print(f"{LIME}{Style.BRIGHT}3. Prepare your SMTP credentials file and set the filename in config.py.")
print(f"{LIME}{Style.BRIGHT}4. Run the script: python main.py\n{Style.RESET_ALL}")

def get_date():
    return datetime.now().strftime("%b %d, %I:%M:%S %p")

def replace_tags(input_str, email):
    s = input_str
    s = s.replace("{email}", email)
    s = s.replace("{date}", get_date())
    s = s.replace("{random_ip}", random_data.ip())
    s = s.replace("{random_country}", random_data.country())
    s = s.replace("{random_device}", random_data.device())
    s = s.replace("{random_browser}", random_data.browser())
    s = s.replace("{random_subject}", random_data.subject())
    s = s.replace("{random_fnamazon}", random_data.fnamazon())
    s = s.replace("{random_fnpaypal}", random_data.fnpaypal())
    s = s.replace("{random_statement}", random_data.statement())
    s = s.replace("{random_shortlink}", random.choice(config.shortlink))

    s = re.sub(r"\{random_number_(\d+)\}", lambda m: random_data.number(int(m.group(1))), s)
    s = re.sub(r"\{random_letterup_(\d+)\}", lambda m: random_data.letterup(int(m.group(1))), s)
    s = re.sub(r"\{random_letterlow_(\d+)\}", lambda m: random_data.letterlow(int(m.group(1))), s)
    s = re.sub(r"\{random_letteruplow_(\d+)\}", lambda m: random_data.letteruplow(int(m.group(1))), s)
    s = re.sub(r"\{random_letternumberuplow_(\d+)\}", lambda m: random_data.letternumberuplow(int(m.group(1))), s)
    return s

def get_customised_message_template(email, html_template):
    msg_template = random.choice(config.message)
    return {
        "subject": replace_tags(msg_template["subject"], email),
        "fromName": replace_tags(msg_template["fromName"], email),
        "fromEmail": replace_tags(msg_template["fromEmail"], email),
        "text": replace_tags(config.send["text"], email),
        "html": replace_tags(html_template, email)
    }

def send_email(email, cnt, html_template, static_date, total):
    smtp_info = random.choice(config.smtp)
    context = ssl.create_default_context()
    msg_data = get_customised_message_template(email, html_template)
    msg = EmailMessage()
    msg["From"] = f'{msg_data["fromName"]} <{msg_data["fromEmail"]}>'
    msg["To"] = email
    msg["Subject"] = msg_data["subject"]
    msg.set_content(msg_data["text"])
    msg.add_alternative(msg_data["html"], subtype="html")

    if config.send.get("useHeader"):
        for k, v in config.custom_headers.items():
            msg[k] = v

    if config.send.get("useAttach"):
        gen_num = random.randint(10000, 99999)
        with open(config.attach["file"], "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=f"updatefile#{gen_num}.pdf")

    try:
        with smtplib.SMTP(smtp_info["host"], smtp_info["port"]) as server:
            if smtp_info.get("auth"):
                server.starttls(context=context)
                server.login(smtp_info["user"], smtp_info["pass"])
            server.send_message(msg)
        print(
            Fore.WHITE + " [+]" +
            Fore.CYAN + f" [{cnt+1}/{total}]" +
            Fore.YELLOW + f" [{get_date()}]" +
            Fore.GREEN + " [JustSender]" +
            Fore.WHITE + f" [{smtp_info.get('user', '')}]" +
            Fore.MAGENTA + f" [sent to :{email.strip()}]" +
            Fore.RED + f" Delay for {config.send['delay']} seconds... "
        )
    except Exception as e:
        with open(f"your-logs/your-failed-{static_date}.txt", "a") as logf:
            logf.write(f"failed => {email}\n")
        print(Fore.RED + f"Error sending to {email}: {e}")

def main():
    static_date = datetime.now().strftime("%Y%m%d%H%M%S")
    with open(config.send["list"], "r") as f:
        mailing_list = [line.strip() for line in f if line.strip()]
    with open(config.send["letter"], "r", encoding="utf-8") as f:
        html_template = f.read()

    print(Fore.WHITE + " [+]" + Fore.BLUE + f" is importing your mailing list from {Fore.CYAN}{config.send['list']}")
    print(Fore.WHITE + " [+]" + Fore.BLUE + f" taking html from {Fore.CYAN}{config.send['letter']}")
    print(Fore.WHITE + " [+]" + Fore.BLUE + " starting the sender engine ... ... ... ")

    for i, email in enumerate(mailing_list):
        send_email(email, i, html_template, static_date, len(mailing_list))
        if (i+1) % config.send["pauseAfter"] == 0:
            print(Fore.RED + f" [+] Paused for {config.send['pauseFor']} seconds after {config.send['pauseAfter']} emails")
            time.sleep(config.send["pauseFor"])
        else:
            time.sleep(config.send["delay"])

if __name__ == "__main__":
    main()
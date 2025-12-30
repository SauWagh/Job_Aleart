import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv
import os

EMAIL = os.environ['ADMIN_EMAIL']
APP_PASSWORD = os.environ['ADMIN_PASSWORD']


if not EMAIL or not APP_PASSWORD:
    raise ValueError("ADMIN_EMAIL or ADMIN_PASSWORD not set. Check GitHub Secrets.")


HEADERS = {"User-Agent" : "Mozilla/5.0"}

SEARCH_URLS = {
    "GaijinPot": "https://jobs.gaijinpot.com/job/index/lang/en?keywords={}",
    "JobsInJapan": "https://jobsinjapan.com/jobs/?search_keywords={}",
    "CareerCross": "https://www.careercross.com/en/job-search/result?keyword={}",
    "Daijob": "https://www.daijob.com/en/jobs/search?kw={}",
    "Wantedly": "https://www.wantedly.com/projects?keyword={}",
    "Indeed Japan": "https://jp.indeed.com/jobs?q={}&l=Japan",
    "Glassdoor Japan": "https://www.glassdoor.co.jp/Job/japan-{}-jobs-SRCH_IL.0,5_IN123.htm"
}

ROLE = [
    "AI Engineer 新卒",
    "Python Full Stack Developer 未経験",
    "Unity Game Developer Junior"
]

def fetch_jobs():
    jobs = set ()

    for role in ROLE:
        query = role.replace(" ", "+")

        for site, url in SEARCH_URLS.items():
            
            try:
                search_url = url.format(query)
                r = requests.get(search_url, headers=HEADERS, timeout=10)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")

                for a in soup.find_all("a",href = True):
                    link = a['href']
                    if any(word in link.lower() for word in ["job", "career", "recruit"]):
                        if link.startswith("/"):
                            base = search_url.split("/")[0] + "/" + search_url.split("/")[2]
                            link = base + link
                        jobs.add(f"{site}: {link}")

            except Exception:
                continue
    return list(jobs)[:25]

def send_email(links):
    body = "🇯🇵 JAPAN JOB ALERTS (FRESHERS)\n\n"
    
    if not links:
        body += "No new job found today"

    else:
        for link in links:
            body += link+ "\n\n"
    
    msg = MIMEText(body)
    msg["Subject"] = f"Job Alerts - {datetime.now().strftime('%d %b %Y')}"
    msg['From'] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    jobs = fetch_jobs()
    send_email(jobs)

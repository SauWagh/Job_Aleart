import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os
from urllib.parse import urljoin, urlparse

# ================== CONFIG ==================
EMAIL = os.environ.get("ADMIN_EMAIL")
APP_PASSWORD = os.environ.get("ADMIN_PASSWORD")

if not EMAIL or not APP_PASSWORD:
    raise ValueError("ADMIN_EMAIL or ADMIN_PASSWORD not set")

HEADERS = {"User-Agent": "Mozilla/5.0"}

COUNTRY_MODE = ["India", "Japan"]  # 🌏 India + Japan only

ROLE = [
    "AI Engineer",
    "Python Full Stack Developer",
    "Junior Software Developer",
    "Unity Game Developer"
]

SEARCH_URLS = {
    # INDIA
    "Indeed India": "https://in.indeed.com/jobs?q={}&l=India",
    "Naukri": "https://www.naukri.com/{}-jobs",
    "Foundit": "https://www.foundit.in/search/{}",
    "Freshersworld": "https://www.freshersworld.com/jobs/jobsearch/{}",

    # JAPAN
    "GaijinPot": "https://jobs.gaijinpot.com/job/index/lang/en?keywords={}",
    "JobsInJapan": "https://jobsinjapan.com/jobs/?search_keywords={}",
    "Daijob": "https://www.daijob.com/en/jobs/search?kw={}",
    "Indeed Japan": "https://jp.indeed.com/jobs?q={}&l=Japan"
}

JOB_KEYWORDS = ["job", "career", "recruit", "position", "opening"]
BLOCK_KEYWORDS = ["login", "signup", "privacy", "terms", "ads", "blog"]

# ================== JOB FETCH ==================
def is_valid_job_link(link):
    link = link.lower()
    if not link.startswith("http"):
        return False
    if any(bad in link for bad in BLOCK_KEYWORDS):
        return False
    return any(word in link for word in JOB_KEYWORDS)

def fetch_jobs():
    jobs = set()

    for role in ROLE:
        query = role.replace(" ", "+")

        for site, url in SEARCH_URLS.items():
            try:
                search_url = url.format(query)
                r = requests.get(search_url, headers=HEADERS, timeout=12)
                r.raise_for_status()

                soup = BeautifulSoup(r.text, "html.parser")

                for a in soup.find_all("a", href=True):
                    link = urljoin(search_url, a["href"])

                    if is_valid_job_link(link):
                        domain = urlparse(link).netloc
                        jobs.add(f"{site} | {domain}\n{link}")

            except Exception:
                continue

    return sorted(jobs)[:30]

# ================== EMAIL ==================
def send_email(job_links):
    body = "🔥 DAILY JOB ALERTS (INDIA + JAPAN)\n\n"

    if not job_links:
        body += "No new jobs found today."
    else:
        for job in job_links:
            body += job + "\n\n"

    msg = MIMEText(body)
    msg["Subject"] = f"Job Alerts - {datetime.now().strftime('%d %b %Y')}"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

# ================== MAIN ==================
if __name__ == "__main__":
    jobs = fetch_jobs()
    send_email(jobs)

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

# Some urls for searching Jobs
SEARCH_URLS = {  
    "GaijinPot": "https://jobs.gaijinpot.com/job/index/lang/en?keywords={}",
    "JobsInJapan": "https://jobsinjapan.com/jobs/?search_keywords={}",
    "CareerCross": "https://www.careercross.com/en/job-search/result?keyword={}",
    "Daijob": "https://www.daijob.com/en/jobs/search?kw={}",
    "Wantedly": "https://www.wantedly.com/projects?keyword={}",
    "Indeed Japan": "https://jp.indeed.com/jobs?q={}&l=Japan",
    "Glassdoor Japan": "https://www.glassdoor.co.jp/Job/japan-{}-jobs-SRCH_IL.0,5_IN123.htm"
}

# Some KEy Role 
ROLE = [ 
    "AI Engineer 新卒",
    "Python Full Stack Developer 未経験",
    "Unity Game Developer Junior"
]

def fetch_jobs():
    jobs = set () # Create Empty set

# loop through job with role and add replace space + 
    for role in ROLE:
        query = role.replace(" ", "+")

# loop through urls that mention in SEARCH_URLS
        for site, url in SEARCH_URLS.items():
            
            #insert the search keyword in website URL
            try:
                search_url = url.format(query)

                #send a GET request to website
                r = requests.get(search_url, headers=HEADERS, timeout=10)
                r.raise_for_status()

                #Convert raw HTML into searchable Contain
                soup = BeautifulSoup(r.text, "html.parser")

                # find all <a>
                for a in soup.find_all("a",href = True):

                    #Extract the actual link URL form <a>
                    link = a['href']

                    #Filter Job
                    if any(word in link.lower() for word in ["job", "career", "recruit"]):

                        #give relative URLs
                        if link.startswith("/"):
                            base = search_url.split("/")[0] + "/" + search_url.split("/")[2]
                            link = base + link

                        #Add job link to Set
                        jobs.add(f"{site}: {link}")

            #if any website fail its skip and Continue
            except Exception:
                continue

    #Convert set to list
    return list(jobs)[:25]

#create email body and add title
def send_email(links):
    body = "🇯🇵 JOB ALERTS (FRESHERS)\n\n"
    
    #if job is not found still its send mail anyway
    if not links:
        body += "No new job found today"

    # add all jobs into mail
    else:
        for link in links:
            body += link+ "\n\n"
    
    #Covert text into email formate
    msg = MIMEText(body)

    #add subject with today date
    msg["Subject"] = f"Job Alerts - {datetime.now().strftime('%d %b %Y')}"

    #send email  
    msg['From'] = EMAIL
    msg["To"] = EMAIL

    #connect with SMPT Server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        #login using email and pass
        server.login(EMAIL, APP_PASSWORD)

        #Send Email
        server.send_message(msg)

#make sure code run when script is executed
if __name__ == "__main__":

    #get all job link and send mail
    jobs = fetch_jobs()
    send_email(jobs)

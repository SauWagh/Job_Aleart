# Job_Aleart Bot

### Job alert Bot is Python based automation tool that find job from multiple job Portal and sends daily job alert through email

<hr>

## How it Work

  1. Job Search
     - Searching multiple job portals using predefined Keywords (freshers/junior roles/developer)
       
  2. Web Serching
     - Parses HTML content using BeautifulSoup
     - Extracts job related links
     - Filters duplicates and irrelevant links
    
  3. Automation
     - Github Action Runs the Script daily using a corn schedule
     - No local machine dependency
    
  4. Email
     - Sends collected job links via Gmail SMTP
     - Credentials are securely stored using GitHub Secrets

<hr>

## Tech
  1. python
  2. BeautifulSoup4 – Web scraping
  3. Requests – HTTP requests
  4. smtplib – Email sending
  5. GitHub Actions – Automation
  6. Cron Jobs – Scheduling
  7. 
<hr>

## Bot Runs automatically every day at 11:00 AM
    11:00 AM IST (05:30 UTC)
    
<hr>

## Add email and password in Environment Variables
     ADMIN_EMAIL --- add your email
     ADMIN_PASSWORD --- add email App Password
     

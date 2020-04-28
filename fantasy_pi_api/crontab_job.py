from crontab import CronTab
import subprocess
import os

out = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
user = out.communicate[0]
user = str(user, encoding="utf-8")[0:-1]

cron = CronTab(user=user)
cron.remove_all()
job = cron.new(
    command="python3 /home/ubuntu/fantasy_portfolio_investment/fantasy_pi_api/api_base.py"
)
job.minute.on("2")
job.hour.also.on("13", "14", "15", "16", "17", "18", "19", "20")
job.dow.on(1, 2, 3, 4, 5, 6, 7)
cron.write()

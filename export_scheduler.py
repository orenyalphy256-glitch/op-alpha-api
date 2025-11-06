from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

sched = BlockingScheduler()

def job():
    subprocess.run(["python", "export_contacts.py"])

sched.add_job(job, "interval", minutes=5)
sched.start()
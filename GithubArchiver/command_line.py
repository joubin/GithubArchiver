#!/usr/bin/env python
import time

from GithubArchiver.GithubArchiver import run_main
import os
import schedule


def main():
    if "true" in os.getenv("GITHUBARCHIVER_RUNDAILY"):
        run_main()
        schedule.every().day.at("01:00").do(run_main)
        while True:
            schedule.run_pending()
            time.sleep(3600)
    else:
        run_main()

import os
import pandas
import smtplib
import datetime as dt
from random import randint
##################### Extra Hard Starting Project ######################
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
HOST_ADDRESS = "smtp.gmail.com"
PORT_NUMBER = 587

this_moment = dt.datetime.now()
today_date = this_moment.day
current_month = this_moment.month
PLACEHOLDER = "[NAME]"

# 1. Update the birthdays.csv
#       Done...

# 2. Check if today matches a birthday in the birthdays.csv
birthdays_df = pandas.read_csv("birthdays.csv")
for (index, row) in birthdays_df.iterrows():
    entity_name = row.entity_name.strip()
    if current_month == row.month and today_date == row.day:
        # 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's
        #    actual name from birthdays.csv
        template_letter_number = randint(1,6)
        with open(f"../Automated Birthday Wisher/letter_templates/letter_{template_letter_number}.txt") as temp_letter:
            letter_to_send = temp_letter.read()
            letter_to_send = letter_to_send.replace(PLACEHOLDER, entity_name)

        # 4. Send the letter generated in step 3 to that person's email address.
        with smtplib.SMTP(host=HOST_ADDRESS, port=PORT_NUMBER) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL_ADDRESS, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL_ADDRESS,
                to_addrs=row.email,
                msg=f"Subject:Happy Birthday!\n\n{letter_to_send}")

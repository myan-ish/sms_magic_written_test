from datetime import datetime, time
import re
import smtplib
import pytz
from email.message import EmailMessage
from decouple import config

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

schedule_message = []
status_file = "status.txt"


def read_from_csv(filename):
    with open(filename, "r") as f:
        data = f.read()

        # Remove the first line
        data = data.split("\n")[1:]

        return data


def validate_phone_number(phone_number):
    if len(phone_number) != 10:
        return False

    if not phone_number.isdigit():
        return False

    return True


def validate_email(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def verify_message(message):
    if len(message) > 160 or len(message) < 1:
        return False
    return True


def working_time(now):
    start = time(10)
    end = time(17)
    now = time(now)
    if start <= end:
        return start <= now < end
    else:
        return start <= now or now < end


def send_message_to_email(email, message):
    print("Validating email")
    if not validate_email(email):
        print("Invalid email")
        with open(status_file, "a") as f:
            f.write(f"Failed to send message to {email}, email not valid" + "\n")
        return

    print("Sending message to email: " + email)
    print("Message: " + message)

    sender_email = "ranaxmond@gmail.com"
    receiver_email = email

    email = EmailMessage()
    email.set_content(message, subtype="html")

    to = receiver_email
    email["From"] = sender_email
    email["To"] = to
    email["Subject"] = "Test Message"

    server = smtplib.SMTP("localhost", 1025)
    server.sendmail(sender_email, to, email.as_string())
    server.quit()

    # server = smtplib.SMTP("smtp.elasticemail.com", 2525)
    # password = config("AUTH_PASSWORD")
    # if password is None:
    #     print("Set the password in the environment variable AUTH_PASSWORD")
    #     return
    # server.login(sender_email, password)
    # server.sendmail(sender_email, to, email.as_string())
    # server.quit()

    with open(status_file, "a") as f:
        f.write(f"Email sent successfully to {receiver_email}" + "\n")


def send_message_as_SMS(phone_number, message):
    print("Validating phone number")

    if not validate_phone_number(phone_number):
        print("Invalid phone number")
        with open(status_file, "a") as f:
            f.write(f"Failed to send SMS to {phone_number}, phone not valid" + "\n")
        return

    print("Sending message to phone number: " + phone_number)
    print("Message: " + message)

    import requests

    url = "https://api.txtbox.in/v1/sms/send"
    payload = "mobile_number=9552772600&sms_text=helloWorld&sender_id=market"
    headers = {
        "apiKey": "9f81fddf27be1aa3e73a0619392cbc0c",
        "content-type": "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    with open(status_file, "a") as f:
        f.write(f"Success to send SMS to {phone_number}, {response.text}" + "\n")


def schedule_or_send_message_and_email(message, email, phone_number, country, date):
    # verify message
    if True:
        if not verify_message(message):
            print("Message is not valid")
            with open(status_file, "a") as f:
                f.write(
                    f"Failed to send SMS to {phone_number}, message not valid" + "\n"
                )
                f.write(f"Failed to send message to {email}, message not valid" + "\n")
            return

    # Check for schedule date
    if date == "":
        # Send message and email immediately since date is not specified
        send_message_to_email(email, message)
        send_message_as_SMS(phone_number, message)
    else:
        # Check if date is in the future we can schedule the message

        # We also should check the timezones of the user and send mail accordingly
        if country == "INDIA":
            india_timezone = pytz.timezone("Asia/Kolkata")
            country_date = (datetime.now(india_timezone)).strftime("%d/%m/%Y")
            country_time = int((datetime.now(india_timezone)).strftime("%H"))

            if country_date == date:

                # Since sending email is not a time sensitive task, we can send it immediately
                send_message_to_email(email, message)

                # Check if it is working time in India and send SMS
                if working_time(country_time):
                    send_message_as_SMS(phone_number, message)
                else:
                    with open(status_file, "a") as f:
                        f.write(
                            f"Pending SMS for {phone_number}, Scheduled for another time."
                            + "\n"
                        )
                    schedule_message.append(
                        (message, email, phone_number, country, date)
                    )
            else:
                print("Scheduled for another time")
                schedule_message.append((message, email, phone_number, country, date))
                with open(status_file, "a") as f:
                    f.write(f"Pending for {phone_number}, not working time" + "\n")

        elif country == "USA":
            usa_timezone = pytz.timezone("America/New_York")
            country_date = (datetime.now(usa_timezone)).strftime("%d/%m/%Y")
            country_time = int((datetime.now(usa_timezone)).strftime("%H"))
            if country_date == date:

                # Since sending email is not a time sensitive task, we can send it immediately
                send_message_to_email(email, message)

                # Check if it is working time in USA and send SMS
                if working_time(country_time):
                    send_message_as_SMS(phone_number, message)

                else:
                    with open(status_file, "a") as f:
                        f.write(
                            f"Pending for {phone_number}, Scheduled for another time."
                            + "\n"
                        )
                    schedule_message.append(
                        (message, email, phone_number, country, date)
                    )
            else:
                print("Scheduled for another time")
                schedule_message.append((message, email, phone_number, country, date))
                with open(status_file, "a") as f:
                    f.write(f"Pending for {phone_number}, not working time" + "\n")


def parse_single_row(row):
    row = row.split(",")
    return row[0], row[1], row[2], row[3], row[4]


if __name__ == "__main__":
    print("Reading from CSV file")
    data = read_from_csv("Sample.csv")

    print("Parsing data")
    for row in data:
        message, email, phone_number, country, date = parse_single_row(row)
        schedule_or_send_message_and_email(message, email, phone_number, country, date)

        # write schedule_message to a file
        with open("schedule_message.txt", "w") as f:
            f.write(str(schedule_message))

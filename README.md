# sms-magic
Here I am using basic python to complete assignment version 1.

# Installation

- [X] Clone this repository
- [X] After installation navigate to the project directory

Generally creating a virtual enviornment is recommended.
```pythom -m venv venv```

Then activate the venv and install the requirements.
```pip install -r requirements.in```
You should be ready to go.

# Understanding the project
All of the messages(Success/Faliure) are saved in ```status.txt```

![image](https://user-images.githubusercontent.com/48282663/210089610-37eef7f8-329c-49eb-991a-73ac3011f785.png)


Messages that aren't send during the time are saved into ```scheduled_message.txt```

![image](https://user-images.githubusercontent.com/48282663/210089682-49da02b0-b719-4059-8e1b-8da0bddfa320.png)



I am using elastic mail to send the message in real time which is done https://github.com/myan-ish/sms-magic/blob/946d2a54bcc863ab3a8f3139575871eefe25bb4e/main.py#L89, which can be seen here.

![image](https://user-images.githubusercontent.com/48282663/210089080-af2377bd-adae-44a9-a784-39c55492e3b0.png)
For that to happend I needed a working email so I did make a few changes in the csv. However I configured the credentials for getting accessing the smtp server into a env file so that might not be accessiable so you can use ```python -m smtpd -c DebuggingServer -n localhost:1025``` this command to host a local SMTP server and uncomment these lines https://github.com/myan-ish/sms-magic/blob/946d2a54bcc863ab3a8f3139575871eefe25bb4e/main.py#L79 to get similar output.

![image](https://user-images.githubusercontent.com/48282663/210089517-de6d1223-92d7-42a9-bb88-021c11aed40d.png)
 

The sms portion should also be workin which is implemented https://github.com/myan-ish/sms-magic/blob/946d2a54bcc863ab3a8f3139575871eefe25bb4e/main.py#L116
I couldn't make futher tests because I don't have an Indian carrier.


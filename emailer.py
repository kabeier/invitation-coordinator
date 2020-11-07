from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from meetings import MeetingMaker
#####Get email addresses and email content varibles

port = 465  # For SSL
password = "INSERT PASS WORD HERE" #####INSERT ACCOUNT PASSWORD HERE
smtp_server = "smtp.gmail.com"
sender_email = "TestKitDummy25@gmail.com"
dicts=MeetingMaker.return_dict()
for adict in dicts:
    country = adict['name']
    receiver_email = ', '.join(
        [email for email in adict['attendees']])
    date=adict['startDate']
    #####Send Emails
    message = MIMEMultipart("alternative")
    message["Subject"] = "Our Partners Meeting is Scheduled"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Hi,
    As you already know we are getting as many of the partners from {country} together for a meeting.
    We have found the dates what work best for the majority of the partners.
    Congratulations we made the date work for you.  
    Please report to the Hilton in you country's capitol for the two day conference starting on {date}
    """
    html = f"""\
    <html>
    <body>
        <p>
            <h3>Hi,</h3>
            As you already know we are getting as many of the partners from {country} together for a meeting.
            We have found the dates what work best for the majority of the partners.
            <h4>Congratulations we made the date work for you.  </h4>
            Please report to the Hilton in you country's capitol for the two day conference starting on <b> {date} </b>
        </p>
    </body>
    </html>
    """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

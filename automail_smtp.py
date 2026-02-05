import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    smtp_server,
    smtp_port,
    sender_email,
    sender_password,
    to_emails,
    cc_emails,
    subject,
    body
):
    """
    Send an email with TO, CC, and BCC.
    """

    # Create email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(to_emails)
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # All recipients (important for CC & BCC delivery)
    all_recipients = to_emails + cc_emails  

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, all_recipients, msg.as_string())
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Failed to send email:", e)



send_email(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    sender_email="vermatest4141@gmail.com",
    sender_password="bgcc xrpx urvt paka",
    to_emails=["djverma6893@gmail.com"],
    cc_emails=["vermaji6893@gmail.com"],
    
    subject="Test Mail by verma",
    body="Hello,\n\nThis is an automated email.\n\nRegards"
)
# bcc_emails=["bcc1@gmail.com"],
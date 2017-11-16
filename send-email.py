#!/usr/bin/python
import argparse
import smtplib
from email.mime.text import MIMEText

def main():
    parser = argparse.ArgumentParser(
        description='send email with gmail from command line')
    parser.add_argument('-r', help='recipient of message', required=True)
    parser.add_argument('-u', help='username for gmail account', required=True)
    parser.add_argument('-p', help='password for gmail account', required=True)
    parser.add_argument('-s', help='subject of the email', required=True)
    parser.add_argument('-b', help='body of the email, example: <html><body>this is the body</body></html>', required=True)

    args = parser.parse_args()

    send_email(args.u, args.p, args.r, args.s, args.b)

def send_email(user, pwd, recipient, subject, body):
    try:
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = user
        msg['To'] = recipient

        # sending
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(user, pwd)
        send_it = session.sendmail(user, recipient, msg.as_string())
        session.quit()
    except Exception, e:
        print 'failed to send mail:\n{0}'.format(e)

if __name__ == '__main__':
    main()

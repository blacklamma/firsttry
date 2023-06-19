from django.utils import timezone
import datetime
from .models import *
from huey import crontab
from huey.contrib.djhuey import task, periodic_task
import smtplib
import imaplib
import email
import smtplib
from email.mime.text import MIMEText


@periodic_task(crontab(minute='*/2'))
def read_email_from_gmail():
    try:
        email_conf = EmailToTicketConf.objects.filter(is_deleted=False)
        if email_conf:
            email_config = email_conf[0]
            email_id = email_config.email_id
            email_pass = email_config.password
            smtp_port = email_config.smtp_host_port
            smtp_server = email_config.email_server
            mail = imaplib.IMAP4_SSL(smtp_server, port=smtp_port)
            mail.login(email_id, email_pass)
            mail.select('inbox')

            data = mail.search(None, '(UNSEEN)')
            mail_ids = data[1]
            id_list = mail_ids[0].split()

            for id in id_list:
                data = mail.fetch(id, '(RFC822)')
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1], 'utf-8'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        incoming_obj = IncomingEmails()
                        incoming_obj.status = 1
                        incoming_obj.from_address = email.utils.parseaddr(email_from)[
                            1]
                        incoming_obj.subject = email_subject
                        try:
                            if not msg.is_multipart():
                                incoming_obj.content = msg.get_payload()
                            else:
                                message_data = msg.get_payload()
                                if message_data:
                                    incoming_obj.content = message_data[0].get_payload(
                                        decode=True).decode()
                        except:
                            pass
                        incoming_obj.received_time = datetime.datetime.now(
                            tz=timezone.utc)
                        incoming_obj.save()
    except Exception as e:
        print(str(e))


@periodic_task(crontab(minute='*/2'))
def send_email():
    try:
        smtp_conf_obj = SMTPConf.objects.filter(is_deleted=False)
        if smtp_conf_obj:
            smtp_conf = smtp_conf_obj[0]
            sender = smtp_conf.host_email
            password = smtp_conf.host_password
            host_port = smtp_conf.host_port
            host_name = smtp_conf.host_name
            outgoing_mails_obj = OutgoingEmails.objects.filter(
                status=(OutgoingEmails.PENDING), is_deleted=False).order_by('-id')[:10:1]
            for outgoing_email in outgoing_mails_obj:
                outgoing_email.status = OutgoingEmails.PROCESSING
                outgoing_email.save()
            with smtplib.SMTP_SSL(host_name, host_port) as smtp_server:
                smtp_server.login(sender, password)
                for outgoing_email in outgoing_mails_obj:
                    try:
                        msg = MIMEText(outgoing_email.content)
                        msg['Subject'] = outgoing_email.subject
                        msg['From'] = sender
                        recipients = outgoing_email.to_address
                        msg['To'] = recipients
                        smtp_server.sendmail(
                            sender, recipients, msg.as_string())
                        outgoing_email.status = OutgoingEmails.SUCCESS
                        outgoing_email.save()
                    except Exception as err:
                        outgoing_email.status = OutgoingEmails.ERROR
                        outgoing_email.save()
    except Exception as err:
        print(str(err))

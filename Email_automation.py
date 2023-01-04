import smtplib
from itertools import cycle
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from time import gmtime, strftime
import time

def get_senders(filename):
    #global sender_email
    sender_email = []
    #global password
    password = []
    with open(filename, mode='r', encoding='utf-8') as sender_file:
        for line in sender_file:
            sender_email.append(line.split()[0])
            password.append(line.split()[1])
    return sender_email, password

def get_targets(filename):
    #global target_email
    target_email = []

    with open(filename, mode='r', encoding='utf-8') as target_file:
        for line in target_file:
            target_email.append(line.split()[0])

    return target_email



def main():


    sender_email, password = get_senders('from.txt')
    target_email = get_targets('to.txt')

    file=open('body.txt', 'r')   #define email body
    body=file.read()

    zip_list = zip(target_email, cycle(sender_email),cycle(password)) if len(target_email) > len(sender_email) else zip(target_email, sender_email,password)


    for email_t, email_s,passwd in zip_list:

        # set up the SMTP server
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        print ("loging in",email_s)
        s.login(email_s, passwd)

        msg = MIMEMultipart()       #create a message

        # setup the parameters of the message
        msg['From']=' "Norton" '
        print('sending from', email_s)
        msg['To']=email_t
        print('sending to', email_t)

        msg['Subject']="Thanks for your order VFH76 987TRD_00"
        # add in the message body
        msg.attach(MIMEText(body, 'plain'))
        
        #Define the file to attach
        filename  = "NOR-LL 360-2 .pdf"
        
        #Open the file in python as a binary
        attachment= open(filename, 'rb') # r for read and b for binary
        
        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        print(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        s.quit()
        time.sleep(2)
if __name__ == '__main__':
    main()

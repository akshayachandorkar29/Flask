"""
This file contains mail information
Author: Akshaya Revaskar
Date: 12/04/2020
"""
from flaskblog import app, mail


class SendMail:

    def send_mail(self, msg):

        mail.send(msg)
        return "Sent"

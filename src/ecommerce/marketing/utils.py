import hashlib
import json
import requests
import re
from django.conf import settings

MAILCHIMP_API_KEY = getattr(settings,"MAILCHIMP_API_KEY",None)
MAILCHIMP_DATA_CENTER = getattr(settings,"MAILCHIMP_DATA_CENTER",None)
MAILCHIMP_EMAIL_AUDIENCE_ID = getattr(settings, "MAILCHIMP_EMAIL_AUDIENCE_ID",None)

def check_email(email):
    if not re.match(r".+@.+\..+",email):
        raise ValueError("String passed is not a valid email address")
    return email

def get_subscriber_hash(member_email):
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()

class Mailchimp(object):
    def __init__(self):
        super(Mailchimp,self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(dc=MAILCHIMP_DATA_CENTER)
        self.audience_id = MAILCHIMP_EMAIL_AUDIENCE_ID
        self.audience_endpoint = "{api_url}/lists/{list_id}".format(api_url=self.api_url,list_id=self.audience_id)

    def get_members_endpoint(self):
        return self.audience_endpoint+"/members"


    def change_subcription_status(self,email, status="unsubscribed"):
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint()+"/"+hashed_email
        data = {"status":self.check_valid_status(status)}
        r = requests.put(endpoint, auth=("",self.key), data=json.dumps(data))
        return r.json()


    def check_subcription_status(self,email):
        hashed_email = get_subscriber_hash(email)
        # print(hashed_email)
        endpoint = self.get_members_endpoint()+"/"+hashed_email
        r = requests.get(endpoint,auth=("",self.key))
        return r.json()

    def check_valid_status(self,status):
        choices = ['subscribed','unsubscribed','cleaned','pending']
        if status not in choices:
            raise ValueError("Not a valid choice for a email status")
        return status

    def add_email(self,email):
        status = "subscribed"
        self.check_subcription_status(status)
        data = {
            "email_address": email,
            "status": status,
        }
        endpoint = self.get_members_endpoint()
        print(endpoint)
        r = requests.post(endpoint, auth=("",self.key), data=json.dumps(data))

        return r.json()

    def ubsubcribed(self, email):
        return self.change_subcription_status(email,status="unsubscribed")

    def subcribed(self,email):
        return self.change_subcription_status(email,status="subscribed")

    def pending(self,email):
        return self.change_subcription_status(email,status="pending")
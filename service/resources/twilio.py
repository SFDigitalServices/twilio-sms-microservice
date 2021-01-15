""" Twilio SMS """
import os
import json
import falcon
import jsend
import pandas as pd
from .hooks import validate_access
from twilio.rest import Client

@falcon.before(validate_access)
class TwilioService():
    """ Email service """
    def on_post(self, req, resp):
        """ Implement POST """
        request_body = req.bounded_stream.read()
        json_params = json.loads(request_body)
        data = json_params["submission"]
        if data and data["data"] and data["data"]["notifyMeByTextMessage"]:

            _from_number = os.environ.get('TWILIO_FROM')
            _to_number = data["data"]["phoneNumber"]
            _message = self.get_sms(data)
            # Update .env with Live Credentials to send actual sms
            account_sid = os.environ.get('TWILIO_SID')
            auth_token = os.environ.get('TWILIO_TOKEN')

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                to=_to_number,
                from_=_from_number, #test From number from twilio
                body=_message)
            if message.sid:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(jsend.success({
                    'message': 'SMS sent!'
                }))
            else:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(jsend.fail({
                    'message': 'Failed to send SMS'
                }))

    @staticmethod
    def get_sms(submission):
        """ get sms message from template """
        dataframe = pd.json_normalize(submission, sep='.')
        lst = dataframe.to_dict(orient='list')

        # default
        with open('service/templates/sms.txt', 'r') as file_obj:
            sms = file_obj.read()

        lang = submission["data"]["whatIsYourPreferredLanguage"]
        sms_path = "service/templates/sms_{0}.txt".format(lang)
        if os.path.exists(sms_path):
            with open(sms_path, 'r') as file_obj:
                sms = file_obj.read()

        for field, value in lst.items():
            sms = sms.replace("{{ "+field+" }}", str(value[0]))

        return sms

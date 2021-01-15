""" Twilio SMS """
import os
import json
import falcon
import jsend
import twilio
from .hooks import validate_access
from twilio.rest import Client

@falcon.before(validate_access)
class TwilioService():
    """ Email service """
    def on_post(self, req, resp):
        """ Implement POST """
        request_body = req.bounded_stream.read()
        json_params = json.loads(request_body)
        print(json_params)
        if json_params["submission"] and json_params["submission"]["data"]:
            _from_number = os.environ.get('TWILIO_FROM')
            _to_number = json_params["submission"]["data"]['phoneNumber']
            print(_to_number)
            _message = 'Successfully sign up for vaccination notification!'
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

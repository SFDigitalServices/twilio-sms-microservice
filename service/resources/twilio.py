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
        data = json.loads(req.stream.read())

        _to_number = data['to_number']
        _message = data['message']
        # Update .env with Live Credentials to send actual sms
        account_sid = os.environ.get('TWILIO_SID')
        auth_token = os.environ.get('TWILIO_TOKEN')

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to=_to_number,
            from_="+15005550006", #test From number from twilio
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

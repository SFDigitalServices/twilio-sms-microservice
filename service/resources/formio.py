"""formio module"""
#pylint: disable=too-few-public-methods
import os
import requests

class Formio():
    """Submission class"""

    api_key = os.environ.get('FORMIO_APIKEY')
    url = os.environ.get('FORMIO_URL')

    @classmethod
    def delete_submission(cls, _fn, submission_id):
        """helper function for deleting a submission on formio"""

        delete_url = Formio.url + '/' + _fn + '/submission/' + str(submission_id)
        payload = {}
        files = {}
        headers = {
            'x-token': Formio.api_key
        }
        try:
            response = requests.request("DELETE", delete_url, headers=headers, \
                data=payload, files=files)
            return response
        except requests.exceptions.RequestException as err:
            print("deletion error:")
            print("{0}".format(err))
            return None

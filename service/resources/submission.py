"""Submission module"""
#pylint: disable=too-few-public-methods
import json
import os
from dateutil import tz
import falcon
import jsend
from .hooks import validate_access
from .models import create_submission
from .formio import Formio

LOCAL_TZ = tz.gettz("America/Los_Angeles")

@falcon.before(validate_access)
class Submission():
    """Submission class"""

    def on_post(self, _req, resp, _fn):
        #pylint: disable=no-self-use
        """
            Record post into the database
        """
        try:
            request_body = _req.bounded_stream.read()
            json_params = json.loads(request_body)
            # pylint: disable=no-member
            if json_params["submission"] and json_params["submission"]["data"]:
                submission = create_submission(self.session, json_params["submission"]["data"], _fn)

                if submission and submission.id:
                    resp.status = falcon.HTTP_200
                    resp.body = json.dumps(jsend.success({
                        'submission_id': submission.id,
                        'date_created': submission.date_created.astimezone(LOCAL_TZ).strftime(
                            "%Y/%m/%d, %H:%M:%S"
                        )
                    }))

                    # delete record on form.io
                    if os.environ.get('PURGE_FORMIO_DATA') == 'True':
                        formio_submission_id = json_params["submission"]["_id"]
                        formio = Formio()
                        deletion = formio.delete_submission(_fn, formio_submission_id)
                        # deletion failed, handle it gracefully
                        if deletion is None:
                            resp.status = falcon.HTTP_100
                            resp.body = json.dumps(jsend.fail({
                                'message': 'Failed to delete submission',
                                'submission_id': submission.id
                                }))
                            #raise Exception
                else:
                    resp.status = falcon.HTTP_400
                    resp.body = json.dumps(jsend.fail({
                        'message': 'Error sending data to database',
                        'timestamp': submission.date_created.astimezone(LOCAL_TZ).strftime(
                            "%Y/%m/%d, %H:%M:%S"
                        )
                    }))
        except Exception as err: # pylint: disable=broad-except
            print("error:")
            print("{0}".format(err))
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(jsend.error("{0}".format(err)))

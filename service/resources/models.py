"""Data Models"""
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

BASE = declarative_base()

def create_models(_fn):
    """helper function for creating SubmissionModel"""
    class SubmissionModel(BASE):
        # pylint: disable=too-few-public-methods
        """Map Submission object to db"""

        __tablename__ = _fn
        __table_args__ = {'extend_existing': True}

        id = sa.Column(sa.Integer, primary_key=True)
        data = sa.Column(sa.JSON, nullable=False)
        date_created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())

    return SubmissionModel

def create_submission(db_session, json_data, _fn):
    """helper function for creating a submission"""

    SubmissionModel = create_models(_fn)
    submission = SubmissionModel(data=json_data, date_created=func.now())

    try:
        db_session.add(submission)
        db_session.commit()
        return submission
    except SQLAlchemyError as err:
        print("create submission error:")
        print("{0}".format(err))
        return None

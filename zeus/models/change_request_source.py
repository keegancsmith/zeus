from zeus.config import db
from zeus.db.types import GUID
from zeus.utils import timezone


class ChangeRequestSource(db.Model):
    change_request_id = db.Column(
        GUID, db.ForeignKey('change_request.id'), primary_key=True)
    source_id = db.Column(
        GUID, db.ForeignKey('source.id'), primary_key=True)

    change_request = db.relationship('ChangeRequest')
    source = db.relationship('Source')
    date_created = db.Column(db.TIMESTAMP(
        timezone=True), nullable=True, onupdate=timezone.now)

    __tablename__ = 'change_request_source'

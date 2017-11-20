from marshmallow import Schema, fields, post_load

from zeus.models import ChangeRequest

from .author import AuthorSchema
from .revision import RevisionSchema


class ChangeRequestSchema(Schema):
    id = fields.UUID(dump_only=True)
    number = fields.Integer(dump_only=True)
    message = fields.Str()
    author = fields.Nested(AuthorSchema())
    parent_revision = fields.Nested(RevisionSchema())
    provider = fields.Str(dump_only=True)
    external_id = fields.Str(dump_only=True)
    url = fields.Str(dump_only=True)
    created_at = fields.DateTime(attribute='date_created', dump_only=True)

    @post_load
    def make_hook(self, data):
        if self.context.get('change_request'):
            cr = self.context['change_request']
            for key, value in data.items():
                setattr(cr, key, value)
        else:
            cr = ChangeRequest(**data)
        return cr


class ChangeRequestCreateSchema(Schema):
    author = fields.Nested(AuthorSchema())
    provider = fields.Str()
    message = fields.Str(required=True)
    external_id = fields.Str()
    url = fields.Str(allow_none=True)
    parent_revision_sha = fields.Str(required=True)
    created_at = fields.DateTime(attribute='date_created')

    @post_load
    def make_hook(self, data):
        return ChangeRequest(**data)

from flask import current_app
from sqlalchemy.exc import IntegrityError

from zeus.config import db
from zeus.models import ChangeRequest, ChangeRequestSource, Source
from zeus.vcs.base import UnknownRevision
from zeus.utils.revisions import identify_revision

from .base_change_request import BaseChangeRequestResource
from ..schemas import SourceCreateSchema


class ChangeRequestSourcesResource(BaseChangeRequestResource):
    def select_resurce_for_update(self):
        return False

    def post(self, cr: ChangeRequest):
        """
        Associate a source with a change request.
        """
        source_schema = SourceCreateSchema(strict=True)
        result = self.schema_from_request(source_schema, partial=True)
        if result.errors:
            return self.respond(result.errors, 403)
        data = result.data

        # HACK(dcramer): we're reusing the build creation infrastructure to
        # generate sources
        # TODO(dcramer): if this source were a patch we'd need the author
        try:
            revision = identify_revision(
                cr.repository, data['revision_sha'])
        except UnknownRevision:
            current_app.logger.warn('invalid ref received', exc_info=True)
            return self.error('unable to find a revision matching ref')

        # TODO(dcramer): need to handle patch case yet
        source = Source.query.filter(
            Source.revision_sha == revision.sha,
            Source.repository_id == cr.repository_id,
        ).first()

        try:
            db.session.add(ChangeRequestSource(
                change_request=cr,
                source=source,
            ))
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return self.respond(status=422)

        return self.respond(status=201)

from zeus.models import ChangeRequestSource


def test_create_change_request_source(
        client, default_login, default_repo, default_repo_access, default_change_request, default_source):
    resp = client.post(
        '/api/repos/{}/change-requests/{}/sources'.format(
            default_repo.get_full_name(),
            default_change_request.number,
        ),
        json={
            'revision_sha': default_source.revision_sha,
        }
    )
    assert resp.status_code == 201

    results = list(ChangeRequestSource.query.filter(
        ChangeRequestSource.change_request_id == default_change_request.id,
    ))
    assert len(results) == 1
    assert results[0].source_id == default_source.id


def test_create_change_request_source_existing(
        client, db_session, default_login, default_repo, default_repo_access, default_change_request, default_source):

    db_session.add(ChangeRequestSource(
        change_request_id=default_change_request.id,
        source_id=default_source.id,
    ))
    db_session.flush()

    resp = client.post(
        '/api/repos/{}/change-requests/{}/sources'.format(
            default_repo.get_full_name(),
            default_change_request.number,
        ),
        json={
            'revision_sha': default_source.revision_sha,
        }
    )
    assert resp.status_code == 422

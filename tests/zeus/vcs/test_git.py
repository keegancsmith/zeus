def _set_author(remote_path, name, email):
def vcs(git_repo_config, default_repo):
    return GitVcs(url=git_repo_config.url, path=git_repo_config.path, id=default_repo.id.hex)
def test_get_default_revision(git_repo_config, vcs):
def test_log_with_authors(git_repo_config, vcs):
    _set_author(git_repo_config.remote_path,
                'Another Committer', 'ac@d.not.zm.exist')
        'cd %s && touch BAZ && git add BAZ && git commit -m "bazzy"' % git_repo_config.remote_path, shell=True
def test_log_with_branches(git_repo_config, vcs):
    remote_path = git_repo_config.remote_path
    assert len(revision.sha) == 40
    assert revisions[0].parents == [revisions[1].sha]
    diff = vcs.export(revisions[0].sha)
        child_in_question=revisions[0].sha, parent_in_question=revisions[1].sha
        child_in_question=revisions[1].sha, parent_in_question=revisions[0].sha
def test_get_known_branches(git_repo_config, vcs):
               git_repo_config.remote_path, shell=True)
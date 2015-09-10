# -*- coding: utf-8 -*-
from peltak.core import git
from peltak.actions import actions


@actions.register(
    'review',
    desc=("Review changes in the current branch against the master. This will "
          "use 'git difftool' to do the comparison. The actual tool used has "
          "to be configured in git.")
)
def action_review(app):
    git.review_branch()


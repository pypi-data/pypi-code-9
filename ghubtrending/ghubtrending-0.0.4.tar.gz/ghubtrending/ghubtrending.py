"""
    Simple weekly twittbot.
    Execute this daily to get a weekly-trending repo into a twitter account.
"""

import os
import json
import github3
import datetime
import configparser as ConfigParser
from birdy.twitter import UserClient


def main():
    """
        - Initialize twitter and github libs
        - Get gh trending repos
        - Check if they've been already posted
        - Post this week's repo if not posted (otherwise next)
    """
    cfg = ConfigParser.ConfigParser()
    cfg.read(os.path.expanduser('~/.ghtrend_bot.cfg'))

    ghub = github3.login(
        cfg.get('github', 'login'),
        cfg.get('github', 'password')
    )

    client = UserClient(
        cfg.get('twitter', 'CONSUMER_KEY'),
        cfg.get('twitter', 'CONSUMER_SECRET'),
        cfg.get('twitter', 'ACCESS_TOKEN'),
        cfg.get('twitter', 'ACCESS_TOKEN_SECRET')
    )

    def get_short_description(obj):
        """
            Get desc in less than 100 characters.
            TODO: Use twitter's current 144 - max_link_lenght
        """
        desc = unicode(obj['description']).encode('utf-8', errors="replace")
        return desc[:100] + (desc[100:] and '...')

    def get_twitt(obj):
        """
            Given a github search result object, get description and
            url in a format acceptable to twitter
        """
        return "{}: {}".format(get_short_description(obj), obj['html_url'])

    def get_first_dow():
        """
            Returns the first day of current week
        """
        time_ = datetime.datetime.now()
        return time_ - datetime.timedelta(time_.weekday())

    def get_dow():
        """
            Gets the current day of week
        """
        time_ = datetime.datetime.now()
        return time_.weekday()

    weekdate = get_first_dow().strftime('%Y-%m-01')

    path_ = os.path.join(
        os.path.expanduser('~/.ghtrending/'), '{}.json'.format(weekdate))

    if not os.path.exists(path_):
        gh_repos = ghub.search_repositories(
            "created:>{}".format(weekdate), sort='stars', number=18)

        # Aaand here goes efficiency!
        repos = [json.loads(repo.as_json()) for repo in gh_repos]

        with open(path_, 'w') as ffile_:
            json.dump(repos, ffile_)
    else:
        with open(path_) as ffile_:
            repos = json.load(ffile_)

    dow = get_dow()

    posted_p = os.path.join(os.path.expanduser('~/.ghtrending/'), 'posted')
    with open(posted_p, 'r') as pposted:
        already_posted = pposted.readlines()

    for repo in repos:
        if repo["html_url"] in already_posted:
            dow += 1  # This logic might lead, on some weeks, to keep posting
            # the latest trending repo =(
            # Let's just hope is nothing very usual

    twitt = get_twitt(repos[dow])
    client.api.statuses.update.post(status=twitt)

    with open(posted_p, 'a') as posted:
        already_posted.write(repos[dow]['html_url'])


if __name__ == '__main__':
    main()

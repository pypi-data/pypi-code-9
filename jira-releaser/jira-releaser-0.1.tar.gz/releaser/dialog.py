def get_repository():
    """
    Get a list of repositories where will be create release branch

    :return:
    """
    repo_urls = []
    url = raw_input("Enter git repository url: ")
    while url:
        if len(url) > 0:
            repo_urls.append(url)

        question = "Enter another git repository url or leave blank line: "
        url = raw_input(question)

    return repo_urls


def get_master_branch(default_branch='master'):
    """
    Get master branch from which will be created release branch

    :type default_branch: str
    :param default_branch: this branch will be use
        if user doesn't select particular branch
    :return:
    """
    question = "From which branch will be created release branch [master]: "
    branch = raw_input(question) or default_branch

    return branch


def get_jira_user():
    question = "Jira user: "
    return raw_input(question)


def get_jira_password():
    question = "Jira password: "
    return raw_input(question)

def get_fix_version():
    question = "Enter fix version: "
    return raw_input(question)


if __name__ == "__main__":
    print get_repository()

    print get_master_branch()
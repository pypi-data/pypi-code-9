"""managing information from GIT"""
from __future__ import print_function

from pprint import pprint

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import banner
import time

class GitInfo(object):

    """This class can be used to return some elementary information
    about the git hub directory.  This includes the:

    * version number of the code
    * the list of people contributing to the code
    * emails of the people contributing
    * a statistic about changed code by person

    Example::

        gitinfo = GitInfo()
        print gitinfo.authors()
        pprint(gitinfo.authors("dict"))
        pprint(gitinfo.emails())
        pprint(gitinfo.emails("dict"))
        pprint(gitinfo.info())
        print gitinfo.stat("laszewski@gmail.com")
        stats = gitinfo.compute()
        print stats

    """

    def __init__(self):
        """init method"""
        pass


    @staticmethod
    def print_authors():
        print(GitInfo.get_authors_by_date(header=True))

    @staticmethod
    def get_authors_by_date(header=False):
        """lists the authors of a git repository sorted by date.

        Example:

            0001 (2015-02-25): Gregor von Laszewski (laszewski@gmail.com)
            0002 (2015-04-14): Fugang Wang (kevinwangfg@gmail.com)

        :rtype: str
        """


        # modified from https://github.com/jgehrcke/git-authors

        result = ""
        # if header:
        #    result = result + "Authors\n"
        #    result = result + "=======\n\n"

        r = Shell.git("log",
                      "--encoding=utf-8",
                      "--full-history",
                      "--reverse",
                      "--format=format:%at;%an;%ae").split("\n")
        seen = set()
        for line in r:
            timestamp, name, email = line.strip().split(";")
            if name not in seen:
                seen.add(name)
                day = time.strftime("%Y-%m-%d", time.gmtime(float(timestamp)))
                result = result + "* {:04d} ({:}): {:} ({:})\n".format(len(seen), day, name, email)
        return result

    def version(self):
        """
        returns the verison of the code from github
        :rtype: the git tags
        """
        return str(Shell.git("describe", "--tags"))[:-1]

    def emails(self, output=None):
        """
        returns the emails of the authors either as a text or as a dict. The
        format is specified as an argument.

        :param output: if "dict" is specified a dict will be returned
        :rtype: dict or array of e-mails dependent on output
        """
        format_string = "'%aN' <%cE>"
        if output == 'dict':
            format_string = "%aN\t%cE"

        result = sorted(set(Shell.git("log",
                      "--all",
                      "--format=" + format_string).split("\n")))

        if output is None:
            return result
        elif output == "dict":
            emails = {}
            for l in result:
                (name, email) = l.split("\t")
                emails[name] = email
            return emails

    def authors(self, output=None):
        """
        returns the authors of the authors either as a text or as a dict. The
        format is specified as an argument.

        :param output: if "dict" is specified a dict will be returned
        """
        result = Shell.git("shortlog", "-s", "-n")
        if output is None:
            return result
        elif output == "dict":
            authors = {}
            for line in result.split("\n"):
                l = " ".join(line.split()).strip()
                (number, name) = l.split(" ", 1)
                authors[name] = int(number)
            return authors

    def info(self):
        """
        returns the information about authors, emails, and commits in a dict.
        :rtype: a dict with the information
        """
        authors = self.authors("dict")
        email = self.emails("dict")

        info = {}
        for name in authors:
            info[name] = {
                "name": name,
                "commits": authors[name],
                "email": email[name]}
        return info

    def stat(self, email):
        """
        returns a statistic of a git author with the given e_mail.

        :param email: name of the author
        :rtype: a dict with the statistics
        """
        result = Shell.git("log", "--all", "--stat", '--author={0}'.format(email)).split("\n")
        sums = [0, 0, 0]
        for line in result:
            if " files changed" in line:
                line = line.strip()
                line = line.replace(" insertions(+)", "")
                line = line.replace(" insertion(+)", "")
                line = line.replace(" deletion(-)", "")
                line = line.replace(" deletions(-)", "")
                line = line.replace(" files changed", "")
                line = line.split(",")
                data = [int(i) for i in line]
                for index in range(0, len(data)):
                    sums[index] += data[index]

        return {"email": email,
                "fileschanged": sums[0],
                "inserted": sums[1],
                "deleted": sums[2],
                "lineschanged": sums[1] + sums[2]}

    def compute(self):
        """
        computes the statistic of all authors in a git repository and
        returns the result as a dict.
        :rtype: a dict with the values
        """
        emails = set(gitinfo.emails("dict").values())

        stats = {}
        sums = {"fileschanged": 0, "inserted":
                0, "deleted": 0, "lineschanged": 0}
        for email in emails:
            print("Calculating stats for", email)
            stats[email] = gitinfo.stat(email)

            sums["fileschanged"] += stats[email]["fileschanged"]
            sums["inserted"] += stats[email]["inserted"]
            sums["deleted"] += stats[email]["deleted"]
            sums["lineschanged"] += stats[email]["lineschanged"]

        for email in emails:
            stats[email] = {'percentage': [
                stats[email]["fileschanged"] / float(sums["fileschanged"]),
                stats[email]["inserted"] / float(sums["inserted"]),
                stats[email]["deleted"] / float(sums["deleted"]),
                stats[email]["lineschanged"] / float(sums["lineschanged"])
            ]}

        return stats

if __name__ == "__main__":

    print (Shell.git("shortlog", "-n", "-s"))


    gitinfo = GitInfo()

    # print gitinfo.version()

    banner("a")
    print(gitinfo.authors())

    banner("b")
    pprint(gitinfo.authors("dict"))

    banner("c")
    pprint(gitinfo.emails())

    banner("d")
    pprint(gitinfo.emails("dict"))

    banner("e")
    pprint(gitinfo.info())

    banner("f")
    print(gitinfo.stat("laszewski@gmail.com"))

    banner("g")
    stats = gitinfo.compute()

    print(stats)

    banner("h")
    for email in stats:
        p = stats[email]["percentage"]
        print(("{0} {1:.3f}% {2:.3f}%  {3:.3f}% {4:.3f}%"
               .format(email, p[0], p[1], p[2], p[3])))

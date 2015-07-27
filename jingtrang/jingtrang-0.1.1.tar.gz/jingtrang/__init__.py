import sys
import subprocess
import pkg_resources


def jing():
    cmd = ["java", "-jar"]
    cmd.append(pkg_resources.resource_filename("jingtrang", "jing.jar"))
    cmd = cmd + sys.argv[1:]
    res = subprocess.call(
        cmd,
        stdout=sys.stdout,
        stderr=sys.stderr,
        stdin=sys.stdin)
    sys.exit(res)


def trang():
    cmd = ["java", "-jar"]
    cmd.append(pkg_resources.resource_filename("jingtrang", "trang.jar"))
    cmd = cmd + sys.argv[1:]
    res = subprocess.call(
        cmd,
        stdout=sys.stdout,
        stderr=sys.stderr,
        stdin=sys.stdin)
    sys.exit(res)

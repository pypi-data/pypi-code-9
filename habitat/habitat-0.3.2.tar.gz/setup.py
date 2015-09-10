from setuptools import setup

setup(
    name="habitat",
    version="0.3.2",
    author="HABHUB Team",
    author_email="root@habhub.org",
    url="http://habitat.habhub.org/",
    description="Next Generation High Altitude Balloon Tracking",
    packages=["habitat", "habitat.parser_modules", "habitat.sensors",
        "habitat.utils", "habitat.views"],
    scripts=["bin/parser", "bin/sign_hotfix", "bin/uploader",
        "bin/upload_design_docs"],
    license="GNU General Public License Version 3",
    install_requires=["M2Crypto>=0.21.1", "couchdbkit>=0.5.4", "crcmod>=1.7",
        "ipaddr>=2.1.9", "PyYAML", "pytz", "strict-rfc3339", "statsd-client"],
)

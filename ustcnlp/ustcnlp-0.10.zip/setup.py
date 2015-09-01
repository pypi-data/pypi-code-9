from setuptools import setup, find_packages
setup(
      name="ustcnlp",
      version="0.10",
      description="Automatic scoring using nlp",
      author="Cheng Ding, WeiWei Duan",
      author_email = "sa514004@mail.ustc.edu.cn",
      url="http://www.ustc.edu.cn",
      license="MIT",
      packages= find_packages(),
      scripts=["scripts/test.py"],
      )
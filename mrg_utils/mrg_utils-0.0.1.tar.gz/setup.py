from setuptools import setup

setup(
    name="mrg_utils",
    version="0.0.1",
    author="Robert Elwell",
    url="https://github.com/relwell/mrg_utils",
    author_email="robert.elwell@gmail.com",
    description="A set of utilities for interacting with Penn-Treebank .mrg-formatted parses and identifying syntactic heads",
    license="GPL",
    packages=["mrg_utils", "mrg_utils.sentence", "mrg_utils.cuecorp", "mrg_utils.docNode", 
              "mrg_utils.headRules", "mrg_utils.mrg_document",
              "mrg_utils.node", "mrg_utils.nonTerminalNode", "mrg_utils.rootNode", "mrg_utils.sentence", 
              "mrg_utils.sexpr_parse", "mrg_utils.terminalNode"],
    )

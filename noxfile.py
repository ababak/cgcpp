"""
(c) Andriy Babak 2025

date: 02/04/2025
modified: 02/04/2025 13:14:21

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: cgcpp
------------------------------
"""

import nox


@nox.session(default=False)
def tests(session):
    session.install("pytest")
    session.run("pytest")


@nox.session
def build_plugin(session):
    session.install_and_run_script("build_plugin.py", *session.posargs)

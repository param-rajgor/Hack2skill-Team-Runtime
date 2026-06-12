# src/jd/jd_parser.py

import sys
import os

sys.path.append(
    os.path.abspath("src")
)

from jd_requirements import (
    REQUIRED_SKILLS,
    PREFERRED_SKILLS,
    NEGATIVE_SIGNALS
)


def parse_jd(jd):

    return {

        "required_skills":
        REQUIRED_SKILLS,

        "preferred_skills":
        PREFERRED_SKILLS,

        "negative_signals":
        NEGATIVE_SIGNALS

    }
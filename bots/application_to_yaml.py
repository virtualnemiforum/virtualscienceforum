import os
import re
from copy import deepcopy
from pathlib import Path
from io import StringIO

from dateutil.parser import parse, ParserError
import github
from ruamel.yaml import YAML

import validatespeakerscornerissue

yaml = YAML()
TALKS_FILE = "speakers_corner_talks.yml"

def add_talk(github, issue_number):
    repo = github.get_repo("virtualscienceforum/virtualscienceforum")
    issue = repo.get_issue(number=issue_number)

    try:
        talks_data = repo.get_contents(TALKS_FILE, ref="master")
        talks = yaml.load(StringIO(talks_data.decoded_content().decode()))
    except github.UnknownObjectException:
        talks_data = None
        talks = []

    if any(talk.get('issue_number') == issue_number for talk in talks):
        issue.create_comment("Not adding a talk; already in the list.")
        return

    try:
        submission = validatespeakerscornerissue.parse_issue(issue.body)
    except ValueError:
        issue.create_comment("Could not process issue, data is invalid.")
        return
    
    try:
        submission['time'] = parse(submission['time'])
    except ParserError:
        issue.create_comment("Could not determine the talk date")

    submission.pop('notes')

    talks.append(dict(
        workflow_issue=issue_number,
        speaker_name=submission.pop("name"),
        speaker_affiliation=submission.pop("affiliation"),
        event_type="speakers_corner",
        **submission,
    ))

    repo.

if __name__ == "__main__":
    issue_number = int(os.getenv("ISSUE_NUMBER"))
    github = github.Github(os.getenv("VSF_BOT_TOKEN"))
    add_talk(github, issue_number)
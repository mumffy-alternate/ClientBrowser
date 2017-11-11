import logging
import os
import re
from datetime import datetime

from docx import Document

from app import db
from app.models import LegacyPhoneLog

PHONELOG_CONTENT_MARKER = "PHONE LOG \(MOST RECENT ON TOP\)"
INPUT_PATH = ur".\sample_data"

logging.basicConfig()
log = logging.getLogger('phonelog_extract')
log.setLevel(logging.DEBUG)


def extract_phonelog(filepath):
    log.debug("Opening %s to extract phone log content", filepath)
    doc = Document(filepath)
    content = ""
    found_delimiter = False
    for p in doc.paragraphs:
        if not found_delimiter:
            if re.match('^\s*' + PHONELOG_CONTENT_MARKER + '\s*$', p.text):
                found_delimiter = True
        else:
            if not re.match('^\s*_+\s*$', p.text):  # skip the horizontal line
                content += p.text + '\n'

    if not found_delimiter:
        return None
    else:
        return content


def get_casename(filename):
    if str(filename).find('-') == -1 or str(filename).lower().find('.docx') == -1:
        return None
    filename = str(filename).replace('-', '/', 1)
    return os.path.splitext(filename)[0]


def export_phonelog(filepath, filename):
    case_name = get_casename(filename)
    if case_name == None:
        log.error("Could not determine Case name for %s (missing dash?).", filename)
        return

    content = extract_phonelog(filepath)
    if content == None:
        log.error("%s did not contain the content marker (%s)", filepath, PHONELOG_CONTENT_MARKER)
        return

    phonelog = LegacyPhoneLog()
    phonelog.case_name = case_name
    phonelog.content = content
    phonelog.extraction_time = datetime.utcnow()
    db.session.add(phonelog)
    db.session.commit()  # TODO commit in a big batch, instead?
    log.debug("added case[%s]'s legacy phone log content to the database.", case_name)


if __name__ == "__main__":
    for root, dirs, files in os.walk(INPUT_PATH):
        for filename in files:
            filepath = os.path.join(root, filename)
            log.debug("")
            if not str(filename).startswith('~') and str(filename).lower().endswith('.docx'):
                export_phonelog(filepath, filename)
            else:
                log.debug("SKIPPING %s", filepath)

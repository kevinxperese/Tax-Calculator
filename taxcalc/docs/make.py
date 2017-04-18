"""
Adds JSON information to input HTML and writes augmented HTML file.
"""
# CODING-STYLE CHECKS:
# pep8 --ignore=E402 make.py
# pylint --disable=locally-disabled make.py

import sys
import os
import json
from collections import OrderedDict

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
INPUT_FILENAME = 'index.htmx'
INPUT_PATH = os.path.join(CUR_PATH, INPUT_FILENAME)
POLICY_PATH = os.path.join(CUR_PATH, '..', 'current_law_policy.json')
# --- JSON PATHS GO HERE --- #
OUTPUT_FILENAME = 'index.html'
OUTPUT_PATH = os.path.join(CUR_PATH, OUTPUT_FILENAME)


def main():
    """
    Contains high-level logic of the script.
    """
    # read INPUT file into text variable
    with open(INPUT_PATH, 'r') as ifile:
        text = ifile.read()

    # augment text variable with information from JSON files
    text = policy_params(text, POLICY_PATH)

    # write text variable to OUTPUT file
    with open(OUTPUT_PATH, 'w') as ofile:
        ofile.write(text)

    # normal return code
    return 0
# end of main function code


def param_text(pname, param):
    """
    Extract attributes from param for pname and return as HTML string.
    """
    txt = '<p><b>{} &mdash; {}</b>'.format(param['section_1'],
                                           param['section_2'])
    txt += '<br><i>CLI Name:</i> {}'.format(pname)
    txt += '<br><i>GUI Name:</i> {}'.format(param['long_name'])
    txt += '<br><i>Description:</i> {}'.format(param['description'])
    if param['notes'] != '':
        txt += '<br><i>Notes:</i> {}'.format(param['notes'])
    if param['cpi_inflated']:
        txt += '<br><i>Inflation Indexed:</i> True'
    else:
        txt += '<br><i>Inflation Indexed:</i> False'
    txt += '<br><i>Known Values:</i>'
    if len(param['col_label']) > 0:
        cols = ', '.join(param['col_label'])
        txt += '<br>&nbsp;&nbsp; for: [{}]'.format(cols)
    for cyr, val in zip(param['row_label'], param['value']):
        txt += '<br>{}: {}'.format(cyr, val)
    txt += '</p>'
    return txt


def policy_params(text, path):
    """
    Read policy parameters from path, integrate them into text, and
    return the integrated text.
    """
    with open(path) as pfile:
        params = json.load(pfile, object_pairs_hook=OrderedDict)
    assert isinstance(params, OrderedDict)
    # construct section dict containing sec1_sec2 titles
    concat_str = ' @ '
    section = OrderedDict()
    using_other_params_section = False
    for pname in params:
        param = params[pname]
        sec1_sec2 = '{}{}{}'.format(param['section_1'],
                                    concat_str,
                                    param['section_2'])
        if sec1_sec2 == concat_str:
            using_other_params_section = True
        elif sec1_sec2 not in section:
            section[sec1_sec2] = 0
    if using_other_params_section:
        section[concat_str] = 0
    # construct parameter text for each sec1_sec2 in section
    for sec1_sec2 in section:
        split_list = sec1_sec2.split(concat_str)
        sec1 = split_list[0]
        sec2 = split_list[1]
        ptext = ''
        for pname in params:
            param = params[pname]
            if sec1 == param['section_1'] and sec2 == param['section_2']:
                ptext += param_text(pname, param)
        # integrate parameter text into text
        old = '<!-- {} -->'.format(sec1_sec2)
        text = text.replace(old, ptext)
    return text


if __name__ == '__main__':
    sys.exit(main())

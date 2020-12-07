#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2020 Joan Montané <jmontane@softcatala.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urllib.request
import pathlib
import zipfile
import os
import shutil
import polib

MYCROFT_SKILLS_DIR = '/opt/mycroft/skills'
MYCROFT_LOCALE = 'ca-es'
POOTLE_LOCALE = 'ca'
WORKING_DIR = './tmp/'
POFILES_DIR = WORKING_DIR + POOTLE_LOCALE + '-mycroft-skills/' + POOTLE_LOCALE + '/mycroft-skills/'

def get_list_of_skills(path):
    return [f.path for f in os.scandir(path) if f.is_dir()]

def get_list_of_pofiles():

    pathlib.Path(WORKING_DIR).mkdir(parents=True, exist_ok=True)

    print('Getting Pootle strings from \'' + POOTLE_LOCALE + ' locale...' )
    url = 'https://translate.mycroft.ai/export/?path=/' + POOTLE_LOCALE + '/mycroft-skills'
    urllib.request.urlretrieve(url, WORKING_DIR + 'export.zip')

    print('Unzipping export.zip...')
    with zipfile.ZipFile(WORKING_DIR + 'export.zip', 'r') as zip_ref:
        zip_ref.extractall(WORKING_DIR)

    return [f.path for f in os.scandir(POFILES_DIR) if (f.is_file() and f.name.endswith('.po'))]

def is_locale_skill(skill):
    return os.path.isdir(skill + '/locale')

def get_pofile(skill):

    skill_name = os.path.basename(skill)
    po_basename = ''
    po_filename = ''
    
    if skill_name[:8] == 'mycroft-' and skill_name[-10:] == '.mycroftai':
        po_basename = 'skill-' + skill_name[8:-10] + '-ca.po'
        po_filename = POFILES_DIR + po_basename
           
    elif skill_name[-10:] == '.mycroftai':
        po_basename = skill_name[:-10] + '-ca.po'
        po_filename = POFILES_DIR + po_basename

    if po_filename in List_of_pofiles:
        return(po_filename)

    return False

def change_pofile_comments(pofile):

    lines = []
    with open(pofile,'r') as f:
        lines = f.readlines()
        f.close()

    newlines = []

    for line in lines:
        if not (line[:1] == '# ' or line[:2] == '#. '):
            if	 line[:3] == '#: ':
                line = '# ' + line[3:]
            newlines.append(line)
 
    with open(pofile + 'new', 'w') as f:
        for line in newlines:
            f.write("%s" % line)
        f.close()

    return


def remove_old_translations(path):

    if os.path.isdir(path + '/' + MYCROFT_LOCALE):
        try:
            shutil.rmtree(path + '/' + MYCROFT_LOCALE)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
    return

def parse_references(references):

    new_references =''
    for line in references.split('\n'):
        if line[:5] == 'tags/':
            new_references = new_references + '\n' + line[5:]
        else:
            new_references = new_references + ' ' + line
    
    new_references = new_references.strip('\n')

    return new_references

def get_translations(pofile):

    po = polib.pofile(pofile)
    references = ''
    targetfiles = {}
    targetlines = []

    for entry in po:
        #tcomment can store multiple references/lines, see version-checker skill
        references = entry.tcomment
        references = parse_references(references)

        for reference in references.split('\n'):
            targetfile = (reference.split(':')[0]).split('/')[1]
            if targetfile not in targetfiles:
                targetfiles[targetfile] = []

            targetline = int(reference.split(':')[1])
            translation = entry.msgstr

            if  translation == '':
                translation = entry.msgid

            targetfiles[targetfile].insert(targetline-1,translation)

    return targetfiles

def write_locale_translations(path, translations):
    
    for file in translations:
        lines = ''
        for line in translations[file]:
            lines = lines+line + '\n'

        if lines != '':
            pathlib.Path(path + '/' + MYCROFT_LOCALE).mkdir(parents=True, exist_ok=True)

            with open(path + '/' + MYCROFT_LOCALE + '/' + file, 'w') as f:
                f.write("%s" % lines)
                f.close()

    return

def write_nonlocale_translations(path, subdir, translations):

    

    for file in translations:
        extension=file.split('.')[-1]
        if (subdir == extension or
           (subdir =='vocab' and extension == 'voc') or
           (subdir =='regex' and extension == 'rx') or
           (subdir =='dialog' and extension == 'value')):
            lines = ''
            for line in translations[file]:
                lines = lines+line + '\n'

            if lines != '':
                pathlib.Path(path + '/' + subdir + '/' + MYCROFT_LOCALE).mkdir(parents=True, exist_ok=True)
        
                with open(path + '/' + subdir + '/' + MYCROFT_LOCALE + '/' + file, 'w') as f:
                    f.write("%s" % lines)
                    f.close()

    return

def get_new_translations(path, pofile):

    pathlib.Path(path + '/' + MYCROFT_LOCALE).mkdir(parents=True, exist_ok=True)

    return

List_of_skills = get_list_of_skills(MYCROFT_SKILLS_DIR)

List_of_pofiles = get_list_of_pofiles()


for skill in List_of_skills:
    print('Working on ' + skill)
    if (is_locale_skill(skill)):
       print('It\'s a locale skill')
       pofile = get_pofile(skill)
       if pofile:
           print('Remove ' + MYCROFT_LOCALE + ' subdir from locale dir')
           remove_old_translations(skill + '/locale')
           print('Change pofile comments')
           change_pofile_comments(pofile)
           translations = {}
           translations = get_translations(pofile+'new')
           write_locale_translations(skill + '/locale', translations)

    else:
       print('It\'s a non-locale skill')
       pofile = get_pofile(skill)
       if pofile:
           print('Change pofile comments')
           change_pofile_comments(pofile)
           translations = {}
           translations = get_translations(pofile+'new')

           for subdir in ['dialog', 'vocab', 'regex']:
               print('Remove ' + MYCROFT_LOCALE + ' subdir from ' + subdir + ' dir')
               remove_old_translations(skill + '/' + subdir)
               write_nonlocale_translations(skill, subdir, translations)


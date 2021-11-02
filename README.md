# mycroft-update-translations
A script to download Mycroft skills translations from pootle and update translated strings to skills directories.

It exports translations from Mycroft Pootle as zip archive, extract po files, parses them and put strings on skills directories.

This script is for personal use, but maybe it can be helpful for someone.

Be carefully, there isn't error catching.

## Arguments
```
-l LOCALE, --locale LOCALE  Locale code (default en-us)
-d DIR,    --dir DIR        Skills dir Skills dir (default /opt/mycroft/skills)
-s SKILL,  --skill SKILL    Skill name (otherwise updates all skills)
```
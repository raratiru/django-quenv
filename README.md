[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/raratiru/django-quenv.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/raratiru/django-quenv/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/81098980cb5b40e899c5161835020509)](https://www.codacy.com/app/raratiru/django-quenv?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=raratiru/django-quenv&amp;utm_campaign=Badge_Grade)

**In Alpha phase, no tests exist and changes are possible to occur.**

Django Quality Environment Report
=================================

This app uses setuptools to gather the names of all packages in a virtualenv.


From the metadata of each package, it collects all available information about
its license(s).


It uses the [lgtm](https://lgtm.com/) api to query the quality metrics of
github based packages.

All data are saved first to a json file and then loaded to the database.
Only one fixture per day can be created.

Finally, it creates a report of any change occurred to a package, namely:
If it was **added**, **removed** or its **license** has **changed.**


Installation
------------
```
pip install django-quenv
```

```
INSTALLED_APPS = [
    ...,
    'quenv',
]
```

```
./manage.py migrate
./manage.py quenv
```

Configuration
-------------
In `settings,py` the following configuration can take place:

`QUENV_PATH`: The path where the fixtures are saved. Default: `.`

`QUENV_UPDATE_DB`: Default `True`, if `False` it only creates the fixtures.

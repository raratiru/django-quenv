**In Alpha phase, no tests exist and changes are possible to occur.**

Django Quality Environment Report
=================================

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6e68470878d84d79b54f95a6831459a4)](https://app.codacy.com/app/raratiru/django-quenv?utm_source=github.com&utm_medium=referral&utm_content=raratiru/django-quenv&utm_campaign=Badge_Grade_Settings)

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

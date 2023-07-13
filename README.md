# drf-system-setting


[![pypi](https://img.shields.io/pypi/v/drf-system-setting.svg)](https://pypi.org/project/drf-system-setting/)
[![python](https://img.shields.io/pypi/pyversions/drf-system-setting.svg)](https://pypi.org/project/drf-system-setting/)
[![Build Status](https://github.com/LinkanDawang/drf-system-setting/actions/workflows/dev.yml/badge.svg)](https://github.com/LinkanDawang/drf-system-setting/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/LinkanDawang/drf-system-setting/branch/main/graphs/badge.svg)](https://codecov.io/github/LinkanDawang/drf-system-setting)



Skeleton project created by Cookiecutter PyPackage


* Documentation: <https://LinkanDawang.github.io/drf-system-setting>
* GitHub: <https://github.com/LinkanDawang/drf-system-setting>
* PyPI: <https://pypi.org/project/drf-system-setting/>
* Free software: MIT


## Requirement
* Python 3.8, 3.9, 3.10, 3.11
* Django 3.2, 4.0, 4.1
* django-rest-framework

## Installation
Install using pip...
```bash
pip install drf-system-setting
```
Add `'drf_system_setting'` to your `INSTALLED_APPS` setting.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...,
    'drf_system_setting',
]
```

To enable access to the user interface add the url path `settings`(just what ever you want) to your `urls.py`:

```python
from django.urls import path, include
urlpatterns = [
    ...,
]

urlpatterns += [
    path('settings/', include('drf_system_setting.urls', namespace='drf_system_setting'))
]
```

before running migrate:

```bash
python manage.py migrate drf_system_setting
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.

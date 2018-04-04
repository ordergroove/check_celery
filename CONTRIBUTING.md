## Setting up your local environment

Assumptions -you have the following available on your system
- Python 2.7
- virtualenv

```
mkdir /path/to/check_celery-env
cd /path/to/check_celery-env
virtualenv --no-site-packages .
source bin/activate
git clone git@github.com:ordergroove/check_celery.git
cd check_celery
pip install -r requirements.txt
```

Final verification, run the tests to confirm everything is happy:
```
python -m unittest discover
```

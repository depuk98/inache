# Inache-Backend-V2

cd Inache-Backend
pip install -r requirements.txt

Create a superuser,enter an email and a password

python3 manage.py createsuperuser

python3 manage.py makemigrations

python3 manage.py migrate

## before running this you need to activate the venv

python -m venv myenv

source myenv/bin/activate

##

python3 manage.py runserver

python3 manage.py crontab add
python3 manage.py crontab show

python3 manage.py migrate accounts migration_number

python -m venv ./venv
source venv/bin/activate
===================================== <br />
python3 manage.py showmigrations :- whether each migration is applied (marked by a [X] next to the migration name).
# inache

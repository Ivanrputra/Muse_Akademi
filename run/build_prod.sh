source ../virtualenv/MuseAcademy/3.7/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
touch tmp/restart.txt

source env/Scripts/activate
pip install -r requirements.txt
python manage.py makemigrations --settings=MuseAcademy.settings_dev
python manage.py migrate --settings=MuseAcademy.settings_dev
python manage.py runserver --settings=MuseAcademy.settings_dev
source env/Scripts/activate
python manage.py makemigrations --settings=MuseAcademy.settings_dev
python manage.py migrate --settings=MuseAcademy.settings_dev
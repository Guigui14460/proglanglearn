# ProgLangLearn

This project is the source code for an educational programming website.


You should be able to have the packages. For that, use this command to install all of the dependencies : 
```sh
pip install -r requirements.txt # venv
pipenv install # pipenv
```

To activate environment :
```sh
# venv
source env/Scripts/activate # unix system
cd env; cd Scripts; cd activate.bat # windows
```

Go to folder first : 
```sh
cd proglanglearn
```

Administration :
- superuser creation :
```sh
python manage.py createsuperuser
```
- use default admin (username: HadesGuigui, Password: hadesguiguiadmin)

To run the project :
```sh
python manage.py runserver
```
To make migrations/migrate for the project's database :
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

To initialize/update files for translations :
```sh
django-admin makemessages -l <lang> -e html,txt,py
```
```sh
django-admin makemessages -a
```
To compile translations :
```sh
django-admin compilemessages
```
To clear sessions :
```sh
python manage.py clearsessions
```

To update style files :
```sh
sass --watch .\scss\global.scss:.\css\global.min.css .\scss\print.scss:.\css\print.min.css --style compressed
```

Custom commands :
1. Remove useless data : `python manage.py uselessdata`

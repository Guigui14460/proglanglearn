# ProgLangLearn

This project has the official source code at proglanglearn.com website.

This project was created in python virtual environment. To activate, you can use these 2 commands :
1. Linux/MacOS : `source env/Scripts/activate`
2. Windows : `cd env; cd Scripts; cd activate.bat`

You should be able to have the packages. For that, use this command to install all of the dependencies : `pip install -r requirements.txt`

To run the project :
```
python manage.py runserver
```
To make migrations/migrate for the project's database :
```
python manage.py makemigrations
```
```
python manage.py migrate
```

To initialize/update files for translations :
```
django-admin makemessages -l <lang> -e html,txt,py
```
```
django-admin makemessages -a
```
To compile translations :
```
django-admin compilemessages
```

To update style files :
```
sass --watch .\scss\global.scss:.\css\global.min.css .\scss\print.scss:.\css\print.min.css --style compressed
```

Custom commands :
1. Remove useless data : `python manage.py uselessdata`
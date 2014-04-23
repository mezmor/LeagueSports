LeagueSports
============

## Installation
1. Install requirements.txt. ```pip install -r requirements.txt```
2. Navigate to the internal LeagueSports folder (where settings.py is located, not the root folder) and create a secret_key.py file. This file should contain a SECRET_KEY variable set to a random string
3. Change the database NAME and STATICFILE_DIRS strings in settings.py to match your computer's path
4. Then run ```git status``` If git detects that you've changed settings.py run the following command ```git update-index --assume-unchanged path/to/LeagueSports/settings.py```

## Running the server
LeagueSports contains two servers, one for serving the website (django) and one for serving the realtime draft (tornado).
To run the servers:

1. Django: ```python manage.py runserver```
2. Drafter: ```python draftserver.py```

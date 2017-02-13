# Messenger Bot

### Setting
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Add .env
```
Add .env file with
export 'FACEBOOK_TOKEN': 'YOUR_FACEBOOK_TOKEN',
export 'VERIFY_TOKEN': 'YOUR_VERIFY_TOKEN',
export 'SERVER_URL': 'https://YOUR_HOSTNAME'

```

### Run
```
python server.py

# default web server port 8080
```

### Delpoy on Heroku
```
Create a new app on heroku 
Add the remote to the git Repo

git push heroku master

```



# To run

To ensure everything has passed over without sharing migration files, in the same dir as manage.py run:

```
python manage.py makemigrations
python manage.py migrate

```
    
Once that runs without error, check localhost/admin -> Players to see if players are there. If not

```
python mange.py shell

####

import csv
from users.models import Player

with open("cleaned_player_db.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Player.objects.get_or_create(
            pid=row[0],
            player=row[1],
            team=row[2],
            position=row[3],
            age=row[4],
            value=row[5],
            nationality=row[6],
            avi=row[7],
            )

```

## TO DO

The reports model for the backend has been created and there is a reports form available. If this form could be integrated into the player_profile.html page, we would be able to fully proceed. There is no player name in the form as this is pulled directly from the page. Some to do's on forms.py - a list of opposition should be added - copy the structure of `VAL_CHOICE`and how that is called in the dropdown options in the forms.py script.

Similar methods of pulling reports needs to be implimented for calibration.

Aggregation can be handled for these in views.py as regular pyton processes.



# fansdiscover

### requirements 
asgiref==3.2.3

certifi==2019.11.28

chardet==3.0.4

Django==3.0.3

django-widget-tweaks==1.4.5

docopt==0.6.2

idna==2.8

pipreqs==0.4.10

pytz==2019.3

requests==2.22.0

sqlparse==0.3.0

urllib3==1.25.8

yarg==0.1.9

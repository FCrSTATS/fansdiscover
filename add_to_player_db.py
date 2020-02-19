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

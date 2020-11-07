import base64
import csv
import os
from datetime import date

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dateutil.relativedelta import relativedelta

from accounts.models import User
from tournament.models import *


def create_tournament():
    title = Title.objects.get(
        name='Gudzumi League',
        kind=Title.KIND_CHOICES[2][0]
    )

    tournament = Tournament(
        title=title,
        name='Gudzumi League 11.2020',
        start_date=date.today().replace(day=1),
        end_date=date.today() + relativedelta(days=31)
    )
    tournament.save()
    with open('../../Gudzumi League 11.2020 - Players.csv') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        group = 0
        for row in spamreader:
            name = row[0].split(' ')
            user, _ = User.objects.get_or_create(
                first_name=name[1],
                last_name=name[0],
                kgs_username=row[1],
                username=row[1],
                password=base64.b64encode(bytes(row[1], 'utf-8'))
            )
            print(user)

            print(row)
            if row[-1]:
                group += 1
            print(group)
            participant = Participant(
                user=user,
                tournament=tournament,
                group=group
            )
            participant.save()


if __name__ == '__main__':
    main()

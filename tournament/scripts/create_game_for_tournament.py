import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from tournament.models import *

DRAW = (
    ((1, 4), (2, 3)),
    ((1, 3), (4, 5)),
    ((1, 2), (3, 5)),
    ((2, 5), (3, 4)),
    ((1, 5), (2, 4))
)


def main(tournament_id):
    participants = Participant.objects.filter(tournament_id=tournament_id)

    groups = [p.group for p in participants.distinct('group')]
    for group in groups:
        group_member = participants.filter(group=group)

        for i, tour in enumerate(DRAW):
            for pair in tour:
                try:
                    white_player = group_member[pair[0]-1]
                    black_player = group_member[pair[1]-1]
                except IndexError:
                    continue

                Game.objects.create(
                    tournament_id=tournament_id,
                    status=Game.STATUS_CHOICES[1][0],
                    white_player=white_player,
                    black_player=black_player,
                    tour=i+1
                )


if __name__ == '__main__':
    main(6)

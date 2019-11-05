import re

from django_rq import job

import requests
from bs4 import BeautifulSoup

from tournament.models import *


__all__ = ('parse_games_from_kgs',)


@job
def parse_games_from_kgs():
    for tournament in Tournament.objects.filter(is_active=True).prefetch_related(
            'participants', 'participants__user'
    ):

        participants = tournament.participants.all()
        done_list = []
        for participant in participants:
            kgs_game_parsing(participant, done_list, tournament.tag, tournament)
            done_list.append(participant.user.username)


def download_link(link):
    if link is None:
        return ''
    ufr = requests.get(link)
    return ufr.content


def kgs_game_parsing(participant, done_list, tag, tournament):
    name = participant.user.username
    url = 'http://www.gokgs.com/gameArchives.jsp?user=+' + name
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find_all('table')

    if not table:
        return 

    tr_list = table[0].find_all('tr')

    if not tr_list:
        return

    # 0 -- ссылка на просмотр
    # 1 -- ник белого
    # 2 -- ник чёрного
    # 3 -- размер доски, фора
    # 4 -- дата и время начала партии
    # 5 -- тип партии (рейтинговая, свободная)
    # 6 -- результат (W+res, B+res,W+Time, B+14.5, ...)

    for tr in tr_list[1:]:

        td_list = tr.find_all('td')
        if not td_list:
            continue

        nick_w = td_list[1].get_text().split(' ')[0]
        nick_b = td_list[2].get_text().split(' ')[0]

        opponent = nick_w if nick_w != participant.user.username else nick_b
        if opponent not in done_list:

            try:
                opponent = tournament.participants.get(user__username=opponent)
            except Participant.DoesNotExist:
                return

            link = td_list[0].find('a').attrs.get('href')
            sgf = download_link(link).decode()
            finding_tag = re.search(tag, sgf)
            colour_of_winner = td_list[6].get_text()
            # handicap = td_list[3].get_text().split(' ')[1]
            try:
                score = float(colour_of_winner.split('+')[1])
            except ValueError:
                score = None

            if finding_tag:
                Game.objects.get_or_create(
                    white_player=participant if participant.user.username == nick_w else opponent,
                    black_player=participant if participant.user.username == nick_b else opponent,
                    tournament=tournament,
                    status='done',
                    # handicap=int(handicap) if handicap else 0,
                    result='white' if colour_of_winner.startswith('W') else 'black',
                    score=score
                )

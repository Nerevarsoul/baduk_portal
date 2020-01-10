from dataclasses import dataclass
from datetime import datetime, time

from django_rq import job

import requests
from bs4 import BeautifulSoup

from tournament.errors import *
from tournament.models import *


__all__ = ('parse_games_from_kgs',)


@job
def parse_games_from_kgs():
    for tournament in Tournament.objects.filter(is_active=True)\
            .prefetch_related('participants', 'participants__user'):
        kgs_parsing = KgsGameParsing(tournament)
        kgs_parsing.run()


@dataclass
class KgsGame:

    white_player: str
    black_player: str
    start_datetime: datetime
    link: str
    colour_of_winner: str

    @classmethod
    def create(cls, data: list):
        """
            0 -- ссылка на просмотр
            1 -- ник белого
            2 -- ник чёрного
            3 -- размер доски, фора
            4 -- дата и время начала партии
            5 -- тип партии (рейтинговая, свободная)
            6 -- результат (W+res, B+res,W+Time, B+14.5, ...)
        """

        if not data or len(data) != 7:
            raise KgsGameCreateError

        return cls(
            white_player=data[1].get_text().split(' ')[0],
            black_player=data[2].get_text().split(' ')[0],
            start_datetime=datetime.strptime(data[4].get_text(), "%m/%d/%y %H:%M %p"),
            link=data[0].find('a').attrs.get('href'),
            colour_of_winner=data[6].get_text()
            # handicap = td_list[3].get_text().split(' ')[1]
        )

    @property
    def is_finished(self) -> bool:
        return self.colour_of_winner != 'Unfinished'

    def get_score(self) -> float:
        try:
            score = float(self.colour_of_winner.split('+')[1])
        except (ValueError, IndexError):
            score = None
        return score


def download_link(link):
    if link is None:
        return ''
    ufr = requests.get(link)
    return ufr.content


class KgsGameParsing:

    KGS_URL = 'http://www.gokgs.com/gameArchives.jsp?user=+'

    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.done_list = []
        self.start_date = datetime.combine(self.tournament.start_date, time.min)
        self.end_game = datetime.combine(self.tournament.end_date, time.max)

    def run(self):
        for participant in self.tournament.participants.all():
            try:
                self.start_participant_parsing(participant)
                self.done_list.append(participant.user.username)
            except EmptyKgsTableError:
                continue

    def get_data_from_kgs(self, name):
        page = requests.get(f'{self.KGS_URL}{name}')
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find_all('table')

        if not table:
            raise EmptyKgsTableError

        tr_list = table[0].find_all('tr')

        if not tr_list:
            raise EmptyKgsTableError

        return tr_list

    def check_game_date(self, game: KgsGame):
        try:
            if self.end_game < game.start_datetime < self.start_date:
                print('6 hours')
                raise
        except ValueError:
            print('ValueError')
            return

    def parsing_game(self, table_line, participant: Participant):
        td_list = table_line.find_all('td')

        game = KgsGame.create(td_list)

        self.check_game_date(game)

        opponent = self.get_opponent(game, participant)

        sgf = self.download_sgf(game)

        if self.tournament.tag in sgf:
            self.save_game(game, participant, opponent)

    def get_opponent(self, game: KgsGame, participant: Participant):
        if game.white_player != participant.user.username:
            opponent = game.white_player
        else:
            opponent = game.black_player

        if opponent in self.done_list:
            raise OpponentDoneError

        return self.tournament.participants.get(user__username=opponent)

    def download_sgf(self, game):
        if game.link is None:
            return ''
        ufr = requests.get(game.link)
        return ufr.content.decode()

    def save_game(self, game, participant, opponent):
        username = participant.user.username
        Game.objects.get_or_create(
            white_player=participant if username == game.white_player else opponent,
            black_player=participant if username == game.black_player else opponent,
            tournament=self.tournament,
            time_started=game.start_datetime,
            status='done',
            # handicap=int(handicap) if handicap else 0,
            result='white' if game.colour_of_winner.startswith('W') else 'black',
            score=game.get_score()
        )

    def start_participant_parsing(self, participant):

        tr_list = self.get_data_from_kgs(participant.user.username)

        for table_line in tr_list[1:]:

            try:
                self.parsing_game(table_line, participant)
            except (KgsGameCreateError, OpponentDoneError, Participant.DoesNotExist):
                continue
            except Exception as e:
                print(participant)
                print(table_line)
                print(e)
                continue

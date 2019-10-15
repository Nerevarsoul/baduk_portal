from datetime import date
from typing import List, Tuple

from django.db import IntegrityError

from accounts.models import User, Subscription
from tsumego.models import Tsumego, TsumegoResult
from tsumego.tasks.base import BaseSpreadSheetParser


class TsumegoResultParser(BaseSpreadSheetParser):

    SUB_MAP = {
        0: 'задачи',
        1: 'лига',
        2: 'теория',
        3: 'форовая лига',
        4: 'специальное',
        5: 'ОГС',
    }

    TSUMEGO_MAP = {
        0: 'life and death',
        1: 'life and death',
        2: 'life and death',
        3: 'life and death',
        4: 'fuseki',
        5: 'fuseki',
        6: 'life and death',
        7: 'life and death',
        8: 'yose',
        9: 'yose',
    }

    LEVEL_MAP = {
        0: '1',
        1: '1',
        2: '1',
        3: '1',
        4: '0',
        5: '0',
        6: '2',
        7: '2',
        8: '2',
        9: '2',
    }

    TRUE = 'TRUE'

    MONTH_MAP = {
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'май': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'ноя': 11,
        'дек': 12,
    }

    def __init__(self, spreadsheet_id):
        super().__init__(spreadsheet_id)
        self.users = []
        self.month = 10
        self.year = 2019

    def get_current_range(self) -> str:
        today = date.today()
        for range_name in self.get_all_ranges():
            month, year = self.get_month_and_year(range_name)
            if month == today.month and year == today.year:
                return range_name

    def get_month_and_year(self, month_sheet: str) -> Tuple[int, int]:
        month, year = month_sheet.split()
        month = self.MONTH_MAP[month[0:3].lower()]
        return month, int(year)

    def run_current(self):
        range_name = self.get_current_range()
        self.handle_range(range_name)

    def run(self, first_range: int):
        for range_name in self.get_all_ranges()[first_range:]:
            self.handle_range(range_name)

    def handle_range(self, range_name):
        self.month, self.year = self.get_month_and_year(range_name)
        res = self.get_sheet(range_name).get('values', [])
        n = 33
        for i, row in enumerate(res):
            if i == 1:
                self.parse_user(row)
            if 2 < i < n:
                today = self.parse_day_result(row)
                if today:
                    n = 0

            # if i > 38:
            #     parse_subscription(row, users)

    def parse_user(self, row: List[str]):
        counter = 3
        while counter < len(row):
            ceil = row[counter]
            if ceil:
                nickname, name = ceil.split('(')
                user, _ = User.objects.get_or_create(
                    username=nickname if nickname else name,
                    first_name=name[:-1]
                )
                self.users.append(user)
            else:
                self.users.append(None)
            counter += 12

    def parse_day_result(self, row: List[str]):

        today = row[0] == self.TRUE
        day = int(row[1])
        task_count = row[2]
        if not task_count:
            return
        task_count = int(task_count)

        tsumegos = []
        for i in range(task_count):
            tsumego, _ = Tsumego.objects.get_or_create(
                number=i + 1,
                date=date(self.year, self.month, day),
                kind=self.TSUMEGO_MAP[i],
                level=self.LEVEL_MAP[i]
            )
            tsumegos.append(tsumego)

        step = task_count + 2
        counter = 0
        while counter < len(self.users):
            user = self.users[counter]
            if user:
                tasks = row[3 + counter * step: 3 + (counter + 1) * step]

                for i, task in enumerate(tasks[:int(task_count)]):
                    if any(tasks[:int(task_count)]):
                        try:
                            tsumego_result = TsumegoResult(
                                user=user,
                                tsumego=tsumegos[i],
                                status='done' if bool(task) else 'failed'
                            )
                            tsumego_result.save()
                        except IntegrityError:
                            pass

                position_task = row[3 + (counter + 1) * step - 1]
                if position_task:
                    position_task = int(position_task)
                    for i in range(position_task):
                        tsumego, _ = Tsumego.objects.get_or_create(
                            number=i + 11,
                            date=date(self.year, self.month, day),
                            kind='position',
                        )

                        tsumego_result = TsumegoResult(
                            user=user,
                            tsumego=tsumego,
                            status='done'
                        )
                        tsumego_result.save()

            counter += 1

        return today

    def parse_subscription(self, row: List[str], users: List[User]):
        if row[1]:
            user = self.find_user(*self.get_user(row[1]), users)
            for i, ceil in enumerate(row[25: 31]):
                if ceil == self.TRUE:
                    user.subscriptions.append(Subscription(self.SUB_MAP[i]))

    def get_user(self, ceil) -> Tuple[str, str]:
        nickname, name = ceil.split('(')
        return nickname, name[:-1]

    def find_user(self, nickname, name):
        if nickname:
            for user in self.users:
                if user.nickname == nickname:
                    return user
        if name:
            for user in self.users:
                if user.name == name:
                    return user
        return

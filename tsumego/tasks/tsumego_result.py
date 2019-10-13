import csv
from typing import List, Tuple
from datetime import date

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

    def __init__(self, spreadsheet_id):
        super().__init__(spreadsheet_id)
        self.users = []
        self.month = 9
        self.year = 2019

    def set_month_and_year(self, month_sheet: str):
        month, year = month_sheet.split()

    def run(self):
        for month_sheet in self.get_all_ranges():
            self.set_month_and_year(month_sheet)
            reader = csv.reader(self.get_sheet(month_sheet))
            n = 33
            for i, row in enumerate(reader):
                if i == 1:
                    self.parse_user(row)
                if 2 < i < n:
                    today = self.parse_day_result(row)
                    if today:
                        n = 0

                # if i > 38:
                #     parse_subscription(row, users)

    def parse_user(self, row: List[str]):
        for ceil in row:
            if ceil:
                nickname, name = ceil.split('(')
                user, _ = User.objects.get_or_create(
                    username=nickname if nickname else name,
                    first_name=name[:-1]
                )
                self.users.append(user)
            else:
                self.users.append(None)

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
                            TsumegoResult.objects.save(
                                user=user,
                                tsumego=tsumegos[i],
                                status='done' if bool(task) else 'failed'
                            )
                        except IntegrityError:
                            pass
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

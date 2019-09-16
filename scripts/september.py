import csv
from typing import List, Tuple
from datetime import date

from accounts.models import User, Subscription
from tsumego.models import Tsumego, TsumegoResult


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


def main():
    with open('09-2019.csv') as csvfile:
        users = []
        spamreader = csv.reader(csvfile)
        n = 33
        for i, row in enumerate(spamreader):
            if i == 1:
                parse_user(row, users)
            if 2 < i < n:
                today = parse_day(row, users)
                if today:
                    n = 0

            # if i > 38:
            #     parse_subscription(row, users)


def parse_user(row: List[str], users: list):
    for ceil in row:
        if ceil:
            nickname, name = ceil.split('(')
            user = User(
                username=nickname if nickname else name,
                first_name=name[:-1]
            )
            user.save()
            users.append(user)


def parse_day(row: List[str], users: List[User]):
    today = row[0] == 'TRUE'
    day = int(row[1])
    task_count = row[2]
    if not task_count:
        return
    task_count = int(task_count)
    tsumegos = []
    for i in range(task_count):
        tsumego = Tsumego(number=i + 1, date=date.today().replace(day=day), kind=TSUMEGO_MAP[i], level=LEVEL_MAP[i])
        tsumego.save()
        tsumegos.append(tsumego)
    step = task_count + 2
    counter = 0
    while counter < len(users):
        user = users[counter]
        tasks = row[3 + counter * step: 3 + (counter + 1) * step]
        for i, task in enumerate(tasks[:int(task_count)]):
            if any(tasks[:int(task_count)]):
                tsumego_result = TsumegoResult(user=user, tsumego=tsumegos[i], status='done' if bool(task) else 'failed')
                tsumego_result.save()
        counter += 1
    return today


def parse_subscription(row: List[str], users: List[User]):
    if row[1]:
        user = find_user(*get_user(row[1]), users)
        for i, ceil in  enumerate(row[25: 31]):
            if ceil == 'TRUE':
                user.subscriptions.append(Subscription(SUB_MAP[i]))


def get_user(ceil) -> Tuple[str, str]:
    nickname, name = ceil.split('(')
    return nickname, name[:-1]


def find_user(nickname, name, users: List[User]):
    if nickname:
        for user in users:
            if user.nickname == nickname:
                return user
    if name:
        for user in users:
            if user.name == name:
                return user
    return


if __name__ == '__main__':
    main()

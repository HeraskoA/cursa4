import datetime
from random import randint

from core.models import Repo, User


def write_test_data():
    data_ = [
        (2000 + i, randint(i * 10 + i, (i * 10 + i) * 2)) for i in range(1, 21)
    ]
    for i in data_:
        for _ in range(i[1]):
            Repo.objects.create(
                user=User.objects.first(),
                deep_link="",
                relative_dir="",
                language="",
                creation_date=datetime.datetime(year=i[0], month=1, day=1).date(),
                is_test=True,
            )

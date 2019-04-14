from ..models import get_tm_session
from ..models.bases import *
from datetime import date
from dateutil.relativedelta import relativedelta


def create_start(session_factory, transaction_manager):
    dbsession = get_tm_session(session_factory, transaction_manager.manager)

    with transaction_manager.manager:
        # admin user
        model = User(name='bunzuk1991', password='kat221008')
        dbsession.add(model)

        #Organisation
        org = Organisation(name='Садочок №1', name_printable='Садочок №1', address='м. Тернопіль', kod_zkpo='0000000', slug='sadochokNo1')
        dbsession.add(org)

        # Relations
        relation_list = {
            'Батько': 'Batyko',
            'Мати': 'Matu',
            'Дідусь': 'Didusy',
            'Бабуся': 'Babusia',
            'Прадідусь': 'Pradidusy',
            'Прабабуся': 'Prababusia',
            'Донька': 'Donyka',
            'Син': 'Sun',
            'Тітка': 'Titka',
            'Дядько': 'Dyadyko',
        }

        for key, value in relation_list.items():
            new_relation = Relation(name=key, actual=True, slug=value)
            dbsession.add(new_relation)

        garden_groups_list = {
            'Ясельна група': ['ЯСГ', 'yaselna-grupa'],
            'Молодша група': ['МОГ', 'molodsha-grupa'],
            'Середня група': ['СЕГ', 'serednya-grupa'],
            'Старша група': ['СТГ', 'starsha-grupa'],
        }

        now = date.today()
        year = date(year=now.year, month=6, day=30)
        past_year = year + relativedelta(years=-1)
        past_year = date(past_year.year, 9, 1)

        for key, value in garden_groups_list.items():
            new_garden_group = GardenGroup(name=key, short_name=value[0], slug=value[1], organisation=org)
            new_group = Group(name=new_garden_group.name, year_in=past_year, year_out=year, gardengroup=new_garden_group)
            dbsession.add(new_garden_group)
            dbsession.add(new_group)

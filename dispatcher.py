import datetime
import random
import re
import settings
from pprint import pprint

re_name_city = re.compile(r'[М]оскв\w+|[К]расноя\w+|[К]аз\w+|[С]анк\w+-\w+|[В]олг\w+|[У]ф\w+|[М]ур\w+|'
                          r'[Н]овос\w+|[К]раснод\w+|[Е]ка\w+|[С]ам\w+|[С]ар\w+|[Б]р\w+|[С]ур\w+|[Х]аб\w+'
                          r'|[С]оч\w+|[Н]ижн\w+-\w+|[Сс]ык\w+|[Н]ов\w+\s\w+|[Б]ар\w+|[И]рк\w+|[С]тав\w+|[О]ре\w+'
                          r'|[П]ер\w+|[С]мол\w+')
re_date = re.compile(r'\d{2}-\d{2}-2020')
re_race = re.compile(r'\d{4}')
re_yes_or_not = re.compile(r'[Дд]а')
re_number = re.compile(r'[1-5]')
re_some_text = re.compile(r'\w+')
re_phone = re.compile(r'\d+')
sites = [
    'Москва', 'Санкт-Петербург', 'Волгоград', 'Уфа', 'Мурманск', 'Новосибирск', 'Краснодар', 'Казань', 'Екатеринбург',
    'Самара', 'Саратов', 'Брянск', 'Сургут', 'Хабаровск', 'Смоленск', 'Сочи', 'Нижний-Новгород', 'Сыктывкар',
    'Новый Уренгой', 'Барнаул', 'Иркутск', 'Красноярск', 'Ставрополь', 'Оренбург', 'Пермь'
]

date = []
flights = []
route = ['{:^13}{:^21}'.format('Дата', '№')]
user_data = []
data_for_dispatcher = {}


def dispatcher_flight(text, context):
    match = re.match(re_date, text)
    if match:
        for city_departure in sites:
            data_for_dispatcher[city_departure] = {}
            for city_arrival in sites:
                if city_arrival == city_departure:
                    continue
                else:
                    data_for_dispatcher[city_departure][city_arrival] = {}
                    for _ in range(0, 5):
                        number_of_flight = str(random.randint(1000, 10000))
                        start_date = datetime.date.today().toordinal()
                        end_date = datetime.date.today().replace(day=31, month=12).toordinal()
                        random_day = datetime.date.fromordinal(random.randint(start_date, end_date))
                        data_for_dispatcher[city_departure][city_arrival][
                            random_day.strftime("%d-%m-%Y")] = number_of_flight
        for my_date, number in data_for_dispatcher[context['Откуда']][context['Куда']].items():
            date.append(my_date)
            flights.append(number)
            route.append(my_date + ' - ' + number)
        # print('\n'.join(date))
        # print('\n'.join(flights))
        x = '\n'.join(route)
        message = f"Из {context['Откуда']}, в {context['Куда']}" \
                  f" есть такие рейсы:\n{x}\n Введите номер:"
        # context.clear()
        return message
    else:
        return False


def dispatcher_city_departure(text, context):
    match = re.match(re_name_city, text)
    if match.group(0) in sites:
        context['Откуда'] = text
        user_data.append('Откуда - ' + text)
        return True
    else:
        return False


def dispatcher_city_arrival(text, context):
    match = re.match(re_name_city, text)
    if match.group(0) in sites:
        context['Куда'] = text
        user_data.append('Куда - ' + text)
        return True
    else:
        return False


def dispatcher_date(text, context):
    match = re.match(re_date, text)
    if match:
        return True
    else:
        return False


def dispatcher_route(text, context):
    match = re.match(re_race, text)
    if match and match.group(0) in flights:
        context['Рейс'] = text
        user_data.append('Рейс - ' + text)

        return True
    else:
        return False


def dispatcher_number(text, context):
    match = re.match(re_number, text)
    if match:
        context['Количество мест'] = text
        user_data.append('Количество мест - ' + text)

        return True
    else:
        return False


def yes_or_not(text, context):
    match = re.match(re_yes_or_not, text)
    if match:
        return True
    else:
        return False


def confirmation_entered_data(text, context):
    match = re.match(re_some_text, text)
    if match:
        message = '\n'.join(user_data) + "\n" + "Данные верны? (Да/Нет)"
        return message
    else:
        return False


def some_text(text, context):
    match = re.match(re_some_text, text)
    if match:
        return True
    else:
        return False


def phone(text, context):
    match = re.match(re_phone, text)
    if match:
        return True
    else:
        return False

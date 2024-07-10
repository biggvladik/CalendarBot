import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build

import config


def check_name(name: str, workers: list):
    for worker in workers:
        if name.lower() in worker.lower():
            return True
    return False


def get_event_by_name(date: str):
    month_number = date.split('.')[1]

    gc = gspread.service_account(filename='credits.json')
    worksheet = gc.open(get_month(config.directory_id, month_number))
    worksheet_list = worksheet.worksheets()
    current_res = []
    for sheet in worksheet_list:
        worksheets = sheet.get_all_values()
        for item in worksheets[1::]:
            if item[0] is None or item[0] == '':
                continue
            sport_name = item[1]
            date_number = item[0].split('\n')[0]
            day_name = item[0].split('\n')[1]
            workers = [i.strip() for i in item[7].split('\n')]
            event_name = item[2].replace('\n', ' ')
            time = item[5]
            if date == date_number:
                current_res.append((date_number, day_name, workers, event_name, time, sport_name))
    return current_res


def make_str(data: list):
    res_s = ''
    for number, s in enumerate(data):
        workers = ', '.join(s[2])
        date = s[0] + ' | ' + s[1] + ' | ' + s[4]
        date = date.replace('\n', ' ')
        name_event = s[3]
        res = (f'<b>Дата</b>: {date}\n'
               f'<b>Вид спорта</b>: {s[-1]}\n'
               f'<b>Событие</b>: {name_event}\n'
               f'<b>Работники</b>: {workers}\n')
        res_s = res_s + res
        res_s = res_s + '-----------------------------------------' + '\n'
    if res_s == '':
        res_s = 'Расписание не найдено!'
    return res_s


def get_month(directory_id: str, month_number: str):
    scopes = ['https://www.googleapis.com/auth/drive']
    service_account_file = 'credits.json'
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)
    service = build('drive', 'v3', credentials=credentials)

    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, createdTime)",
                                   q=f"'{directory_id}' in parents").execute()
    results['files'] = sorted(results['files'], key=lambda x: x['createdTime'])
    return [i['name'] for i in results['files'][-2:] if month_number in i['name']][0]


def get_month_full(directory_id: str):
    scopes = ['https://www.googleapis.com/auth/drive']
    service_account_file = 'credits.json'
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)
    service = build('drive', 'v3', credentials=credentials)

    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, createdTime)",
                                   q=f"'{directory_id}' in parents").execute()

    results['files'] = sorted(results['files'], key=lambda x: x['createdTime'])
    return results


def make_distrib(players: list, events: list):
    for event in events:
        for player in players:
            for player_name in [i.strip().lower() for i in event[2]]:
                if player['name'].lower().strip() in player_name:
                    player['event'].append(event)

    return players


def make_result_distrib(events: list):
    s = ''
    for number, event in enumerate(events):
        status = (lambda x: '+' if x else '-')(event[2])
        s = s + (f'<b>ДАТА</b>: {event[0]}\n'
                 f'<b>РАБОТНИК</b>: {event[3]}\n'
                 f'<b>СТАТУС</b>: {status}\n')
        if number != len(events) - 1:
            s = s + '----------------\n'
    if s == '':
        return 'Событий в этот день не найдено!'
    return s


def make_full_str(string: str):
    substring = "-----------------------------------------"

    # Находим индекс последнего вхождения подстроки в строку
    index = string.rfind(substring)

    # Если подстрока найдена, удаляем ее
    if index != -1:
        new_string = string[:index] + string[index + len(substring):]
        return new_string
    return string

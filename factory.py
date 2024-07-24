import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import config


def check_name(name: str, workers: list):
    for worker in workers:
        if name.lower() in worker.lower():
            return True
    return False


def get_event_by_name_old(date: str):
    month_number = date.split('.')[1]
    date_datetime = datetime.strptime(date, '%d.%m.%Y')
    gc = gspread.service_account(filename='credits.json')
    worksheet = gc.open(get_month(config.directory_id, month_number))
    worksheet_list = worksheet.worksheets()
    current_res = []
    date_number_old = None
    for sheet in worksheet_list:
        worksheets = sheet.get_all_values()
        for item in worksheets[1::]:
            if item[0] == '' and item[7] == '':
                continue
            if item[0] == '' and item[7] and current_res and current_res[-1][0] == date_number_old:
                current_res[-1][2] += [i.strip() for i in item[7].split('\n')]
                continue

            if item[0] == '' and item[7] and not current_res:
                continue

            sport_name = item[1]
            date_number = item[0].split('\n')[0]

            if date_datetime < datetime.strptime(date_number, '%d.%m.%Y'):
                return current_res

            date_number_old = date_number
            day_name = item[0].split('\n')[1]
            workers = [i.strip() for i in item[7].split('\n')]
            event_name = item[2].replace('\n', ' ')
            time = item[5]
            if date == date_number:
                current_res.append([date_number, day_name, workers, event_name, time, sport_name])

    return current_res


def make_str(data: list):
    res_s = ''
    for number, s in enumerate(data):
        workers = ', '.join(set(s[2]))
        date = s[0]
        date = date.replace('\n', ' ')
        name_event = (lambda x: x[3] if x[3] else x[-1])(s)
        res = (f'<b>Дата</b>: {date}\n'
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
    return [i['name'] for i in results['files'] if month_number in i['name']][0]


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
        status = (lambda x: '✅' if x == 1 else '❌')(event[2])
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


def get_event_by_name(date: str):
    print('get_event_by_name', date)
    month_number = date.split('.')[1]
    date_datetime = datetime.strptime(date, '%d.%m.%Y')
    gc = gspread.service_account(filename='credits.json')
    worksheet = gc.open(get_month(config.directory_id, month_number))
    worksheet_list = worksheet.worksheets()
    current_res = []
    day_number_old = None
    date_number_old = None
    worksheet_data = []
    for sheet in worksheet_list:
        worksheets = sheet.get_all_values()
        worksheet_data.append(worksheets)

        for item in worksheets[1::]:
            if item[0] == '' and item[7] == '':
                continue
            if item[0] == '' and item[7] and current_res and current_res[-1][0] == date_number_old and not (item[2]):
                current_res[-1][2] += [i.strip() for i in item[7].split('\n')]
                continue

            if item[0] == '' and item[7] and not current_res:
                continue

            sport_name = item[1]
            date_number = item[0].split('\n')[0]
            if date_number == '':
                date_number = date_number_old
            if date_datetime < datetime.strptime(date_number, '%d.%m.%Y'):
                return current_res

            date_number_old = date_number
            try:
                day_name = item[0].split('\n')[1]
                day_number_old = day_name

            except Exception as error:
                print(error)
                day_name = day_number_old

            workers = [i.strip() for i in item[7].split('\n')]
            print(workers)
            event_name = item[2].replace('\n', ' ')
            time = item[5]
            if date == date_number:
                current_res.append([date_number, day_name, workers, event_name, time, sport_name])

    return current_res

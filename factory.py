import gspread
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io

import config


def check_name(name:str,workers:list):
    for worker in workers:
        if name.lower() in worker.lower():
            return True
    return False
def get_event_by_name(name:str,month_name:str):
    now = datetime.now()
    gc = gspread.service_account(filename='credits.json')
    worksheet = gc.open(month_name)
    worksheet_list = worksheet.worksheets()
    current_res = []
    for sheet in worksheet_list:
        worksheets = sheet.get_all_values()
        for item in worksheets[1::]:
            if item[0] is None or item[0] == '':
                continue
            date_number = item[0].split('\n')[0]
            day_name = item[0].split('\n')[1]
            workers = item[7].split('\n')
            event_name = item[2].replace('\n','')
            time = item[5]
            if check_name(name,workers) and datetime.strptime(date_number,'%d.%m.%Y') > now:
                current_res.append((date_number,day_name,workers,event_name,time))
    return current_res

def make_str(data:list):

    res_s = ''
    for number,s in enumerate(data):
        workers = ', '.join(s[2])
        name_s = str(number) +'.' + ' | ' + s[0] + ' | ' + s[1] + ' | ' + workers + ' | ' + s[3] + ' | ' + s[4] + ' | '
        res_s = res_s + name_s + '\n' + '-----------------------------------------' +  '\n'

    if res_s =='':
        res_s = 'Расписание не найдено!'
    return res_s




def get_month(directory_id:str ):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'credits.json'
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)


    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, createdTime)",q=f"'{directory_id}' in parents").execute()
    results['files'] = sorted(results['files'], key=lambda x: x['createdTime'])
    return [i['name'] for i in results['files'][-2:]]


print(get_month(config.directory_id))
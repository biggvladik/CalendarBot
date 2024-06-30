import gspread
from datetime import datetime



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
    return res_s





import requests
import json
import datetime
from schema import Schema

login_url='https://app.dev.getdecode.io/authentication/login'
username="bantupalli.sriharsha@entropiktech.com"
password="Harsha@10150"
organization_id=''
get_user_organiztion_id_url='https://app.dev.getdecode.io/authentication/get-user-organizations'
list_organization_id_url=f'https://in.dev.apicx.getdecode.io/v1/studies/list?organisation_id={organization_id}'
date_format1="%Y-%m-%d"
date_format2="%Y-%m"
study_count=0

def generate_headers():
    #To generater authorization id and id token
    request_json={'username': username, 'password': password, 'workspace': "beintern"}
    jsondata=json.dumps(request_json)
    response=requests.post(login_url, data=jsondata)
    assert response.status_code==200, 'Error'
    c=response.content
    c=json.loads(c.decode('utf-8'))
    access_token=c['data']['access_token']
    id_token=c['data']['id_token']

    return {'authorization': access_token, 'id_token': id_token, 'workspace_id': '01GG7AW75CHDNZ2BNYKZS9ZHMF'}


def generate_organization_id(url):
    #To generate organization id using get method
    global organization_id

    response=requests.get(url, headers=headers1)
    assert response.status_code==200, 'Error'
    c=response.content
    c=json.loads(c.decode('utf-8'))
    organization_id=c['data'][0]['id']


def generate_study_count(url):
    #To generate no. of blocks on a specific date
    global study_count
    date1=month1=year1=0

    workspace_id1=input('Enter workspace_id: ')
    n=input("Enter d for day, m for month or y for year: ")
    print(n)

    if(n=='d'):
        date1=input('Enter date: ')
        month1=input('Enter month: ')
        year1=input('Enter year: ')
        default_date=f'{year1}-{month1}-{date1}'
        date1=datetime.datetime.strptime(default_date, date_format1)
        print(f'You are looking for {date1}')
    if(n=='m'):
        month1=input('Enter month: ')
        year1=input('Enter year: ')
        default_date=f'{year1}-{month1}'
        month1=datetime.datetime.strptime(default_date, date_format2)
        print(f'You are looking for {month1}')
    if(n=='y'):
        year1=input('Enter year: ')
        default_date=f'{year1}-09-03'
        year1=datetime.datetime.strptime(default_date, date_format1)
        year1=year1.year
        print(f'You are looking for {year1}')

    request_json={"page_size":20,"timezone":"Asia/Calcutta","last_evaluated_key":None,"selected_collection_identifier":""}
    jsondata=json.dumps(request_json)
    response=requests.post(url, headers=headers1, data=jsondata)
    assert response.status_code==200, 'Error'
    c=response.content
    c=json.loads(c.decode('utf-8'))

    for i in range(0, len(c['data']['studies'])):
        date=c['data']['studies'][i]['last_modified_date']
        print(date)
        workspace_id2=c['data']['studies'][i]['workspace_id']
        study_created=datetime.datetime.strptime(date, date_format1)
        x=f'{study_created.year}-{study_created.month}'
        date2=study_created
        month2=datetime.datetime.strptime(x, date_format2)
        year2=study_created.year
        
        if(workspace_id1==workspace_id2 and date1==date2):
            study_count=study_count+1
        if(workspace_id1==workspace_id2 and month1==month2):
            study_count=study_count+1
        if(workspace_id1==workspace_id2 and year1==year2):
            study_count=study_count+1


headers1=generate_headers()
generate_organization_id(get_user_organiztion_id_url)
generate_study_count(list_organization_id_url)
print("Study_count: ",study_count)



import datetime
import ipware
import json
import os

USERS_FILE_PATH = './utils/users.json'


def get_client_ip(request):
    client_ip, is_routable = ipware.get_client_ip(request)
    return client_ip


def linkedin_verification_ip_token_date(request):
    ip = get_client_ip(request)
    my_file = os.path.isfile(USERS_FILE_PATH)
    if my_file is True:
        json_data = open(USERS_FILE_PATH, 'r')
    else:
        json_data = open(USERS_FILE_PATH, 'w')
        json_data.write("{}")
        json_data.close()
        json_data = open(USERS_FILE_PATH, 'r')
    users = json.load(json_data)
    if ip in users:
        user = users[ip]
        today = datetime.datetime.now()
        date_use = datetime.datetime.strptime(user['Date'], "%Y-%m-%d %H:%M:%S.%f")
        tmp = date_use+datetime.timedelta(days=60)
        if tmp > today:
            response = True
        else:
            del users[ip]
            f = open(USERS_FILE_PATH, "w")
            f.write(json.dumps(users, indent=4))
            f.close()
            json_data.close()
            response = False
    else:
        response = False
    return response

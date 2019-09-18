import json
from datetime import datetime


with open('_U1ZQR43RB.json') as f:
    data = json.load(f)


group_by_user = {}
_last_time = {}


def _to_datetime(ts):
    msg_time = float(ts)
    return datetime.fromtimestamp(msg_time)


for user in data:
    if user['type'] != 'message':
        continue

    ts = user['ts']
    username = user['user']
    msg_txt = user['text']

    if not msg_txt:
        msg_txt = user['files']

    two_min = 2*60  # seconds
    group_msg = group_by_user.get(username)
    if group_msg:
        msg_time = _to_datetime(ts)
        if (msg_time - _last_time[username]['dt']).seconds < two_min:
            group_by_user[username][_last_time[username]['ts']].append(msg_txt)
        else:
            if isinstance(msg_txt, list):
                group_by_user[username][ts] = msg_txt
            else:
                group_by_user[username][ts] = [msg_txt]
            _last_time[username] = {
                'dt': _to_datetime(ts),
                'ts': ts
            }
    else:
        group_by_user[username] = {
            ts: [msg_txt]
        }
        _last_time[username] = {
            'dt': _to_datetime(ts),
            'ts': ts
        }


for user in group_by_user:
    with open(f'{user}.json', 'w') as user_file:
        json.dump(group_by_user[user], user_file, indent=4)

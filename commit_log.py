import datetime
import json
import time

import requests

'''
授权信息
更换成自己的token
'''
access_token = "your token"
owner = "txrj"
repo = "tx-cloud"

base_url = "https://gitee.com/api"

'''
需要匹配的作者信息，二选一，也可以全选，会根据下列配置进行获取提交信息
'''
author_names = ['lhr', 'zzlhr']
author_emails = ['2388399752@qq.com']

'''
提交的内容数组
'''
commits = []

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

'''
获取的提交commit时间区间
'''
begin_time = time.mktime(today.timetuple())
end_time = time.mktime(tomorrow.timetuple())


def author_you(commit_author_name, commit_author_email):
    for author_name in author_names:
        if commit_author_name == author_name:
            return True
    for author_email in author_emails:
        if author_email == commit_author_email:
            return True
    return False


def get_commits():
    api_path = "/v5/repos/{owner}/{repo}/commits"
    api_path = api_path.replace("{owner}", owner).replace("{repo}", repo)
    url = base_url + api_path + "?access_token=" + access_token + "&page=1&per_page=20"
    resp = requests.get(url)
    resp_json = json.loads(resp.text)
    for item in resp_json:
        commit = item['commit']
        commit_author_name = commit['author']['name']
        commit_author_email = commit['author']['email']
        commit_time = commit['commiter']['date'][0:19].replace('T', ' ')
        # 格式化统一时间进行匹配
        commit_time_datatime = time.mktime(time.strptime(commit_time, "%Y-%m-%d %H:%M:%S"))

        if not (int(begin_time) < int(commit_time_datatime) & int(commit_time_datatime) < int(end_time)):
            # 时间不在需要区间
            continue
        commit_message = commit['message']
        if author_you(commit_author_name, commit_author_email):
            commits.append(commit_message)
        print('commit: author=%s, email=%s, message=%s, time=%s'
              % (commit_author_name, commit_author_email, commit_message, commit_time))


get_commits()
print(commits)

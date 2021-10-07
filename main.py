import requests
from github import Github
from tabulate import tabulate

def get_repo_commits(repo_name):
    g = Github(login_or_token="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")
    repo = g.get_repo(repo_name)
    last_commits = repo.get_commits()[:10]
    return last_commits

def get_data_from_json(json_data):
    commit_data = dict()
    commit_data['commit_id'] = json_data['commit_id']
    commit_data['author'] = json_data['user']['login']
    commit_data['date'] = json_data['updated_at']
    commit_data['comment_text'] = json_data['body']
    return commit_data

def print_data(data):
    headers = []
    table = []
    for name in data[0]:
        headers.append(name)
    for el in data:
        table_row = []
        for key, value in el.items():
            table_row.append(value)
        table.append(table_row)
    print(tabulate(table, headers, tablefmt="grid"))




link = input()
#link = 'https://github.com/WebsterQR/CPA-1-Test-Task'
repo_name = "/".join(link.split('/')[-2:])


last_commits = get_repo_commits(repo_name)

result = []

for commit in last_commits:
    comments_url = commit.comments_url
    comments = requests.get(comments_url)
    if not comments.json():
        continue
    json_data = comments.json()
    for comment in json_data:
        commit_data = get_data_from_json(comment)
        result.append(commit_data)

print_data(result)
import requests
import json

url = 'https://api.github.com'
user = 'Octokit'
# user = 'Mstislav13'

response = requests.get(f"{url}/users/{user}/repos")
data = response.json()

for repos in data:
    title_name = repos['name']
    print(f'{title_name}')

with open('list_task_1.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

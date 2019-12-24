from django.utils.translation import gettext as _

from decouple import config
from github import Github
import requests


client = Github(config('GITHUB_USER'), config('GITHUB_SECRET'))
admin_user = client.get_user()


class GithubRepo:
    def __init__(self, username):
        self.username = username
        self.github_user = client.get_user(username)

    def get_user_repos(self):
        return self.github_user.get_repos()

    def get_repos_informations(self):
        repos = self.get_user_repos()
        list_repo = []
        for repo in repos:
            try:
                read_file = repo.get_contents("README.md")
                download_url = read_file.download_url
                r = requests.get(download_url)
                text = r.text
                if text[0] == '#':
                    description = text.split("\n")[1:]
                else:
                    description = text.split("\n")
            except:
                description = [_(
                    "Aucun fichier nommé 'README.md' n'a été trouvé à la racine de ce dépôt.")]
            obj = {
                'name': repo.name,
                'url': repo.html_url,
                'description': description,
                'watchers': repo.watchers_count,
                'stars': repo.stargazers_count,
            }
            list_repo.append(obj)
        return list_repo

    def get_personal_repos_informations(self):
        repos = self.get_user_repos()
        list_repo = []
        for repo in repos:
            if not repo.fork:
                try:
                    read_file = repo.get_contents("README.md")
                    download_url = read_file.download_url
                    r = requests.get(download_url)
                    text = r.text
                    if text[0] == '#':
                        description = ' '.join(text.split("\n")[1:])
                    else:
                        description = text
                except:
                    description = [_(
                        "Aucun fichier nommé 'README.md' n'a été trouvé à la racine de ce dépôt.")]
                obj = {
                    'name': repo.name,
                    'url': repo.html_url,
                    'description': description,
                    'watchers': repo.watchers_count,
                    'stars': repo.stargazers_count,
                }
                list_repo.append(obj)
        return list_repo

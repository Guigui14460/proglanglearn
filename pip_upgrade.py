import datetime
import os
import pip
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call


def get_outdated():
    list_command = pip.commands.list.ListCommand()
    options, args = list_command.parse_args([])
    packages = get_installed_distributions()
    return list_command.get_outdated(packages, options)


def upgrade_oudated(all_pkgs=False):
    packages_upgraded = []
    if all_pkgs:
        to_upgrade = get_packages(upgrade=True)
    else:
        to_upgrade = get_outdated()
    for dist in to_upgrade:
        call(f"pip install --upgrade {dist.project_name}", shell=True)
        packages_upgraded.append(dist.project_name)
    if len(packages_upgraded) > 0:
        print('Following packages upgraded successfully :')
        for pkg in packages_upgraded:
            print('-', pkg)
    print('\n')


def set_archive_filepath(requirements_path, filepath=None, item=0):
    if filepath is None:
        base_filepath = os.path.join(requirements_path, "archive.txt")
    else:
        if item >= 0:
            item += 1
        today = str(datetime.date.today())
        base_filepath = os.path.join(
            requirements_path, f"archive_{today}_{item}.txt")
    if os.path.exists(base_filepath):
        return set_archive_filepath(requirements_path, filepath=base_filepath, item=item)
    return base_filepath


def save_archive(archive_list):
    print('Saving archive ...')
    requirements_path = os.path.join(os.getcwd(), "archives")
    if not os.path.exists(requirements_path):
        os.mkdir(requirements_path)
    filepath = set_archive_filepath(requirements_path)
    with open(filepath, 'w+') as archive:
        for rq in sorted(archive_list, key=str.lower):
            archive.write(str(rq) + '\n')


def make_archive():
    print('Making archive ...')
    current = get_packages()
    save_archive(current)
    print('Archive done !')


def get_packages(upgrade=False):
    print('Getting packages ...')
    current = []
    for dist in get_installed_distributions():
        if upgrade:
            current.append(dist)
        else:
            current.append(str(dist.as_requirement()))
    return current


def get_requirements_location(next_to=None):
    if next_to is not None:
        location = None
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if str(file) == str(next_to):
                    location = os.path.join(root, 'requirements.txt')
                    return location
    return None


def save_requirements(next_to=None):  # can next_to='manage.py'
    packages = get_packages()
    print('Saving requirements ...')
    location = get_requirements_location(next_to=next_to)
    if location is None:
        location = os.path.join(os.getcwd(), 'requirements.txt')
    with open(location, 'w') as f:
        for pkg in sorted(packages, key=str.lower):
            f.write(str(pkg) + '\n')
    print('Requirements saved !')


make_archive()
upgrade_oudated(all_pkgs=False)
save_requirements()

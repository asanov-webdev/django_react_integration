import os
from tools.copyFile import copyFile

config = open('config.txt', 'r')
react_app_name = 'react_app'
should_start_react_app = True
react_app_path = '.'
react_templates_path = f'./templates/react_app/'


def handle_config():
    global react_app_name, should_start_react_app, react_app_path, react_templates_path

    for line in config:
        if line.startswith('react_app_name'):
            react_app_name = line.split('=')[1][:-1]
        if line.startswith('should_start_react_app'):
            value = line.split('=')[1]

            if value == '1':
                should_start_react_app = True
            elif value == '0':
                should_start_react_app = False
            else:
                print(f'"{value}" не является допустимым значением параметра should_start_react_app.')
        if line.startswith('react_app_path'):
            value = line.split('=')[1][:-1]
            if not os.path.isdir(value):
                print(f'"{value}" не является директорией.')
            elif not os.path.exists(f'{value}/{react_app_path}'):
                print(f'"{value}" уже содержите в себе директорию "{react_app_path}"')
            else:
                react_app_path = value
        if line.startswith('react_templates_path'):
            value = line.split('=')[1][:-1]
            if not os.path.isdir(value):
                print(f'"{value}" не является директорией.')
            else:
                react_templates_path = value


if __name__ == '__main__':
    handle_config()

    createApp = f'cd {react_app_path} && yarn create react-app {react_app_name}'
    installPackages = f'cd {react_app_path} && cd {react_app_name} && yarn add axios'

    os.system(createApp)
    os.system(installPackages)

    REACT_DEST_PATH = f'{react_app_path}/{react_app_name}/src/'

    project_templates = ['axios-config.js', 'api.js', 'App.js']

    for t in project_templates:
        print(react_templates_path + t)
        print(REACT_DEST_PATH + t)
        copyFile(react_templates_path + t, REACT_DEST_PATH + t)

    if should_start_react_app:
        run = f'cd {react_app_path} && cd {react_app_name} && yarn start'
        os.system(run)

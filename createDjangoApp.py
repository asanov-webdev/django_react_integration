import os
import webbrowser
from tools.copyFile import copyFile

config = open('config.txt', 'r')
django_app_name = 'django_app'
should_start_django_app = True
django_app_path = '.'
django_templates_path = f'./templates/django_app/'
should_create_example_model = True


def handle_config():
    global django_app_name, should_start_django_app, django_app_path, django_templates_path, should_create_example_model

    for line in config:
        if line.startswith('django_app_name'):
            django_app_name = line.split('=')[1][:-1]

            try:
                replace_app_name()
            except:
                print(f'"{django_app_name}" не является допустимым значением параметра django_app_name.')
        if line.startswith('should_start_django_app'):
            value = line.split('=')[1][:-1]

            if value == '1':
                should_start_django_app = True
            elif value == '0':
                should_start_django_app = False
            else:
                print(f'"{value}" не является допустимым значением параметра should_start_django_app.')
        if line.startswith('django_app_path'):
            value = line.split('=')[1][:-1]
            if not os.path.isdir(value):
                print(f'"{value}" не является директорией.')
            elif os.path.exists(f'{value}/{django_app_name}'):
                print(f'"{value}" уже содержит в себе директорию "{django_app_name}"')
            else:
                django_app_path = value
        if line.startswith('django_templates_path'):
            value = line.split('=')[1][:-1]
            if not os.path.isdir(value):
                print(f'"{value}" не является директорией.')
            else:
                django_templates_path = value
        if line.startswith('should_create_example_model'):
            value = line.split('=')[1][:-1]

            if value == '1':
                should_create_example_model = True
            elif value == '0':
                should_create_example_model = False
            else:
                print(f'"{value}" не является допустимым значением параметра should_create_example_model.')


def replace_app_name():
    f = open(django_templates_path + 'django_app/settings.py', "r")
    contents = f.readlines()
    f.close()

    contents[44] = f'ROOT_URLCONF = \'{django_app_name}.urls\'\n'
    contents[62] = f'WSGI_APPLICATION = \'{django_app_name}.wsgi.application\'\n'

    f = open(django_templates_path + 'django_app/settings.py', "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


if __name__ == '__main__':
    handle_config()

    startProject = f'cd {django_app_path} && django-admin startproject {django_app_name} && cd {django_app_name} && ' \
                   f'django-admin startapp app0'

    installPackages = fr'cd {django_app_path} && cd {django_app_name} && py -m venv env && env\scripts\activate && ' \
                      r'pip install django djangorestframework django-cors-headers'

    os.system(startProject)
    os.system(installPackages)

    project_templates = ['settings.py', 'urls.py']

    DJANGO_DEST_PATH = f'{django_app_path}/{django_app_name}/'

    for t in project_templates:
        copyFile(django_templates_path + f'django_app/' + t, DJANGO_DEST_PATH + f'{django_app_name}/' + t)

    if should_create_example_model:
        app_templates = ['models.py', 'serializers.py', 'urls.py', 'views.py']

        for t in app_templates:
            copyFile(django_templates_path + 'app0/' + t, DJANGO_DEST_PATH + 'app0/' + t)

    migrate = fr'cd {django_app_path} && cd {django_app_name} && env\scripts\activate && ' \
              fr'python manage.py makemigrations && python manage.py migrate'

    os.system(migrate)

    if should_start_django_app:
        run = fr'cd {django_app_path} && cd {django_app_name} && env\scripts\activate && python manage.py runserver'

        webbrowser.open('http://127.0.0.1:8000/api/app0/')
        os.system(run)

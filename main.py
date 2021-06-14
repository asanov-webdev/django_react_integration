import os
import re
from multiprocessing import Pool

processes = []
config = open('config.txt')
react_app_name = ''
django_app_name = ''
django_templates_path = f'./templates/django_app/'


def get_react_app_name():
    global react_app_name
    for line in config:
        if line.startswith('react_app_name'):
            react_app_name = line.split('=')[1][:-1]


def get_django_app_name():
    global django_app_name
    for line in config:
        if line.startswith('django_app_name'):
            django_app_name = line.split('=')[1][:-1]


def handle_config():
    global django_templates_path
    for line in config:
        if line.startswith('create_django_app'):
            value = line.split('=')[1][:-1]

            if value == '1':
                processes.append('createDjangoApp.py')
            elif value != '0':
                print(f'"{value}" не является допустимым значением параметра create_django_app.')
        elif line.startswith('create_react_app'):
            value = line.split('=')[1][:-1]

            if value == '1':
                processes.append('createReactApp.py')
            elif value != '0':
                print(f'"{value}" не является допустимым значением параметра create_react_app.')
        elif line.startswith('django_templates_path'):
            value = line.split('=')[1][:-1]
            if not os.path.isdir(value):
                print(f'"{value}" не является директорией.')
            else:
                django_templates_path = value


def run_process(process):
    os.system('python {}'.format(process))


def generate_app():
    handle_config()

    with Pool(2) as pool:
        pool.map(run_process, processes)


def add_request():
    function_name = input_parts[1].split('=')[1]
    request_type = input_parts[2].split('=')[1]
    url = input_parts[3].split('=')[1]

    f = open('requestTemplate.txt', 'r')
    text = f.read()

    result = re.findall(r'{{ \w+ }}', text)
    sub_result = re.sub(result[0], function_name, text)
    sub_result1 = re.sub(result[1], request_type, sub_result)
    sub_result2 = re.sub(result[2], url, sub_result1)

    if len(react_app_name) < 1:
        get_react_app_name()

    file_object = open(f'{react_app_name}/src/api.js', 'a')
    file_object.write(sub_result2)
    file_object.close()

    f.close()


def add_endpoint():
    print(input_parts)
    model_name = input_parts[1].split('=')[1]
    use_base_models = input_parts[2].split('=')[1]
    url = input_parts[2].split('=')[1]
    app_name = input_parts[3].split('=')[1]

    if len(django_app_name) < 1:
        get_django_app_name()

    # MODELS

    f = open(django_templates_path + f'models/{model_name}.txt', "r")
    text = f.read()
    f.close()

    models_file_object = open(f'{django_app_name}/{app_name}/models.py', 'a')
    models_file_object.write(f'\n\n{text}')
    models_file_object.close()

    # SERIALIZERS

    serializers_file = open('serializersTemplate.txt', 'r')
    serializers_text = serializers_file.read()

    serializers_result = re.findall(r'{{ \w+ }}', serializers_text)
    sub_serializers_result = re.sub(serializers_result[0], model_name, serializers_text)

    serializers_file_object = open(f'{django_app_name}/{app_name}/serializers.py', 'a')
    serializers_file_object.write(f'\n{sub_serializers_result}')
    serializers_file_object.close()

    # URLS

    urls_file_read = open(f'{django_app_name}/{app_name}/urls.py', 'r')
    contents = urls_file_read.readlines()
    urls_file_read.close()

    contents[len(contents) - 1] = f'\tpath(\'{url}\', views.{model_name}ListCreate.as_view()),\n]'

    urls_file_write = open(f'{django_app_name}/{app_name}/urls.py', 'w')
    contents = "".join(contents)
    urls_file_write.write(contents)
    urls_file_write.close()

    # VIEWS

    views_file = open('viewsTemplate.txt', 'r')
    views_text = views_file.read()

    views_result = re.findall(r'{{ \w+ }}', views_text)
    sub_views_result = re.sub(views_result[0], model_name, views_text)

    views_file_object = open(f'{django_app_name}/{app_name}/views.py', 'a')
    views_file_object.write(f'\n{sub_views_result}')
    views_file_object.close()


if __name__ == "__main__":
    while True:
        print(os.getcwd() + '>', end='')
        user_input = input()
        input_parts = user_input.split(' ')
        command = input_parts[0]

        if command == 'generate_app':
            generate_app()
        elif command == 'add_request':
            add_request()
        elif command == 'add_endpoint':
            add_endpoint()
        else:
            print(f'"{command}" не является поддерживаемой коммандой.')

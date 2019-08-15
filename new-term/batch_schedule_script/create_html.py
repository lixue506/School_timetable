"""
    Author: mushan
    Date: 2019/2/23 15:02
    Version: 1.0
    Describe: 将数据格式化，传递给HTML模板
"""

from os import path

from .read_information import read_schedule
from .template_call import html_template


def create_schedule(path_dict):
    """创建课表详情网页 文件字典（路径，输出路径，文件）：path_dict"""
    for file in path_dict['files_path']:
        if file.strip().endswith('.xls'):
            content = read_schedule(path.join(path_dict['root_dir'], file))
            html = html_template('schedule.html', content)
            out_path = path.join(path_dict['out_dir'], path.splitext(file)[0] + '.html')
            with open(out_path, 'w', encoding='utf-8') as file_path:
                file_path.write(html)
            print(path.splitext(file)[0]+'文件已创建')


def create_class_list(class_list):
    content = {}
    for file in class_list:
        if file.strip().endswith('.xls'):
            major = content.setdefault(file[0:2], {})
            major.setdefault('head', set())
            major['head'].add('20' + file[2:4])
            grade = major.setdefault('body', {})
            classes = grade.setdefault(file[4:6], set())
            classes.add(path.splitext(file)[0])

    for key, value in content.items():
        value['head'] = sorted(value['head'])
        for k, v in value['body'].items():
            value['body'][k] = sorted(v)
        value['body'] = sorted(value['body'].items(), key=lambda x: x[0])

    return {'class': content}


def create_classroom_list(classroom_list):
    content = {}
    for classroom in classroom_list:
        if classroom.strip().endswith('.xls'):
            number, room = classroom.split('-')
            floor = content.setdefault(number, {})
            room_list = floor.setdefault(room[0], [])
            room_list.append(path.splitext(classroom)[0])

    return {'number': content}


def create_teacher_list(teacher_list):
    content = {}
    for teacher in teacher_list:
        if teacher.strip().endswith('.xls'):
            name_list = content.setdefault(teacher[0], [])
            name_list.append(path.splitext(teacher)[0])

    return {'name': content}


def create_list(path_dict, type_name):
    """创建目录网页 文件字典（路径，输出路径，文件）：path_dict HTML模板名：template_name"""
    if type_name == 'class':
        content = create_class_list(path_dict['files_path'])
    elif type_name == 'classroom':
        content = create_classroom_list(path_dict['files_path'])
    elif type_name == 'teacher':
        content = create_teacher_list(path_dict['files_path'])
    else:
        return

    html = html_template(type_name+'_list.html', content)
    out_path = path.join(path_dict['out_dir'], 'index.html')
    with open(out_path, 'w', encoding='utf-8') as file_path:
        file_path.write(html)
    print('index.html 文件已创建')

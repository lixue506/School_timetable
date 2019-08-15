"""
    Author: mushan
    Date: 2019/2/23 10:12
    Version: 1.0
    Describe: 控制文件，可以根据老师给的 xls 文件批量生成班级课表、教室课表、教师课表
"""

import sys

from os import path, walk, mkdir

current_path = path.abspath(path.dirname(__file__))
root_path = path.split(current_path)[0]
sys.path.append(root_path)

from batch_schedule_script.create_html import create_schedule, create_list


def read_list(file_dir):
    """读取目录信息 文件路径：file_dir"""
    if not path.isdir(file_dir) and not path.exists(file_dir):
        return None

    root, sub_dir, files_path = list(walk(file_dir))[0]
    path_dict = {
        'root_dir': root,
        'out_dir': path.join(root, 'html'),
        'files_path': files_path
    }
    if not path.exists(path_dict['out_dir']):
        mkdir(path_dict['out_dir'])
    return path_dict


def main():
    problem_list = ['class', 'classroom', 'teacher']
    for problem in problem_list:
        if input('Do you want to create {} schedule? Please enter (Y/N): '.format(problem)).upper() == 'Y':
            file_dir = input('Please enter the path of the {} schedule: '.format(problem))
            path_dict = read_list(file_dir)
            if not path_dict:
                print('File path error')
                return
            create_list(path_dict, problem)
            create_schedule(path_dict)


if __name__ == '__main__':
    main()

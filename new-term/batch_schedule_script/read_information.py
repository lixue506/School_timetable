"""
    Author: mushan
    Date: 2019/2/23 10:56
    Version: 1.0
    Describe: 读取 .xls 文件中的课表信息
"""

import xlrd


def read_schedule(file):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)

    # 获取标题信息
    title_string = sheet.cell_value(0, 0)
    title_list = title_string.split()
    # 学期：semester 课表：title 其他：other
    semester, title, other = title_list[0], title_list[1], title_list[2]
    content = {
        'semester': semester,
        'title': title,
        'other': other,
    }

    schedule_data = []
    for row in range(2, 7):
        cells = []
        for column in range(2, 9):
            cells.append(sheet.row_values(row)[column])
        schedule_data.append(cells)

    course_list = ['first', 'Second', 'Third', 'Fourth', 'Fifth']
    for index, data in enumerate(schedule_data):
        content[course_list[index]] = data

    return content

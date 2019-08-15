"""
    Author: mushan
    Date: 2019/2/23 10:50
    Version: 1.0
    Describe: 调用 html 模板
"""

from jinja2 import Environment, FileSystemLoader
from os import path

# 加载模板路径
PATH = path.dirname(path.abspath(__file__))
TEMPLATE_ENV = Environment(
    loader=FileSystemLoader(path.join(PATH, 'template'))
)


def html_template(template_file, content):
    """模板文件名：template_file 内容字典：content"""
    return TEMPLATE_ENV.get_template(template_file).render(content)

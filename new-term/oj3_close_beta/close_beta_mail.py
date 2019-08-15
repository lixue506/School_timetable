"""
    Author: mushan
    Date: 2018/12/25 20:51
    Version: 1.0
    Describe: SDUT OnlineJudge3 内测码群发脚本 — 读取xlsx文件，第一列姓名，第二列邮箱地址（不需要表头，直接存放内容）
"""

import yagmail
import pymysql
import string
import sys
import time

from openpyxl import load_workbook
from random import choice


class Mail:
    def __init__(self, user, password, host, port=25):
        self.mail = yagmail.SMTP(user=user, password=password, host=host, port=port, smtp_ssl=False, smtp_starttls=False)

    def send_mail(self, to, title, contents):
        self.mail.send(to=to, subject=title, contents=contents)

    def __del__(self):
        self.mail.close()


class Mysql:
    def __init__(self, host, database, user, password):
        self.db = pymysql.connect(host=host, user=user, password=password, db=database, charset='utf8')

    def insert(self, key, note, time):
        cursor = self.db.cursor()
        sql = 'INSERT INTO `key`(`key`, note, `time`) VALUE (%s, %s, %s)'
        try:
            cursor.execute(sql, (key, note, time))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
        finally:
            cursor.close()

    def find(self, key):
        cursor = self.db.cursor()
        sql = 'SELECT * FROM `key` WHERE `key`=%s'
        try:
            cursor.execute(sql, (key, ))
            if cursor.fetchone():
                return True
        except Exception as e:
            print(e)
        finally:
            cursor.close()

        return False

    def __del__(self):
        self.db.close()


def get_user(path):
    wb = load_workbook(filename=path, read_only=True)
    sheet = wb.active
    for row in sheet.rows:
        info = []
        if row[1].value:
            for cell in row:
                info.append(cell.value)
        else:
            break
        yield info


def main():
    sys.argv.append('')
    filename = sys.argv[1]
    if filename == '':
        filename = input('请输入邮箱表格（xlsx）的路径：')

    base_str = string.ascii_uppercase + string.digits
    mail = Mail(user=mail_user, password=mail_password, host=mail_host)
    mysql = Mysql(host=db_host, database=db_database, user=db_user, password=db_password)

    for info in get_user(filename):
        key_str = ''
        for j in range(8):
            key_str += choice(base_str)

        while mysql.find(key_str):
            key_str = ''
            for j in range(8):
                key_str += choice(base_str)

        note = 'OJ3内测-第二批用户 — 姓名：{}   邮箱：{}'.format(info[0], info[1])
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        mysql.insert(key_str, note, time_str)

        title = '【SDUT OJ】OnlineJudge 3 内测邀请函'
        content = [
            '亲爱的{name}:'.format(name=info[0]),
            '<br />',
            '恭喜你获得了 OnlineJudge 3 内测资格。我们诚挚地邀请你加入到 OnlineJudge 3 的内测队伍中，体验 OJ 的新功能并和我们一起完善。',
            '你的内测码（OJBK）：<strong>{OJBK}</strong>'.format(OJBK=key_str),
            '点击进入 <a href="https://acm.sdut.edu.cn/onlinejudge3_beta" target="_blank">OnlineJudge 3</a> ，输入 OJBK 即可开始体验。',
            '<br />',
            'SDUTACM 运维技术中心',
            '<br />',
            '敬上',
        ]
        mail.send_mail(info[1], title, content)
        print('已发送给：{}'.format(info[0]))


if __name__ == '__main__':
    # 邮箱信息
    mail_user = 'user'
    mail_password = 'password'
    mail_host = 'mail_server'

    # 连接数据库信息
    db_host = 'ip'
    db_database = 'database'
    db_user = 'user'
    db_password = 'password'

    main()

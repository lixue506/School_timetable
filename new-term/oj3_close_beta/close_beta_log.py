"""
    Author: mushan
    Date: 2019/1/1 14:07
    Version: 1.0
    Describe: SDUT OnlineJudge3 内测码日志异常警告（同一内测码使用用户超过三个，将会群发邮件到指定邮箱）每天定时3点检测
"""

import pymysql
import yagmail


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

    def find(self, sql, *parameter):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql, parameter)
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()

        return None

    def __del__(self):
        self.db.close()


def main():
    mysql = Mysql(db_host, db_database, db_user, db_password)
    mail = Mail(mail_user, mail_password, mail_host)

    title = '【SDUT OJ】OnlineJudge 3 内测日志（异常警告）'
    content = [
        '<br />',
        '以下是截止到凌晨3点钟，不同用户使用同一内测码登录 OnlineJudge 3 的统计信息',
        '<br />',
    ]

    sql = 'SELECT `key`, COUNT(DISTINCT username) username_count FROM log GROUP BY `key` HAVING username_count > 2'
    results = mysql.find(sql)
    log_str = '<table border="1" style="text: center"><tr><th>内测码</th><th>用户数</th><th>用户信息（username）</th></tr>'

    if results:
        for result in results:
            log_str += '<tr><td>{}</td><td>{}</td>'.format(result[0], result[1])
            sql = 'SELECT DISTINCT(username) FROM log WHERE `key`=%s'

            username_str = ', '.join(user[0] for user in mysql.find(sql, result[0]))
            log_str += '<td>' + username_str + '</td></tr>'

        content.append(log_str+'</table>')

        content.extend(
            [
                'SDUTACM 运维技术中心',
                '敬上',
            ]
        )

        for info in email:
            content.insert(0, '亲爱的{name}:'.format(name=info[0]))
            mail.send_mail(info[1], title, content)
            print('已发送：{}'.format(info[0]))


if __name__ == '__main__':
    # 邮箱信息
    mail_user = 'user'
    mail_password = 'password'
    mail_host = 'mail_server'

    # 异常 log 的接收用户信息
    email = [
        ('甄彬', 'zhenbin0212@qq.com'),
        ('刘洋', '609160502@qq.com'),
        ('赵祥宇', '15666431608@163.com'),
        ('刘星海', 'xinghaink@163.com')
    ]

    # 连接数据库信息
    db_host = 'ip'
    db_database = 'database'
    db_user = 'user'
    db_password = 'password'

    main()

import sqlite3
from flask import url_for
import time
import math
import re


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addMessage(self,text):

        try:

            self.__cur.execute("SELECT COUNT() as `count` FROM message WHERE url LIKE ?", (url,))
            res = self.__cur.fetchone()
            base = url_for('static', filename='images_html')
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>>",
                          text)

            tm = math.floor(time.time())
            who = "ERema"
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?,?)", (who, text, tm))
            self.__db.commit()

        except sqlite3.Error as e:

            print("Ошибка добавления статьи в БД " + str(e))

            return False

        return True


    def getPost(self, alias):

        try:

            self.__cur.execute("SELECT title, text FROM posts WHERE url LIKE ? LIMIT 1", (alias,))
            res = self.__cur.fetchone()

            if res:


                return res

        except sqlite3.Error as e:

            print("Ошибка получения статьи из БД " + str(e))

        return (False, False)


    def getPostsAnonce(self):

        try:

            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()

            if res: return res

        except sqlite3.Error as e:

            print("Ошибка получения статьи из БД " + str(e))

        return []


    def addUser(self, name, email, hpsw):

        try:

            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")#self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE ?",email)
            res = self.__cur.fetchone()

            if res['count'] > 0:

                print("Пользователь с таким email уже существует")

                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (name, email, hpsw))
            self.__db.commit()

        except sqlite3.Error as e:

            print("Ошибка добавления пользователя в БД " + str(e))

            return False

        return True

    def getUser(self, user_id):

        try:

            self.__cur.execute(f"SELECT * FROM users WHERE id = ? LIMIT 1",user_id)
            res = self.__cur.fetchone()

            if not res:

                print("Пользователь не найден")

                return False

            return res

        except sqlite3.Error as e:

            print("Ошибка получения данных из БД " + str(e))

        return False


    def getUserByEmail(self,email):

        try:

            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()

            if not res:

                print("Пользователь не найден")

                return False

            return res

        except sqlite3.Error as e:

            print("Ошибка получения данных из БД "+str(e))

        return False


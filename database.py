import sqlite3
import time
import random

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

class Database:
   
    def create_new_user(self, user_id, nick='unknown'):
        try:
            nick += str(user_id)
            sql = f'NSERT INTO users(vk_id, nick) VALUES ({user_id}, "{nick}")'
            cursor.execute(sql)
            conn.commit()
            return 'Ok'
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite: " + str(error))
            return "Ошибка при работе с SQLite: " + str(error)

    def add_mission(id, name, desc, rewards):
        sql = f'INSERT INTO Missions(id, name, desc, rewards) VALUES ("{id}", "{name}", "{desc}", "{rewards}")'
        cursor.execute(sql)
        conn.commit()

    def get_random_mission():
        sql = f'SELECT*FROM Missions'
        cursor.execute(sql)
        missions = cursor.fetchall()
        mission = random.choice(missions)
        return mission

    #add_mission(1, 'Во имя Ленина', 'Добудьте одинаковое количество дерева, железа, еды', 'exp+100, gold+100')
    #add_mission(2, 'Древесина!', 'Добудьте дерево', '+wood, +exp 15')
    #add_mission(3, 'Железо!', 'Добудьте железо', '+iron, +exp 20')
    #add_mission(4, 'Охота!', 'Добудьте мясо животных', '+food, +exp 18')
    #add_mission(5, 'ЗОЛОТО!!!', 'Прододите любой свой предмет за золото', '+gold, +exp 30')
     
sql = f"""create table Missions(
        id integer primary key,
        name text unique,
        desc text,
        rewards text)"""
cursor.execute(sql)
conn.commit()
      
sql = f"""create table Missions(
        id integer primary key,
        name text unique,
        desc text,
        rewards text)"""
cursor.execute(sql)
conn.commit()

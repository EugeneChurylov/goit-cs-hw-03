from faker import Faker
import psycopg2
import random

fake = Faker()

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

# Створення курсора
cur = conn.cursor()

# Створення таблиць
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    )
''')

# Вставка початкових значень для таблиці status
status_values = ['new', 'in progress', 'completed']
for status in status_values:
    cur.execute("INSERT INTO status (name) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM status WHERE name = %s)", (status, status))
conn.commit()

# Функція для вставки користувачів
def insert_users(num_users):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
        conn.commit()

# Функція для вставки завдань
def insert_tasks(num_tasks, num_users, num_statuses):
    for _ in range(num_tasks):
        title = fake.sentence()
        description = fake.text()
        status_id = random.randint(1, num_statuses)
        user_id = random.randint(1, num_users)
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (title, description, status_id, user_id))
        conn.commit()

# Кількість користувачів, завдань та статусів
num_users = 10
num_tasks = 20
num_statuses = 3

# Вставка користувачів та завдань
insert_users(num_users)
insert_tasks(num_tasks, num_users, num_statuses)

# Закриття курсора та з'єднання
cur.close()
conn.close()

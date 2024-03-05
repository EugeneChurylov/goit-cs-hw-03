from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до бази даних
client = MongoClient('mongodb+srv://goitlearn:YhJxUkpUlMe36Vvz@cluster0.kpmth4m.mongodb.net/')
db = client.test
collection = db['cats']

def read_all_records():
    """Функція для виведення всіх записів із колекції."""
    records = collection.find({})
    for record in records:
        print(record)

def read_cat_info(name):
    """Функція, яка виводить інформацію про кота за ім'ям."""
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print("Кота з таким ім'ям не знайдено.")

def update_cat_age(name, new_age):
    """Функція, яка оновлює вік кота за ім'ям."""
    collection.update_one({"name": name}, {"$set": {"age": new_age}})
    print("Вік кота оновлено.")

def add_feature_to_cat(name, new_feature):
    """Функція, яка додає нову характеристику до списку features кота за ім'ям."""
    cat = collection.find_one({"name": name})
    if cat:
        features = cat.get("features", [])
        if features is None:
            features = []
        features.append(new_feature)
        collection.update_one({"name": name}, {"$set": {"features": features}})
        print("Характеристику додано.")
    else:
        print("Кота з таким ім'ям не знайдено.")


def delete_cat_by_name(name):
    """Функція для видалення запису з колекції за ім'ям тварини."""
    collection.delete_one({"name": name})
    print("Запис про кота видалено.")

def delete_all_records():
    """Функція для видалення всіх записів із колекції."""
    collection.delete_many({})
    print("Усі записи видалено.")

# Тестування функцій
# read_all_records()
# read_cat_info("Lama")
# update_cat_age("barsik", 4)
# add_feature_to_cat("barsik", "любить спати")
# delete_cat_by_name("Lama")
# delete_all_records()

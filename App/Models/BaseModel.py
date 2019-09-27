from peewee import *

mysql_db = MySQLDatabase('influencer', user='root', password='', host='127.0.0.1', port=3306, charset='utf8mb4')

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db

# class Users(BaseModel):
#     name = CharField()
#     email = CharField()

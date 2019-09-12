from peewee import *

mysql_db = MySQLDatabase('php_analyzer', user='root', password='', host='127.0.0.1', port=3306)

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db

class Users(BaseModel):
    name = CharField()
    email = CharField()

# class FacebookUser(BaseModel):
#     class Meta:
#         table_name = 'facebook_users'

#     username = CharField()
#     name = CharField()
#     profile_picture_url = CharField()
#     likes = IntegerField()
#     followers = IntegerField()
#     is_verified = BooleanField()
#     added_date = DateTimeField()
#     is_featured = BooleanField()

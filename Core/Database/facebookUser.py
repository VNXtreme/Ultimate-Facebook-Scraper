from peewee import *

from Database.db import BaseModel


class FacebookUser(BaseModel):
    class Meta:
        table_name = 'facebook_users'

    username = CharField()
    name = CharField()
    profile_picture_url = CharField()
    likes = IntegerField()
    followers = IntegerField()
    is_verified = BooleanField()
    added_date = DateTimeField()
    is_featured = BooleanField()
    is_private = BooleanField()

    @classmethod
    def update_or_create(cls, fbUsername: str, defaultsObject: object):
        user, created = cls.get_or_create(
            username=fbUsername, defaults=defaultsObject
        )
        if not created:
            for key, value in defaultsObject.items():
                setattr(user, key, value)
            user.save()

        return user

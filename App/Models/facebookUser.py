from datetime import datetime

from peewee import *

from .BaseModel import BaseModel


class FacebookUser(BaseModel):
    class Meta:
        table_name = 'facebook_users'

    username = CharField()
    name = CharField()
    profile_picture_url = CharField()
    likes = IntegerField()
    followers = IntegerField()
    gender = CharField()
    is_verified = BooleanField()
    added_date = DateTimeField()
    is_featured = BooleanField()
    is_private = BooleanField()
    updated_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now())

    @classmethod
    def update_or_create(cls, fbUsername: str, defaultsObject: object):
        user, created = cls.get_or_create(
            username=fbUsername, defaults=defaultsObject
        )
        if not created:
            for key, value in defaultsObject.items():
                setattr(user, key, value)
                user.updated_at = datetime.now()
            user.save()

        return user

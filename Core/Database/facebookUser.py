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

    def update_follower_number(self, fbUsername, followerNumber):
        user, created = self.get_or_create(username=fbUsername,
                                           defaults={
                                               'followers': followerNumber}
                                           )
        if not created:
            user.followers = followerNumber
            user.save()

    @classmethod
    def update_or_create(cls, fbUsername, defaultsObject):
        user, created = cls.get_or_create(
            username=fbUsername, defaults=defaultsObject
        )
        if not created:
            for key, value in defaultsObject.items():
                setattr(user, key, value)
            user.save()

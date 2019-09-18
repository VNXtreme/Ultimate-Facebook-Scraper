from datetime import datetime

from peewee import *

from Database.db import BaseModel


class facebookPostInsight(BaseModel):
    class Meta:
        table_name = 'facebook_post_insights'

    facebookpost_id = IntegerField()
    consumption_link_clicks = IntegerField(default=0)
    consumption_other_clicks = IntegerField(default=0)
    consumption_photo_view = IntegerField(default=0)
    consumption_video_play = IntegerField(default=0)
    engaged_users = IntegerField(default=0)
    engagements = IntegerField(default=0)
    impressions = IntegerField(default=0)
    post_clicks = IntegerField(default=0)
    reaction = CharField(default=None)
    reaction_anger = CharField(default=None)
    reaction_haha = CharField(default=None)
    reaction_like = CharField(default=None)
    reaction_love = CharField(default=None)
    reaction_sorry = CharField(default=None)
    reaction_wow = CharField(default=None)
    comments = CharField(default=None)
    shares = CharField(default=None)
    video_views = IntegerField(default=0)
    updated_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now())

    @classmethod
    def update_or_create(cls, facebookpostId: str, reactions: list):
        likes, loves, hahas, total, comments, shares = reactions

        defaultsObject = {
            'reaction': total,
            'reaction_like': likes,
            'reaction_love': loves,
            'reaction_haha': hahas,
            'comments': comments,
            'shares': shares,
        }

        postInsight, created = cls.get_or_create(
            facebookpost_id=facebookpostId, defaults=defaultsObject
        )

        # print(link, created)
        if not created:
            for key, value in defaultsObject.items():
                setattr(postInsight, key, value)
            postInsight.updated_at = datetime.now()
            postInsight.save()

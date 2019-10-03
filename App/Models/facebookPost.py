from datetime import datetime

from peewee import *

from App.Controllers.Functions.common import reaction_string_to_number

from .BaseModel import BaseModel
from .facebookPostInsight import facebookPostInsight


class FacebookPost(BaseModel):
    class Meta:
        table_name = 'facebook_posts'

    profile_id = IntegerField()
    title = TextField()
    link = TextField()
    message = TextField()
    message_picture = TextField()
    post_time = CharField()
    reaction_number = IntegerField(default=0)
    comment_number = IntegerField(default=0)
    share_number = IntegerField(default=0)
    updated_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now())

    @classmethod
    def update_or_create(cls, link: str, defaultsObject: object):
        post, created = cls.get_or_create(
            link=link, defaults=defaultsObject
        )

        # print(link, created)
        if not created:
            for key, value in defaultsObject.items():
                setattr(post, key, value)
            post.updated_at = datetime.now()
            post.save()

        return post

    @classmethod
    def update_or_create_fbpost(cls, userId: int, fbPosts: list):
        for post in fbPosts:
            link, postMessage, postImage, time, title, reactions = post
            
            facebookPost = cls.update_or_create(link, {
                'profile_id': userId,
                'title': title,
                'message': postMessage,
                'message_picture': postImage,
                'post_time': time,
                'reaction_number': reaction_string_to_number(reactions[3]),
                'comment_number': reaction_string_to_number(reactions[4]),
                'share_number': reaction_string_to_number(reactions[5])
            })

            facebookPostInsight.update_or_create(facebookPost.id, reactions)

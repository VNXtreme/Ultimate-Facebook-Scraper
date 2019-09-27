from datetime import datetime

from peewee import *

from Database.BaseModel import BaseModel
from Database.facebookPostInsight import facebookPostInsight


class FacebookPost(BaseModel):
    class Meta:
        table_name = 'facebook_posts'

    profile_id = IntegerField()
    title = TextField()
    link = TextField()
    message = TextField()
    message_picture = TextField()
    post_time = CharField()
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
            # print(postMessage, "\n")
            facebookPost = cls.update_or_create(link, {
                'profile_id': userId,
                'title' : title,
                'message' : postMessage,
                'message_picture' : postImage,
                'post_time' : time
            })

            facebookPostInsight.update_or_create(facebookPost.id, reactions)

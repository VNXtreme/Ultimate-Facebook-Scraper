from datetime import datetime

from peewee import *

from Database.db import BaseModel


class FacebookPost(BaseModel):
    class Meta:
        table_name = 'facebook_posts'

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

    @classmethod
    def update_or_create_fbpost(cls, fbPosts: list):
        for post in fbPosts:
            link, postMessage, postImage, time, title, reactions = post
            # print(postMessage, "\n")
            cls.update_or_create(link, {
                'title' : title,
                'message' : postMessage,
                'message_picture' : postImage,
                'post_time' : time
            })

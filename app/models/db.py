from tortoise import fields, models
from passlib.hash import bcrypt
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=100)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def __str__(self):
        return self.email


class Post(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='posts')
    text = fields.TextField()


class Evaluation(models.Model):
    """
    evaluation = True - Like
    evaluation = False - Dislike
    """

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='evaluations')
    post = fields.ForeignKeyField('models.Post', related_name='evaluations')
    evaluation = fields.BooleanField()


User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

from django.db import models


# Test models for checking merged inlines
class MergedInlineModel(models.Model):
    """
    Taking idea from Rest Framework's own tests
    Base for test models that creates a unified app label
    """

    class Meta:
        app_label = "tests"
        abstract = True


# Classes for testing base setup
class Author(MergedInlineModel):
    name = models.CharField(max_length=250)


class Play(MergedInlineModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    year = models.IntegerField()


class Poem(MergedInlineModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    style = models.CharField(max_length=100)


# Class for testing custom ordering
class Kingdom(MergedInlineModel):
    name = models.CharField(max_length=100)


class King(MergedInlineModel):
    kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    alive = models.BooleanField(default=False)


class Soldier(MergedInlineModel):
    kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    house = models.CharField(max_length=150)

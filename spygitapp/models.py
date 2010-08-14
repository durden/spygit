from django.db import models


class Errors(models):
    error_type = models.IntegerField()
    short_descr = models.TextField()
    long_descr = models.TextField()


class Runs(models):
    project_name = models.CharField(max_length=300)
    project_url = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    twitter_user = models.CharField(max_length=300)
    git_revision = models.CharField(max_length=40)


class Files(models):
    filename = models.CharField(max_length=300)
    run = models.ForeignKey('Runs')

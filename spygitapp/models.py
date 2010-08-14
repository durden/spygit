from django.db import models


class Error(models.Model):
    error_type = models.IntegerField()
    short_descr = models.TextField()
    long_descr = models.TextField()


class Run(models.Model):
    project_name = models.CharField(max_length=300)
    project_url = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    twitter_user = models.CharField(max_length=300)
    git_revision = models.CharField(max_length=40)


class File(models.Model):
    filename = models.CharField(max_length=300)
    run = models.ForeignKey('Run')


class RunError(models.Model):
    error = models.ForeignKey('Error')
    file = models.ForeignKey('File')
    line_number = models.IntegerField()


class Line(models.Model):
    file = models.ForeignKey('File')
    line_number = models.IntegerField()
    text= models.TextField()

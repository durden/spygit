from django.db import models


class Error(models.Model):
    error_type = models.IntegerField()
    short_descr = models.TextField()

    def __unicode__(self):
        return u'%d' % (self.error_type)


class Run(models.Model):
    project_name = models.CharField(max_length=300)
    project_url = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    twitter_user = models.CharField(max_length=300, blank=True)
    git_revision = models.CharField(max_length=40)

    def __unicode__(self):
        return u'%s - %s' % (self.project_name, self.git_revision[0:5])


class File(models.Model):
    filename = models.CharField(max_length=300)
    run = models.ForeignKey('Run')

    def __unicode__(self):
        return u'%s %s' % (self.run, self.filename)


class RunError(models.Model):
    error = models.ForeignKey('Error')
    file = models.ForeignKey('File')
    line_number = models.IntegerField()
    error_descr = models.TextField()

    def __unicode__(self):
        return u'%s- %s' % (self.file.filename, self.line_number)


class Line(models.Model):
    file = models.ForeignKey('File')
    line_number = models.IntegerField()
    text = models.TextField()

    def __unicode__(self):
        return u'%s' % (self.text[0:20])

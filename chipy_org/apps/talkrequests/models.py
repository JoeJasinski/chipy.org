from django.db import models
from django.conf import settings
from django.utils.text import Truncator

from chipy_org.libs.models import CommonModel


class TalkRequestQuerySet(models.QuerySet):

    def active(self):
        return self.filter(active=True)

EXPERIENCE_LEVELS = (
    ('novice', 'Novice'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
)


class TalkRequest(CommonModel):
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=64)
    text = models.TextField()
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        'talkrequests.TalkCategory',
        blank=True, null=True)
    recent_date = models.DateField(
        help_text="When was this last talked about?",
        blank=True, null=True)

    class Meta:
        verbose_name = "Talk Request"
        verbose_name_plural = "Talk Requests"

    def __unicode__(self):
        return "({}) {}".format(self.id, Truncator(self.text).chars(75))

    objects = TalkRequestQuerySet.as_manager()


class TalkVote(CommonModel):
    talk_request = models.ForeignKey('talkrequests.TalkRequest')
    ip_address = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    class Meta:
        verbose_name = "Talk Vote"
        verbose_name_plural = "Talk Votes"

    def __unicode__(self):
        return "({}) {}".format(self.id, self.ip_address)


class TalkCategory(CommonModel):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Talk Category"
        verbose_name_plural = "Talk Categories"

    def __unicode__(self):
        return "({}) {}".format(self.id, self.slug)

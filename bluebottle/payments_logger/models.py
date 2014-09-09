from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import Truncator
from djchoices import DjangoChoices, ChoiceItem
from django.utils.translation import ugettext as _

from django_extensions.db.fields import CreationDateTimeField
from bluebottle.payments.models import Payment


class PaymentLogLevels(DjangoChoices):

    info = ChoiceItem('info', label=_("INFO"))
    warn = ChoiceItem('warn', label=_("WARN"))
    error = ChoiceItem('error', label=_("ERROR"))


# TODO: Add fields for: source file, source line number, source version, IP
class PaymentLogEntry(models.Model):

    message = models.CharField(max_length=400)
    level = models.CharField(max_length=15, choices=PaymentLogLevels.choices)
    timestamp = CreationDateTimeField()

    payment = models.ForeignKey(Payment, related_name='payments')

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = _("Payment Log")
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0} {1}'.format(self.get_level_display(), Truncator(self.message).words(6))

    def log_entry(self):
        return '[{0}]  {1: <5}  {2 <5}  {3}'.format(self.timestamp.strftime("%d/%b/%Y %H:%M:%S"),
                                                    self.get_type_display(), self.get_level_display(), self.message)

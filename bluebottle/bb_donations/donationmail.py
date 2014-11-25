from apps.mail import send_mail
from django.dispatch.dispatcher import receiver
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import pre_save
from django.template import Context
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.utils import translation
from django.template.loader import get_template
from bluebottle.utils.model_dispatcher import get_donation_model


def successful_donation_fundraiser_mail(instance):

    # should be only when the status is success
    try:
        receiver = instance.fundraiser.owner
    except:
        # donation it's not coming from a fundraiser
        return
    fundraiser_link = '/go/fundraisers/{0}'.format(instance.fundraiser.id)
    context = Context({'amount': instance.amount,
                       'site': 'https://' + Site.objects.get_current().domain,
                       'link': fundraiser_link,
                       'receiver': receiver.get_short_name()
                       })
    subject = _('You received a new donation')
    translation.activate(receiver.primary_language)
    translation.deactivate()
    text_content = get_template('new_oneoff_donation_fundraiser.mail.txt').render(context)
    html_content = get_template('new_oneoff_donation_fundraiser.mail.html').render(context)
    msg = EmailMultiAlternatives(subject=subject, body=text_content, to=[receiver.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def new_oneoff_donation(instance):
    """
    Send project owner a mail if a new "one off" donation is done. We consider a donation done if the status is pending.
    """
    donation = instance

    # Only process the donation if it is of type "one off".
    # if donation.order.order_type != :
    #     return


    project_url = '/go/projects/{0}'.format(donation.project.slug)

    if donation.project.owner.email:
        # Send email to the project owner.
        send_mail(
            template_name='new_oneoff_donation.mail',
            subject=_('You received a new donation'),
            to=donation.project.owner,
            amount=donation.amount,
            donor_name=donation.order.user.first_name,
            link=project_url,
        )

    if donation.order.user.email:
        # Send email to the project supporter
        send_mail(
            template_name="new_oneoff_donation.mail",
            subject=_("You supported {0}".format(donation.project.title)),
            to=donation.order.user,
            link=project_url
        )

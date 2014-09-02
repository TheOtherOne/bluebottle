import factory
import factory.fuzzy
from django.utils.timezone import now
from datetime import timedelta

from bluebottle.fundraisers.models import FundRaiser

from .accounts import BlueBottleUserFactory
from .geo import CountryFactory
from .projects import ProjectFactory


class FundRaiserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = FundRaiser

    owner = factory.SubFactory(BlueBottleUserFactory)
    project = factory.SubFactory(ProjectFactory)
    title = factory.Sequence(lambda n: 'Project_{0}'.format(n))
    description = factory.Sequence(lambda n: 'Project_{0}'.format(n))
    amount = 1000
    deadline = factory.fuzzy.FuzzyDateTime(now(), now() + timedelta(weeks=4))

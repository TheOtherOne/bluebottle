import decimal
import datetime
from bluebottle.bb_projects.models import ProjectPhase
from bluebottle.test.factory_models.orders import OrderFactory
from bluebottle.test.factory_models.organizations_factories import OrganizationFactory
from bluebottle.utils.model_dispatcher import get_project_model

from django_dynamic_fixture import N, G

from bluebottle.payouts.models import ProjectPayout, OrganizationPayout
from bluebottle.donations.models import Donation
from bluebottle.test.factory_models.donations import DonationFactory
from bluebottle.test.factory_models.projects import ProjectFactory
from bluebottle.test.utils import BluebottleTestCase
from bluebottle.utils.utils import StatusDefinition

PROJECT_MODEL = get_project_model()

class PayoutTestCase(BluebottleTestCase):
    """ Test case for Payouts. """

    def setUp(self):
        super(PayoutTestCase, self).setUp()

        # Set up a project ready for payout
        organization = OrganizationFactory.create()
        organization.save()
        self.project = ProjectFactory.create(organization=organization, amount_asked=50)

        # Update phase to campaign.
        self.project.status = ProjectPhase.objects.get(slug='campaign')
        self.project.save()

        self.order = OrderFactory.create()

        self.donation = DonationFactory.create(
            project=self.project,
            order=self.order,
            amount=60
        )
        self.donation.save()

    def _reload_project(self):
        # Stale project instances aren't updated, so we have to reload it from the db again.
        self.project = PROJECT_MODEL.objects.get(pk=self.project.id)

    def test_save(self):
        """ Test saving a payout. """

        # Generate new payout
        payout = N(ProjectPayout, completed=None)

        # Validate
        payout.clean()

        # Save it
        payout.save()

    def test_unicode(self):
        """ Test unicode() on payout. """

        payout = G(ProjectPayout, completed=None)
        self.assertTrue(unicode(payout))

    def test_completed(self):
        """ Test the transition to settled. """

        payout = G(ProjectPayout, completed=None, status=StatusDefinition.IN_PROGRESS)
        payout.save()

        self.assertFalse(payout.completed)

        # Change status to settled
        payout.status = StatusDefinition.SETTLED
        payout.save()

        # Completed date should now be set
        self.assertTrue(payout.completed)

    def test_create_payout(self):
        """
        Test automatically generating a payout.
        """

        # No payouts should exist yet as project is not in act phase yet
        self.assertFalse(ProjectPayout.objects.exists())

        # Set status of donation to pending
        self.donation.order.locked()
        self.donation.order.pending()

        # Update phase to act.
        self._reload_project()
        self.project.status = ProjectPhase.objects.get(slug='realised')
        self.project.save()

        # Payout should have been created
        self.assertEquals(ProjectPayout.objects.count(), 1)

        payout = ProjectPayout.objects.all()[0]

        # Check the project and the amount
        self.assertEquals(payout.project, self.project)
        self.assertEquals(payout.amount_raised, decimal.Decimal('60.00'))

    def test_invoice_reference(self):
        """ Test generating invoice_reference. """

        # Set status of donation to paid
        self.donation.order.locked()
        self.donation.order.succeeded()
        self.donation.order.save()

        # Update phase to act.
        self._reload_project()
        self.project.status = ProjectPhase.objects.get(slug='realised')
        self.project.save()

        # Fetch payout
        payout = ProjectPayout.objects.all()[0]

        self.assertIn(str(self.project.id), payout.invoice_reference)
        self.assertIn(str(payout.id), payout.invoice_reference)

    def test_create_payment_rule_five(self):
        """ Projects should get payment rule five. """

        # Set status of donation to paid
        self.donation.order.locked()
        self.donation.order.succeeded()
        self.donation.order.save()

        # Update phase to act.
        self._reload_project()
        self.project.status = ProjectPhase.objects.get(slug='realised')
        self.project.save()

        payout = ProjectPayout.objects.all()[0]
        payout.payout_rule = 'five'
        payout.calculate_amounts()

        self.assertEquals(payout.payout_rule, ProjectPayout.PayoutRules.five)
        self.assertEquals(payout.organization_fee, decimal.Decimal('3'))
        self.assertEquals(payout.amount_payable, decimal.Decimal('57'))

    def test_amounts_new(self):
        """ Test amounts for new donations. """

        # Update phase to act.
        self._reload_project()
        self.project.status = ProjectPhase.objects.get(slug='realised')
        self.project.save()

        # Fetch payout
        payout = ProjectPayout.objects.all()[0]

        # No money is even pending
        self.assertEquals(payout.amount_raised, decimal.Decimal('0.00'))
        self.assertEquals(payout.amount_payable, decimal.Decimal('0.00'))

        self.assertEquals(payout.get_amount_pending(), decimal.Decimal('0.00'))
        self.assertEquals(payout.get_amount_safe(), decimal.Decimal('0.00'))
        self.assertEquals(payout.get_amount_failed(), decimal.Decimal('0.00'))

    def test_amounts_pending(self):
        """ Test amounts for pending donations. """

        # Set status of donation
        self.donation.order.locked()
        self.donation.order.pending()
        self.donation.order.save()

        # Update phase to act.
        self._reload_project()
        self.project.status = ProjectPhase.objects.get(slug='realised')
        self.project.save()

        # Fetch payout
        payout = ProjectPayout.objects.all()[0]

        # Money is pending but not paid
        self.assertEquals(payout.amount_raised, decimal.Decimal('60.00'))
        self.assertEquals(payout.amount_payable, decimal.Decimal('57'))

        self.assertEquals(payout.get_amount_pending(), decimal.Decimal('60.00'))
        self.assertEquals(payout.get_amount_safe(), decimal.Decimal('0.00'))
        self.assertEquals(payout.get_amount_failed(), decimal.Decimal('0.00'))

    def test_amounts_failed(self):
        """
        Test amounts for pending donation changed into failed after creating payout.
        """

        # Set status of donation to pending first
        self.donation.order.locked()
        self.donation.order.pending()
        self.donation.order.save()

        # Update phase to act.
        self._reload_project()
        self.project.status = ProjectPhase.objects.get(slug='realised')
        self.project.save()

        # Set status of donation to failed
        self.donation.order.failed()

        # Fetch payout
        payout = ProjectPayout.objects.all()[0]

        # Saved amounts should be same as pending
        self.assertEquals(payout.amount_raised, decimal.Decimal('0.0'))
        self.assertEquals(payout.amount_payable, decimal.Decimal('0.0'))

        # Real time amounts should be different
        self.assertEquals(payout.get_amount_pending(), decimal.Decimal('0.00'))
        self.assertEquals(payout.get_amount_safe(), decimal.Decimal('0.00'))
        self.assertEquals(payout.get_amount_failed(), decimal.Decimal('0.00'))

    def test_amounts_paid(self):
        """ Test amounts for paid donations. """

        # Setup organization
        organization = self.project.organization
        organization.account_name = 'Funny organization'
        organization.account_iban = 'NL90ABNA0111111111'
        organization.account_bic = 'ABNANL2A'
        organization.save()

        # Set status of donation to paid
        self.donation.order.locked()
        self.donation.order.succeeded()

        # Update phase to act.
        self._reload_project()
        self.project.status = ProjectPhase.objects.get(slug='realised')
        self.project.save()



        # Fetch payout
        payout = ProjectPayout.objects.all()[0]

        # Money is safe now, nothing's pending
        self.assertEquals(payout.amount_raised, decimal.Decimal('60.00'))
        self.assertEquals(payout.amount_payable, decimal.Decimal('57'))

        self.assertEquals(payout.get_amount_pending(), decimal.Decimal('0.00'))
        self.assertEquals(payout.get_amount_safe(), decimal.Decimal('60.00'))
        self.assertEquals(payout.get_amount_failed(), decimal.Decimal('0.00'))


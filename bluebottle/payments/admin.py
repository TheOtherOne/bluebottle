from bluebottle.payments.models import Payment, OrderPayment
from bluebottle.payments_docdata.admin import DocdataPaymentAdmin
from bluebottle.payments_docdata.models import DocdataPayment
from bluebottle.payments_mchanga.admin import MchangaPaymentAdmin
from bluebottle.payments_mchanga.models import MchangaPayment
from bluebottle.payments_mock.admin import MockPaymentAdmin
from bluebottle.payments_mock.models import MockPayment
from django.contrib import admin
from django.core.urlresolvers import reverse
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin


class OrderPaymentAdmin(admin.ModelAdmin):
    model = OrderPayment
    raw_id_fields = ('user', )
    readonly_fields = ('order_link', 'payment_link', 'authorization_action', 'amount', 'integration_data', 'payment_method')

    def order_link(self, obj):
        object = obj.order
        print object._meta.app_label
        print object._meta.module_name
        url = reverse('admin:{0}_{1}_change'.format(object._meta.app_label, object._meta.module_name), args=[object.id])
        print url
        return "<a href='{0}'>Order: {1}</a>".format(str(url), object.id)

    order_link.allow_tags = True

    def payment_link(self, obj):
        object = obj.payment
        print object._meta.app_label
        print object._meta.module_name
        url = reverse('admin:{0}_{1}_change'.format(object._meta.app_label, object._meta.module_name), args=[object.id])
        print url
        return "<a href='{0}'>{1}: {2}</a>".format(str(url), object.polymorphic_ctype, object.id)

    payment_link.allow_tags = True

admin.site.register(OrderPayment, OrderPaymentAdmin)


class OrderPaymentInline(admin.TabularInline):
    model = OrderPayment
    extra = 0
    can_delete = False
    readonly_fields = ('order_payment_link', 'amount', 'user', 'payment_method', 'status')
    fields = readonly_fields

    def order_payment_link(self, obj):
        object = obj
        print object._meta.app_label
        print object._meta.module_name
        url = reverse('admin:{0}_{1}_change'.format(object._meta.app_label, object._meta.module_name), args=[object.id])
        print url
        return "<a href='{0}'>OrderPayment {1}</a>".format(str(url), obj.id)

    order_payment_link.allow_tags = True

    def has_add_permission(self, request):
        return False


class PaymentAdmin(PolymorphicParentModelAdmin):

    base_model = Payment

    list_display = ('created', 'order_payment_amount', 'polymorphic_ctype', 'status')
    # list_filter = ('status', )
    ordering = ('-created', )

    # FIXME: Make this dynamic
    child_models = (
        (MchangaPayment, MchangaPaymentAdmin),
        (DocdataPayment, DocdataPaymentAdmin),
        (MockPayment, MockPaymentAdmin),
    )

    def order_payment_amount(self, instance):
        return instance.order_payment.amount

admin.site.register(Payment, PaymentAdmin)


class BasePaymentAdmin(PolymorphicChildModelAdmin):
    base_model = Payment
from django.contrib import admin
from .models import Language
import csv
from django.http import HttpResponse


class LanguageAdmin(admin.ModelAdmin):
    model = Language
    list_display = ('code', 'language_name', 'native_name')

admin.site.register(Language, LanguageAdmin)


<<<<<<< HEAD
=======


>>>>>>> booking/development-prod
def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    Taken from https://djangosnippets.org/snippets/2369/

    Example:
    class YourModelAdmin(admin.ModelAdmin):
        list_display = (...)
        list_filter = [...]
        actions = [export_as_csv_action("CSV Export", fields=[...])]
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv
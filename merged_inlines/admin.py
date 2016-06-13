from django.contrib import admin


class MergedInlineAdmin(admin.ModelAdmin):
    # optional field ordering variable
    merged_field_order = None
    merged_inline_order = 'id'

    # Edited Change_Form Template with one inline form
    change_form_template = 'admin/change_form_merged_inlines.html'

    class Media:
        js = ('admin/js/merged_inlines.js',)

    # iterates over all the inline_formsets and collects them into a lists,
    # that are then sent to the
    # change_view as extra context
    def render_change_form(
            self, request, context, add=False,
            change=False, form_url='', obj=None):
        inline_admin_formsets = context['inline_admin_formsets']
        all_forms = []
        all_fields = []
        i = 0
        for formset in inline_admin_formsets:
            for form in formset:
                form.verbose_name = form.form._meta.model._meta.verbose_name.title()
                all_forms.append((form, {}))
                for fieldset in form:
                    for line in fieldset:
                        for field in line:
                            if (field.field.name, field.field.label) not in all_fields and not field.field.is_hidden:
                                all_fields.append(
                                    (field.field.name, field.field.label)
                                )
                            all_forms[i][1][field.field.name] = field
                i += 1

        # Sort the forms based on given field.
        end = len(all_forms)-1
        all_forms.sort(
            key=lambda x: getattr(
                x[0].form.instance,
                self.merged_inline_order
            ) if getattr(
                x[0].form.instance,
                self.merged_inline_order) is not None else end)

        # Sort the fields based in merged_inline_order, if given
        if self.merged_field_order is not None:
            all_fields.sort(key=lambda x: self.merged_field_order.index(x[0]))

        extra_context = {}

        extra_context['all_fields'] = all_fields
        extra_context['all_forms'] = all_forms

        context.update(extra_context)

        return super(MergedInlineAdmin, self).render_change_form(
                request, context, add, change, form_url, obj)

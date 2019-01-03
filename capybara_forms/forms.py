from django import forms

from capybara_forms.renderers.filter import render_filter_fields
from capybara_forms.utils import get_advert_data_for_form_values, \
    validate_data, get_data_fields, get_filter_conditions, wrap_values
from capybara_forms.renderers.form import render_form_fields, \
    render_form_fields_from_model, render_advert_fields
from capybara_forms.widgets import JSONEditorWidget


class CapybaraFormsModelForm(forms.ModelForm):
    error_css_class = 'error'
    data_errors = {}  # {field_name: error_message}
    category = None

    fields_in_model = []  # Fields in Meta.model needs to be rendered in form
    fields_in_model_override = {}
    fields_in_filter = []
    fields_in_filter_override = {}

    def __init__(self, category, *args, **kwargs):
        super(CapybaraFormsModelForm, self).__init__(*args, **kwargs)
        self.category = category
        self.data_errors = {}

    def is_valid(self):
        ret = super(CapybaraFormsModelForm, self).is_valid()
        for f in self.errors:
            self.fields[f].widget.attrs.update({
                'class': self.fields[f].widget.attrs.get('class', '') +
                         ' {0}'.format(self.error_css_class)
            })

        instance_data = get_data_fields(self.data)
        instance_data = get_advert_data_for_form_values(
            self.category.params, instance_data)
        data_errors = validate_data(self.category, instance_data)
        for error_field, error_message in data_errors:
            self.add_data_error(error_field, error_message)

        if data_errors:
            return False

        return ret

    def add_data_error(self, error_field, error_message):
        if error_field in self.data_errors:
            if error_message not in self.data_errors[error_field]:
                self.data_errors[error_field].append(error_message)
        else:
            self.data_errors[error_field] = [error_message]

    def save(self, commit=True):
        instance = super(CapybaraFormsModelForm, self).save(commit=False)
        instance.category = self.category
        instance_data = get_data_fields(self.data)
        instance.data = get_advert_data_for_form_values(self.category.params, instance_data)

        if commit:
            instance.save()

        return instance

    def filter_adverts(self):
        queryset = self._meta.model.objects.filter(category=self.category)
        filter_values = get_data_fields(self.data)
        filter_values.update({
            field: self.data.get(field, '') for field in self.fields_in_filter if field in self.data
        })
        conditions = get_filter_conditions(
            self.category.search_params, self.fields_in_filter, filter_values)
        queryset = queryset.filter(**conditions)
        return queryset

    def render_form(self):
        if self.instance.pk:
            instance_values = wrap_values({
                field: getattr(self.instance, field, None)
                for field in self.fields_in_model
            })
        else:
            instance_values = wrap_values(self.data)

        model_part = render_form_fields_from_model(self, instance_values, self.errors)

        if self.instance.data:
            data_values = self.instance.data
        else:
            data_values = wrap_values(get_data_fields(self.data))

        category_part = render_form_fields(self.category, data_values, self.data_errors)

        return model_part + category_part

    def render_filter(self):
        data_fields = get_data_fields(self.data)
        data_fields.update({
            field: self.data.get(field, '') for field in self.fields_in_filter if field in self.data
        })
        return render_filter_fields(self, data_fields)

    def render_item(self):
        return render_advert_fields(self.instance)

    def get_default_filter_template(self):
        return None


def CategoryAdminForm(CategoryClass):
    class FormClass(forms.ModelForm):

        class Meta:
            model = CategoryClass
            fields = '__all__'
            widgets = {
                'params': JSONEditorWidget(),
                'search_params': JSONEditorWidget()
            }

        class Media:
            css = { 'all': ('/static/capybara_forms/css/jsoneditor.min.css',)}
            js = ('/static/capybara_forms/js/jsoneditor.min.js', )

    return FormClass

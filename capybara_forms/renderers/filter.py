import re
from django.template.loader import render_to_string
from django.conf import settings

from capybara_forms.models import SelectData
from capybara_forms.utils import django_field_to_capybara_field


def _render_filter_string(field, filter_values):
    return render_to_string('capybara_forms/filter/string.html', {'field': field})


def _render_filter_select(field, filter_values):
    not_selected = getattr(settings, 'CAPYBARA_FORMS_NOT_SELECTED', 'Not selected')

    if 'nested_on' in field:
        field['nested_prefix'] = field['options']

    if 'nested_on' in field and int(filter_values.get(field['nested_on'], 0)) > 0:
        nested_id = filter_values.get(field['nested_on'])
        field['options'] = SelectData.objects.filter(
            parent_id=nested_id
        ).order_by('value').values_list('pk', 'value')
    elif type(field['options']) is not list:
        field['options'] = SelectData.objects.filter(
            key=field['options']
        ).order_by('value').values_list('pk', 'value')

    if field.get('value') is not None:
        field['value'] = int(field['value'])

    return render_to_string('capybara_forms/filter/select.html', {
        'field': field,
        'not_selected': not_selected
    })


def _render_filter_number(field, filter_values):
    return render_to_string('capybara_forms/filter/number.html', {'field': field})


def _render_filter_number_select(field, filter_values):
    if 'options' not in field or type(field['options']) is not list:
        field['options'] = []
        if 'start' in field and 'end' in field and 'step' in field:
            start = field['start']
            step = field['step']
            end = field['end']
            current = start
            while current <= end if step > 0 else current >= end:
                field['options'].append(str(current))
                current += step

    field['value'] = field.get('value', '0')
    not_selected = getattr(settings, 'CAPYBARA_FORMS_NOT_SELECTED', 'Not selected')

    return render_to_string('capybara_forms/filter/number_select.html', {
        'field': field,
        'not_selected': not_selected
    })


def _render_filter_checkbox(field, filter_values):
    return render_to_string('capybara_forms/filter/checkbox.html', {'field': field})


FILTER_FIELD_TYPES_TO_FUNCTIONS = {
    'string': _render_filter_string,
    'select': _render_filter_select,
    'number': _render_filter_number,
    'number_select': _render_filter_number_select,
    'checkbox': _render_filter_checkbox,
}


def render_filter_fields(form, filter_values):
    category = form.category
    data = category.search_params
    form_groups = {}

    fields_in_filter = getattr(form, 'fields_in_filter', [])
    for field in fields_in_filter:
        field_data = django_field_to_capybara_field(form, field)
        if field in form.fields_in_filter_override:
            field_data.update(form.fields_in_filter_override[field])

        if field_data and field_data['type'] in FILTER_FIELD_TYPES_TO_FUNCTIONS:
            if field_data['name'] in filter_values:
                field_data['value'] = filter_values[field_data['name']]

            render_function = FILTER_FIELD_TYPES_TO_FUNCTIONS[field_data['type']]
            form_groups[field] = render_function(field_data, filter_values)

    for field in data:
        if 'type' in field and field['type'] in FILTER_FIELD_TYPES_TO_FUNCTIONS:
            if field['name'] in filter_values:
                field['value'] = filter_values[field['name']]

            render_function = FILTER_FIELD_TYPES_TO_FUNCTIONS[field['type']]
            form_groups[field['name']] = render_function(field, filter_values)

    if category.filter_template:
        fields = re.findall('{(\w+)}', category.filter_template)
        result = category.filter_template
        for field_name in form_groups:
            if field_name in fields:
                result = result.replace('{' + field_name + '}',
                                        '<div class="cpb_form_item">' +
                                        form_groups[field_name] +
                                        '</div>')

        return result
    else:
        default_template = form.get_default_filter_template()
        if default_template:
            model_content = default_template
            for field_name in form.fields_in_filter:
                model_content = model_content.replace('{' + field_name + '}',
                                                      '<div class="cpb_form_item">' +
                                                      form_groups[field_name] +
                                                      '</div>')
        else:
            model_content = '\n'.join([
                '<div class="cpb_form_item">' + form_groups[field] + '</div>'
                for field in form.fields_in_filter
            ])

        category_content = '\n'.join([
            '<div class="cpb_form_item">' + form_groups[field] + '</div>'
            for field in data if field in form_groups
        ])

        return model_content + category_content

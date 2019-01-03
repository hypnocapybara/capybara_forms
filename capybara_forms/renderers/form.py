import re

from django.template.loader import render_to_string
from django.conf import settings

from capybara_forms.models import SelectData
from capybara_forms.defines import colors
from capybara_forms.utils import float_to_string, django_field_to_capybara_field


def render_field_to_template(template, field, advert_data, data_errors, transform=None):
    value = advert_data.get(field['name'], {}).get('value')
    if transform == 'float' and isinstance(value, float):
        value = float_to_string(value) if value else ''
    elif transform == 'bool':
        value = bool(value)

    return render_to_string(template, {
        'field': field,
        'value': value,
        'errors': data_errors.get(field['name'], [])
    })


def _render_form_string(field, advert_data, data_errors):
    return render_field_to_template(
        'capybara_forms/form/string.html', field, advert_data, data_errors)


def _render_form_select(field, advert_data, data_errors):
    not_selected = getattr(settings, 'CAPYBARA_FORMS_NOT_SELECTED', 'Not selected')

    if 'nested_on' in field:
        field['nested_prefix'] = field['options']

    if 'nested_on' in field and advert_data.get(field['nested_on']):
        field_data = advert_data.get(field['nested_on'])
        field['options'] = SelectData.objects.filter(
            parent_id=field_data['value']
        ).order_by('value').values_list('pk', 'value')
    elif type(field['options']) is not list:
        field['options'] = SelectData.objects.filter(
            key=field['options']
        ).order_by('value').values_list('pk', 'value')

    return render_to_string('capybara_forms/form/select.html', {
        'field': field,
        'value': advert_data.get(field['name'], {}).get('value'),
        'not_selected': not_selected,
        'errors': data_errors.get(field['name'], [])
    })


def _render_form_number(field, advert_data, data_errors):
    return render_field_to_template(
        'capybara_forms/form/number.html', field, advert_data, data_errors, 'float')


def _render_form_checkbox(field, advert_data, data_errors):
    return render_field_to_template(
        'capybara_forms/form/checkbox.html', field, advert_data, data_errors, 'bool')


def _render_form_color(field, advert_data, data_errors):
    return render_to_string('capybara_forms/form/color.html', {
        'field': field,
        'value': int(advert_data.get('color', {}).get('value', 0)),
        'colors': colors,
        'errors': data_errors.get('color', [])
    })


FIELD_TYPES_TO_FUNCTIONS = {
    'string': _render_form_string,
    'select': _render_form_select,
    'number': _render_form_number,
    'checkbox': _render_form_checkbox,
    'color': _render_form_color,
}


def render_form_fields(category, advert_data, data_errors):
    if category.form_template:
        fields_in_form = re.findall('{(\w+)}', category.form_template)
        result = category.form_template

        for field in category.params:
            if 'type' in field and field['type'] in FIELD_TYPES_TO_FUNCTIONS:
                field_type = field['type']
                if field_type == 'color':
                    field_name = 'color'
                else:
                    field_name = field['name']

                if field_name in fields_in_form:
                    render_function = FIELD_TYPES_TO_FUNCTIONS[field['type']]
                    result = result.replace('{'+field_name+'}',
                                            '<div class="cpb_form_item">' +
                                            render_function(field, advert_data, data_errors) +
                                            '</div>')
        return result
    else:
        form_groups = []

        for field in category.params:
            if 'type' in field and field['type'] in FIELD_TYPES_TO_FUNCTIONS:
                render_function = FIELD_TYPES_TO_FUNCTIONS[field['type']]
                form_groups.append(render_function(field, advert_data, data_errors))

        form_groups = [
            '<div class="cpb_form_item">' + item + '</div>'
            for item in form_groups
        ]

        return '\n'.join(form_groups)


def render_form_fields_from_model(form, advert_values, errors):
    result = []
    fields = form.fields_in_model

    for field in fields:
        data = django_field_to_capybara_field(form, field)
        if field in form.fields_in_model_override:
            data.update(form.fields_in_model_override[field])

        render_function = FIELD_TYPES_TO_FUNCTIONS[data['type']]
        result.append(
            '<div class="cpb_form_item">' +
            render_function(data, advert_values, errors) +
            '</div>')

    return '\n'.join(result)


def render_advert_fields(advert):
    data = advert.data
    category_data = advert.category.params

    if not data:
        return ''

    advert_fields = []

    for category_field in category_data:
        if 'type' not in category_field:
            continue

        field_type = category_field['type']
        if field_type == 'color':
            field_name = 'color'
        else:
            field_name = category_field['name']

        if field_name in data:
            field = data[field_name]
            field_value = ''

            if field_type == 'string':
                field_value = field.get('value', '')
            elif field_type == 'number':
                field_value = str(field.get('value', '')).rstrip('0').rstrip('.')
            elif field_type == 'select':
                field_value = field.get('display_value', '')
            elif field_type == 'checkbox':
                field_value = "&#x2713;" if field.get('value') else ''
            elif field_type == 'color':
                color_index = int(field.get('value', 0))
                if color_index:
                    field_value = colors[color_index-1][1]

            field_row = '''
            <div class="cpb_field_item">
                <div class="cpb_field_label">
                    <span class="cpb_field_label_title">%s</span>
                </div>
                <div class="cpb_field_value">%s</div>
            </div>
            ''' % (field['display_name'], field_value)
            advert_fields.append(field_row)

    return '\n'.join(advert_fields)

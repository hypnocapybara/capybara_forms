import re
import json

from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields import CharField, \
    IntegerField, FloatField, BooleanField


def get_data_fields(data):
    result = {}

    for item in data:
        if data[item]:
            key = re.findall(u'^data\[([\w_]+)\]$', item, re.UNICODE)
            if key:
                key = key[0]
                result[key] = data[item]

    return result


def get_filter_conditions(category_data, fields_in_filter, filter_values):
    result = {}

    for data_item in category_data:
        if 'name' in data_item and 'type' in data_item:
            name = data_item['name']

            if name in filter_values:
                value = filter_values[name]
                modifier = ''

                if name.endswith('_from'):
                    name = name[:-5]
                    modifier = '__gte'

                if name.endswith('_to'):
                    name = name[:-3]
                    modifier = '__lte'

                if data_item['type'] == 'select' and int(value) > 0:
                    result['data__' + name + '__value' + modifier] = int(value)
                elif data_item['type'] in ['number', 'number_select'] and float(value) > 0:
                    result['data__' + name + '__value' + modifier] = float(value)
                elif data_item['type'] == 'checkbox':
                    result['data__' + name + '__value'] = value == 'on'

    for name in fields_in_filter:
        if filter_values.get(name, ''):
            value = filter_values[name]
            modifier = ''

            if name.endswith('_from'):
                name = name[:-5]
                modifier = '__gte'

            if name.endswith('_to'):
                name = name[:-3]
                modifier = '__lte'

            result[name + modifier] = value

    return result


def get_advert_data_for_form_values(category_data, form_data):
    result = {}
    for field in category_data:
        if 'type' in field:
            field_type = field['type']
            if field_type == 'color':
                field_name = 'color'
            else:
                if 'name' not in field:
                    continue

                field_name = field['name']

            display_name = field['display_name'] if 'display_name' in field else field_name.title()

            if field_name in form_data:
                row = {
                    'type': field['type'],
                    'display_name': display_name,
                    'value': form_data[field_name]
                }

                if field['type'] == 'select':
                    row['value'], row['display_value'] = json.loads(form_data[field_name])
                    if int(row['value']) == 0:
                        continue

                if field['type'] == 'checkbox':
                    row['value'] = form_data[field_name] == 'on'

                if field['type'] == 'number':
                    row['value'] = float(form_data[field_name].replace(',', '.'))

                result[field_name] = row

    return result


def validate_data(category, data):
    result = []
    # first, check requirement
    for field in category.params:
        if 'required' in field and field['required']:
            valid = field['name'] in data and 'value' in data[field['name']] and data[field['name']]['value']
            if not valid:
                result.append((field['name'], u'Необходимо заполнить поле'))

    return result


def django_field_to_capybara_field(form, field):
    model = form.Meta.model
    field_name = field

    try:
        field_type = model._meta.get_field(field)
    except FieldDoesNotExist:
        if field.endswith('_from'):
            field_name = field
            field = field[:-5]
        elif field.endswith('_to'):
            field_name = field
            field = field[:-3]
        else:
            return {}

        field_type = model._meta.get_field(field)

    if getattr(field_type, 'choices', ()):
        result = {
            'type': 'select',
            'options': [list(item) for item in field_type.choices]
        }
    elif isinstance(field_type, IntegerField) or isinstance(field_type, FloatField):
        result = {'type': 'number'}
    elif isinstance(field_type, BooleanField):
        result = {'type': 'checkbox'}
    elif isinstance(field_type, CharField):
        result = {'type': 'string'}
    else:
        return {}

    result.update({
        'name': field_name,
        'required': not getattr(field_type, 'blank', False) is True,
        'display_name': field_type.verbose_name.title(),
        'placeholder': form.fields[field].widget.attrs.get('placeholder', ''),
        'full_name': field_name
    })
    return result


def float_to_string(val):
    return str(val).rstrip('0').rstrip('.')


def wrap_values(values):
    """
    Transforms form values to format, used in model and rendering functions
    :param values: values from form in {key: value} format
    :return: wrapped dict
    """
    return {
        key: {'value': values[key]}
        for key in values
    }

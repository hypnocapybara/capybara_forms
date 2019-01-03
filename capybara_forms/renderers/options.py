from django.conf import settings

from capybara_forms.models import SelectData


def render_nested_options(key, is_filter):
    not_selected = getattr(settings, 'CAPYBARA_FORMS_NOT_SELECTED', 'Not selected')

    if is_filter:
        result = [u"<option value='0'>{0}</option>".format(not_selected)]
    else:
        result = [u"<option value='[0,\"{0}\"]'>{0}</option>".format(not_selected)]

    data = SelectData.objects.filter(key=key).order_by('value').values_list('pk', 'value')
    for row in data:
        if is_filter:
            result.append("<option value='%s'>%s</option>" % (
                row[0], row[1]
            ))
        else:
            result.append("<option value='%s'>%s</option>" % (
                '[%s, "%s"]' % row,
                row[1]
            ))

    return '\n'.join(result)

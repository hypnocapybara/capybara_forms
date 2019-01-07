from .models import Category
from .category_data import get_cats_category, \
    get_cats_filter, get_cats_filter_template


def create_category(title, form=None, filter=None,
                    form_template=None, filter_template=None):
    if not form:
        form = get_cats_category()

    if not filter:
        filter = get_cats_filter()

    if not form_template:
        form_template = ''

    if not filter_template:
        filter_template = get_cats_filter_template()

    return Category.objects.create(
        title=title,
        params=form,
        search_params=filter,
        form_template=form_template,
        filter_template=filter_template)

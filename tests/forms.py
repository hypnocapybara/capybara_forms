from capybara_forms.forms import CapybaraFormsModelForm

from .models import Advert


class AdvertForm(CapybaraFormsModelForm):
    fields_in_model = ['title', 'price']
    fields_in_model_override = {
        'price': {
            'display_name': 'La priece',
            'placeholder': 'Enter price of your animal'
        }
    }
    fields_in_filter = ['price_from', 'price_to']
    fields_in_filter_override = {
        'price_from': {
            'placeholder': 'from',
            'display_name': '',  # make it empty to hide a label
        },
        'price_to': {
            'placeholder': 'to',
            'display_name': '',  # make it empty to hide a label
        }
    }

    # def get_default_filter_template(self):
    #     return render_to_string('parts/filter.html')

    class Meta:
        model = Advert
        fields = ('title', 'price')

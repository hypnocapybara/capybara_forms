from django.test import TestCase

from .utils import create_category
from .forms import AdvertForm
from .models import Advert


class CapybaraFormTestCase(TestCase):
    def setUp(self):
        super(CapybaraFormTestCase, self).setUp()
        self.category = create_category('Cats')

    def test_filter(self):
        advert = Advert.objects.create(
            category=self.category,
            title='advert 1',
            price=100,
            data={
                "name": {
                    "type": "string",
                    "value": "vasa",
                    "display_name": "Name"
                },
                "year": {
                    "type": "number",
                    "value": 2005,
                    "display_name": "Birth year"
                },
                "breed": {
                    "type": "select",
                    "value": 1,
                    "display_name": "Breed",
                    "display_value": "Oriental"
                },
                "color": {
                    "type": "color",
                    "value": "1",
                    "display_name": "Cat's color"
                },
                "height": {
                    "type": "number",
                    "value": 10,
                    "display_name": "Height"
                },
                "weight": {
                    "type": "number",
                    "value": 5,
                    "display_name": "Weight"
                },
                "vaccinated": {
                    "type": "checkbox",
                    "value": True,
                    "display_name": "is vaccinated"
                }
            })
        form = AdvertForm(self.category)
        adverts = form.filter_adverts()
        self.assertSetEqual(
            set([advert.pk for advert in adverts]),
            {advert.pk}
        )

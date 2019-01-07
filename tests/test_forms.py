from django.test import TestCase
from lxml import html

from capybara_forms.models import SelectData

from .utils import create_category
from .forms import AdvertForm
from .models import Advert


class CapybaraFormTestCase(TestCase):
    def setUp(self):
        super(CapybaraFormTestCase, self).setUp()
        self.category = create_category('Cats')
        self.breed1 = SelectData.objects.create(
            key='select.cat.breed',
            value='Oriental'
        )
        self.breed2 = SelectData.objects.create(
            key='select.cat.breed',
            value='Bengal'
        )
        self.advert1 = Advert.objects.create(
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
                    "value": self.breed1.pk,
                    "display_name": "Breed",
                    "display_value": self.breed1.value
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

        self.advert2 = Advert.objects.create(
            category=self.category,
            title='advert 2',
            price=200,
            data={
                "name": {
                    "type": "string",
                    "value": "july",
                    "display_name": "Name"
                },
                "year": {
                    "type": "number",
                    "value": 2010,
                    "display_name": "Birth year"
                },
                "breed": {
                    "type": "select",
                    "value": self.breed2.pk,
                    "display_name": "Breed",
                    "display_value": self.breed2.value
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

    def test_filter(self):
        form = AdvertForm(self.category)
        adverts = form.filter_adverts()
        self.assertSetEqual(
            set([advert.pk for advert in adverts]),
            {self.advert1.pk, self.advert2.pk}
        )

        form = AdvertForm(self.category, data={'price_from': 150, 'price_to': 300})
        adverts = form.filter_adverts()
        self.assertSetEqual(
            set([advert.pk for advert in adverts]),
            {self.advert2.pk}
        )

        form = AdvertForm(self.category, data={'data[breed]': self.breed1.pk})
        adverts = form.filter_adverts()
        self.assertSetEqual(
            set([advert.pk for advert in adverts]),
            {self.advert1.pk}
        )

        form = AdvertForm(self.category, data={'data[breed]': self.breed1.pk})
        adverts = form.filter_adverts()
        self.assertSetEqual(
            set([advert.pk for advert in adverts]),
            {self.advert1.pk}
        )

        form = AdvertForm(self.category, data={'data[year_from]': 2009})
        adverts = form.filter_adverts()
        self.assertSetEqual(
            set([advert.pk for advert in adverts]),
            {self.advert2.pk}
        )

    def test_render_form(self):
        form = AdvertForm(self.category)
        content = form.render_form()
        page = html.fragment_fromstring('<div>' + content + '</div>')
        items_count = len(page.xpath('//div[@class="cpb_form_item"]'))
        self.assertEqual(items_count, 9)

    def test_render_filter(self):
        form = AdvertForm(self.category)
        content = form.render_filter()
        page = html.fragment_fromstring('<div>' + content + '</div>')
        items_count = len(page.xpath('//div[@class="cpb_form_item"]'))
        self.assertEqual(items_count, 10)

    def test_render_item(self):
        form = AdvertForm(self.category, instance=self.advert1)
        content = form.render_item()
        page = html.fragment_fromstring('<div>' + content + '</div>')
        items_count = len(page.xpath('//div[@class="cpb_field_item"]'))
        self.assertEqual(items_count, 7)

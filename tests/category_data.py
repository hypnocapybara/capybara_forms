cats_category = [
    {
        "name": "breed",
        "type": "select",
        "options": "select.cat.breed",
        "required": True,
        "display_name": "Breed"
    },
    {
        "name": "year",
        "type": "number",
        "required": True,
        "max_value": 2020,
        "min_value": 1980,
        "placeholder": "Enter birth year of your cat",
        "display_name": "Birth year"
    },
    {
        "name": "weight",
        "type": "number",
        "placeholder": "Enter the weight of your cat",
        "display_name": "Weight"
    },
    {
        "name": "height",
        "type": "number",
        "placeholder": "Height (only placeholder, without display name)"
    },
    {
        "type": "color",
        "display_name": "Cat's color"
    },
    {
        "name": "name",
        "type": "string",
        "placeholder": "Enter cat nickname",
        "display_name": "Name"
    },
    {
        "name": "vaccinated",
        "type": "checkbox",
        "display_name": "is vaccinated"
    }
]


cats_filter = [
    {
        "name": "breed",
        "type": "select",
        "options": "select.cat.breed",
        "placeholder": "Breed",
        "display_name": "Breed"
    },
    {
        "end": 1950,
        "name": "year_from",
        "step": -1,
        "type": "number_select",
        "start": 2018
    },
    {
        "end": 1950,
        "name": "year_to",
        "step": -1,
        "type": "number_select",
        "start": 2018
    },
    {
        "name": "weight_from",
        "type": "number",
        "placeholder": "Weight, from"
    },
    {
        "name": "weight_to",
        "type": "number",
        "placeholder": "Weight, to"
    },
    {
        "name": "vaccinated",
        "type": "checkbox",
        "display_name": "is vaccinated"
    }
]

cats_filter_template = '''
<div class="cpb_form_item">
    <label class="cpb_form_label cpb_form_label-select">
       Price
    </label>
    <div class="cpb_filter_group">
        {price_from}
        <div class="cpb_filter_tiret"></div>
        {price_to}
    </div>
</div>
{breed}
<div class="cpb_form_item">
    <label class="cpb_form_label cpb_form_label-select">
       Birth year
    </label>
    <div class="cpb_filter_group">
        {year_from}
        <div class="cpb_filter_tiret"></div>
        {year_to}
    </div>
</div>
{weight_from}
{weight_to}
{vaccinated}
'''

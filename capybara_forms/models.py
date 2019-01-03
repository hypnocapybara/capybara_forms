from django.db import models
from django.contrib.postgres.fields import JSONField


class CapybaraFormsCategory(models.Model):
    params = JSONField(verbose_name='Category fields', default=dict, null=True)
    search_params = JSONField(verbose_name='Filter fields', default=dict, null=True)
    form_template = models.TextField(
        blank=True, null=True)
    filter_template = models.TextField(
        blank=True, null=True)

    class Meta:
        abstract = True


def CapybaraFormsModel(CategoryModel):
    class CapybaraFormsEntryClass(models.Model):
        category = models.ForeignKey(
            CategoryModel,
            on_delete=models.CASCADE)
        data = JSONField(
            blank=True, null=True,
            verbose_name='Category fields data')

        class Meta:
            abstract = True

    return CapybaraFormsEntryClass


class SelectData(models.Model):
    key = models.CharField(
        max_length=80)
    value = models.CharField(
        max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True, null=True)

    def __str__(self):
        return '%s : %s' % (self.key, self.value)

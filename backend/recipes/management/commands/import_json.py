import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(
            'recipes/management/commands/data/ingredients.json', 'rb'
        ) as f:
            data = json.load(f)
            for item in data:
                print(item)
                Ingredient.objects.create(name=item['name'],
                                          measurement_unit=item
                                          ['measurement_unit'])

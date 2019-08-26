# Create your tests here.
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import DataError
from django.test import TestCase

from marketAnalysis.models import Citizen, Import


class CitizenTest(TestCase):
    # Test Citizen Model
    def test_citizen_model(self):
        imprt = Import.objects.create()
        # Check text size > 256
        with transaction.atomic():
            with self.assertRaises(DataError):
                Citizen.objects.create(imports=imprt, **{"citizen_id": 1,
                                                         "town": "М" * 257,
                                                         "street": "Льва Толстого",
                                                         "building": "16к7стр5",
                                                         "apartment": 7,
                                                         "name": "Иванов Сергей Иванович",
                                                         "birth_date": "1995-06-01",
                                                         "gender": "male", })
        # Check charOrDigValidate validator
        with transaction.atomic():
            instance = Citizen.objects.create(imports=imprt, **{"citizen_id": 2,
                                                                "town": """Минск   fdfdf/.""",
                                                                "street": "1.",
                                                                "building": "16к7стр5",
                                                                "apartment": 7,
                                                                "name": "Иванов Сергей Иванович",
                                                                "birth_date": "1995-06-01",
                                                                "gender": "male",
                                                                })
            with self.assertRaises(ValidationError):
                instance.full_clean()
        # Check gender type
        with transaction.atomic():
            instance = Citizen.objects.create(imports=imprt, **{"citizen_id": 2,
                                                                "town": """Минск""",
                                                                "street": "Иосифа Бродского",
                                                                "building": "16к7стр5",
                                                                "apartment": 7,
                                                                "name": "Иванов Сергей Иванович",
                                                                "birth_date": "1995-06-01",
                                                                "gender": "mal",
                                                                })
            with self.assertRaises(ValidationError):
                instance.full_clean()
        # Check that all is good
        with transaction.atomic():
            instance = Citizen.objects.create(imports=imprt, **{"citizen_id": 2,
                                                                "town": """Минск   """,
                                                                "street": "Иосифа Бродскогоdd",
                                                                "building": "16к7стр5",
                                                                "apartment": 7,
                                                                "name": "Иванов Сергей Иванович",
                                                                "birth_date": "1995-06-01",
                                                                "gender": "male",
                                                                })
            instance.full_clean()

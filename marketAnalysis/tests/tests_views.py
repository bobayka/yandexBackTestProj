import copy

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.utils import json

from marketAnalysis.serializers import ImportCreateSerializer

set1 = {
    "citizens": [
        {
            "citizen_id": 1,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "26.12.1986",
            "gender": "male",
            "relatives": [
                2, 3, 4, 5, 6
            ]
        },
        {
            "citizen_id": 2,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Сергей Иванович",
            "birth_date": "01.04.1997",
            "gender": "male",
            "relatives": [
                1
            ]
        },
        {
            "citizen_id": 3,
            "town": "Керчь",
            "street": "Иосифа Бродского",
            "building": "2",
            "apartment": 11,
            "name": "Романова Мария Леонидовна",
            "birth_date": "23.11.1986",
            "gender": "female",
            "relatives": [1, 4]
        },
        {
            "citizen_id": 4,
            "town": "Керчь",
            "street": "Иосифа Бродского",
            "building": "2",
            "apartment": 11,
            "name": "Романова Мария Леонидовна",
            "birth_date": "23.11.1986",
            "gender": "female",
            "relatives": [1, 3]
        },
        {
            "citizen_id": 5,
            "town": "Керчь",
            "street": "Иосифа Бродского",
            "building": "2",
            "apartment": 11,
            "name": "Романова Мария Леонидовна",
            "birth_date": "23.11.1950",
            "gender": "female",
            "relatives": [1]
        },
        {
            "citizen_id": 6,
            "town": "Керчь",
            "street": "Иосифа Бродского",
            "building": "2",
            "apartment": 11,
            "name": "Романова Мария Леонидовна",
            "birth_date": "1.3.1933",
            "gender": "female",
            "relatives": [1]
        }
    ]
}


class ImportCitizensTest(TestCase):
    def setUp(self) -> None:
        self.RightCitizen = {
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "name": "Иванов Иван Иванович",
                    "birth_date": "26.12.1986",
                    "gender": "male",
                    "relatives": []
                }]}

    def test_invalid_post_citizens(self):
        # Check birthday < date.today()
        checkBirthdayCitizen = copy.deepcopy(self.RightCitizen)
        checkBirthdayCitizen['citizens'][0]['birth_date'] = "12.12.2022"
        resp = self.client.post('/imports', data=json.dumps(checkBirthdayCitizen), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

        # Check null field
        checkNullField = copy.deepcopy(self.RightCitizen)
        checkNullField['citizens'][0]['citizen_id'] = None
        resp = self.client.post('/imports', data=json.dumps(checkNullField), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

        # Check miss field
        checkMissFiels = copy.deepcopy(self.RightCitizen)
        checkMissFiels['citizens'][0].pop('town')
        resp = self.client.post('/imports', data=json.dumps(checkMissFiels), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

        # Check citizens uniqueness
        checkCitizenUniqueness = copy.deepcopy(self.RightCitizen)
        checkCitizenUniqueness['citizens'].append(checkCitizenUniqueness['citizens'][0])
        resp = self.client.post('/imports', data=json.dumps(checkCitizenUniqueness), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

        # Check not existing relatives
        checkNotExistingRelaitves = copy.deepcopy(self.RightCitizen)
        checkNotExistingRelaitves['citizens'].append(copy.deepcopy(checkNotExistingRelaitves['citizens'][0]))
        checkNotExistingRelaitves['citizens'][0]['relatives'].append(3)
        checkNotExistingRelaitves['citizens'][1]['citizen_id'] = 2
        checkNotExistingRelaitves['citizens'][1]['relatives'].append(1)
        resp = self.client.post('/imports', data=json.dumps(checkNotExistingRelaitves), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

        # Check   bilateral relationship

        bilateralRelationship = checkNotExistingRelaitves
        bilateralRelationship['citizens'][0]['relatives'] = []
        resp = self.client.post('/imports', data=json.dumps(bilateralRelationship), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_valid_post_citizens(self):
        resp = self.client.post('/imports', data=json.dumps(set1), content_type='application/json')
        self.assertEqual(resp.status_code, 201)


class CitizenUpdateTest(TestCase):
    def setUp(self) -> None:
        serializer = ImportCreateSerializer(data=set1)
        if serializer.is_valid():
            data = serializer.save().pk
            self.importObj = data
        else:
            raise ValidationError

    def test_update_citizen(self):

        # Check updating
        resp = self.client.patch(path=f'/imports/{self.importObj}/citizens/1', data=json.dumps({
            "town": "Moscow",
            "street": "Dnepropetrovskaya",
            "building": "16dfg",
            "apartment": 7,
            "name": "Bobkov Denis",
            "birth_date": "26.12.1986",
            "relatives": []}),
                                 content_type='application/json')
        self.assertEqual(json.loads(resp.content), {"data": {
            "citizen_id": 1,
            "town": "Moscow",
            "street": "Dnepropetrovskaya",
            "building": "16dfg",
            "apartment": 7,
            "name": "Bobkov Denis",
            "birth_date": "26.12.1986",
            "gender": "male",
            "relatives": []}})
        self.assertEqual(resp.status_code, 200)

        # Check relations change
        resp = self.client.patch(path=f'/imports/{self.importObj}/citizens/2', data=json.dumps({
            "town": "Moscow",
            "street": "Zharova",
            "building": "16fdfdlkotttltdfg",
            "apartment": 7,
            "name": "Alexeev Denis",
            "birth_date": "26.12.1996"}), content_type='application/json')
        self.assertEqual(json.loads(resp.content), {"data": {
            "citizen_id": 2,
            "town": "Moscow",
            "street": "Zharova",
            "building": "16fdfdlkotttltdfg",
            "apartment": 7,
            "name": "Alexeev Denis",
            "birth_date": "26.12.1996",
            "gender": "male",
            "relatives": []}})
        self.assertEqual(resp.status_code, 200)


class CitizenGetTest(TestCase):
    def setUp(self) -> None:
        serializer = ImportCreateSerializer(data=set1)
        if serializer.is_valid():
            data = serializer.save().pk
            self.importObj = data
        else:
            raise ValidationError

    def test_get_citizens(self):
        resp = self.client.get(path=f'/imports/{self.importObj}/citizens', content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(path=f'/imports/1505050/citizens', content_type='application/json')
        self.assertEqual(resp.status_code, 400)


class GiftDistributionTest(TestCase):
    def setUp(self) -> None:
        serializer = ImportCreateSerializer(data=set1)
        if serializer.is_valid():
            data = serializer.save().pk
            self.importObj = data
        else:
            raise ValidationError

    def test_gift_distribution(self):
        resp = self.client.get(path=f'/imports/{self.importObj}/citizens/birthdays', content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.maxDiff = None
        self.assertEqual(json.loads(resp.content), {
            "data": {
                "1": [],
                "2": [],
                "3": [
                    {
                        "citizen_id": 1,
                        "presents": 1
                    }
                ],
                "4": [
                    {
                        "citizen_id": 1,
                        "presents": 1
                    }
                ],
                "5": [],
                "6": [],
                "7": [],
                "8": [],
                "9": [],
                "10": [],
                "11": [
                    {
                        "citizen_id": 1,
                        "presents": 3
                    },
                    {
                        "citizen_id": 3,
                        "presents": 1
                    },
                    {
                        "citizen_id": 4,
                        "presents": 1
                    },

                ],
                "12": [
                    {
                        "citizen_id": 2,
                        "presents": 1
                    },
                    {
                        "citizen_id": 3,
                        "presents": 1
                    },
                    {
                        "citizen_id": 4,
                        "presents": 1
                    },
                    {
                        "citizen_id": 5,
                        "presents": 1
                    },
                    {
                        "citizen_id": 6,
                        "presents": 1
                    },
                ]
            }
        })


class AgePercentileTest(TestCase):
    def setUp(self) -> None:
        serializer = ImportCreateSerializer(data=set1)
        if serializer.is_valid():
            data = serializer.save().pk
            self.importObj = data
        else:
            raise ValidationError

    def test_get_PercentileAge(self):
        resp = self.client.get(path=f'/imports/{self.importObj}/towns/stat/percentile/age',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content)['data'][1]["p50"], 27)

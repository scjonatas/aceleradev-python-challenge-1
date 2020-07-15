from main import classify_by_phone_number
from json import load


class TestChallenge1:

    records = []

    def setup_class(self):
        with open('records.json') as json_file:
            self.records = load(json_file)

    def test_len(self):
        result = classify_by_phone_number(self.records)
        assert len(result) == 6

    def test_order(self):
        result = classify_by_phone_number(self.records)
        for i in range(len(result) - 1):
            assert result[i]['total'] > result[i + 1]['total']

    def test_decimals(self):
        result = classify_by_phone_number(self.records)
        for record in result:
            (integer_part, decimal_part) = str(record['total']).split('.')
            assert len(decimal_part) <= 2

    def test_answer(self):
        answer = [
            {'source': '41-833333333', 'total': 4.77},
            {'source': '48-999999999', 'total': 4.68},
            {'source': '41-885633788', 'total': 3.96},
            {'source': '48-996355555', 'total': 2.61},
            {'source': '41-886383097', 'total': 1.53},
            {'source': '48-996383697', 'total': 1.35}
        ]
        result = classify_by_phone_number(self.records)
        for i in range(len(result)):
            assert result[i]['source'] == answer[i]['source']
            assert result[i]['total'] == answer[i]['total']

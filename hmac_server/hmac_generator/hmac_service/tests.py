from django.test import TestCase, Client

# from urllib.parse import urlencode


class HMACTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_hmac(self):
        test_cases = [
            {
                "url": "/api/v1/hmac/",
                "body": "foo=1",
                "status_code": 201,
                "signature": "38a21635c6f1ebd968d71fbc455977ec03166c50",
            },
            {
                "url": "/",
                "body": "foo=1",
                "status_code": 201,
                "signature": "38a21635c6f1ebd968d71fbc455977ec03166c50",
            },
            {
                "url": "/api/v1/hmac/",
                "body": "",
                "status_code": 201,
                "signature": "e66342c12524a7f2bd7b3556fa61ec40eaab9a66",
            },
            {
                "url": "/",
                "body": "",
                "status_code": 201,
                "signature": "e66342c12524a7f2bd7b3556fa61ec40eaab9a66",
            },
            {
                "url": "/api/v1/hmac/",
                "body": "a",
                "status_code": 201,
                "signature": "22d4a73ac56e57c18c1739a6e9e114a2a796fced",
            },
            {
                "url": "/",
                "body": "a",
                "status_code": 201,
                "signature": "22d4a73ac56e57c18c1739a6e9e114a2a796fced",
            },
            {
                "url": "/api/v1/hmac/",
                "body": "a=",
                "status_code": 201,
                "signature": "4d751170d4ab2bc701617594a4f3b9f3b98007fd",
            },
            {
                "url": "/",
                "body": "a=",
                "status_code": 201,
                "signature": "4d751170d4ab2bc701617594a4f3b9f3b98007fd",
            },
        ]
        for test_case in test_cases:
            response = self.client.post(
                test_case["url"],
                test_case["body"],
                content_type="application/x-www-form-urlencoded",
            )
            self.assertEqual(response.status_code, test_case["status_code"])
            self.assertEqual(response.json()["signature"], test_case["signature"])

    def test_hmac_invalid_utf8(self):
        test_cases = [
            {
                "url": "/api/v1/hmac/",
                "body": b"\x00\xaa\xff",
                "status_code": 400,
            },
            {
                "url": "/",
                "body": b"\x00\xaa\xff",
                "status_code": 400,
            },
        ]
        for test_case in test_cases:
            response = self.client.post(
                test_case["url"],
                test_case["body"],
                content_type="application/x-www-form-urlencoded",
            )
            self.assertEqual(response.status_code, test_case["status_code"])
            self.assertEqual(response.json(), "Invalid UTF8")

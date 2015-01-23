# -*- coding: utf-8 -*-

import os

import django
from django.test import TestCase
from django.test.utils import override_settings


django.setup()


PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


class DataSelect1TestCase(TestCase):

    fixtures = [os.path.join(PATH, 'dataselect.json')]

    def test_version(self):
        # 1 - HTTP OK
        response = self.client.get('/fdsnws/dataselect/1/version')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/plain')
        self.assertEqual(response.content, b'1.1.1')
        # 2 - incorrect trailing slash will work too
        response = self.client.get('/fdsnws/dataselect/1/version/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/plain')
        self.assertEqual(response.content, b'1.1.1')

    def test_wadl(self):
        # 1 - HTTP OK
        response = self.client.get('/fdsnws/dataselect/1/application.wadl')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         'application/xml; charset=utf-8')
        self.assertTrue(response.content.startswith(b'<?xml'))
        # 2 - incorrect trailing slash will work too
        response = self.client.get('/fdsnws/dataselect/1/application.wadl/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         'application/xml; charset=utf-8')
        self.assertTrue(response.content.startswith(b'<?xml'))

    def test_index(self):
        # 1 - redirect if APPEND_SLASH = True
        response = self.client.get('/fdsnws/dataselect/1')
        self.assertEqual(response.status_code, 301)
        # 2 - HTTP OK
        response = self.client.get('/fdsnws/dataselect/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')

    def test_query(self):
        # 1 - start time must be specified
        param = '?'
        response = self.client.get('/fdsnws/dataselect/1/query' + param)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Start time must be specifi' in response.reason_phrase)
        # 2 - start time must be parseable
        param = '?start=0'
        response = self.client.get('/fdsnws/dataselect/1/query' + param)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Error parsing starttime' in response.reason_phrase)
        # 3 - end time must be specified
        param = '?start=2012-01-01'
        response = self.client.get('/fdsnws/dataselect/1/query' + param)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('End time must be specified' in response.reason_phrase)
        # 4 - end time must be parseable
        param = '?start=2012-01-01&end=0'
        response = self.client.get('/fdsnws/dataselect/1/query' + param)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Error parsing endtime' in response.reason_phrase)
        # 5 - start time must before endtime
        param = '?start=2012-01-01&end=2012-01-01'
        response = self.client.get('/fdsnws/dataselect/1/query' + param)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Start time must be before end time' in
                        response.reason_phrase)
        param = '?start=2012-01-02&end=2012-01-01'
        response = self.client.get('/fdsnws/dataselect/1/query' + param)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Start time must be before end time' in
                        response.reason_phrase)
        # 6 - channel is required
        param = '?start=2012-01-01&end=2012-01-02&net=GE&sta=APE'
        response = self.client.get('/fdsnws/dataselect/1/query' + param)
        self.assertEqual(response.status_code, 413)
        self.assertTrue('No channels specified' in response.reason_phrase)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_URL='memory://')
    def test_query_data(self):
        # not existing - error 500
        #param = '?start=2012-01-01&end=2012-01-02&net=GE&sta=APE&cha=EHE'
        #response = self.client.get('/fdsnws/dataselect/1/query' + param)
        #print(response.reason_phrase)
        #self.assertEqual(response.status_code, 500)
        #print(response.reason_phrase)
        #self.assertTrue('No channels specified' in response.reason_phrase)
        # not existing - error 404
        #param = '?start=2012-01-01&end=2012-01-02&net=GE&sta=APE&cha=EHE&nodata=404'
        #response = self.client.get('/fdsnws/dataselect/1/query' + param)
        #print(response.reason_phrase)
        #self.assertEqual(response.status_code, 500)
        #self.assertTrue('No channels specified' in response.reason_phrase)
        # existing
        param = '?start=2013-05-24T06:00:00&end=2013-05-24T06:01:00&net=TA&station=X60A&cha=BHE'
        response = self.client.get('/fdsnws/dataselect/1/query' + param)
        self.assertEqual(response.status_code, 200)
        print(response.reason_phrase)

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import json

import unittest2 as unittest

from stacktester import openstack


class ServersMetadataTest(unittest.TestCase):

    def setUp(self):
        self.os = openstack.Manager()

        post_body = json.dumps({
            'server' : {
                'name' : 'testserver',
                'imageRef' : 3,
                'flavorRef' : 1,
                'metadata' : {
                    'testEntry' : 'testValue'
                }
            }
        })

        response, body = self.os.nova.request(
            'POST', '/servers', body=post_body)

        data = json.loads(body)

        self.server_id = data['server']['id']
        self.os.nova.wait_for_server_status(self.server_id, 'ACTIVE')

    def tearDown(self):
        self.os.nova.request('DELETE', '/servers/%s' % self.server_id)

    def test_get_servers_metdata(self):
        """Test that we can retrieve metadata for a server"""

        response, body = self.os.nova.request('GET', '/servers/%s/meta' % self.server_id)
        result = json.loads(body)['metadata']
        self.assertEqual(result['testEntry'], 'testValue')

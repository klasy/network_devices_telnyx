#!/usr/bin/env python

from unittest import TestCase, TestLoader, TextTestRunner
from processor import Processor

class TestDevice(TestCase):
    """ Test Device Class """

    def setUp(self):
        # setting up the suite for the test
        self.processor = Processor("test_vlans.csv", "", "")
        self.processor.process_vlan_file()

        # we get the device with id 0 for the test
        self.device = self.processor.net.devices[0]

    def tearDown(self):
        del self.device
        del self.processor

    def test_get_primary_secondary_vlan_ids(self):
        # test current device id is the very first one in the list
        id = self.device.get_cur_primary_vlan_id()
        self.assertEqual(id, 2)

        # test we have corresponding secondary id
        # and it's index is 0
        secondary_id_ind = self.device.get_corresponding_secondary_vlan(id)
        self.assertEqual(secondary_id_ind, 0)
        self.assertEqual(self.device.secondary_vlan_ids[secondary_id_ind], 2)
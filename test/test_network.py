#!/usr/bin/env python

from unittest import TestCase
from processor import Processor
from network_device import Device

class TestNetwork(TestCase):

    """ Test the Network Class """

    test_keys = [0, 1, 2]
    test_primary_vlans = {0: [2, 5, 8],
                          1: [1, 5, 6, 9],
                          2: [1, 4, 10]}
    test_secondary_vlans = {0: [2, 3, 4, 6, 7, 8, 10],
                            1: [1, 4, 5, 7],
                            2: []}
    test_first_lowest = {0: 2, 1: 1, 2: 1}

    def setUp(self):
        # setting up the suite for the test
        self.processor = Processor("test_vlans.csv", "", "")
        self.processor.process_vlan_file()
        self.processor.net.fillout_lowest_vlan_ids()

    def tearDown(self):
        del self.processor

    def test_devices(self):
        for i in xrange(len(self.processor.net.devices)):
            key = self.processor.net.devices.keys()[i]
            value = self.processor.net.devices[key]

            self.assertEqual(key, self.test_keys[i])
            self.assertIsInstance(value, Device)
            self.assertListEqual(self.test_primary_vlans[key], value.primary_vlan_ids)
            self.assertListEqual(self.test_secondary_vlans[key], value.secondary_vlan_ids)

    def test_lowest_vlans(self):
        for i in xrange(len(self.processor.net.lowest_vlans)):
            key = self.processor.net.lowest_vlans.keys()[i]
            value = self.processor.net.lowest_vlans[key]

            self.assertEqual(key, self.test_keys[i])
            self.assertEqual(value, self.test_first_lowest[i])

    def test_get_lowest_device_id(self):
        # getting first lowest device id with lowest vlan
        lowest = self.processor.net.get_lowest_device_id()
        self.assertEqual(lowest, 1)

        self.processor.net.devices[lowest].remove_used_vlan()
        self.processor.net.reset_counter(lowest)
        # now updating this device's vlan
        self.processor.net.update_lowest_vlan_id(lowest)
        # and getting a new lowest device id with lowest vlan
        lowest = self.processor.net.get_lowest_device_id()
        self.assertEqual(lowest, 2)

        # and the last one just in case
        self.processor.net.devices[lowest].remove_used_vlan()
        self.processor.net.reset_counter(lowest)
        self.processor.net.update_lowest_vlan_id(lowest)
        lowest = self.processor.net.get_lowest_device_id()
        self.assertEqual(lowest, 0)

    def test_update_lowest_vlan_id(self):
        # testing update lowest_vlans dictionary
        for key, cur_lowest in self.processor.net.lowest_vlans.iteritems():
            self.assertEqual(cur_lowest, self.test_primary_vlans[key][0])

            self.processor.net.devices[key].remove_used_vlan()
            self.processor.net.reset_counter(key)
            self.processor.net.update_lowest_vlan_id(key)
            next_lowest = self.processor.net.devices[key].get_cur_primary_vlan_id()
            self.assertEqual(next_lowest, self.test_primary_vlans[key][1])
#!/usr/bin/env python

from unittest import TestCase
from processor import Processor

import csv, sys

class TestProcessor(TestCase):

    """ Testing the Processor class """

    def setUp(self):
        self.processor = Processor("test_vlans.csv", "test_requests.csv", "")
        self.processor.process_vlan_file()

        # get first vlans
        for device in self.processor.net.devices.values():
            device.primary_vlan_ids.sort()
            device.secondary_vlan_ids.sort()

        self.processor.net.fillout_lowest_vlan_ids()

        self.output = []

    def tearDown(self):
        del self.processor
        del self.output

    def read_output_file(self):
        with open("data/test_output.csv", 'rb') as out_f:
            reader = csv.DictReader(out_f)
            try:
                for row in reader:
                    tmp_row = {"request_id": int(row["request_id"]),
                               "device_id": int(row["device_id"]),
                               "primary_port": int(row["primary_port"]),
                               "vlan_id": int(row["vlan_id"])}
                    self.output.append(tmp_row)
            except csv.Error, e:
                sys.exit('file %s, line %d: %s' % ("data/test_output.csv", reader.line_num, e))

    def test_integration(self):
        # generate the output by the code
        output = self.processor.process_requests_file()
        # read the output from the file we are given
        self.read_output_file()

        # compare
        for i in xrange(len(output)):
            self.assertDictEqual(output[i], self.output[i])
#!/usr/bin/env python

from network_device import Device
from network import Network

import csv, sys
import os.path

class Processor:

    def __init__(self, v_file, r_file, o_file):
        self.net = Network()

        self.vlans_filename = "data/" + v_file
        self.requests_filename = "data/" + r_file
        self.output_filename = "data/" + o_file

        self.requests = {}

    def process_vlan_file(self):
        """
        A function to pull all the info from the vlans file and put it to work
        :return: nothing
        """

        # checkng if file exists first
        if not os.path.isfile(self.vlans_filename):
            raise Exception("There's no vlans file!!!")

        with open(self.vlans_filename, 'rb') as vlans_f:
            reader = csv.DictReader(vlans_f)
            try:
                for row in reader:
                    device_id, primary_port, vlan_id = int(row["device_id"]), \
                                                       int(row["primary_port"]), \
                                                       int(row["vlan_id"])
                    if device_id in self.net.devices.keys():
                        device = self.net.devices[device_id]
                    else:
                        device = Device(device_id)
                        self.net.devices[device_id] = device
                    device.fill_device_vlan_pool(primary_port, vlan_id)
            except csv.Error, e:
                sys.exit('file %s, line %d: %s' % (self.vlans_filename, reader.line_num, e))

    def process_requests_file(self):
        """
        A function to pull out all the data frm requests file and put it to work
        :return: nothing
        """
        out_list = []

        # checking if file exists first
        if not os.path.isfile(self.requests_filename):
            raise Exception("There's no requests file!!!")

        # in Python3 I would replace this line with
        # with open(self.requests_filename, 'rb', newline='') as req_f:
        # but using Python2, so ...
        with open(self.requests_filename, 'rb') as req_f:
            reader = csv.DictReader(req_f)
            for line in reader:
                request_id, redundant = int(line["request_id"]), int(line["redundant"])
                out_val = self.handle_request(request_id, redundant)
                out_list.extend(out_val)

        return out_list

    def create_output(self, result_lists):
        """
        Here we'll write the output to the output.csv
        :return: nothing
        """
        with open(self.output_filename, 'wb') as f:
            fnames = ['request_id', 'device_id', 'primary_port', 'vlan_id']
            writer = csv.DictWriter(f, fieldnames=fnames)

            writer.writeheader()
            writer.writerows(result_lists)

    def handle_request(self, request_id, redundant):
        """
        A function to send request to be processed
        :param request_id: id of the request
        :param redundant: if request is redundant, True or False
        """
        result_out = []

        # so we need the primary vlan id in any case
        # might be changed if request is redundant
        lowest_device = self.net.get_lowest_device_id()
        device = self.net.devices[lowest_device]
        lowest_primary_vlan = self.net.lowest_vlans[lowest_device]

        if redundant:
            lowest_secondary_vlan_id = device.get_corresponding_secondary_vlan(lowest_primary_vlan)
            # we need 2-nd output vlan
            while lowest_secondary_vlan_id == -1:
                # so look out for the secondary vlan id
                device.increase_the_counter()
                self.net.update_lowest_vlan_id(lowest_device)
                lowest_device = self.net.get_lowest_device_id()
                device = self.net.devices[lowest_device]
                lowest_primary_vlan = self.net.lowest_vlans[lowest_device]
                lowest_secondary_vlan_id = device.get_corresponding_secondary_vlan(lowest_primary_vlan)

            tmp = {"request_id": request_id, "device_id": lowest_device, "primary_port": 0, "vlan_id": lowest_primary_vlan}
            result_out.append(tmp)
            self.net.devices[lowest_device].remove_used_vlan(True, lowest_secondary_vlan_id)
        else:
            self.net.devices[lowest_device].remove_used_vlan()

        self.net.reset_counter(lowest_device)
        self.net.fillout_lowest_vlan_ids()

        # creating non-redundant output
        tmp = {"request_id": request_id, "device_id": lowest_device, "primary_port": 1, "vlan_id": lowest_primary_vlan}
        result_out.append(tmp)

        return result_out
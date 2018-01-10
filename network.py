#!/usr/bin/env python


class Network:

    def __init__(self):
        # dictionary of device_id: device
        self.devices = {}

        # dictionary of device_id: lowest_vlan at the moment
        self.lowest_vlans = {}

    def fillout_lowest_vlan_ids(self):
        for id, device in self.devices.iteritems():
            lowest_id = device.get_cur_primary_vlan_id()
            self.lowest_vlans[id] = lowest_id

    def update_lowest_vlan_id(self, device_id):
        device = self.devices[device_id]
        self.lowest_vlans[device_id] = device.get_cur_primary_vlan_id()

    def get_lowest_device_id(self):
        from sys import maxint

        lowest = maxint
        lowest_key = maxint

        for key, value in self.lowest_vlans.iteritems():
            # here we are considering only the first lowest
            # if it's a tie, choose the VLAN IDs on the device
            # with the lowest device id
            if lowest > value:
                lowest = value
                lowest_key = key

        return lowest_key

    def reset_counter(self, device_id):
        """
        In case wewent far ahead for each of the devices in seaking the secondary vlan
        """

        for key, device in self.devices.iteritems():
            device.id_counter = 0
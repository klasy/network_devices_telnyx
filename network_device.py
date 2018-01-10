#!/usr/bin/env python

from sys import maxint

class Device(object):

    def __init__(self, device_id):
        self.device_id = device_id
        self.primary_vlan_ids = []
        self.secondary_vlan_ids = []

        # we are always starting at 0
        self.id_counter = 0

    def get_device_id(self):
        return self.device_id

    def get_cur_primary_vlan_id(self):
        if len(self.primary_vlan_ids) > 0 and len(self.primary_vlan_ids) > self.id_counter:
            return self.primary_vlan_ids[self.id_counter]
        else:
            return maxint

    def increase_the_counter(self):
        self.id_counter = self.id_counter + 1

    def get_corresponding_secondary_vlan(self, primary_vlan):
        if len(self.secondary_vlan_ids) == 0:
            return -1

        start, end = 0, len(self.secondary_vlan_ids) - 1
        # return -1 if we did not find
        return self.binary_search_for_secondary_vlan(primary_vlan, start, end)

    def binary_search_for_secondary_vlan(self, primary_vlan, start, end):
        if len(self.secondary_vlan_ids) == 0:
            return -1

        if end >= start:
            med = (start + end) // 2
            if self.secondary_vlan_ids[med] == primary_vlan:
                return med
            elif self.secondary_vlan_ids[med] > primary_vlan:
                return self.binary_search_for_secondary_vlan(primary_vlan, start, med - 1)
            else:
                return self.binary_search_for_secondary_vlan(primary_vlan, med + 1, end)
        else:
            # otherwise we did not find the element in the array
            return -1

    def fill_device_vlan_pool(self, primary, vlan_id):
        if primary:
            self.primary_vlan_ids.append(vlan_id)
        else:
            self.secondary_vlan_ids.append(vlan_id)

    def remove_used_vlan(self, is_secondary=False, secondary_id=0):
        tmp = self.primary_vlan_ids.pop(self.id_counter)
        if is_secondary:
            tmp = self.secondary_vlan_ids.pop(secondary_id)
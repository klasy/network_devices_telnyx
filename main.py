#!/usr/bin/env python

from processor import Processor

def main():
    pr = Processor("vlans.csv", "requests.csv", "output.csv")
    pr.process_vlan_file()

    # get first vlans
    for device in pr.net.devices.values():
        device.primary_vlan_ids.sort()
        device.secondary_vlan_ids.sort()

    pr.net.fillout_lowest_vlan_ids()

    output = pr.process_requests_file()
    pr.create_output(output)

if __name__ == "__main__":
    main()
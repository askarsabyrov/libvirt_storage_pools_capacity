#!/usr/bin/env python

import libvirt
import sys
import json

def connect(libvirt_connection="qemu:///system"):
    conn = libvirt.open(libvirt_connection)
    conn.storagePoolLookupByName
    if conn is None:
        print('Failed to open connection to %s' % (libvirt_connection))
        sys.exit(1)
    return conn


if __name__ == "__main__":
    conn = connect()

    result = dict()

    for pool in conn.listStoragePools():
        result[pool] = dict()
        result[pool]["volumes"] = []
        result[pool]["total_capacity_gb"] = 0.0
        pool_obj = conn.storagePoolLookupByName(pool)
        for volume_name in pool_obj.listVolumes():
            volume_obj = pool_obj.storageVolLookupByName(volume_name)
            volume = dict()
            volume["name"] = volume_name
            info = volume_obj.info()
            volume["capacity_gb"] = info[1] / 1073741824.0
            volume["allocation_gb"] = info[2] / 1073741824.0
            result[pool]["total_capacity_gb"] = result[pool]["total_capacity_gb"] + volume["capacity_gb"]
            result[pool]["volumes"].append(volume)
        

    print(json.dumps(result,indent=4))

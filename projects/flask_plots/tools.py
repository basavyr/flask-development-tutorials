from dataclasses import dataclass
from datetime import datetime

import random


def get_current_time():
    return f'{datetime.utcnow()}'


def get_node_list():
    node_list = [
        (f'node-{idx}', random.choice(['controller', 'compute', 'ceph', 'agent']), f'10.0.1.{idx}') for idx in range(25)]

    return node_list


def get_node_types(node_list):
    node_type_list = []
    idx = 0
    for node_name, node_type, node_ip_addr in node_list:
        if(node_type == 'controller'):
            node_type_list.append(f'ctrl-os-{idx}')
        elif node_type == 'compute':
            node_type_list.append(f'compute-os-{idx}')
        elif node_type == 'ceph':
            node_type_list.append(f'ceph-os-{idx}')
        elif node_type == 'agent':
            node_type_list.append(f'agent-os-{idx}')
        idx = idx + 1

    return node_type_list


def get_openstack_map():
    map_name = 'openstack-01'
    map_id = '#01a'

    return map_name, map_id


def main():
    test_node_list = get_node_list()
    node_types = get_node_types(test_node_list)


if __name__ == '__main__':
    main()

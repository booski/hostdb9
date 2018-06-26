# coding=utf-8

import sys

def read(client, vlans, cnames, print_warnings):
    lines = []
    if cnames:
        for cname in client.list_cnames():
            lines.append('cname\t' + cname['name'])
            lines.append('target\t' + cname['canonical'])
            lines.append('')
    for vlan in client.list_vlans():
        net = vlan['network']
        if net not in vlans:
            continue
        lines.append('')
        lines.append('network\t' + net)
        for ip in client.list_vlan_ips(net):
            types = ip['types']
            addr = ip['ip_address']
            lines.append('')
            if types and 'HOST' not in types:
                lines.append('host\t' + addr + '\t# in use as: '+', '.join(types))
                continue
            lines.append('host\t' + addr)
            names = ip['names']
            name = ''
            extra = ''
            if len(names) > 0:
                name = names[0]
                if len(names) > 1:
                    extra = '\t# additional names: ' + ', '.join(names[1:])
                    if print_warnings:
                        print('Warning! '+ addr + ' has several names. '
                              + 'Adding extra names as file comment.',
                              file=sys.stderr)
            if name:
                append_line = 'name\t' + name
                if extra:
                    append_line += extra
                lines.append(append_line)
                (comment, aliases) = client.get_host_info(name)
                if comment:
                    lines.append('comment\t' + comment)
                for alias in aliases:
                    lines.append('alias\t' + alias)
            mac = ip['mac_address']
            if mac and not name.startswith('dhcp'):
                lines.append('mac\t' + mac)
    return lines

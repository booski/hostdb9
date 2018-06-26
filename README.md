# A CLI client for Infoblox

Depends on: requests

## Installation
* Pull the git repo
* Copy `config.ini.example` to `config.ini` and make necessary changes
* Use the `dump` command to create an initial DNS file. You may want to manually split it into parts.
* Run the `update` command. It should report that everything is in sync.
* Done.

## Usage
### Commands
There are two commands: dump and update

    hostdb dump

This will print the current running DNS configuration to stdout, according to the DNS file format.

    hostdb update

This will read the configuration from the zonefile(s) and the running DNS configuration, calculate changes and try to apply them.

### Switches
Switches are documented in the program itself, please run `hostdb --help` for more information.

## DNS configuration format
In general, the file format consists of lines consisting of a keyword followed by a value. A complete definition of a DNS object will usually require several grouped lines.

The file can contain comments that are ignored by the program. A comment starts with a '#' (hash) character, and ends with a newline.

Whenever a hostname must be specified, a shorthand can be used: All hostnames that do not contain a '.' (period) will automatically get the default domain (as spcified by the `tld` setting in `config.ini`) appended in DNS.

There are also several 'magic' names: `reserved`, `dhcp`, `unused` and `ledig`. All of these will have the host's IP address appended in dash format.

For example:

    host 127.0.0.1
    name reserved

This will result in the DNS name `reserved-127-0-0-1.example.com`, given that you have set `example.com` as your TLD in `config.ini`.

### Networks
A network is defined by one line as follows:

    network 127.0.0.0/24

This would define the localhost network and allow you to define hosts within that network.

All hosts belonging to this network must be defined after this line and before the next network line. Typically you would keep one DNS file per network and begin each file with the network declaration.

### Hosts
A host is defined by one or more lines as follows:

    host    127.0.0.1            # mandatory
    name    myhost.example.com   # mandatory if specifying any further lines
    mac     aa:bb:cc:dd:ee:ff    # optional
    comment An example host      # optional
    alias   myalias.example.com  # optional

All hosts must be defined as part of a network (see above), and the first line of the group must always be a `host` line.

### CNAMEs
A CNAME record is defined by two configuration lines:

    cname  alias.example.com
    target canonical.example.com

This would create the CNAME alias.example.com, pointing at canonical.example.com.

The `cname` line must precede the `target` line. CNAMEs are independent of networks.

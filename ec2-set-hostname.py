#!/usr/bin/python
#
#    Set up the hostname for ec2.
#    Copyright 2008 Canonical Ltd.
#
#    Author: Chuck Short <chuck.short@canonical.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import urllib
import os
from Cheetah.Template import Template

api_ver = '2008-02-01'
metadata = None

def get_ami_id():
    api_ver = '2008-02-01'
    metadata = None

    url = 'http://169.254.169.254/%s/meta-data' % api_ver
    ami_id = urllib.urlopen('%s/ami-id/' %url).read()
    return ami_id

def set_hostname(filename):
    api_ver = '2008-02-01'
    metadata = None

    base_url = 'http://169.254.169.254/%s/meta-data' % api_ver
    my_hostname = urllib.urlopen('%s/local-hostname/' % base_url).read()
    os.system('hostname %s' % my_hostname)

    # replace the ubuntu hostname in /etc/hosts
    mp = {'hostname': my_hostname}
    t = Template(file="/etc/ec2-init/templates/hosts.tmpl", searchList=[mp])

    os.system("rm  /etc/hosts")
    f = open("/etc/hosts", "w")
    f.write('%s' %(t))
    f.close()
    os.system('touch %s' %(filename))

id = get_ami_id()
filename = '/var/ec2/.hostname-already-ran.%s' %id
if os.path.exists(filename):
   print "Hostname already set previously....skipping!"
else:
   set_hostname(filename)

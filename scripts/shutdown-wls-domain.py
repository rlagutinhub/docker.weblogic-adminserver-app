#!/usr/bin/env python
# -*- coding: UTF-8 -*-
  
# NAME:   SHUTDOWN-WLS-DOMAIN.PY
# DESC:   SHUTDOWN WLS DOMAIN
# DATE:   07-10-2019
# LANG:   PYTHON WLST
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU

import os
import sys
import time
import getopt


libraries_file = os.environ.get('SCRIPTS_DIR', '') + '/libraries.py'
sys.path.append(os.path.dirname(os.path.expanduser(libraries_file)))


import libraries as lib


domain_name                 = DOMAIN_NAME
admin_name                  = ADMIN_NAME
admin_listen_port           = int(ADMIN_LISTEN_PORT)
production_mode             = PRODUCTION_MODE
administration_port_enabled = ADMINISTRATION_PORT_ENABLED
administration_port         = int(ADMINISTRATION_PORT)
username                    = username
password                    = password

domain_path                 = '/u01/oracle/user_projects/domains/%s' % domain_name


def main():

    # admin_url = 't3://localhost:' + str(ADMIN_LISTEN_PORT)
    if ADMINISTRATION_PORT_ENABLED == 'false':
        admin_url = 't3://localhost:' + str(ADMIN_LISTEN_PORT)
    
    else:
        admin_url = 't3s://localhost:' + str(ADMINISTRATION_PORT)

    print('domain_name                 : [%s]' % domain_name)
    print('admin name                  : [%s]' % admin_name)
    print('admin_listen_port           : [%s]' % admin_listen_port)
    print('production_mode             : [%s]' % production_mode)
    print('administration_port_enabled : [%s]' % administration_port_enabled)
    print('administration_port         : [%s]' % administration_port)
    print('domain_path                 : [%s]' % domain_path)
    print('admin_url                   : [%s]' % admin_url)
    print('username                    : [%s]' % username)
    print('password                    : [%s]' % password)

    lib.check_value(domain_name, "domain_name")
    lib.check_value(admin_name, "admin_name")
    lib.check_value(admin_listen_port, "admin_listen_port")
    lib.check_value(production_mode, "production_mode")
    lib.check_value(administration_port_enabled, "administration_port_enabled")
    lib.check_value(administration_port, "administration_port")
    lib.check_value(domain_path, "domain_path")
    lib.check_value(admin_url, "admin_url")
    lib.check_value(username, "username")
    lib.check_value(password, "password")

    try:

        # WLST Offline - AdministrationPort disable
        # if lib.check_bool(administration_port_enabled):
            # readDomain(domain_path)
            # cd('/')
            # cmo.setAdministrationPortEnabled(false)
            # # cmo.setAdministrationPortEnabled(true)
            # updateDomain()
            # closeDomain()

        connect(username, password, admin_url, adminServerName=admin_name)
        shutdown('AdminServer','Server', ignoreSessions='true')
        disconnect()

        # WLST Offline - AdministrationPort enable
        # if lib.check_bool(administration_port_enabled):
            # readDomain(domain_path)
            # cd('/')
            # # cmo.setAdministrationPortEnabled(false)
            # cmo.setAdministrationPortEnabled(true)
            # updateDomain()
            # closeDomain()

    except Exception, ex:
        # print ex.toString()
        print('Error: %s' % ex)
        dumpStack()
        cancelEdit('y')
        sys.exit(1)


if __name__ != '__main__':
    main()

elif __name__ == '__main__':
    print('This script has to be executed with weblogic WLST')

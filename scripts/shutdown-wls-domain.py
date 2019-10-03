#!/usr/bin/env python
# -*- coding: UTF-8 -*-
  
# NAME:   SHUTDOWN-WLS-DOMAIN.PY
# DESC:   SHUTDOWN WLS DOMAIN
# DATE:   08-09-2019
# LANG:   PYTHON WLST
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU

import os
import sys


domain_name                 = DOMAIN_NAME
admin_name                  = ADMIN_NAME
admin_listen_port           = int(ADMIN_LISTEN_PORT)
production_mode             = PRODUCTION_MODE
administration_port_enabled = ADMINISTRATION_PORT_ENABLED
administration_port         = int(ADMINISTRATION_PORT)
username                    = username
password                    = password

domain_path                 = '/u01/oracle/user_projects/domains/%s' % domain_name


def check_value(value, name):

    check_value = True
    try:
        if len(str(value)) == 0:
            check_value = False
    except:
        check_value = False

    if not check_value:
        print('Error: The parameter [%s] is not set! Exit!' % name)
        sys.exit(1)

def check_bool(value):

    if value is True or value is False:
        return value

    value = str(value).strip().lower()
    return not value in ['false','f','null','n','0','']

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

    check_value(domain_name, "domain_name")
    check_value(admin_name, "admin_name")
    check_value(admin_listen_port, "admin_listen_port")
    check_value(production_mode, "production_mode")
    check_value(administration_port_enabled, "administration_port_enabled")
    check_value(administration_port, "administration_port")
    check_value(domain_path, "domain_path")
    check_value(admin_url, "admin_url")
    check_value(username, "username")
    check_value(password, "password")

    try:

        # WLST Offline - AdministrationPort disable
        # if check_bool(administration_port_enabled):
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
        # if check_bool(administration_port_enabled):
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

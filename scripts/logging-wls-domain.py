#!/usr/bin/env python
# -*- coding: UTF-8 -*-
  
# NAME:   LOGGING-WLS-DOMAIN.PY
# DESC:   MODIFY WLS LOGGING AND ADD CONTAINER ID
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

# Const
KEYS_VALUE = 'keys'
SECTION_VALUE = 'Logging'


def main():
  
    admin_url = 't3://localhost:' + str(ADMIN_LISTEN_PORT)
    # if ADMINISTRATION_PORT_ENABLED == 'false':
    #     admin_url = 't3://localhost:' + str(ADMIN_LISTEN_PORT)
    #
    # else:
    #     admin_url = 't3s://localhost:' + str(ADMINISTRATION_PORT)

    cid = False
    properties = False
  
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:c:', ['properties=','cid='])
  
    except getopt.GetoptError:
        pass
  
    # print('argv: ', sys.argv[1:])
    # print('opts: ', opts)
  
    try:
        for opt, arg in opts:
            if opt in ('-p', '--properties'):
                if os.path.isfile(arg):
                    properties = arg
 
            elif opt in ('-c', '--cid'):
                cid = arg
  
    except NameError:
        pass
  
    if not cid or not properties:
        print('modify-wls-domain.py -p <path-to-properties-file> -c 123456789abc')
        sys.exit(1)
  
    # print('properties:', properties)
    # print('cid       :', cid)
  
    print('domain_name                      : [%s]' % domain_name)
    print('admin name                       : [%s]' % admin_name)
    print('admin_listen_port                : [%s]' % admin_listen_port)
    print('production_mode                  : [%s]' % production_mode)
    print('administration_port_enabled      : [%s]' % administration_port_enabled)
    print('administration_port              : [%s]' % administration_port)
    print('domain_path                      : [%s]' % domain_path)
    print('admin_url                        : [%s]' % admin_url)
    print('username                         : [%s]' % username)
    print('password                         : [%s]' % password)
    print('properties                       : [%s]' % properties)
    print('cid                              : [%s]' % cid)
  
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
    lib.check_value(properties, "properties")
    lib.check_value(cid, "cid")

    pars = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE)
    settings = pars.settings

    if not settings:
        print('Error: %s' % settings)
        sys.exit(1)

    try:

        # WLST Offline - AdministrationPort disable
        if lib.check_bool(administration_port_enabled):
            readDomain(domain_path)
            cd('/')
            cmo.setAdministrationPortEnabled(false)
            # cmo.setAdministrationPortEnabled(true)
            updateDomain()
            closeDomain()

        # WLST Online - Modify logging settings
        startServer(adminServerName=admin_name,
                domainName=domain_name,
                url=admin_url,
                username=username,
                password=password,
                domainDir=domain_path,
                jvmArgs='-Xms512m -Xmx512m')

        connect(username, password, admin_url)

        edit()
        startEdit()

        # print('Disable Admin Console')
        # cd('/')
        # cmo.setConsoleEnabled(false)

        for key in settings:

            log_path = settings[key]['path']
            log_file = settings[key]['file']
            log_fileMinSize = settings[key]['fileMinSize']
            log_fileCount = settings[key]['fileCount']
            log_rotateLogOnStartup = settings[key]['rotateLogOnStartup']

            print('log_path                        : [%s]' % log_path)
            print('log_file                        : [%s]' % log_file)
            print('log_fileMinSize                 : [%s]' % log_fileMinSize)
            print('log_fileCount                   : [%s]' % log_fileCount)
            print('log_rotateLogOnStartup          : [%s]' % log_rotateLogOnStartup)

            lib.check_value(log_path, "log_path")
            lib.check_value(log_file, "log_file")
            lib.check_value(log_fileMinSize, "log_fileMinSize")
            lib.check_value(log_fileCount, "log_fileCount")
            lib.check_value(log_rotateLogOnStartup, "log_rotateLogOnStartup")

            if key == 'domain':
                if log_path.lower() != ('/Log/' + domain_name).lower():
                    print('Error: The parameter [log.domain.path=%s] is incorrect! Exit!' % log_path)
                    sys.exit(1)

            if key == 'diagnostic':
                log_file = log_file + '-' + str(cid)

            else:
                log_file = log_file.replace('.log', '-' + str(cid) + ".log")

            print('Setup logging                   : [%s]' % log_file)

            if key == 'diagnostic':
                cd(log_path)
                cmo.setImageDir(str(log_file))
                # cmo.setImageTimeout(int(log_timeout))

            else:
                cd(log_path)
                cmo.setFileName(str(log_file))
                cmo.setRotateLogOnStartup(lib.check_bool(log_rotateLogOnStartup))
                cmo.setFileCount(int(log_fileCount))
                cmo.setFileMinSize(int(log_fileMinSize))
    
        save()
        activate(block = 'true')
        shutdown(block = 'true')
        disconnect()

        # WLST Offline - AdministrationPort enable
        if lib.check_bool(administration_port_enabled):
            readDomain(domain_path)
            cd('/')
            # cmo.setAdministrationPortEnabled(false)
            cmo.setAdministrationPortEnabled(true)
            updateDomain()
            closeDomain()

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

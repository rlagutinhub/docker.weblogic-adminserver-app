#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# NAME:   DEPLOYMENTS-WLS-DOMAIN.PY
# DESC:   DEPLOY WLS APP
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
SECTION_VALUE_BASE = 'Base'
SECTION_VALUE_SEC = 'Security'
SECTION_VALUE_DEPLOY = 'Deployments'


def main():

    admin_url = 't3://localhost:' + str(ADMIN_LISTEN_PORT)
    # if ADMINISTRATION_PORT_ENABLED == 'false':
    #     admin_url = 't3://localhost:' + str(ADMIN_LISTEN_PORT)
    #
    # else:
    #     admin_url = 't3://localhost:' + str(ADMINISTRATION_PORT)

    mode = False
    properties = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:m:', ['properties=','mode='])

    except getopt.GetoptError:
        pass

    # print('argv: ', sys.argv[1:])
    # print('opts: ', opts)

    try:
        for opt, arg in opts:
            if opt in ('-p', '--properties'):
                if os.path.isfile(arg):
                    properties = arg

            elif opt in ('-m', '--mode'):
                mode = arg

    except NameError:
        pass

    if not properties or not mode in ('offline', 'online'):
        print('modify-wls-domain.py -p <path-to-properties-file> -m [offline|online]')
        sys.exit(1)

    # print('properties:', properties)
    # print('mode      :', mode)

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

    pars = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE)
    settings = pars.settings

    if not settings:
        print('Error: %s' % settings)
        sys.exit(1)

    try:
        if mode == 'offline':

            readDomain(domain_path)

            for key in settings:

                app_name = settings[key]['name']
                app_type = settings[key]['type']
                app_sourcePath = settings[key]['sourcePath']
                app_securityDDModel = settings[key]['securityDDModel']

                print('app_name                         : [%s]' % app_name)
                print('app_type                         : [%s]' % app_type)
                print('app_sourcePath                   : [%s]' % app_sourcePath)
                print('app_securityDDModel              : [%s]' % app_securityDDModel)

                lib.check_value(app_name, "app_name")
                lib.check_value(app_type, "app_type")
                lib.check_value(app_sourcePath, "app_sourcePath")
                lib.check_value(app_securityDDModel, "app_securityDDModel")

                if not os.path.isfile(app_sourcePath):
                    print('Error: not found %s' % app_sourcePath)
                    sys.exit(1)

                print('Offline deploy application       : [%s]' % app_name)

                cd('/')
                app = create(app_name, app_type)
                app.setSourcePath(app_sourcePath)
                app.setSecurityDDModel(app_securityDDModel)
                app.setStagingMode('nostage')

            assign(app_type, app_name, 'Target', admin_name)
            # assign(app_type, app_name, 'Target', cluster_name)

            updateDomain()
            closeDomain()

        if mode == 'online':

            # WLST Offline - AdministrationPort disable
            if lib.check_bool(administration_port_enabled):
                readDomain(domain_path)
                cd('/')
                cmo.setAdministrationPortEnabled(false)
                # cmo.setAdministrationPortEnabled(true)
                updateDomain()
                closeDomain()

            # WLST Online - Deploy application
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


            for key in settings:

                app_name = settings[key]['name']
                app_type = settings[key]['type']
                app_sourcePath = settings[key]['sourcePath']
                app_securityDDModel = settings[key]['securityDDModel']

                print('app_name                         : [%s]' % app_name)
                print('app_type                         : [%s]' % app_type)
                print('app_sourcePath                   : [%s]' % app_sourcePath)
                print('app_securityDDModel              : [%s]' % app_securityDDModel)

                lib.check_value(app_name, "app_name")
                lib.check_value(app_type, "app_type")
                lib.check_value(app_sourcePath, "app_sourcePath")
                lib.check_value(app_securityDDModel, "app_securityDDModel")

                if not os.path.isfile(app_sourcePath):
                    print('Error: not found %s' % app_sourcePath)
                    sys.exit(1)

                print('Online deploy application        : [%s]' % app_name)

                progress = deploy(app_name, app_sourcePath, stageMode='nostage', securityModel=app_securityDDModel, upload='true')
                progress.printStatus()

            save()
            activate(block='true')
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

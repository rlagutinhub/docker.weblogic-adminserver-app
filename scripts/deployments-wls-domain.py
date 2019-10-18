#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# NAME:   DEPLOYMENTS-WLS-DOMAIN.PY
# DESC:   DEPLOY WLS APP
# DATE:   11-10-2019
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


# Const
KEYS_VALUE = 'keys'
SECTION_VALUE_BASE = 'Base'
SECTION_VALUE_SEC = 'Security'
SECTION_VALUE_DEP = 'Deployments'


def main():

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

    pars_base = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE_BASE)
    settings_base = pars_base.settings

    if not settings_base:
        print('Error: %s' % settings_base)
        sys.exit(1)

    for key in settings_base:

        domain_name = settings_base[key]['domain_name']
        admin_name = settings_base[key]['admin_name']
        admin_listen_port = int(settings_base[key]['admin_listen_port'])
        production_mode = settings_base[key]['production_mode']
        administration_port_enabled = settings_base[key]['administration_port_enabled']
        administration_port = int(settings_base[key]['administration_port'])
        admin_console_enabled = settings_base[key]['admin_console_enabled']

    pars_sec = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE_SEC)
    settings_sec = pars_sec.settings

    if not settings_sec:
        print('Error: %s' % settings_sec)
        sys.exit(1)

    for key in settings_sec:

        username = settings_sec[key]['username']
        password = settings_sec[key]['password']

    domain_path = '/u01/oracle/user_projects/domains/%s' % domain_name
    # domain_template = '/u01/oracle/wlserver/common/templates/wls/wls.jar'

    print(lib.bcolors.BOLD + 'domain_name                                : [%s]' % domain_name + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'admin_name                                 : [%s]' % admin_name + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'admin_listen_port                          : [%s]' % admin_listen_port + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'production_mode                            : [%s]' % production_mode + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'administration_port_enabled                : [%s]' % administration_port_enabled + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'administration_port                        : [%s]' % administration_port + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'admin_console_enabled                      : [%s]' % admin_console_enabled + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'username                                   : [%s]' % "******" + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'password                                   : [%s]' % "******" + lib.bcolors.ENDC)
    print(lib.bcolors.BOLD + 'domain_path                                : [%s]' % domain_path + lib.bcolors.ENDC)
    # print(lib.bcolors.BOLD + 'domain_template                            : [%s]' % domain_template + lib.bcolors.ENDC)

    lib.check_value(domain_name, "domain_name")
    lib.check_value(admin_name, "admin_name")
    lib.check_value(admin_listen_port, "admin_listen_port")
    lib.check_value(production_mode, "production_mode")
    lib.check_value(administration_port_enabled, "administration_port_enabled")
    lib.check_value(administration_port, "administration_port")
    lib.check_value(admin_console_enabled, "admin_console_enabled")
    lib.check_value(username, "username")
    lib.check_value(password, "password")
    lib.check_value(domain_path, "domain_path")
    # lib.check_value(domain_template, "domain_template")

    admin_url = 't3://localhost:' + str(admin_listen_port)
    # if administration_port_enabled == 'false':
    #     admin_url = 't3://localhost:' + str(admin_listen_port)
    # else:
    #     admin_url = 't3s://localhost:' + str(administration_port)

    pars_dep = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE_DEP)
    settings_dep = pars_dep.settings

    if not settings_dep:
        print('Error: %s' % settings_dep)
        sys.exit(1)

    try:
        if mode == 'offline':

            readDomain(domain_path)

            for key in settings_dep:

                app_name = settings_dep[key]['name']
                app_type = settings_dep[key]['type']
                app_sourcePath = settings_dep[key]['sourcePath']
                app_securityDDModel = settings_dep[key]['securityDDModel']

                print(lib.bcolors.BOLD + 'app_name                                   : [%s]' % app_name + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'app_type                                   : [%s]' % app_type + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'app_sourcePath                             : [%s]' % app_sourcePath + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'app_securityDDModel                        : [%s]' % app_securityDDModel + lib.bcolors.ENDC)

                lib.check_value(app_name, "app_name")
                lib.check_value(app_type, "app_type")
                lib.check_value(app_sourcePath, "app_sourcePath")
                lib.check_value(app_securityDDModel, "app_securityDDModel")

                if not os.path.isfile(app_sourcePath):
                    print('Error: not found %s' % app_sourcePath)
                    sys.exit(1)

                print(lib.bcolors.WARNING + 'Offline deploy application                 : [%s]' % app_name + lib.bcolors.ENDC)

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


            for key in settings_dep:

                app_name = settings_dep[key]['name']
                app_type = settings_dep[key]['type']
                app_sourcePath = settings_dep[key]['sourcePath']
                app_securityDDModel = settings_dep[key]['securityDDModel']

                print(lib.bcolors.BOLD + 'app_name                                   : [%s]' % app_name + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'app_type                                   : [%s]' % app_type + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'app_sourcePath                             : [%s]' % app_sourcePath + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'app_securityDDModel                        : [%s]' % app_securityDDModel + lib.bcolors.ENDC)

                lib.check_value(app_name, "app_name")
                lib.check_value(app_type, "app_type")
                lib.check_value(app_sourcePath, "app_sourcePath")
                lib.check_value(app_securityDDModel, "app_securityDDModel")

                if not os.path.isfile(app_sourcePath):
                    print('Error: not found %s' % app_sourcePath)
                    sys.exit(1)

                print(lib.bcolors.WARNING + 'Online deploy application                  : [%s]' % app_name + lib.bcolors.ENDC)

                if str(app_type).lower() == 'library':
                    progress = deploy(app_name, app_sourcePath, stageMode='nostage', libraryModule='true', securityModel=app_securityDDModel, upload='true')
                    progress.printStatus()
                
                else:
                    progress = deploy(app_name, app_sourcePath, stageMode='nostage', libraryModule='false', securityModel=app_securityDDModel, upload='true')
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

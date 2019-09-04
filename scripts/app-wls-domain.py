#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# NAME:   APP-WLS-DOMAIN.PY
# DESC:   DEPLOY WLS APP
# DATE:   31-08-2019
# LANG:   PYTHON WLST
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU

import os
import sys
import time
import getopt

from java.io import FileInputStream


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
    return not value in ['false','f','n','0','']

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

    propInputStream = FileInputStream(properties)
    configProps = Properties()
    configProps.load(propInputStream)

    app_name=configProps.get("app.name")
    app_path=configProps.get("app.path")
    app_file=configProps.get("app.file")

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
    print('app_name                         : [%s]' % app_name)
    print('app_path                         : [%s]' % app_path)
    print('app_file                         : [%s]' % app_file)

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
    check_value(properties, "properties")

    check_value(app_name, "app_name")
    check_value(app_path, "app_path")
    check_value(app_file, "app_file")

    if not os.path.isfile(app_path + '/' + app_file):
        print('Error: not found %s' % app_path + '/' + app_file)
        sys.exit(1)

    try:
        if mode == 'offline':
            # WLST Offline - Deploy application
            print('Offline deploy application       : [%s]' % app_name)
            readDomain(domain_path)

            cd('/')
            app = create(app_name, 'AppDeployment')
            app.setSourcePath(app_path + '/' + app_file)
            app.setStagingMode('nostage')

            assign('AppDeployment', app_name, 'Target', admin_name)
            # assign('AppDeployment', app_name, 'Target', cluster_name)

            updateDomain()
            closeDomain()

        if mode == 'online':
            # WLST Online - Deploy application
            print('Online deploy application        : [%s]' % app_name)
            # WLST Offline - AdministrationPort disable
            if check_bool(administration_port_enabled):
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
                    jvmArgs='-Xms512m -Xmx512m -XX:PermSize=256m -XX:MaxPermSize=256m')

            connect(username, password, admin_url)

            edit()
            startEdit()

            progress = deploy(app_name, app_path + '/' + app_file, stageMode='nostage', upload='true')
            progress.printStatus()

            save()
            activate(20000,block='true')
            shutdown(block = 'true')
            disconnect()

            # WLST Offline - AdministrationPort enable
            if check_bool(administration_port_enabled):
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

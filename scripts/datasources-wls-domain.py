#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# NAME:   DATASOURCES-WLS-DOMAIN.PY
# DESC:   CREATE WLS DATASOURCES
# DATE:   18-10-2019
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
SECTION_VALUE_DS = 'DataSources'


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

    pars_ds = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE_DS)
    settings_ds = pars_ds.settings

    if not settings_ds:
        print('Error: %s' % settings_ds)
        sys.exit(1)

    try:
        if mode == 'offline':

            readDomain(domain_path)

            for key in settings_ds:

                ds_url = settings_ds[key]['url']
                ds_user = settings_ds[key]['user']
                ds_password = settings_ds[key]['password']
                ds_Name = settings_ds[key]['Name']
                ds_jndiName = settings_ds[key]['jndiName']
                ds_GlobalTransactionsProtocol = settings_ds[key]['GlobalTransactionsProtocol']
                ds_driver = settings_ds[key]['driver']
                ds_MaxCapacity = settings_ds[key]['MaxCapacity']
                ds_ConnectionCreationRetryFrequencySeconds = settings_ds[key]['ConnectionCreationRetryFrequencySeconds']
                ds_TestTableName = settings_ds[key]['TestTableName']
                ds_XaSetTransactionTimeout = settings_ds[key]['XaSetTransactionTimeout']
                ds_XaTransactionTimeout = settings_ds[key]['XaTransactionTimeout']

                print(lib.bcolors.BOLD + 'ds_url                                     : [%s]' % ds_url + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_user                                    : [%s]' % "******" + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_password                                : [%s]' % "******" + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_Name                                    : [%s]' % ds_Name + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_jndiName                                : [%s]' % ds_jndiName + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_GlobalTransactionsProtocol              : [%s]' % ds_GlobalTransactionsProtocol + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_driver                                  : [%s]' % ds_driver + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_MaxCapacity                             : [%s]' % ds_MaxCapacity + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_ConnectionCreationRetryFrequencySeconds : [%s]' % ds_ConnectionCreationRetryFrequencySeconds + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_TestTableName                           : [%s]' % ds_TestTableName + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_XaSetTransactionTimeout                 : [%s]' % ds_XaSetTransactionTimeout + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_XaTransactionTimeout                    : [%s]' % ds_XaTransactionTimeout + lib.bcolors.ENDC)

                lib.check_value(ds_url, "ds_url")
                lib.check_value(ds_user, "ds_user")
                lib.check_value(ds_password, "ds_password")
                lib.check_value(ds_Name, "ds_Name")
                lib.check_value(ds_jndiName, "ds_jndiName")
                lib.check_value(ds_GlobalTransactionsProtocol, "ds_GlobalTransactionsProtocol")
                lib.check_value(ds_driver, "ds_driver")
                lib.check_value(ds_MaxCapacity, "ds_MaxCapacity")
                lib.check_value(ds_ConnectionCreationRetryFrequencySeconds, "ds_ConnectionCreationRetryFrequencySeconds")
                lib.check_value(ds_TestTableName, "ds_TestTableName")
                lib.check_value(ds_XaSetTransactionTimeout, "ds_XaSetTransactionTimeout")
                lib.check_value(ds_XaTransactionTimeout, "ds_XaTransactionTimeout")

                print(lib.bcolors.WARNING + 'Offline create datasource                  : [%s]' % ds_Name + lib.bcolors.ENDC)

                cd('/')
                create(ds_Name, 'JDBCSystemResource')

                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
                set('Name', ds_Name)

                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
                create(ds_Name + '_ds_params', 'JDBCDataSourceParams')

                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCDataSourceParams/' + 'NO_NAME_0')
                set('JNDIName', ds_jndiName)

                if lib.check_bool(ds_GlobalTransactionsProtocol):
                    cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCDataSourceParams/' + 'NO_NAME_0')
                    set('GlobalTransactionsProtocol', ds_GlobalTransactionsProtocol)

                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
                create(ds_Name + '_driver_params', 'JDBCDriverParams')
                
                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCDriverParams/' + 'NO_NAME_0')
                set('URL', ds_url)
                set('DriverName', ds_driver)
                set('PasswordEncrypted', ds_password)

                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCDriverParams/' + 'NO_NAME_0')
                create(ds_Name + '_driver_props', 'Properties')

                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCDriverParams/' + 'NO_NAME_0' + '/Properties/' + 'NO_NAME_0')
                create('user', 'Property')

                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCDriverParams/' + 'NO_NAME_0' + '/Properties/' + 'NO_NAME_0' + '/Property/' + 'user')
                set('Value', ds_user)

                if lib.check_bool(ds_TestTableName) or lib.check_bool(ds_MaxCapacity) or lib.check_bool(ds_ConnectionCreationRetryFrequencySeconds):
                    cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
                    create(ds_Name + '_conn_pool_params', 'JDBCConnectionPoolParams')

                if lib.check_bool(ds_TestTableName):
                    cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCConnectionPoolParams/' + 'NO_NAME_0')
                    set('TestTableName', ds_TestTableName)

                if lib.check_bool(ds_MaxCapacity):
                    cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCConnectionPoolParams/' + 'NO_NAME_0')
                    set('MaxCapacity', int(ds_MaxCapacity))

                if lib.check_bool(ds_ConnectionCreationRetryFrequencySeconds):
                    cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCConnectionPoolParams/' + 'NO_NAME_0')
                    set('ConnectionCreationRetryFrequencySeconds', int(ds_ConnectionCreationRetryFrequencySeconds))

                if lib.check_bool(ds_XaSetTransactionTimeout) or lib.check_bool(ds_XaTransactionTimeout):
                    cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
                    create(ds_Name + '_xa_params', 'JDBCXAParams')

                if lib.check_bool(ds_XaSetTransactionTimeout):
                    cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCXAParams/' + 'NO_NAME_0')
                    set('XaSetTransactionTimeout', ds_XaSetTransactionTimeout)

                if lib.check_bool(ds_XaTransactionTimeout):
                    cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCXAParams/' + 'NO_NAME_0')
                    set('XaTransactionTimeout', int(ds_XaTransactionTimeout))

                assign('JDBCSystemResource', ds_Name, 'Target', admin_name)

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

            for key in settings_ds:

                ds_url = settings_ds[key]['url']
                ds_user = settings_ds[key]['user']
                ds_password = settings_ds[key]['password']
                ds_Name = settings_ds[key]['Name']
                ds_jndiName = settings_ds[key]['jndiName']
                ds_GlobalTransactionsProtocol = settings_ds[key]['GlobalTransactionsProtocol']
                ds_driver = settings_ds[key]['driver']
                ds_MaxCapacity = settings_ds[key]['MaxCapacity']
                ds_ConnectionCreationRetryFrequencySeconds = settings_ds[key]['ConnectionCreationRetryFrequencySeconds']
                ds_TestTableName = settings_ds[key]['TestTableName']
                ds_XaSetTransactionTimeout = settings_ds[key]['XaSetTransactionTimeout']
                ds_XaTransactionTimeout = settings_ds[key]['XaTransactionTimeout']

                print(lib.bcolors.BOLD + 'ds_url                                     : [%s]' % ds_url + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_user                                    : [%s]' % "******" + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_password                                : [%s]' % "******" + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_Name                                    : [%s]' % ds_Name + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_jndiName                                : [%s]' % ds_jndiName + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_GlobalTransactionsProtocol              : [%s]' % ds_GlobalTransactionsProtocol + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_driver                                  : [%s]' % ds_driver + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_MaxCapacity                             : [%s]' % ds_MaxCapacity + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_ConnectionCreationRetryFrequencySeconds : [%s]' % ds_ConnectionCreationRetryFrequencySeconds + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_TestTableName                           : [%s]' % ds_TestTableName + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_XaSetTransactionTimeout                 : [%s]' % ds_XaSetTransactionTimeout + lib.bcolors.ENDC)
                print(lib.bcolors.BOLD + 'ds_XaTransactionTimeout                    : [%s]' % ds_XaTransactionTimeout + lib.bcolors.ENDC)

                lib.check_value(ds_url, "ds_url")
                lib.check_value(ds_user, "ds_user")
                lib.check_value(ds_password, "ds_password")
                lib.check_value(ds_Name, "ds_Name")
                lib.check_value(ds_jndiName, "ds_jndiName")
                lib.check_value(ds_GlobalTransactionsProtocol, "ds_GlobalTransactionsProtocol")
                lib.check_value(ds_driver, "ds_driver")
                lib.check_value(ds_MaxCapacity, "ds_MaxCapacity")
                lib.check_value(ds_ConnectionCreationRetryFrequencySeconds, "ds_ConnectionCreationRetryFrequencySeconds")
                lib.check_value(ds_TestTableName, "ds_TestTableName")
                lib.check_value(ds_XaSetTransactionTimeout, "ds_XaSetTransactionTimeout")
                lib.check_value(ds_XaTransactionTimeout, "ds_XaTransactionTimeout")

                print(lib.bcolors.WARNING + 'Online create datasource                   : [%s]' % ds_Name + lib.bcolors.ENDC)

                cd('/')
                cmo.createJDBCSystemResource(ds_Name)

                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name)
                cmo.setName(ds_Name)

                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCDataSourceParams/' + ds_Name)
                cmo.setJNDINames(jarray.array([String(ds_jndiName)], String))

                if lib.check_bool(ds_GlobalTransactionsProtocol):
                    cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCDataSourceParams/' + ds_Name)
                    cmo.setGlobalTransactionsProtocol(ds_GlobalTransactionsProtocol)

                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCDriverParams/' + ds_Name)
                cmo.setUrl(ds_url)
                cmo.setDriverName(ds_driver)
                cmo.setPassword(ds_password)

                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCDriverParams/' + ds_Name + '/Properties/' + ds_Name)
                cmo.createProperty('user')

                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCDriverParams/' + ds_Name + '/Properties/' + ds_Name + '/Properties/user')
                cmo.setValue(ds_user)

                if lib.check_bool(ds_TestTableName):
                    cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCConnectionPoolParams/' + ds_Name)
                    cmo.setTestTableName(ds_TestTableName)

                if lib.check_bool(ds_MaxCapacity):
                    cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCConnectionPoolParams/' + ds_Name)
                    cmo.setMaxCapacity(int(ds_MaxCapacity))

                if lib.check_bool(ds_ConnectionCreationRetryFrequencySeconds):
                    cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCConnectionPoolParams/' + ds_Name)
                    cmo.setConnectionCreationRetryFrequencySeconds(int(ds_ConnectionCreationRetryFrequencySeconds))

                if lib.check_bool(ds_XaSetTransactionTimeout):
                    cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCXAParams/' + ds_Name)
                    cmo.setXaSetTransactionTimeout(True)

                if lib.check_bool(ds_XaTransactionTimeout):
                    cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCXAParams/' + ds_Name)
                    cmo.setXaTransactionTimeout(int(ds_XaTransactionTimeout))

                cd('/SystemResources/' + ds_Name)
                # set('Targets',jarray.array([ObjectName('com.bea:Name=' + cluster_name + ',Type=Cluster')], ObjectName))
                set('Targets',jarray.array([ObjectName('com.bea:Name=' + admin_name + ',Type=Server')], ObjectName))

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

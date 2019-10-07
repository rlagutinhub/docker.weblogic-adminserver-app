#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# NAME:   DATASOURCES-WLS-DOMAIN.PY
# DESC:   CREATE WLS DATASOURCES
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
SECTION_VALUE = 'DataSources'


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

    print('domain_name                                : [%s]' % domain_name)
    print('admin name                                 : [%s]' % admin_name)
    print('admin_listen_port                          : [%s]' % admin_listen_port)
    print('production_mode                            : [%s]' % production_mode)
    print('administration_port_enabled                : [%s]' % administration_port_enabled)
    print('administration_port                        : [%s]' % administration_port)
    print('domain_path                                : [%s]' % domain_path)
    print('admin_url                                  : [%s]' % admin_url)
    print('username                                   : [%s]' % username)
    print('password                                   : [%s]' % password)
    print('properties                                 : [%s]' % properties)

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

                ds_url = settings[key]['url']
                ds_user = settings[key]['user']
                ds_password = settings[key]['password']
                ds_Name = settings[key]['Name']
                ds_jndiName = settings[key]['jndiName']
                ds_GlobalTransactionsProtocol = settings[key]['GlobalTransactionsProtocol']
                ds_driver = settings[key]['driver']
                ds_MaxCapacity = settings[key]['MaxCapacity']
                ds_ConnectionCreationRetryFrequencySeconds = settings[key]['ConnectionCreationRetryFrequencySeconds']
                ds_TestTableName = settings[key]['TestTableName']
                ds_XaSetTransactionTimeout = settings[key]['XaSetTransactionTimeout']
                ds_XaTransactionTimeout = settings[key]['XaTransactionTimeout']

                print('ds_url                                     : [%s]' % ds_url)
                print('ds_user                                    : [%s]' % ds_user)
                print('ds_password                                : [%s]' % ds_password)
                print('ds_Name                                    : [%s]' % ds_Name)
                print('ds_jndiName                                : [%s]' % ds_jndiName)
                print('ds_GlobalTransactionsProtocol              : [%s]' % ds_GlobalTransactionsProtocol)
                print('ds_driver                                  : [%s]' % ds_driver)
                print('ds_MaxCapacity                             : [%s]' % ds_MaxCapacity)
                print('ds_ConnectionCreationRetryFrequencySeconds : [%s]' % ds_ConnectionCreationRetryFrequencySeconds)
                print('ds_TestTableName                           : [%s]' % ds_TestTableName)
                print('ds_XaSetTransactionTimeout                 : [%s]' % ds_XaSetTransactionTimeout)
                print('ds_XaTransactionTimeout                    : [%s]' % ds_XaTransactionTimeout)

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

                print('Offline create datasource                  : [%s]' % ds_Name)

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

            for key in settings:

                ds_url = settings[key]['url']
                ds_user = settings[key]['user']
                ds_password = settings[key]['password']
                ds_Name = settings[key]['Name']
                ds_jndiName = settings[key]['jndiName']
                ds_GlobalTransactionsProtocol = settings[key]['GlobalTransactionsProtocol']
                ds_driver = settings[key]['driver']
                ds_MaxCapacity = settings[key]['MaxCapacity']
                ds_ConnectionCreationRetryFrequencySeconds = settings[key]['ConnectionCreationRetryFrequencySeconds']
                ds_TestTableName = settings[key]['TestTableName']
                ds_XaSetTransactionTimeout = settings[key]['XaSetTransactionTimeout']
                ds_XaTransactionTimeout = settings[key]['XaTransactionTimeout']

                print('ds_url                                     : [%s]' % ds_url)
                print('ds_user                                    : [%s]' % ds_user)
                print('ds_password                                : [%s]' % ds_password)
                print('ds_Name                                    : [%s]' % ds_Name)
                print('ds_jndiName                                : [%s]' % ds_jndiName)
                print('ds_GlobalTransactionsProtocol              : [%s]' % ds_GlobalTransactionsProtocol)
                print('ds_driver                                  : [%s]' % ds_driver)
                print('ds_MaxCapacity                             : [%s]' % ds_MaxCapacity)
                print('ds_ConnectionCreationRetryFrequencySeconds : [%s]' % ds_ConnectionCreationRetryFrequencySeconds)
                print('ds_TestTableName                           : [%s]' % ds_TestTableName)
                print('ds_XaSetTransactionTimeout                 : [%s]' % ds_XaSetTransactionTimeout)
                print('ds_XaTransactionTimeout                    : [%s]' % ds_XaTransactionTimeout)

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

                print('Online create datasource                   : [%s]' % ds_Name)

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

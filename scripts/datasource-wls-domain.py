#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# NAME:   DATASOURCE-WLS-DOMAIN.PY
# DESC:   CREATE WLS DATASOURCE
# DATE:   02-10-2019
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
    return not value in ['false','f','null','n','0','']

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

    ds_url=configProps.get("ds.url")
    ds_user=configProps.get("ds.user")
    ds_password=configProps.get("ds.password")
    ds_Name=configProps.get("ds.Name")
    ds_jndiName=configProps.get("ds.jndiName")
    ds_GlobalTransactionsProtocol=configProps.get("ds.GlobalTransactionsProtocol")
    ds_driver=configProps.get("ds.driver")
    ds_MaxCapacity=configProps.get("ds.MaxCapacity")
    ds_ConnectionCreationRetryFrequencySeconds=configProps.get("ds.ConnectionCreationRetryFrequencySeconds")
    ds_TestTableName=configProps.get("ds.TestTableName")
    ds_XaSetTransactionTimeout=configProps.get("ds.XaSetTransactionTimeout")
    ds_XaTransactionTimeout=configProps.get("ds.XaTransactionTimeout")

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
    check_value(ds_url, "ds_url")
    check_value(ds_user, "ds_user")
    check_value(ds_password, "ds_password")
    check_value(ds_Name, "ds_Name")
    check_value(ds_jndiName, "ds_jndiName")
    check_value(ds_GlobalTransactionsProtocol, "ds_GlobalTransactionsProtocol")
    check_value(ds_driver, "ds_driver")
    check_value(ds_MaxCapacity, "ds_MaxCapacity")
    check_value(ds_ConnectionCreationRetryFrequencySeconds, "ds_ConnectionCreationRetryFrequencySeconds")
    check_value(ds_TestTableName, "ds_TestTableName")
    check_value(ds_XaSetTransactionTimeout, "ds_XaSetTransactionTimeout")
    check_value(ds_XaTransactionTimeout, "ds_XaTransactionTimeout")

    try:
        if mode == 'offline':
            # WLST Offline - Create datasource
            # https://docs.oracle.com/cd/E13222_01/wls/docs90/config_scripting/domains.html
            print('Offline create datasource                  : [%s]' % ds_Name)
            readDomain(domain_path)

            cd('/')
            create(ds_Name, 'JDBCSystemResource')

            cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
            set('Name', ds_Name)

            cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
            create(ds_Name + '_ds_params', 'JDBCDataSourceParams')

            cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCDataSourceParams/' + 'NO_NAME_0')
            set('JNDIName', ds_jndiName)

            if check_bool(ds_GlobalTransactionsProtocol):
                # TwoPhaseCommit
                # LoggingLastResource
                # EmulateTwoPhaseCommit
                # OnePhaseCommit # Default Value
                # None
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

            if check_bool(ds_TestTableName) or check_bool(ds_MaxCapacity) or check_bool(ds_ConnectionCreationRetryFrequencySeconds):
                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
                create(ds_Name + '_conn_pool_params', 'JDBCConnectionPoolParams')

            if check_bool(ds_TestTableName):
                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCConnectionPoolParams/' + 'NO_NAME_0')
                set('TestTableName', ds_TestTableName)

            if check_bool(ds_MaxCapacity):
                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCConnectionPoolParams/' + 'NO_NAME_0')
                set('MaxCapacity', int(ds_MaxCapacity))

            if check_bool(ds_ConnectionCreationRetryFrequencySeconds):
                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCConnectionPoolParams/' + 'NO_NAME_0')
                set('ConnectionCreationRetryFrequencySeconds', int(ds_ConnectionCreationRetryFrequencySeconds))

            if check_bool(ds_XaSetTransactionTimeout) or check_bool(ds_XaTransactionTimeout):
                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name)
                create(ds_Name + '_xa_params', 'JDBCXAParams')

            if check_bool(ds_XaSetTransactionTimeout):
                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCXAParams/' + 'NO_NAME_0')
                set('XaSetTransactionTimeout', ds_XaSetTransactionTimeout)

            if check_bool(ds_XaTransactionTimeout):
                cd('/JDBCSystemResource/' + ds_Name + '/JdbcResource/' + ds_Name + '/JDBCXAParams/' + 'NO_NAME_0')
                set('XaTransactionTimeout', int(ds_XaTransactionTimeout))

            assign('JDBCSystemResource', ds_Name, 'Target', admin_name)

            updateDomain()
            closeDomain()

        if mode == 'online':
            # WLST Online - Create datasource
            print('Online create datasource                   : [%s]' % ds_Name)
            # WLST Offline - AdministrationPort disable
            if check_bool(administration_port_enabled):
                readDomain(domain_path)
                cd('/')
                cmo.setAdministrationPortEnabled(false)
                # cmo.setAdministrationPortEnabled(true)
                updateDomain()
                closeDomain()

            # WLST Online - Deploy application
            # https://oracle-base.com/articles/web/wlst-create-data-source
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

            cd('/')
            cmo.createJDBCSystemResource(ds_Name)

            cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name)
            cmo.setName(ds_Name)

            cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCDataSourceParams/' + ds_Name)
            cmo.setJNDINames(jarray.array([String(ds_jndiName)], String))

            if check_bool(ds_GlobalTransactionsProtocol):
                # TwoPhaseCommit
                # LoggingLastResource
                # EmulateTwoPhaseCommit
                # OnePhaseCommit # Default Value
                # None
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

            if check_bool(ds_TestTableName):
                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCConnectionPoolParams/' + ds_Name)
                cmo.setTestTableName(ds_TestTableName)

            if check_bool(ds_MaxCapacity):
                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCConnectionPoolParams/' + ds_Name)
                cmo.setMaxCapacity(int(ds_MaxCapacity))

            if check_bool(ds_ConnectionCreationRetryFrequencySeconds):
                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCConnectionPoolParams/' + ds_Name)
                cmo.setConnectionCreationRetryFrequencySeconds(int(ds_ConnectionCreationRetryFrequencySeconds))

            if check_bool(ds_XaSetTransactionTimeout):
                cd('/JDBCSystemResources/' + ds_Name + '/JDBCResource/' + ds_Name + '/JDBCXAParams/' + ds_Name)
                cmo.setXaSetTransactionTimeout(True)

            if check_bool(ds_XaTransactionTimeout):
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

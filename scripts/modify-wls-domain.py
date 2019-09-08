#!/usr/bin/env python
# -*- coding: UTF-8 -*-
  
# NAME:   MODIFY-WLS-DOMAIN.PY
# DESC:   MODIFY WLS SETTINGS AND ADD CONTAINER ID
# DATE:   28-08-2019
# LANG:   PYTHON WLST
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU
  
# Examples:
  
# cat /u01/oracle/properties/domain_modify.properties
# log.admin.path=/Servers/AdminServer/Log/AdminServer
# log.admin.file=../../logs/server/AdminServer.log
# log.admin.fileMinSize=10000
# log.admin.fileCount=50
# log.admin.rotateLogOnStartup=True
# log.access.path=/Servers/AdminServer/WebServer/AdminServer/WebServerLog/AdminServer
# log.access.file=../../logs/server/access.log
# log.access.fileMinSize=10000
# log.access.fileCount=50
# log.access.rotateLogOnStartup=True
# log.datasource.path=/Servers/AdminServer/DataSource/AdminServer/DataSourceLogFile/AdminServer
# log.datasource.file=../../logs/server/datasource.log
# log.datasource.fileMinSize=10000
# log.datasource.fileCount=50
# log.datasource.rotateLogOnStartup=True
# log.diagnostic.path=/Servers/AdminServer/ServerDiagnosticConfig/AdminServer
# log.diagnostic.file=../../logs/server/diagnostic_images
# log.diagnostic.timeout=1
# log.domain.path=/Log/base_domain
# log.domain.file=../../logs/server/base_domain.log
# log.domain.fileMinSize=10000
# log.domain.fileCount=50
# log.domain.rotateLogOnStartup=True
  
# wlst.sh -skipWLSModuleScanning
# connect('weblogic', 'welcome1', 't3://localhost:7001')
# edit()
# startEdit()
  
# cd('/Servers/AdminServer/Log/AdminServer')
# cmo.setFileName('../../logs/server/AdminServer.TEST.log')
# cmo.setRotateLogOnStartup(True)
# cmo.setFileCount(50)
# cmo.setFileMinSize(10000)
  
# cd('/Log/base_domain')
# cmo.setFileName('../../logs/server/base_domain.TEST.log')
# cmo.setRotateLogOnStartup(True)
# cmo.setFileCount(50)
# cmo.setFileMinSize(10000)
  
# cd('/Servers/AdminServer/WebServer/AdminServer/WebServerLog/AdminServer')
# cmo.setFileName('../../logs/server/access.TEST.log')
# cmo.setRotateLogOnStartup(True)
# cmo.setFileCount(50)
# cmo.setFileMinSize(10000)
  
# save()
# activate(block = 'true')
# disconnect()
  
# wlst.sh -skipWLSModuleScanning \
#  -loadProperties /u01/oracle/properties/domain.properties \
#  -loadProperties /u01/oracle/properties/domain_security.properties \
#   /u01/oracle/modify-wls-domain.py -p /u01/oracle/properties/domain_modify.properties -c 351c67cea47a
  
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
  
    propInputStream = FileInputStream(properties)
    configProps = Properties()
    configProps.load(propInputStream)
  
    log_admin_path=configProps.get("log.admin.path")
    log_admin_file=configProps.get("log.admin.file")
    log_admin_fileMinSize=configProps.get("log.admin.fileMinSize")
    log_admin_fileCount=configProps.get("log.admin.fileCount")
    log_admin_rotateLogOnStartup=configProps.get("log.admin.rotateLogOnStartup")
    log_access_path=configProps.get("log.access.path")
    log_access_file=configProps.get("log.access.file")
    log_access_fileMinSize=configProps.get("log.access.fileMinSize")
    log_access_fileCount=configProps.get("log.access.fileCount")
    log_access_rotateLogOnStartup=configProps.get("log.access.rotateLogOnStartup")
    log_datasource_path=configProps.get("log.datasource.path")
    log_datasource_file=configProps.get("log.datasource.file")
    log_datasource_fileMinSize=configProps.get("log.datasource.fileMinSize")
    log_datasource_fileCount=configProps.get("log.datasource.fileCount")
    log_datasource_rotateLogOnStartup=configProps.get("log.datasource.rotateLogOnStartup")
    log_diagnostic_path=configProps.get("log.diagnostic.path")
    log_diagnostic_file=configProps.get("log.diagnostic.file")
    log_diagnostic_timeout=configProps.get("log.diagnostic.timeout")
    log_domain_path=configProps.get("log.domain.path")
    log_domain_file=configProps.get("log.domain.file")
    log_domain_fileMinSize=configProps.get("log.domain.fileMinSize")
    log_domain_fileCount=configProps.get("log.domain.fileCount")
    log_domain_rotateLogOnStartup=configProps.get("log.domain.rotateLogOnStartup")
  
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
    print('log_admin_path                   : [%s]' % log_admin_path)
    print('log_admin_file                   : [%s]' % log_admin_file)
    print('log_admin_fileMinSize            : [%s]' % log_admin_fileMinSize)
    print('log_admin_fileCount              : [%s]' % log_admin_fileCount)
    print('log_admin_rotateLogOnStartup     : [%s]' % log_admin_rotateLogOnStartup)
    print('log_access_path                  : [%s]' % log_access_path)
    print('log_access_file                  : [%s]' % log_access_file)
    print('log_access_fileMinSize           : [%s]' % log_access_fileMinSize)
    print('log_access_fileCount             : [%s]' % log_access_fileCount)
    print('log_access_rotateLogOnStartup    : [%s]' % log_access_rotateLogOnStartup)
    print('log_datasource_path              : [%s]' % log_datasource_path)
    print('log_datasource_file              : [%s]' % log_datasource_file)
    print('log_datasource_fileMinSize       : [%s]' % log_datasource_fileMinSize)
    print('log_datasource_fileCount         : [%s]' % log_datasource_fileCount)
    print('log_datasource_rotateLogOnStartup: [%s]' % log_datasource_rotateLogOnStartup)
    print('log_diagnostic_path              : [%s]' % log_diagnostic_path)
    print('log_diagnostic_file              : [%s]' % log_diagnostic_file)
    print('log_diagnostic_timeout           : [%s]' % log_diagnostic_timeout)
    print('log_domain_path                  : [%s]' % log_domain_path)
    print('log_domain_file                  : [%s]' % log_domain_file)
    print('log_domain_fileMinSize           : [%s]' % log_domain_fileMinSize)
    print('log_domain_fileCount             : [%s]' % log_domain_fileCount)
    print('log_domain_rotateLogOnStartup    : [%s]' % log_domain_rotateLogOnStartup)
  
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
    check_value(cid, "cid")
  
    check_value(log_admin_path, "log_admin_path")
    check_value(log_admin_file, "log_admin_file")
    check_value(log_admin_fileMinSize, "log_admin_fileMinSize")
    check_value(log_admin_fileCount, "log_admin_fileCount")
    check_value(log_admin_rotateLogOnStartup, "log_admin_rotateLogOnStartup")
    check_value(log_access_path, "log_access_path")
    check_value(log_access_file, "log_access_file")
    check_value(log_access_fileMinSize, "log_access_fileMinSize")
    check_value(log_access_fileCount, "log_access_fileCount")
    check_value(log_access_rotateLogOnStartup, "log_access_rotateLogOnStartup")
    check_value(log_datasource_path, "log_datasource_path")
    check_value(log_datasource_file, "log_datasource_file")
    check_value(log_datasource_fileMinSize, "log_datasource_fileMinSize")
    check_value(log_datasource_fileCount, "log_datasource_fileCount")
    check_value(log_datasource_rotateLogOnStartup, "log_datasource_rotateLogOnStartup")
    check_value(log_diagnostic_path, "log_diagnostic_path")
    check_value(log_diagnostic_file, "log_diagnostic_file")
    check_value(log_diagnostic_timeout, "log_diagnostic_timeout")
    check_value(log_domain_path, "log_domain_path")
    check_value(log_domain_file, "log_domain_file")
    check_value(log_domain_fileMinSize, "log_domain_fileMinSize")
    check_value(log_domain_fileCount, "log_domain_fileCount")
    check_value(log_domain_rotateLogOnStartup, "log_domain_rotateLogOnStartup")
 
    if log_domain_path.lower() != ('/Log/' + domain_name).lower():
        print('Error: The parameter [log.domain.path=%s] is incorrect! Exit!' % log_domain_path)
        sys.exit(1)
 
    log_admin_file = log_admin_file.replace('.log', '-' + str(cid) + ".log")
    log_access_file = log_access_file.replace('.log', '-' + str(cid) + ".log")
    log_datasource_file = log_datasource_file.replace('.log', '-' + str(cid) + ".log")
    log_diagnostic_file = log_diagnostic_file + '-' + str(cid)
    log_domain_file = log_domain_file.replace('.log', '-' + str(cid) + ".log")
  
    try:

        # WLST Offline - AdministrationPort disable
        if check_bool(administration_port_enabled):
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

        print('Setup logging : [%s]' % log_admin_file)
        cd(log_admin_path)
        cmo.setFileName(str(log_admin_file))
        cmo.setRotateLogOnStartup(check_bool(log_admin_rotateLogOnStartup))
        cmo.setFileCount(int(log_admin_fileCount))
        cmo.setFileMinSize(int(log_admin_fileMinSize))
  
        print('Setup logging : [%s]' % log_access_file)
        cd(log_access_path)
        cmo.setFileName(str(log_access_file))
        cmo.setRotateLogOnStartup(check_bool(log_access_rotateLogOnStartup))
        cmo.setFileCount(int(log_access_fileCount))
        cmo.setFileMinSize(int(log_access_fileMinSize))
  
        print('Setup logging : [%s]' % log_datasource_file)
        cd(log_datasource_path)
        cmo.setFileName(str(log_datasource_file))
        cmo.setRotateLogOnStartup(check_bool(log_datasource_rotateLogOnStartup))
        cmo.setFileCount(int(log_datasource_fileCount))
        cmo.setFileMinSize(int(log_datasource_fileMinSize))
  
        print('Setup logging : [%s]' % log_diagnostic_file)
        cd(log_diagnostic_path)
        cmo.setImageDir(str(log_diagnostic_file))
        cmo.setImageTimeout(int(log_diagnostic_timeout))
  
        print('Setup logging : [%s]' % log_domain_file)
        cd(log_domain_path)
        cmo.setFileName(str(log_domain_file))
        cmo.setRotateLogOnStartup(check_bool(log_domain_rotateLogOnStartup))
        cmo.setFileCount(int(log_domain_fileCount))
        cmo.setFileMinSize(int(log_domain_fileMinSize))
  
        save()
        activate(block = 'true')
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


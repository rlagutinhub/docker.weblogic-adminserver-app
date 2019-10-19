#!/usr/bin/env python
# -*- coding: UTF-8 -*-
  
# NAME:   MODIFY-WLS-DOMAIN.PY
# DESC:   MODIFY WLS
# DATE:   19-10-2019
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
SECTION_VALUE_LOG = 'Logging'
SECTION_VALUE_SEC_REALM_AUTHPROV = 'SecurityRealmAuthenticationProviders'
SECTION_VALUE_SEC_REALM_ROLEMAPP = 'SecurityRealmRoleMapping'

def main():

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

    pars_log = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE_LOG)
    settings_log = pars_log.settings

    if not settings_log:
        print('Error: %s' % settings_log)
        sys.exit(1)

    pars_sec_realm_authprov = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE_SEC_REALM_AUTHPROV)
    settings_sec_realm_authprov = pars_sec_realm_authprov.settings

    if not settings_sec_realm_authprov:
        print('Error: %s' % settings_sec_realm_authprov)
        sys.exit(1)

    pars_sec_realm_rolemapp = lib.ConfigParserClass(file_value=properties, keys_value=KEYS_VALUE, section_value=SECTION_VALUE_SEC_REALM_ROLEMAPP)
    settings_sec_realm_rolemapp = pars_sec_realm_rolemapp.settings

    if not settings_sec_realm_rolemapp:
        print('Error: %s' % settings_sec_realm_rolemapp)
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

        for key in settings_log:

            log_path = settings_log[key]['path']
            log_file = settings_log[key]['file']
            log_fileMinSize = settings_log[key]['fileMinSize']
            log_fileCount = settings_log[key]['fileCount']
            log_rotateLogOnStartup = settings_log[key]['rotateLogOnStartup']

            print(lib.bcolors.BOLD + 'log_path                                   : [%s]' % log_path + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'log_file                                   : [%s]' % log_file + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'log_fileMinSize                            : [%s]' % log_fileMinSize + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'log_fileCount                              : [%s]' % log_fileCount + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'log_rotateLogOnStartup                     : [%s]' % log_rotateLogOnStartup + lib.bcolors.ENDC)

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

            print(lib.bcolors.WARNING + 'Setup logging                              : [%s]' % log_file + lib.bcolors.ENDC)

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

        for key in settings_sec_realm_authprov:

            sec_realm_authprov_realm = settings_sec_realm_authprov[key]['realm']
            sec_realm_authprov_name = settings_sec_realm_authprov[key]['name']
            sec_realm_authprov_type = settings_sec_realm_authprov[key]['type']
            sec_realm_authprov_ControlFlag = settings_sec_realm_authprov[key]['ControlFlag']

            print(lib.bcolors.BOLD + 'sec_realm_authprov_realm                   : [%s]' % sec_realm_authprov_realm + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'sec_realm_authprov_name                    : [%s]' % sec_realm_authprov_name + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'sec_realm_authprov_type                    : [%s]' % sec_realm_authprov_type + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'sec_realm_authprov_ControlFlag             : [%s]' % sec_realm_authprov_ControlFlag + lib.bcolors.ENDC)

            lib.check_value(sec_realm_authprov_realm, "sec_realm_authprov_realm")
            lib.check_value(sec_realm_authprov_name, "sec_realm_authprov_name")
            lib.check_value(sec_realm_authprov_type, "sec_realm_authprov_type")
            lib.check_value(sec_realm_authprov_ControlFlag, "sec_realm_authprov_ControlFlag")

            print(lib.bcolors.WARNING + 'Setup Security Realm Auth Providers        : [%s]' % sec_realm_authprov_name + lib.bcolors.ENDC)
            
            if not sec_realm_authprov_name in ('DefaultAuthenticator', 'DefaultIdentityAsserter'):

                if lib.check_bool(sec_realm_authprov_name) and lib.check_bool(sec_realm_authprov_type):
                    cd('/SecurityConfiguration/' + domain_name + '/Realms/' + sec_realm_authprov_realm)
                    cmo.createAuthenticationProvider(sec_realm_authprov_name, sec_realm_authprov_type)

                if lib.check_bool(sec_realm_authprov_ControlFlag):
                    cd('/SecurityConfiguration/' + domain_name + '/Realms/' + sec_realm_authprov_realm + '/AuthenticationProviders/' + sec_realm_authprov_name)
                    cmo.setControlFlag(sec_realm_authprov_ControlFlag)

            else:

                if lib.check_bool(sec_realm_authprov_ControlFlag):
                    cd('/SecurityConfiguration/' + domain_name + '/Realms/' + sec_realm_authprov_realm + '/AuthenticationProviders/' + sec_realm_authprov_name)
                    cmo.setControlFlag(sec_realm_authprov_ControlFlag)

        for key in settings_sec_realm_rolemapp:

            sec_realm_rolemapp_realm = settings_sec_realm_rolemapp[key]['realm']
            sec_realm_rolemapp_name = settings_sec_realm_rolemapp[key]['name']
            sec_realm_rolemapp_type = settings_sec_realm_rolemapp[key]['type']

            print(lib.bcolors.BOLD + 'sec_realm_rolemapp_realm                   : [%s]' % sec_realm_rolemapp_realm + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'sec_realm_rolemapp_name                    : [%s]' % sec_realm_rolemapp_name + lib.bcolors.ENDC)
            print(lib.bcolors.BOLD + 'sec_realm_rolemapp_type                    : [%s]' % sec_realm_rolemapp_type + lib.bcolors.ENDC)

            lib.check_value(sec_realm_rolemapp_realm, "sec_realm_rolemapp_realm")
            lib.check_value(sec_realm_rolemapp_name, "sec_realm_rolemapp_name")
            lib.check_value(sec_realm_rolemapp_type, "sec_realm_rolemapp_type")

            print(lib.bcolors.WARNING + 'Setup Security Realm Role Mapping          : [%s]' % sec_realm_rolemapp_name + lib.bcolors.ENDC)

            if not sec_realm_rolemapp_name in ('XACMLRoleMapper'):

                if lib.check_bool(sec_realm_rolemapp_name) and lib.check_bool(sec_realm_rolemapp_type):
                    cd('/SecurityConfiguration/' + domain_name + '/Realms/' + sec_realm_authprov_realm)
                    cmo.createRoleMapper(sec_realm_rolemapp_name, sec_realm_rolemapp_type)

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

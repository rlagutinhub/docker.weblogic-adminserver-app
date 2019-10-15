#!/usr/bin/env python
# -*- coding: UTF-8 -*-
  
# NAME:   CREATE-WLS-DOMAIN.PY
# DESC:   CREATE WLS DOMAIN
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


def main():

    properties = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:', ['properties='])

    except getopt.GetoptError:
        pass

    # print('argv: ', sys.argv[1:])
    # print('opts: ', opts)

    try:
        for opt, arg in opts:
            if opt in ('-p', '--properties'):
                if os.path.isfile(arg):
                    properties = arg

    except NameError:
        pass

    if not properties:
        print('modify-wls-domain.py -p <path-to-properties-file>')
        sys.exit(1)

    # print('properties:', properties)

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
    domain_template = '/u01/oracle/wlserver/common/templates/wls/wls.jar'

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
    print(lib.bcolors.BOLD + 'domain_template                            : [%s]' % domain_template + lib.bcolors.ENDC)

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
    lib.check_value(domain_template, "domain_template")

    try:
        # Open default domain template
        # ============================
        readTemplate(domain_template)

        set('Name', domain_name)
        setOption('DomainName', domain_name)

        # Set Administration Port 
        # =======================
        if administration_port_enabled != "false":
            set('AdministrationPort', administration_port)
            set('AdministrationPortEnabled', 'true')

        # Disable Admin Console
        # --------------------
        if admin_console_enabled != "true":
            cmo.setConsoleEnabled(false)

        # Configure the Administration Server and SSL port.
        # =================================================
        cd('/Servers/AdminServer')
        set('Name', admin_name)
        set('ListenAddress', '')
        set('ListenPort', admin_listen_port)
        if administration_port_enabled != "false":
            create('AdminServer','SSL')
            cd('SSL/AdminServer')
            set('Enabled', 'True')

        # Define the user password for weblogic
        # =====================================
        cd(('/Security/%s/User/weblogic') % domain_name)
        cmo.setName(username)
        cmo.setPassword(password)

        # Write the domain and close the domain template
        # ==============================================
        setOption('OverwriteDomain', 'true')
        setOption('ServerStartMode',production_mode)

        # Create Node Manager
        # ===================
        #cd('/NMProperties')
        #set('ListenAddress','')
        #set('ListenPort',5556)
        #set('CrashRecoveryEnabled', 'true')
        #set('NativeVersionEnabled', 'true')
        #set('StartScriptEnabled', 'false')
        #set('SecureListener', 'false')
        #set('LogLevel', 'FINEST')

        # Set the Node Manager user name and password 
        # ===========================================
        #cd('/SecurityConfiguration/%s' % domain_name)
        #set('NodeManagerUsername', username)
        #set('NodeManagerPasswordEncrypted', password)

        # Write Domain
        # ============
        writeDomain(domain_path)
        closeTemplate()

        # Exit WLST
        # =========
        # exit()

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

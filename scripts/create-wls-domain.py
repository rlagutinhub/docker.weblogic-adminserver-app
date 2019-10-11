#!/usr/bin/env python
# -*- coding: UTF-8 -*-
  
# NAME:   CREATE-WLS-DOMAIN.PY
# DESC:   CREATE WLS DOMAIN
# DATE:   28-08-2019
# LANG:   PYTHON WLST
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU

# Get vars
# ============================
domain_name                 = DOMAIN_NAME
admin_name                  = ADMIN_NAME
admin_listen_port           = int(ADMIN_LISTEN_PORT)
production_mode             = PRODUCTION_MODE
administration_port_enabled = ADMINISTRATION_PORT_ENABLED
administration_port         = int(ADMINISTRATION_PORT)
admin_console_enabled       = ADMIN_CONSOLE_ENABLED

domain_path                 = '/u01/oracle/user_projects/domains/%s' % domain_name
domain_template             = '/u01/oracle/wlserver/common/templates/wls/wls.jar'

print('domain_name                 : [%s]' % domain_name)
print('admin name                  : [%s]' % admin_name)
print('admin_listen_port           : [%s]' % admin_listen_port)
print('production_mode             : [%s]' % production_mode)
print('administration_port_enabled : [%s]' % administration_port_enabled)
print('administration_port         : [%s]' % administration_port)
print('admin_console_enabled       : [%s]' % admin_console_enabled)

print('domain_path                 : [%s]' % domain_path)
print('domain_template             : [%s]' % domain_template)

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
exit()

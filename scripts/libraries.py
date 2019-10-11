#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import ConfigParser


class ConfigParserClass(object):

    def __init__(self, file_value=None, keys_value=None, section_value=None):
        
        self.file_value = file_value
        self.keys_value = keys_value
        self.section_value = section_value

        self.config = ConfigParser.ConfigParser()

        try:
            # open(self.file_value, 'rb').read(1)
            self.config.read(self.file_value)

        except:
            pass

        self.params = self.__get_param()
        self.sections = self.__get_sections()
        self.keys = self.__get_keys()
        self.settings = self.__get_settings()

    def __get_param(self):

        if str(self.section_value).lower() == 'base':
            param_domain_name = 'domain_name'
            param_admin_name = 'admin_name'
            param_admin_listen_port = 'admin_listen_port'
            param_production_mode = 'production_mode'
            param_administration_port_enabled = 'administration_port_enabled'
            param_administration_port = 'administration_port'
            param_admin_console_enabled = 'admin_console_enabled'
            param_derby_enabled = 'derby_enabled'

            return [
                param_domain_name,
                param_admin_name,
                param_admin_listen_port,
                param_production_mode,
                param_administration_port_enabled,
                param_administration_port,
                param_admin_console_enabled,
                param_derby_enabled
            ]

        elif str(self.section_value).lower() == 'security':
            param_username = 'username'
            param_password = 'password'

            return [
                param_username,
                param_password
            ]

        elif str(self.section_value).lower() == 'java':
            param_user_mem_args = 'user_mem_args'
            param_java_options = 'java_options'

            return [
                param_user_mem_args,
                param_java_options
            ]

        elif str(self.section_value).lower()  == 'logging':
            param_path = 'path'
            param_file = 'file'
            param_fileMinSize = 'fileMinSize'
            param_fileCount = 'fileCount'
            param_rotateLogOnStartup = 'rotateLogOnStartup'

            return [
                param_path,
                param_file,
                param_fileMinSize,
                param_fileCount,
                param_rotateLogOnStartup
            ]

        elif str(self.section_value).lower()  == 'datasources':
            param_url = 'url'
            param_user = 'user'
            param_password = 'password'
            param_Name = 'Name'
            param_jndiName = 'jndiName'
            param_GlobalTransactionsProtocol = 'GlobalTransactionsProtocol'
            param_driver = 'driver'
            param_MaxCapacity = 'MaxCapacity'
            param_ConnectionCreationRetryFrequencySeconds = 'ConnectionCreationRetryFrequencySeconds'
            param_TestTableName = 'TestTableName'
            param_XaSetTransactionTimeout = 'XaSetTransactionTimeout'
            param_XaTransactionTimeout = 'XaTransactionTimeout'

            return [
                param_url,
                param_user,
                param_password,
                param_Name,
                param_jndiName,
                param_GlobalTransactionsProtocol,
                param_driver,
                param_MaxCapacity,
                param_ConnectionCreationRetryFrequencySeconds,
                param_TestTableName,
                param_XaSetTransactionTimeout,
                param_XaTransactionTimeout
            ]

        elif str(self.section_value).lower() == 'deployments':
            param_name = 'name'
            param_type = 'type'
            param_source_path = 'sourcePath'
            param_security_dd_model = 'securityDDModel'

            return [
                param_name,
                param_type,
                param_source_path,
                param_security_dd_model
            ]

        else:
            return None

    def __get_sections(self):

        sections = self.config.sections()

        if not sections:
            return None

        else:
            return sections

    def __get_keys(self):

        if not self.section_value or not self.keys_value:
            return None

        keys = list()

        try:
            keys_get = self.config.get(self.section_value, self.keys_value)

        except:
            return None

        for key in keys_get.split():
            keys.append(key)

        return keys

    def __get_settings(self):

        if not self.section_value or not self.keys_value or not self.keys or not self.sections or not self.params:
            return None

        settings = dict()

        for key_item in self.keys:

            settings_item = dict()

            for param_item in self.params:

                key_param = key_item + "." + param_item

                if not self.config.has_option(self.section_value, key_param):
                    continue

                key_value = self.config.get(self.section_value, key_param)
                settings_item[param_item] = key_value
            
            settings[key_item] = settings_item.copy()
            settings_item.clear()

        return settings


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

    pass


if __name__ != '__main__':
    main()

elif __name__ == '__main__':
    print('This script has to be executed with weblogic WLST')

# -*- coding: utf-8 -*-
from lazagne.config.module_info import ModuleInfo
from lazagne.config.constant import constant
import os


class CredFiles(ModuleInfo):
    def __init__(self):
        ModuleInfo.__init__(self, 'credfiles', 'windows', dpapi_used=True)

    def run(self):
        pwd_found = []
        if constant.user_dpapi and constant.user_dpapi.unlocked:
            main_vault_directory = os.path.join(constant.profile['APPDATA'], u'..', u'Local', u'Microsoft', u'Credentials')
            main_vault_directory = os.path.abspath(main_vault_directory)
            creds_directory = os.path.join(constant.profile['APPDATA'], u'Microsoft', u'Credentials')
            system_creds = r"C:\Windows\System32\config\systemprofile\AppData\Local\Microsoft\Credentials"
            creds = []

            if os.path.exists(creds_directory):
                creds += [os.path.join(creds_directory, cred_file) for cred_file in os.listdir(creds_directory)]

            if os.path.exists(main_vault_directory):
                creds += [os.path.join(main_vault_directory, cred_file) for cred_file in os.listdir(main_vault_directory)]

            if os.path.exists(system_creds):
                creds += [os.path.join(system_creds, cred_file) for cred_file in os.listdir(system_creds)]

            for cred_file in creds:
                try:
                    cred = constant.user_dpapi.decrypt_cred(cred_file)
                except:
                    print("--------------- filed: ", cred_file, "----------------")
                    cred = False
                if cred:
                    pwd_found.append(cred)

        return pwd_found

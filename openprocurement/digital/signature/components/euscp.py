# -*- coding: utf-8 -*-

import os
import logging
import base64

from openprocurement.digital.signature import BASE_DIR
from openprocurement.digital.signature.components.EUSignCP.Usage.v2.Interface.x64.EUSignCP import *


logger = logging.getLogger(__name__)


class EUSignCP(object):
    def __init__(self, password):
        self.pIface = self.initial_eucp_library

        logger.info('EUSignCP library initialized: {}'.format(self.pIface.IsInitialized()))

        self.DATA_PATH = os.path.join(BASE_DIR, 'data')

        self.settings = dict(
            szPath=os.path.join(self.DATA_PATH, 'certificates'),
            bCheckCRLs=False,
            bAutoRefresh=True,
            bOwnCRLsOnly=False,
            bFullAndDeltaCRLs=False,
            bAutoDownloadCRLs=False,
            bSaveLoadedCerts=True,
            dwExpireTime=3600
        )

        self.pIface.SetFileStoreSettings(self.settings)
        self.KEY_FILE_PATH = os.path.join(self.DATA_PATH, 'Key-6.dat')

        if not self.pIface.IsPrivateKeyReaded():
            try:
                self.pIface.ReadPrivateKeyFile(self.KEY_FILE_PATH, password, None)
                logger.info('Private key file was successfully read')
            except RuntimeError, e:
                logger.error('Read private key file failed: {}'.format(e.message.decode('1251')))
                exit()
                raise e

        logger.info('Create session...')

        self.client_data = list()
        self.client_session = list()
        self.server_session = list()

        try:
            self.client_session_step1()
            self.server_session_step1()
            self.client_session_step2()
            self.server_session_step2()
        except RuntimeError, e:
            logger.error('Session creation error: {}'.format(e.message.decode('1251')))
            exit()
            raise e

        self.initial_session()

        self.cert = dict()
        self.cert_info_initial()

    @property
    def initial_eucp_library(self):
        logger.info('Initial library...')
        EULoad()
        pIface = EUGetInterface()
        pIface.Initialize()

        return pIface

    def client_session_step1(self):
        self.pIface.ClientSessionCreateStep1(10000, self.client_session, self.client_data)

    def client_session_step2(self):
        self.pIface.ClientSessionCreateStep2(
            self.client_session[0], self.client_data[0], len(self.client_data[0]), self.client_data
        )

    def server_session_step1(self):
        self.pIface.ServerSessionCreateStep1(
            10000, self.client_data[0], len(self.client_data[0]), self.server_session, self.client_data
        )

    def server_session_step2(self):
        self.pIface.ServerSessionCreateStep2(self.server_session[0], self.client_data[0], len(self.client_data[0]))

    def initial_session(self):
        client_session_is_initialized = self.pIface.SessionIsInitialized(self.client_session[0])
        server_session_is_initialized = self.pIface.SessionIsInitialized(self.server_session[0])

        if all([client_session_is_initialized, server_session_is_initialized]):
            logger.info('Session successfully created')
        else:
            logger.info('Session creation failed')
            exit()

    def cert_info_initial(self):
        self.pIface.SessionGetPeerCertificateInfo(self.client_session[0], self.cert)

    @property
    def cert_info(self):
        return self.cert

    @staticmethod
    def b64encode(altchars):
        altchars = str(altchars)
        encoded_data = base64.b64encode(altchars)
        return encoded_data

    @staticmethod
    def b64decode(altchars):
        altchars = str(altchars)
        decoded_data = base64.b64decode(altchars)
        return decoded_data

    def enc(self, altchars):
        logger.info('Encryption session...')
        altchars = str(altchars)
        self.pIface.SessionEncrypt(self.client_session[0], altchars, len(altchars), self.client_data)
        cipher = self.b64encode(self.client_data[0])

        return cipher

    def dec(self, cipher):
        logger.info('Decryption session...')
        data = self.b64decode(cipher)
        self.pIface.SessionDecrypt(self.server_session[0], data, len(data), self.client_data)
        altchars = self.client_data[0]

        return altchars

    def close(self):
        self.pIface.SessionDestroy(self.server_session[0])
        self.pIface.SessionIsInitialized(self.client_session[0])
        self.pIface.SessionDestroy(self.server_session[0])
        self.pIface.Finalize()
        EUUnload()
        logger.info('Session close')
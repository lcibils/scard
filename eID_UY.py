#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Clase que implementa los métodos necesarios para la gestión de operaciones con el documento de identidad
    electrónico del Uruguay (CI)
'''


# https://realpython.com/primer-on-python-decorators/

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.util import toHexString
from functools import wraps
import hashlib

class eID_UY():
    def __init__(self):
        self.IAS_seleccionado = False
        self.PIN_verificado = False
        self.cardtype = AnyCardType()

    def _check_IAS(f):
        '''
            Decorador que verifica que se haya realizado la verificación de IAS
        '''
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            return f(inst, *args, **kwargs) if inst.IAS_seleccionado else (False, 'Falta verificar IAS')
        return wrapped

    def _check_PIN(f):
        '''
            Decorador que verifica que se haya realizado la verificación de PIN
        '''
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            return f(inst, *args, **kwargs) if inst.IAS_seleccionado else (False, 'Falta verificar PIN')
        return wrapped

    def _apdu(self, comando, data=[]):
        '''
            Ejecuta comandos apdu
        '''

        apdu = comando if not data else comando + data
        response, sw1, sw2 = self.cardservice.connection.transmit(apdu)
        return response, sw1, sw2

    def _get_value(self, res, from_, len_):
        '''
            Devuelve el string de la respuesta de un comando apdu
             a partir de un lugar (from_) y durante un largo (len_)
            en formato ASCII
        '''

        r = ''
        for i in range(len_):
            r += str(chr(res[from_ + i]))
        return r

    def _crear_dict_datos_personales(self, res):
        '''
            from res return a dict with personal data
        '''

        value_names = ['PrimerApellido', 'SegundoApellido', 'Nombres', 'Nacionalidad', 'FechaDeNacimiento',
                       'LugarDeNacimiento', 'NumeroDeCi', 'FechaDeExpedicion', 'FechaDeExpiracion', 'Observaciones']
        pers = {}
        idx = 0
        for i in range(10):
            if res[idx] == 31 and res[idx + 1] == i + 1:
                pers[value_names[i]] = self._get_value(res, idx + 3, res[idx + 2])
                idx += 3 + res[idx + 2]
        return pers

    def _leer_imagen(self, offset, len):
        p1 = offset // 256
        p2 = offset - p1 * 256
        print('read binary', len)
        comando = [0x00, 0xB0, int(hex(p1), 16), int(hex(p2), 16), int(hex(len), 16)]
        response, _, _ = self._apdu(comando)
        return response

    # Métodos visibles por el cliente

    def verificar_eID_en_lector(self):
        '''
            Verifica que la tarjeta esté puesta en el lector
        :return: True si está puesta, False en caso contrario.
        '''

        print('insert a card (SIM card if possible) within 10s')
        try:
            cardrequest = CardRequest(timeout=10, cardType=self.cardtype)
            self.cardservice = cardrequest.waitforcard()

            # attach the console tracer
            observer = ConsoleCardConnectionObserver()
            self.cardservice.connection.addObserver(observer)
            self.cardservice.connection.connect()
            return True
        except CardRequestTimeoutException:
            print('time-out: no card inserted during last 10s')
            return False

    def verificar_atr_documento(self):
        if self.verificar_eID_en_lector():
            atr = self.cardservice.connection.getATR()
            return atr[0] == 0x3B & atr[1] == 0x7f
        else:
            return False

    def seleccionar_applet_IAS(self):
        '''
            Selección del Applet de firma IAS
        :return: True si pudo seleccionar, False y el error en caso contrario
        '''

        SELECT = [0x00, 0xA4, 0x04, 0x00, 0x0c]
        UY_CARD = [0xA0, 0x00, 0x00, 0x00, 0x18, 0x40, 0x00, 0x00, 0x01, 0x63, 0x42, 0x00, 0x00]
        _, sw1, sw2 = self._apdu(SELECT, UY_CARD)
        if sw1 == 0x90:
            print('tarjeta correcta')
            self.IAS_seleccionado = True
            return True, None, None
        else:
            print('tarjeta incorrecta')
            return False, sw1, sw2

    @_check_IAS
    def verificar_pin(self, pin):
        '''
            Verifica que el pin es válido
        '''
        if len(pin) > 12:
            print('el pin no puede tener más de 12 dígitos')
            return False
        else:
            DATA = [int((hex(ord(c))), 16) for c in pin]
            padl = 12 - len(pin)
            if padl > 0:
                for _ in range(padl):
                    DATA.append(0x00)
        CMD =[0x00, 0x20, 0x00, 0x11, 0x0c]
        _, sw1, sw2 = self._apdu(CMD, DATA)
        if sw1 == 0x90:
            print('pin válido')
            self.PIN_verificado = True
            return True, None, None
        else:
            print('pin inválido')
            return False, sw1, sw2

    @_check_IAS
    def obtener_datos_persona(self):
        '''
            Obtiene los datos personales
        :return: Diccionario con los datos personales, o el error encontrado
        '''

        # select file
        print('select file')
        CMD = [0x00, 0xa4, 0x00, 0x00, 0x02]
        DATA = [0x70, 0x02, 0x06]
        _, sw1, sw2 = self._apdu(CMD, DATA)
        if sw1 != 0x61:
            print('Error en selección archivo datos personales')
            return False, sw1, sw2

        # get response
        print('get response')
        CMD = [0x00, 0xc0, 0x00, 0x00, 0x06]
        response, sw1, sw2 = self._apdu(CMD)
        if sw1 != 0x61:
            print('Error en respuesta archivo datos personales')
            return False, sw1, sw2

        if response[4] == 0:
            lb = response[5]
        else:
            print('archivo con más de 255 bytes, ver cómo leerlo!!!')
            return False
        # print(response, sw1, sw2)

        # read Binary
        print('read binary')
        CMD = [0x00, 0xB0, 0x00, 0x00]
        response, sw1, sw2 = self._apdu(CMD, [lb])
        if sw1 == 0x90:
            print('datos válidos')
            return True, self._crear_dict_datos_personales(response)
        else:
            print('Error al leer binario de datos personales')
            return False, sw1, sw2

    @_check_IAS
    def obtener_imagen(self):
        '''
            Obtiene la imagen en formato jpg
        '''

        # select file
        print('select file')
        CMD = [0x00, 0xa4, 0x00, 0x00, 0x02]
        DATA = [0x70, 0x04, 0x06]
        response, sw1, sw2 = self._apdu(CMD, DATA)
        if sw1 != 0x61:
            print('Error en select archivo imagen')
            return False, sw1, sw2

        # get response
        print('get response')
        CMD = [0x00, 0xc0, 0x00, 0x00, 0x06]
        response, sw1, sw2 = self._apdu(CMD)
        if sw1 != 0x61:
            print('Error al leer respuesta archivo imagen')
            return False, sw1, sw2

        # get binaries
        len_ = response[4] * 256 + response[5]
        r = []
        offset = 0
        i = 1
        while len_ > 255:
            print(i)
            r += self._leer_imagen(offset, 255)
            i += 1
            len_ -= 255
            offset += 255
        r += self._leer_imagen(offset, len_)
        return bytearray(r[5:])

    @_check_PIN
    def firma_digital(self, file):

        # hash del archivo
        m = hashlib.sha256()
        m.update(file)
        file_sha = [x for x in bytes.fromhex(m.hexdigest())]

        # MSE_SET_DST
        print('mse_set-dst')
        CMD = [0x00, 0x22, 0x41, 0xb6, 0x06]
        DATA = [0x84, 0x01, 0x01, 0x80, 0x01, 0x02]
        response, sw1, sw2 = self._apdu(CMD, DATA)
        if sw1 != 0x90:
            print('Error en comando MSE_SET_DST')
            return False, sw1, sw2

        # PSO_HASH
        print('pso_hash')
        l_file_sha = len(file_sha)
        le = l_file_sha + 2
        print('le: ', le)
        CMD = [0x00, 0x2a, 0x90, 0xa0, le, 0x90, l_file_sha]
        print('cmd + data: ', CMD + file_sha)
        response, sw1, sw2 = self._apdu(CMD, file_sha)

        # # get response
        # print('get response')
        # CMD = [0x00, 0xc0, 0x00, 0x00, 0x06]
        # response, sw1, sw2 = self._apdu(CMD)

        # PSO_CDS
        print('pso_cds')
        CMD = [0x00, 0x2a, 0x9e, 0x9a, 0x100]
        response, sw1, sw2 = self._apdu(CMD)
        return response








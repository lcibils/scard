from smartcard.util import HexListToBinString, toHexString, toBytes

#
# print(str(chr(67)))
#
# CMD =[0x00, 0x20, 0x00, 0x11, 0x0c]
# DATA = [0x32, 0x30, 0x35, 0x37, 0x31, 0x32, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00]
#
# apdu = CMD + DATA
# print(apdu)
# pin = input('PIN: ')
#
# if len(pin) > 12:
#     print('el pin no puede tener más de 12 dígitos')
# else:
#     DATA = [int((hex(ord(c))), 16) for c in pin]
#     padl = 12 - len(pin)
#     if padl > 0:
#         for i in range(padl):
#             DATA.append(0x00)
#
# apdu = CMD + DATA
# print(apdu)
#
# def get_value(res, from_, len_):
#     r = ''
#     for i in range(len_):
#         r += str(chr(res[from_ + i]))
#     return r
#
#
# def get_data(res):
#     '''
#     from res return a dict with personal data
#     '''
#     value_names = ['PrimerApellido', 'SegundoApellido', 'Nombres', 'Nacionalidad', 'FechaDeNacimiento',
#                    'LugarDeNacimiento', 'NumeroDeCi', 'FechaDeExpedicion', 'FechaDeExpiracion', 'Observaciones']
#     pers = {}
#     idx = 0
#     for i in range(10):
#         if res[idx] == 31 and res[idx + 1] == i + 1:
#             pers[value_names[i]] = get_value(res, idx + 3, res[idx + 2])
#             idx += 3 + res[idx + 2]
#     return(pers)
#
# def get_lengh(res):
#
#
#
# r = [31, 1, 16, 67, 73, 66, 73, 76, 83, 32, 83, 65, 78, 68, 65, 78, 83, 73, 79, 31, 2, 0, 31, 3, 11, 76, 85, 73, 83, 32, 70, 76, 65, 86, 73, 79, 31, 4, 3, 85, 82, 89, 31, 5, 8, 50, 48, 48, 57, 49, 57, 53, 55, 31, 6, 14, 77, 79, 78, 84, 69, 86, 73, 68, 69, 79, 47, 85, 82, 89, 31, 7, 8, 49, 53, 48, 57, 57, 48, 53, 54, 31, 8, 4, 37, 2, 32, 22, 31, 9, 8, 50, 53, 48, 50, 50, 48, 50, 54, 31, 10, 0]
#
# print(get_data(r))


def read_b(offset = 0, le=0):
    p1 = offset // 256
    p2 = offset - p1 * 256
    print('p1: {} - p2: {} - le: {}'.format(hex(p1), hex(p2), hex(le)))
    return 0

def get_binary(res):
    '''
        receive response from get_response
        lenght comes in bytes 4 and 5 (start in 0) of response
        :return: the complete binary
    '''
    #  6F 13 81 02 36 6A 61 0F
#     len_ = res[4]*256 + res[5]
#     r = 0
#     i = 1
#     offset = 0
#     le = 0xff
#     while len_ > 255:
#         print(i)
#         r += read_b(offset, le=le)
#         i += 1
#         len_ -= 255
#         offset += 255
#     r += read_b(offset, le=int(hex(len_),16))
#
#
# r = [0x6F,0x13,0x81,0x02,0x36,0x6A,0x61,0x0F]
#
# # get_binary(r)
#
# print(r[6:])
#
# from PIL import Image

# from functools import wraps
#
# class a():
#     def __init__(self):
#         self.a = False
#         self.b = False
#
#     def _check(f, var):
#         @wraps(f)
#         def wrapped(inst, *args, **kwargs):
#             return f(inst, *args, **kwargs) if var else False
#         return wrapped
#
#     def vara(self):
#         self.a = True
#
#     def varb(self):
#         self.b = True
#
#     @_check(self.a)
#     def f(self, p):
#         print('3', p)
#         return 77
#
# b = a()
# print('1', b.f(55))
#
# b.var()
# print('2', b.f(66))

import hashlib

m = hashlib.sha256()
m.update(b"Ejemplo de firma en APDU utilizando el nuevo documento eID")
h = m.hexdigest()
print(h)
print(h)

print(bytes.fromhex(h))

print([hex(x) for x in bytes.fromhex(h)])






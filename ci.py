from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.util import toHexString

def get_value(res, from_, len_):
    r = ''
    for i in range(len_):
        r += str(chr(res[from_ + i]))
    return r


def get_data(res):
    '''
    from res return a dict with personal data
    '''
    value_names = ['PrimerApellido', 'SegundoApellido', 'Nombres', 'Nacionalidad', 'FechaDeNacimiento',
                   'LugarDeNacimiento', 'NumeroDeCi', 'FechaDeExpedicion', 'FechaDeExpiracion', 'Observaciones']
    pers = {}
    idx = 0
    for i in range(10):
        if res[idx] == 31 and res[idx + 1] == i + 1:
            pers[value_names[i]] = get_value(res, idx + 3, res[idx + 2])
            idx += 3 + res[idx + 2]
    return(pers)

def read_b(offset, k):
    p1 = offset // 256
    p2 = offset - p1 * 256
    print('read binary', k)
    apdu = [0x00, 0xB0, int(hex(p1), 16), int(hex(p2), 16), int(hex(k), 16)]
    response, sw1, sw2 = cardservice.connection.transmit(apdu)
    return response

# request any card type
cardtype = AnyCardType()


# request card insertion
print('insert a card (SIM card if possible) within 10s')
try:
    cardrequest = CardRequest(timeout=10, cardType=cardtype)
    cardservice = cardrequest.waitforcard()

    # attach the console tracer
    observer = ConsoleCardConnectionObserver()
    cardservice.connection.addObserver(observer)
except CardRequestTimeoutException:
    print('time-out: no card inserted during last 10s')
    quit()

# connect to the card and perform a few transmits
cardservice.connection.connect()

# print ATR
atr = cardservice.connection.getATR()
print(toHexString(atr))


# Selección del Applet de firma IAS
# SELECT = [0x00, 0xA4, 0x04, 0x00, 0x0c]
# UY_CARD = [0xA0, 0x00, 0x00, 0x00, 0x18, 0x40, 0x00, 0x00, 0x01, 0x63, 0x42, 0x00, 0x00]
# apdu = SELECT + UY_CARD
#
# response, sw1, sw2 = cardservice.connection.transmit(apdu)
#
# if sw1 == 0x90:
#     print('tarjeta correcta')
# else:
#     print('tarjeta incorrecta')
# quit()

# Verificación de PIN - verifyPIN

# CMD =[0x00, 0x20, 0x00, 0x11, 0x0c]
# DATA = [0x32, 0x30, 0x35, 0x37, 0x31, 0x32, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00]
# apdu = CMD + DATA
# print(apdu)
# response, sw1, sw2 = cardservice.connection.transmit(apdu)
#
# if sw1 == 0x90:
#     print('pin correcto')
# else:
#     print('pin incorrecto')
#     quit()

# datos personales


# select file
print('select file')
CMD =[0x00, 0xa4, 0x00, 0x00, 0x02]
DATA = [0x70, 0x02, 0x06]
apdu = CMD + DATA
response, sw1, sw2 = cardservice.connection.transmit(apdu)
print(sw1, sw2)

# get response
print('get response')
CMD = [0x00, 0xc0, 0x00, 0x00, 0x06]
apdu = CMD
response, sw1, sw2 = cardservice.connection.transmit(apdu)

if response[4] == 0:
    lb = response[5]
else:
    print('archivo con más de 255 bytes, ver cómo leerlo!!!')
    quit()
# print(response, sw1, sw2)

# read Binary
print('read binary')
apdu = [0x00, 0xB0, 0x00, 0x00, lb]
response, sw1, sw2 = cardservice.connection.transmit(apdu)
print(get_data(response))

# imagen

# select file
print('select file')
CMD =[0x00, 0xa4, 0x00, 0x00, 0x02]
DATA = [0x70, 0x04, 0x06]
apdu = CMD + DATA
response, sw1, sw2 = cardservice.connection.transmit(apdu)

# get response
print('get response')
CMD = [0x00, 0xc0, 0x00, 0x00, 0x06]
apdu = CMD
response, sw1, sw2 = cardservice.connection.transmit(apdu)

len_ = response[4] * 256 + response[5]
r = []
offset = 0
i = 1
while len_ > 255:
    print(i)
    r += read_b(offset, 255)
    i += 1
    len_ -= 255
    offset += 255
r += read_b(offset, len_)
data = bytearray(r[5:])
with open("foto.jpg", "wb") as outfile:
    outfile.write(data)





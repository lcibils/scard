#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from eID_UY import eID_UY

doc = eID_UY()

print(doc.verificar_eID_en_lector())
print(doc.seleccionar_applet_IAS())
print('Obtiene datos persona: ', doc.obtener_datos_persona())
print('Verifica pin: ', doc.verificar_pin('2057121'))
file = doc.obtener_imagen()
if not file:
    print('error en obtener imagen')
else:
    with open("foto.jpg", "wb") as outfile:
        outfile.write(file)
    print('foto obtenida!')

firma = b"Ejemplo de firma en APDU utilizando el nuevo documento eID"

print('hash cifrado: ', doc.firma_digital(firma))



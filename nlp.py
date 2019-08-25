
#! /usr/bin/env python
"""
Sample script that tries to select the DF_TELECOM on all inserted cards.

__author__ = "http://www.gemalto.com"

Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
Copyright 2010 Ludovic Rousseau
Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException

# define the apdus used in this script
GET_RESPONSE = [0XA0, 0XC0, 00, 00]
# SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
# DF_TELECOM = [0x7F, 0x10]
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x0c]
UY_CARD = [0xA0, 0x00, 0x00, 0x00, 0x18, 0x40, 0x00, 0x00, 0x01, 0x63, 0x42, 0x00, 0x00]
# request any card type
cardtype = AnyCardType()

try:
    # request card insertion
    print('insert a card (SIM card if possible) within 10s')
    cardrequest = CardRequest(timeout=10, cardType=cardtype)
    cardservice = cardrequest.waitforcard()

    # attach the console tracer
    observer = ConsoleCardConnectionObserver()
    cardservice.connection.addObserver(observer)

    # connect to the card and perform a few transmits
    cardservice.connection.connect()

    apdu = SELECT + UY_CARD
    response, sw1, sw2 = cardservice.connection.transmit(apdu)

    # there is a UY_CARD
    if sw1 == 0x9F:
        apdu = GET_RESPONSE + [sw2]
        response, sw1, sw2 = cardservice.connection.transmit(apdu)

    else:
        print('no DF_TELECOM: response: {}, sw1: {}, sw2: {}'.format(response, sw1, sw2))

except CardRequestTimeoutException:
    print('time-out: no card inserted during last 10s')

import sys
if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)

# #! /usr/bin/env python
# """
# Sample script that defines a custom card connection observer.
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
# from smartcard.CardType import AnyCardType
# from smartcard.CardRequest import CardRequest
# from smartcard.CardConnectionObserver import CardConnectionObserver
# from smartcard.util import toHexString
#
#
# class TracerAndSELECTInterpreter(CardConnectionObserver):
#     """This observer will interprer SELECT and GET RESPONSE bytes
#     and replace them with a human readable string."""
#
#     def update(self, cardconnection, ccevent):
#
#         if 'connect' == ccevent.type:
#             print('connecting to ' + cardconnection.getReader())
#
#         elif 'disconnect' == ccevent.type:
#             print('disconnecting from ' + cardconnection.getReader())
#
#         elif 'command' == ccevent.type:
#             str = toHexString(ccevent.args[0])
#             str = str.replace("A0 A4 00 00 02", "SELECT")
#             str = str.replace("A0 C0 00 00", "GET RESPONSE")
#             print('>', str)
#
#         elif 'response' == ccevent.type:
#             if [] == ccevent.args[0]:
#                 print('<  []', "%-2X %-2X" % tuple(ccevent.args[-2:]))
#             else:
#                 print('<',
#                       toHexString(ccevent.args[0]),
#                       "%-2X %-2X" % tuple(ccevent.args[-2:]))
#
#
# # define the apdus used in this script
# GET_RESPONSE = [0XA0, 0XC0, 00, 00]
# SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
# DF_TELECOM = [0x7F, 0x10]
#
#
# # we request any type and wait for 10s for card insertion
# cardtype = AnyCardType()
# cardrequest = CardRequest(timeout=10, cardType=cardtype)
# cardservice = cardrequest.waitforcard()
#
# # create an instance of our observer and attach to the connection
# observer = TracerAndSELECTInterpreter()
# cardservice.connection.addObserver(observer)
#
#
# # connect and send APDUs
# # the observer will trace on the console
# cardservice.connection.connect()
#
# apdu = SELECT + DF_TELECOM
# response, sw1, sw2 = cardservice.connection.transmit(apdu)
# if sw1 == 0x9F:
#     apdu = GET_RESPONSE + [sw2]
#     response, sw1, sw2 = cardservice.connection.transmit(apdu)
# else:
#     print('no DF_TELECOM')
#
# import sys
# if 'win32' == sys.platform:
#     print('press Enter to continue')
#     sys.stdin.read(1)
#
# #! /usr/bin/env python
# """
# Sample script that monitors card connection events.
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
# from smartcard.CardType import AnyCardType
# from smartcard.CardRequest import CardRequest
# from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
#
# # define the apdus used in this script
# GET_RESPONSE = [0XA0, 0XC0, 00, 00]
# SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
# DF_TELECOM = [0x7F, 0x10]
#
#
# # request any card type
# cardtype = AnyCardType()
# cardrequest = CardRequest(timeout=1.5, cardType=cardtype)
# cardservice = cardrequest.waitforcard()
#
#
# # attach the console tracer
# observer = ConsoleCardConnectionObserver()
# cardservice.connection.addObserver(observer)
#
#
# # connect to the card and perform a few transmits
# cardservice.connection.connect()
#
# apdu = SELECT + DF_TELECOM
# response, sw1, sw2 = cardservice.connection.transmit(apdu)
#
# if sw1 == 0x9F:
#     apdu = GET_RESPONSE + [sw2]
#     response, sw1, sw2 = cardservice.connection.transmit(apdu)
#
#
# import sys
# if 'win32' == sys.platform:
#     print('press Enter to continue')
#
# #! /usr/bin/env python
# """
# Sample script that illustrates card connection decorators.
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
# from smartcard.CardType import AnyCardType
# from smartcard.CardRequest import CardRequest
# from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
# from smartcard.CardConnectionDecorator import CardConnectionDecorator
# from smartcard.util import toHexString
#
# # define two custom CardConnectionDecorator
# # the decorators are very simple, just to illustrate
# # shortly how several decorators can be added to the
# # card connection
#
#
# class SecureChannelConnection(CardConnectionDecorator):
#     '''This decorator is a mockup of secure channel connection.
#     It merely pretends to cypher/uncypher upon apdu transmission.'''
#
#     def __init__(self, cardconnection):
#         CardConnectionDecorator.__init__(self, cardconnection)
#
#     def cypher(self, bytes):
#         '''Cypher mock-up; you would include the secure channel logics here.'''
#         print('cyphering', toHexString(bytes))
#         return bytes
#
#     def uncypher(self, data):
#         '''Uncypher mock-up;
#         you would include the secure channel logics here.'''
#         print('uncyphering', toHexString(data))
#         return data
#
#     def transmit(self, bytes, protocol=None):
#         """Cypher/uncypher APDUs before transmission"""
#         cypheredbytes = self.cypher(bytes)
#         data, sw1, sw2 = CardConnectionDecorator.transmit(
#             self, cypheredbytes, protocol)
#         if [] != data:
#             data = self.uncypher(data)
#         return data, sw1, sw2
#
#
# class FakeATRConnection(CardConnectionDecorator):
#     '''This decorator changes the fist byte of the ATR. This is just an example
#     to show that decorators can be nested.'''
#
#     def __init__(self, cardconnection):
#         CardConnectionDecorator.__init__(self, cardconnection)
#
#     def getATR(self):
#         """Replace first BYTE of ATR by 3F"""
#         atr = CardConnectionDecorator.getATR(self)
#         return [0x3f] + atr[1:]
#
#
# # define the apdus used in this script
# GET_RESPONSE = [0XA0, 0XC0, 00, 00]
# SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
# DF_TELECOM = [0x7F, 0x10]
#
#
# # request any card type
# cardtype = AnyCardType()
# cardrequest = CardRequest(timeout=1.5, cardType=cardtype)
# cardservice = cardrequest.waitforcard()
#
# # attach the console tracer
# observer = ConsoleCardConnectionObserver()
# cardservice.connection.addObserver(observer)
#
# # attach our decorator
# cardservice.connection = FakeATRConnection(
#     SecureChannelConnection(cardservice.connection))
#
# # connect to the card and perform a few transmits
# cardservice.connection.connect()
#
# print('ATR', toHexString(cardservice.connection.getATR()))
#
# apdu = SELECT + DF_TELECOM
# response, sw1, sw2 = cardservice.connection.transmit(apdu)
#
# if sw1 == 0x9F:
#     apdu = GET_RESPONSE + [sw2]
#     response, sw1, sw2 = cardservice.connection.transmit(apdu)
#
#
# import sys
# if 'win32' == sys.platform:
#     print('press Enter to continue')
#     sys.stdin.read(1)
#
# #! /usr/bin/env python
# """Sample script for APDU error checking.
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
#
#
# from smartcard.CardType import AnyCardType
# from smartcard.CardRequest import CardRequest
# from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
#
# from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
# from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
# from smartcard.sw.ISO7816_8ErrorChecker import ISO7816_8ErrorChecker
# from smartcard.sw.ISO7816_9ErrorChecker import ISO7816_9ErrorChecker
# from smartcard.sw.SWExceptions import SWException, WarningProcessingException
#
#
# # define the apdus used in this script
# GET_RESPONSE = [0XA0, 0XC0, 00, 00]
# SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
# DF_TELECOM = [0x7F, 0x10]
#
#
# if __name__ == '__main__':
#
#     print('Insert a card within 10 seconds')
#     print('Cards without a DF_TELECOM will except')
#
#     # request any card type
#     cardtype = AnyCardType()
#     cardrequest = CardRequest(timeout=10, cardType=cardtype)
#     cardservice = cardrequest.waitforcard()
#
#     # use ISO7816-4 and ISO7816-8 error checking strategy
#     # first check iso7816_8 errors, then iso7816_4 errors
#     errorchain = []
#     errorchain = [ErrorCheckingChain(errorchain, ISO7816_9ErrorChecker())]
#     errorchain = [ErrorCheckingChain(errorchain, ISO7816_8ErrorChecker())]
#     errorchain = [ErrorCheckingChain(errorchain, ISO7816_4ErrorChecker())]
#     cardservice.connection.setErrorCheckingChain(errorchain)
#
#     # filter Warning Processing Exceptions (sw1 = 0x62 or 0x63)
#     cardservice.connection.addSWExceptionToFilter(WarningProcessingException)
#
#     # attach the console tracer
#     observer = ConsoleCardConnectionObserver()
#     cardservice.connection.addObserver(observer)
#
#     # connect to the card and perform a few transmits
#     cardservice.connection.connect()
#
#     try:
#         apdu = SELECT + DF_TELECOM
#         response, sw1, sw2 = cardservice.connection.transmit(apdu)
#
#         if sw1 == 0x9F:
#             apdu = GET_RESPONSE + [sw2]
#             response, sw1, sw2 = cardservice.connection.transmit(apdu)
#
#     except SWException as e:
#         print(str(e))
#
#     cardservice.connection.disconnect()
#
#     import sys
#     if 'win32' == sys.platform:
#         print('press Enter to continue')
#         sys.stdin.read(1)
#
# #! /usr/bin/env python
# """Sample script for APDU error checking with a custom error checker.
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
#
# from smartcard.CardType import AnyCardType
# from smartcard.CardRequest import CardRequest
# from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
#
# from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
# from smartcard.sw.ErrorChecker import ErrorChecker
# from smartcard.sw.SWExceptions import SWException
#
#
# class MyErrorChecker(ErrorChecker):
#     """Our custom error checker that will except if 0x61<sw1<0x70."""
#
#     def __call__(self, data, sw1, sw2):
#         print(sw1, sw2)
#         if 0x61 < sw1 and 0x70 > sw1:
#             raise SWException(data, sw1, sw2)
#
# # define the apdus used in this script
# GET_RESPONSE = [0XA0, 0XC0, 00, 00]
# SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
# DF_TELECOM = [0x7F, 0x10]
#
# if __name__ == '__main__':
#
#     print('Insert a card within 10 seconds')
#     print('Cards without a DF_TELECOM will except')
#
#     # request any card
#     cardtype = AnyCardType()
#     cardrequest = CardRequest(timeout=10, cardType=cardtype)
#     cardservice = cardrequest.waitforcard()
#
#     # our error checking chain
#     errorchain = []
#     errorchain = [ErrorCheckingChain([], MyErrorChecker())]
#     cardservice.connection.setErrorCheckingChain(errorchain)
#
#     # attach the console tracer
#     observer = ConsoleCardConnectionObserver()
#     cardservice.connection.addObserver(observer)
#
#     # send a few apdus; exceptions will occur upon errors
#     cardservice.connection.connect()
#
#     try:
#         SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
#         DF_TELECOM = [0x7F, 0x10]
#         apdu = SELECT + DF_TELECOM
#         response, sw1, sw2 = cardservice.connection.transmit(apdu)
#         if sw1 == 0x9F:
#             GET_RESPONSE = [0XA0, 0XC0, 00, 00]
#             apdu = GET_RESPONSE + [sw2]
#             response, sw1, sw2 = cardservice.connection.transmit(apdu)
#     except SWException as e:
#         print(e, "%x %x" % (e.sw1, e.sw2))
#
#         cardservice.connection.disconnect()
#
#     import sys
#     if 'win32' == sys.platform:
#         print('press Enter to continue')
#         sys.stdin.read(1)
#
# #! /usr/bin/env python
# """
# Sample script that demonstrates how to create a custom CardType.
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
# from smartcard.CardType import CardType
# from smartcard.CardRequest import CardRequest
# from smartcard.util import toHexString
#
#
# class DCCardType(CardType):
# # define our custom CardType
# # this card type defines direct convention card (first atr byte equal to 0x3b)
#
#     def matches(self, atr, reader=None):
#         return atr[0] == 0x3B
#
#
# # request a direct convention card
# cardtype = DCCardType()
# cardrequest = CardRequest(timeout=1, cardType=cardtype)
# cardservice = cardrequest.waitforcard()
#
#
# # connect and print atr and reader
# cardservice.connection.connect()
# print(toHexString(cardservice.connection.getATR()))
# print(cardservice.connection.getReader())
#
#
# import sys
# if 'win32' == sys.platform:
#     print('press Enter to continue')
#     sys.stdin.read(1)
#
# #! /usr/bin/env python
# """
# Sample script that monitors smartcard readers.
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
#
# from time import sleep
#
# from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver
#
#
# class printobserver(ReaderObserver):
#     """A simple reader observer that is notified
#     when readers are added/removed from the system and
#     prints the list of readers
#     """
#
#     def update(self, observable, actions):
#         (addedreaders, removedreaders) = actions
#         print("Added readers", addedreaders)
#         print("Removed readers", removedreaders)
#
# if __name__ == '__main__':
#     print("Add or remove a smartcard reader to the system.")
#     print("This program will exit in 10 seconds")
#     print("")
#     readermonitor = ReaderMonitor()
#     readerobserver = printobserver()
#     readermonitor.addObserver(readerobserver)
#
#     sleep(10)
#
#     # don't forget to remove observer, or the
#     # monitor will poll forever...
#     readermonitor.deleteObserver(readerobserver)
#
#     import sys
#     if 'win32' == sys.platform:
#         print('press Enter to continue')
#         sys.stdin.read(1)
#
# #! /usr/bin/env python
# """
# Sample script that monitors smartcard insertion/removal.
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
# from time import sleep
#
# from smartcard.CardMonitoring import CardMonitor, CardObserver
# from smartcard.util import toHexString
#
#
# # a simple card observer that prints inserted/removed cards
# class PrintObserver(CardObserver):
#     """A simple card observer that is notified
#     when cards are inserted/removed from the system and
#     prints the list of cards
#     """
#
#     def update(self, observable, actions):
#         (addedcards, removedcards) = actions
#         for card in addedcards:
#             print("+Inserted: ", toHexString(card.atr))
#         for card in removedcards:
#             print("-Removed: ", toHexString(card.atr))
#
# if __name__ == '__main__':
#     print("Insert or remove a smartcard in the system.")
#     print("This program will exit in 10 seconds")
#     print("")
#     cardmonitor = CardMonitor()
#     cardobserver = PrintObserver()
#     cardmonitor.addObserver(cardobserver)
#
#     sleep(10)
#
#     # don't forget to remove observer, or the
#     # monitor will poll forever...
#     cardmonitor.deleteObserver(cardobserver)
#
#     import sys
#     if 'win32' == sys.platform:
#         print('press Enter to continue')
#         sys.stdin.read(1)
#
# #! /usr/bin/env python
# """
# Sample script to illustrate toHexString() utility method
#
# __author__ = "http://www.gemalto.com"
#
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# """
#
# from smartcard.util import *
#
#
# print(40 * '-')
# bytes = [59, 101, 0, 0, 156, 17, 1, 1, 3]
# print('bytes = [59, 101, 0, 0, 156, 17, 1, 1, 3]')
# print('toHexString(bytes) =', toHexString(bytes))
# print('toHexString(bytes, COMMA) =', toHexString(bytes, COMMA))
# print('toHexString(bytes, PACK) =', toHexString(bytes, PACK))
# print('toHexString(bytes, HEX) =', toHexString(bytes, HEX))
# print('toHexString(bytes, HEX | COMMA) =', toHexString(bytes, HEX | COMMA))
# print('toHexString(bytes, HEX | UPPERCASE) =',
#       toHexString(bytes, HEX | UPPERCASE))
# print('toHexString(bytes, HEX | UPPERCASE | COMMA) =',
#       toHexString(bytes, HEX | UPPERCASE | COMMA))
#
#
# print(40 * '-')
# bytes = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
# print('bytes = [ 0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03 ]')
# print('toHexString(bytes, COMMA) =', toHexString(bytes, COMMA))
# print('toHexString(bytes) =', toHexString(bytes))
# print('toHexString(bytes, PACK) =', toHexString(bytes, PACK))
# print('toHexString(bytes, HEX) =', toHexString(bytes, HEX))
# print('toHexString(bytes, HEX | COMMA) =', toHexString(bytes, HEX | COMMA))
# print('toHexString(bytes, HEX | UPPERCASE) =',
#       toHexString(bytes, HEX | UPPERCASE))
# print('toHexString(bytes, HEX | UPPERCASE | COMMA) =',
#       toHexString(bytes, HEX | UPPERCASE | COMMA))
#
#
# import sys
# if 'win32' == sys.platform:
#     print('press Enter to continue')
#     sys.stdin.read(1)

#! /usr/bin/env python
"""
Sample for python PCSC wrapper module: send a Control Code to a card or
reader
__author__ = "Ludovic Rousseau"
Copyright 2009-2010 Ludovic Rousseau
Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr
This file is part of pyscard.
pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.
pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""


from smartcard.scard import *
from smartcard.util import toASCIIBytes
from smartcard.pcsc.PCSCExceptions import *
import sys


def can_do_verify_pin(hCard):
    FEATURE_VERIFY_PIN_DIRECT = 6
    return parse_get_feature_request(hCard, FEATURE_VERIFY_PIN_DIRECT)


def can_do_modify_pin(hCard):
    FEATURE_MODIFY_PIN_DIRECT = 7
    return parse_get_feature_request(hCard, FEATURE_MODIFY_PIN_DIRECT)


def parse_get_feature_request(hCard, feature):
    # check the reader can do a verify pin
    CM_IOCTL_GET_FEATURE_REQUEST = SCARD_CTL_CODE(3400)
    hresult, response = SCardControl(hcard, CM_IOCTL_GET_FEATURE_REQUEST, [])
    if hresult != SCARD_S_SUCCESS:
        raise BaseSCardException(hresult)
    print(response)
    while len(response) > 0:
        tag = response[0]
        if feature == tag:
            return (((((response[2] << 8) +
                    response[3]) << 8) +
                    response[4]) << 8) + response[5]
        response = response[6:]


def verifypin(hCard, control=None):
    if control is None:
        control = can_do_verify_pin(hCard)
        if control is None:
            raise Exception("Not a pinpad")

    command = [0x00,  # bTimerOut
               0x00,  # bTimerOut2
               0x82,  # bmFormatString
               0x04,  # bmPINBlockString
               0x00,  # bmPINLengthFormat
               0x08, 0x04,  # wPINMaxExtraDigit
               0x02,  # bEntryValidationCondition
               0x01,  # bNumberMessage
               0x04, 0x09,  # wLangId
               0x00,  # bMsgIndex
               0x00, 0x00, 0x00,  # bTeoPrologue
               13, 0, 0, 0,  # ulDataLength
               0x00, 0x20, 0x00, 0x00, 0x08, 0x30, 0x30, 0x30, 0x30, 0x30,
               0x30, 0x30, 0x30]  # abData
    hresult, response = SCardControl(hcard, control, command)
    if hresult != SCARD_S_SUCCESS:
        raise BaseSCardException(hresult)
    return hresult, response

try:
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult != SCARD_S_SUCCESS:
        raise EstablishContextException(hresult)
    print('Context established!')

    try:
        hresult, readers = SCardListReaders(hcontext, [])
        if hresult != SCARD_S_SUCCESS:
            raise ListReadersException(hresult)
        print('PCSC Readers:', readers)

        if len(readers) < 1:
            raise Exception("No smart card readers")

        for zreader in readers:

            print('Trying to Control reader:', zreader)

            try:
                hresult, hcard, dwActiveProtocol = SCardConnect(
                    hcontext, zreader, SCARD_SHARE_SHARED,
                    SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
                if hresult != SCARD_S_SUCCESS:
                    raise BaseSCardException(hresult)
                print('Connected with active protocol', dwActiveProtocol)

                try:
                    SELECT = [0x00, 0xA4, 0x04, 0x00, 0x06, 0xA0, 0x00,
                              0x00, 0x00, 0x18, 0xFF]
                    hresult, response = SCardTransmit(
                        hcard,
                        dwActiveProtocol,
                        SELECT)
                    if hresult != SCARD_S_SUCCESS:
                        raise BaseSCardException(hresult)

                    cmd_verify = can_do_verify_pin(hcard)
                    if (cmd_verify):
                        print("can do verify pin: 0x%08X" % cmd_verify)

                    cmd_modify = can_do_modify_pin(hcard)
                    if (cmd_modify):
                        print("can do modify pin: 0x%08X" % cmd_modify)

                    hresult, response = verifypin(hcard, cmd_verify)
                    print('Control:', response)
                finally:
                    hresult = SCardDisconnect(hcard, SCARD_UNPOWER_CARD)
                    if hresult != SCARD_S_SUCCESS:
                        raise BaseSCardException(hresult)
                    print('Disconnected')

            except error as message:
                print(error, message)

    finally:
        hresult = SCardReleaseContext(hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise ReleaseContextException(hresult)
        print('Released context.')

except error as e:
    print(e)

if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)
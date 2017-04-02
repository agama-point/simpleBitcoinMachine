#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import time
from builtins import input

from PIL import Image

from octopusEngine.simpleBitcoinMachine.currency import (
    BitcoinCurrency, InvalidTransactionValue, LitecoinCurrency, NotEnoughTransactionConfirmations,
    UncomfirmedTransaction, convert_currency)


def emulator(args=None):
    curr = input("What currency do you want to use? (BTC, LTC): ")
    if curr not in ["BTC", "LTC"]:
        print("Invalid currency")
        sys.exit(1)

    if curr == "BTC":
        curr_obj = BitcoinCurrency(address=input("Wallet: "))
    if curr == "LTC":
        curr_obj = LitecoinCurrency(address=input("Wallet: "))

    amount = float(input("Enter the amount in %s: " % curr))
    print("Obtaining convert rates...")
    print("USD: %f $" % convert_currency(curr, "USD", amount))
    print("CZK: %f Kc" % convert_currency(curr, "CZK", amount))
    if curr == "BTC":
        qrGet="bitcoin:" + curr_obj.address + "?amount=" + str(amount)
    if curr == "LTC":
        qrGet="litecoin:" + curr_obj.address + "?amount=" + str(amount)

    os.system('qrencode -o qrcode.png ' + qrGet)
    img=Image.open('qrcode.png')
    img.show(title="QR Payment")

    print("Waiting for payment 30s.")
    time.sleep(30)

    while True:
        trans=curr_obj.get_last_transaction()
        try:
            out = curr_obj.is_transaction_valid(trans, amount)
            if out:
                print("Payment recieved from %s" % (
                    curr_obj.get_address_of_author_of_transaction(trans)))
                break
        except UncomfirmedTransaction:
            print("ERR: transaction is not yet confirmed!")
        except NotEnoughTransactionConfirmations:
            print("ERR: The transaction haven't get yet enough confirmations. "
                  "Have %d out of 2" % (trans["confirmations"]))
        except InvalidTransactionValue as e:
            print(str(e))
        except AttributeError as e:
            if trans is None:
                print("ERR: No transactions yet.")
            else:
                raise e
        print("Sleeping 10s for another check.")
        time.sleep(10)

if __name__ == "__main__":
    emulator()

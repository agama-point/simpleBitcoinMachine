"""Library for handling operations with cryptocurrencies."""
from blockr.api import Api

from octopusEngine.simpleBitcoinMachine.utils import first, parse_utc

class TransactionException(Exception):
    """Base Exception for Transaction errors."""

    pass

class NotEnoughTransactionConfirmations(TransactionException):
    """Error during validation. Not enough confirmations."""

    confirmations = 0
    wanted = None

    def __init__(self, confirmations, wanted):
        """Get number of confirmations and wanted number."""
        self.confirmations = confirmations
        self.wanted = wanted

    def __str__(self):
        """Convert Exception to str."""
        return "Transaction doesn't have wanted amount of confirmations %d out of %d" % (
            self.confirmations, self.wanted)

class UncomfirmedTransaction(NotEnoughTransactionConfirmations):
    """Error during validation. The transaction is uncomfirmed."""

    def __init__(self):
        """Initialize UncomfirmedTransaction."""
        pass # override parent __init__

    def __str__(self):
        """Convert Exception to str."""
        return "This transaction is unverified."

class InvalidTransactionValue(TransactionException):
    """The transaction doesn't have wanted amount."""

    value = None
    wanted = None

    def __init__(self, value, wanted):
        """Get obtained value and wanted value."""
        self.value = value
        self.wanted = wanted

    def __str__(self):
        """Convert Exception to str."""
        return "Transaction is for different price wanted %d, but transaction gives only %d" % (
            self.wanted, self.price
        )

class BlockrCurrency(object):
    """API for Blockr.

    parameters:
    * currency str: Name of currency used.
    """

    address = None
    api = None
    currency = None

    def __init__(self, address):
        """Initialize BlockrCurrency.

        parameters:
        * address str: The default address.
        """
        self.address = address
        self.api = Api(self.currency, use_https=True)

    def _get_my_output(self, transaction, address=None):
        return first((o for o in transaction["trade"]["vouts"]
                      if o["address"] == (address or self.address)), {})

    def get_address(self, address=None):
        """Get information about adress.

        parameters:
        * address str: if specified this address use it instead of self.address
        """
        return self.api.address(address or self.address)["data"]

    def get_last_transaction(self, address=None):
        """Get last transaction.

        parameters:
        * address str: passes to self.get_address()
        """
        return self.get_address(address)["last_tx"]

    def get_transaction(self, transaction_id):
        """Get transaction out of it's ID.

        parameters:
        * transaction_id str: ID of transaction
        """
        return self.api.transaction(transaction_id)["data"]

    def _use_or_get_transaction(self, transaction):
        if type(transaction) == str:
            return self.get_transaction(transaction)
        elif type(transaction) == dict:
            return transaction
        else:
            raise TypeError

    def is_transaction_valid(self, transaction, value, confirmations=2):
        """Check if transaction is valid.

        parameters:
        * transaction (transaction dict)|str: transaction dictionary or transaction_id
        * value                        float: Amount we want
        * confirmations                  int: Minimal number of confirmations for
                                              transaction default 2

        Exceptions:
        * NotEnoughTransactionConfirmations - Less than required confirmations
        * InvalidTransactionValue           - Transaction value is lesser
        * UnconfirmedTransaction            - Transaction isn't confirmed yet.
        """
        tx = self._use_or_get_transaction(transaction)
        output = self._get_my_output(tx)
        # The amount can be higher e.g. Tip
        if output.get("amount", None) >= value and \
                transaction["confirmations"] >= confirmations and \
                not transaction["is_unconfirmed"]:
            return True
        elif not transaction["confirmations"] >= confirmations:
            raise NotEnoughTransactionConfirmations(transaction["confirmations"], confirmations)
        elif not output.get("amount", None) >= value:
            raise InvalidTransactionValue(output.get("amount", 0), value)
        elif transaction["is_unconfirmed"]:
            raise UncomfirmedTransaction
        else:
            print(output.get("amount", None), value, transaction["confirmations"] >= confirmations)

    def get_address_of_author_of_transaction(self, transaction):
        """Get adress of author of transaction.

        parameters:
        * transaction (transaction dict)|str: transaction dictionary or transaction_id
        """
        return self._use_or_get_transaction(transaction)["trade"]["vins"][0]["address"]

    def get_time_of_transaction(self, transaction):
        """Get datetime.datetime of transaction.

        parameters:
        * transaction (transaction dict)|str: transaction dictionary or transaction_id
        """
        return parse_utc(self._use_or_get_transaction(transaction)["time_utc"])

    def get_exchange_rates(self):
        """Get exchange_rate for Class currency."""
        return self.api.exchange_rate()["data"]

    def get_exchange_rate_time(self, exchange_rate=None):
        """Get time of update of exchange_rate.

        parameters:
        * exchange_rate exchange_rate dict: Exchange rate (optional)
        """
        return parse_utc((exchange_rate or self.get_exchange_rates())["updated_utc"])

    def get_exchange_rate_for_currency(self, currency, exchange_rate=None):
        """Get exchange_rate between Class currency and selected currency.

        parameters:
        * currency                  string: Name of selected currency ("CZK", "USD")
        * exchange_rate exchange_rate dict: Exchange rate (optional)
        """
        if exchange_rate is None:
            exchange_rate = self.get_exchange_rates()
        return exchange_rate["rates"][
            currency.upper() if currency != exchange_rate["base"] else "BTC"]

    def exchange_currency(self, currency, value, exchange_rate=None):
        """Exchange between Class currency and selected currency.

        Formula:
            value * (1.0 / rate) = x

        parameters:
        * currency                  string: Selected currency
        * value                      float: Number of coins of Class currency
        * exchange_rate exchange_rate dict: Exchange rate (optional)
        """
        return value * (1.0 / self.get_exchange_rate_for_currency(exchange_rate, currency))

class BitcoinCurrency(BlockrCurrency):
    """Bitcoin currency at Blockr.

    For more see BlockrCurrency class.
    """

    currency = "Bitcoin"

class LitecoinCurrency(BlockrCurrency):
    """Litecoin currency at Blockr.

    For more see BlockrCurrency class.
    """

    currency = "Litecoin"

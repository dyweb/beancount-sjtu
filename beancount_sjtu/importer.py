"""Importer of jAccount API for E-card Transaction.
"""

import json
from datetime import datetime
from enum import Enum

from beancount.core import data
from beancount.core.amount import Amount, Decimal
from beancount.ingest import importer

PAYEE = '上海交通大学'


class Assets(Enum):
    FIXME = 'Assets:FIXME'


class Description(Enum):
    SUBSIDIES = '补助'
    CORRESPONDENCE = '建立银行卡对应关系'
    CARD_CALIBRATION = '卡片校正'
    INFORMATION_CHANGE = '持卡人信息变更'
    ELECTRONIC_ACCOUNT_OPENING = '电子账户开户'
    ACCOUNT_CONSOLIDATION_IN = '账户合并（转入）'
    ACCOUNT_CONSOLIDATION_OUT = '账户合并（转出）'

    ALIPAY = '支付宝转账'

    RECEIVING_SUBSIDIES = '领取补助'
    CARDHOLDER_SPENDING = '持卡人消费'
    BANK_CARD_SPENDING = '银行卡消费'


class SJTUECardImporter(importer.ImporterProtocol):
    def __init__(
        self,
        account,
        category,
    ):
        self.account = account
        self.category = category

    def identify(self, file):
        """Return true if this importer matches the given file.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          A boolean, true if this importer can handle this file.
        """
        with open(file.name, 'r') as f:
            jsondata = json.load(f)
            return jsondata['errno'] == 0 and \
                jsondata['error'] == 'success' and \
                jsondata['total'] > 0

    def extract(self, file, existing_entries=None):
        """Extract transactions from a file.

        If the importer would like to flag a returned transaction as a known
        duplicate, it may opt to set the special flag "__duplicate__" to True,
        and the transaction should be treated as a duplicate by the extraction
        code. This is a way to let the importer use particular information about
        previously imported transactions in order to flag them as duplicates.
        For example, if an importer has a way to get a persistent unique id for
        each of the imported transactions. (See this discussion for context:
        https://groups.google.com/d/msg/beancount/0iV-ipBJb8g/-uk4wsH2AgAJ)

        Args:
          file: A cache.FileMemo instance.
          existing_entries: An optional list of existing directives loaded from
            the ledger which is intended to contain the extracted entries. This
            is only provided if the user provides them via a flag in the
            extractor program.
        Returns:
          A list of new, imported directives (usually mostly Transactions)
          extracted from the file.
        """
        with open(file.name, 'r') as f:
            entries = []

            jsondata = json.load(f)
            for index, entity in enumerate(jsondata['entities']):
                description = Description(entity['description'])
                # FIXME:
                if description not in [
                        Description.RECEIVING_SUBSIDIES,
                        Description.CARDHOLDER_SPENDING,
                        Description.BANK_CARD_SPENDING
                ]:
                    continue

                meta = data.new_metadata(file.name, index)
                _datetime = datetime.fromtimestamp(entity['dateTime'] / 1000)

                meta['time'] = str(_datetime.time())

                system, merchant = entity['system'], entity['merchant']
                if not (system == '' and merchant == ''):
                    meta['system'] = system
                    meta['merchant'] = merchant

                amount = Amount(
                    Decimal(entity['amount']).quantize(Decimal('1.00')), 'CNY')

                postings = [
                    data.Posting(
                        self.account,
                        amount,
                        None,
                        None,
                        None,
                        None,
                    ),
                ]

                account = Assets.FIXME.value
                if description in [
                        Description.CARDHOLDER_SPENDING,
                        Description.BANK_CARD_SPENDING
                ]:
                    account = self.category

                postings.append(
                    data.Posting(
                        account,
                        -amount,
                        None,
                        None,
                        None,
                        None,
                    ))

                txn = data.Transaction(meta, _datetime.date(), self.FLAG,
                                       PAYEE, description.value,
                                       data.EMPTY_SET, data.EMPTY_SET,
                                       postings)
                entries.append(txn)
            return entries

    def file_account(self, file):
        """Return an account associated with the given file.

        Note: If you don't implement this method you won't be able to move the
        files into its preservation hierarchy; the bean-file command won't
        work.

        Also, normally the returned account is not a function of the input
        file--just of the importer--but it is provided anyhow.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          The name of the account that corresponds to this importer.
        """

    def file_name(self, file):
        """A filter that optionally renames a file before filing.

        This is used to make tidy filenames for filed/stored document files. If
        you don't implement this and return None, the same filename is used.
        Note that if you return a filename, a simple, RELATIVE filename must be
        returned, not an absolute filename.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          The tidied up, new filename to store it as.
        """

    def file_date(self, file):
        """Attempt to obtain a date that corresponds to the given file.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          A date object, if successful, or None if a date could not be extracted.
          (If no date is returned, the file creation time is used. This is the
          default.)
        """

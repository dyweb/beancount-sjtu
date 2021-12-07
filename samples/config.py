#!/usr/bin/env python3

import beancount.ingest.extract
from beancount_sjtu.importer import SJTUECardImporter

beancount.ingest.extract.HEADER = ''

CONFIG = [
    SJTUECardImporter(account='Assets:CN:SVC:SJTU',
                      category='Expenses:SJTU:Cafeteria'),
]

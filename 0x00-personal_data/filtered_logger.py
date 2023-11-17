#!/usr/bin/env python3
"""0x00. Personal data"""
import logging
import re
from typing import List
import typing
import mysql.connector
import os

PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    FIELDS_FORMAT = "({})".format('|'.join(PII_FIELDS))

    def __init__(self, fields: typing.List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records using filter_datum
            """
        return filter_datum(self.FIELDS_FORMAT, self.REDACTION,
                            super(RedactingFormatter).format(record),
                            self.SEPARATOR)


def get_db(self) -> mysql.connector.connection.MySQLConnection:
    """returns a MySQLConnection object"""
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD'),
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
    )

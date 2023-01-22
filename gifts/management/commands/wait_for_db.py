"""
Django command to wait for the database to be available
"""

from django.core.management.base import BaseCommand
import time
from django.db import Error
from MySQLdb._exceptions import OperationalError
from django.db import connection


class Command(BaseCommand):

  def handle(self, *args, **options):
    self.stdout.write('Waiting for database')
    db_up = False
    while db_up is False:
      try:
        connection.connect()
        db_up = True
      except (OperationalError, Error):
        self.stdout.write('Database unavailable, waiting 1 second...')
        time.sleep(1)

    self.stdout.write(self.style.SUCCESS('Database available!'))

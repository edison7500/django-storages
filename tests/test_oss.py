try:
    from unittest import mock
except ImportError:  # Python 3.2 and below
    import mock

import datetime

from django.test import TestCase
from django.core.files.base import ContentFile


from storages.backends import oss
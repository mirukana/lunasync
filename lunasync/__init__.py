# Copyright 2018 miruka
# This file is part of lunasync, licensed under LGPLv3.

# pylint: disable=wrong-import-position

from copy import copy

import lunafind

LOG = copy(lunafind.LOG)

from .__about__ import __doc__
from . import config, savedata
config.reload()

from .main import sync

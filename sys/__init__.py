# The display order is very important in __init__.py
# - The module that is called first must be listed at the bottom.
#

from .init import AppInit as app_init
from .init import PltInit as plt_init



# This is to make imports easier from main.py
# It lets you fetch the level pages straight from the levels file without needing to specify level1.py, level2.py, etc.

from .level1 import *
from .level2 import *
from .level3 import *
from .level4 import *
from .level5 import *
from .level6 import *
from .level7 import *
from .level8 import *
from .level9 import *
from .level10 import *

__all__ = ['Level1Page', 'Level2Page', 'Level3Page', 'Level4Page', 'Level5Page',
           'Level6Page', 'Level7Page', 'Level8Page', 'Level9Page', 'Level10Page']

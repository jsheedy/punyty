import logging

import numpy as np
from skimage.draw import line_aa, line

from .renderer import Renderer
from .. import geom

logger = logging.getLogger(__name__)


class TTYRenderer(Renderer):
    """ renders to a tty """
    pass
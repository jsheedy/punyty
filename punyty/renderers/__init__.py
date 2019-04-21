import logging
from .array_renderer import ArrayRenderer


logger = logging.getLogger(__name__)


try:
    from .sdl_renderer import SDLRenderer
except ImportError:
    logger.warning(f'SDLRenderer unable to import SDL. Try: pip install PySDL')

from .tty_renderer import TTYRenderer
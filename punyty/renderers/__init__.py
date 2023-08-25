import logging


logger = logging.getLogger(__name__)


try:
    from .sdl_renderer import SDLRenderer
except ImportError:
    logger.warning("SDLRenderer unable to import SDL. Try: pip install PySDL")

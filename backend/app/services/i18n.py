# ============================
# backend/app/core/i18n.py
# ============================
from pathlib import Path
from babel import Locale
from babel.support import Translations
from fastapi import Request
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Store translations
translations = {}


def setup_i18n():
    """
    Configure internationalization
    """
    locales_dir = Path(__file__).parent.parent / "locales"
    
    for lang in settings.SUPPORTED_LANGUAGES:
        try:
            trans = Translations.load(locales_dir, [lang])
            translations[lang] = trans
            logger.info(f"Loaded translations for {lang}")
        except Exception as e:
            logger.error(f"Failed to load translations for {lang}: {e}")
            # Use empty translations as fallback
            translations[lang] = Translations()


def get_locale(request: Request) -> str:
    """
    Get locale from request headers or user preference
    """
    # Try to get from Accept-Language header
    accept_language = request.headers.get("Accept-Language", "")
    if accept_language:
        try:
            locale = Locale.parse(accept_language.split(",")[0].split("-")[0])
            if locale.language in settings.SUPPORTED_LANGUAGES:
                return locale.language
        except:
            pass
    
    # Try to get from user preference (if authenticated)
    if hasattr(request.state, "user") and request.state.user:
        return request.state.user.preferred_language
    
    # Default to configured default language
    return settings.DEFAULT_LANGUAGE


def get_translation(request: Request) -> Translations:
    """
    Get translation for current request
    """
    locale = get_locale(request)
    return translations.get(locale, translations[settings.DEFAULT_LANGUAGE])
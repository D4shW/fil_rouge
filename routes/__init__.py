from .main import bp as main_bp
from .auth import bp as auth_bp
from .cart import bp as cart_bp
from .api import bp as api_bp
from .admin import bp as admin_bp

__all__ = ['main_bp', 'auth_bp', 'cart_bp', 'api_bp', 'admin_bp']

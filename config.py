import os
import secrets

_base = os.path.dirname(os.path.abspath(__file__))
_instance = os.path.join(_base, 'instance')
os.makedirs(_instance, exist_ok=True)

_key_file = os.path.join(_instance, 'secret.key')
if not os.path.exists(_key_file):
    with open(_key_file, 'w') as _f:
        _f.write(secrets.token_hex(32))
with open(_key_file) as _f:
    _stored_key = _f.read().strip()


class Config:
    INSTANCE_PATH = _instance
    DB_PATH = os.path.join(_instance, 'store.db')
    SECRET_KEY = os.environ.get('SECRET_KEY', _stored_key)
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin1234')

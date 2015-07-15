try:
    #python2
    from secret_client import SecretClient
except ImportError:
    #python3
    from .secret_client import SecretClient
    

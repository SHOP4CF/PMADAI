from functools import wraps, partial
from envyaml import EnvYAML


class Auth:
    """
    This class is responsible for the appropriate handling of the development and production environment.
    When running the application in the development environment, allows you to log in a test user.
    """
    CONFIG = EnvYAML("../config.yml")

    @classmethod
    def valid_only_on_dev_env(cls, func=None):
        """
        This method is actually a decorator, which wraps the application methods that checks system credentials with a test user.
        When the application is run in the development environment and the login validation function is called -
        this decorator will check correctness of test user credentials. In production environment, login will fail.

        Parameters
        ----------
        func
            function/method that check test user credentials.
        """
        if not func:
            return partial(cls.valid_only_on_dev_env)

        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.CONFIG['general']['deployment_env'].lower() == 'develop':
                return func(*args, **kwargs)
            elif cls.CONFIG['general']['deployment_env'].lower() == 'production':
                return False

        return wrapper

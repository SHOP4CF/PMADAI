from functools import wraps, partial
from envyaml import EnvYAML


class OracleDB:
    """
    This class is responsible for the appropriate handling of the development and production environment.
    When running the application in the development environment,
    this class removes the tables from the database, in a tight case leaves the tables unchanged.
    """

    CONFIG = EnvYAML("../config.yml")

    def __init__(self, connection, sqlcode, db_component):
        """
        Parameters
        ----------
        connection
            connection to database
        sqlcode
            SQL code that reports an exception when removing a database item that does not exist in this database.
            It varies depending on the item being deleted.
            The sqlcode -2289 matches "ORA-02289: sequence does not exist"
            The sqlcode -942 matches "ORA-00942: table or view does not exist"
            The sqlcode -4080 matches "ORA-04080: trigger not exist"
            Error with the specified code is caught if the component being deleted does not exist in the database.
        db_component
            name od database component {'table', 'sequence'}
        """
        self.connection = connection
        self.sqlcode = sqlcode
        self.db_component = db_component

    @classmethod
    def drop_table_if_on_dev_env(cls, func=None, component_names=None):
        """
        This method is actually a decorator, which wraps the application methods that make up the database schemas.
        When the application is run in the development environment and the schema creation method is called -
        this decorator will handle in first order removal of this schema from the database.

        Parameters
        ----------
        func
            function/method that creates a database component
        component_names
            creating component name - 'table'
        """
        if not func:
            return partial(cls.drop_table_if_on_dev_env, component_names=component_names)

        @wraps(func)
        def wrapper(*args, **kwargs):
            connection = cls.get_connection(args[0])
            obj = cls(connection=connection, sqlcode=-942, db_component='table')
            if cls.CONFIG['general']['deployment_env'].lower() == 'develop':
                obj.dev_environment(component_names)
            elif cls.CONFIG['general']['deployment_env'].lower() == 'production':
                obj.prod_environment(component_names)
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def drop_sequence_if_on_dev_env(cls, func=None, component_names=None):
        """
        This method is actually a decorator, which wraps the application methods that make up the database schemas.
        When the application is run in the development environment and the schema creation method is called -
        this decorator will handle in first order removal of this schema from the database.

        Parameters
        ----------
        func
            function/method that creates a database component
        component_names
            creating component name - 'sequence'
        """
        if not func:
            return partial(cls.drop_sequence_if_on_dev_env, component_names=component_names)

        @wraps(func)
        def wrapper(*args, **kwargs):
            connection = cls.get_connection(args[0])
            obj = cls(connection=connection, sqlcode=-2289, db_component='sequence')
            if cls.CONFIG['general']['deployment_env'].lower() == 'develop':
                obj.dev_environment(component_names)
            elif cls.CONFIG['general']['deployment_env'].lower() == 'production':
                obj.prod_environment(component_names)
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def drop_trigger_if_on_dev_env(cls, func=None, component_names=None):
        """
        This method is actually a decorator, which wraps the application methods that make up the database schemas.
        When the application is run in the development environment and the schema creation method is called -
        this decorator will handle in first order removal of this schema from the database.

        Parameters
        ----------
        func
            function/method that creates a database component
        component_names
            creating component name - 'sequence'
        """
        if not func:
            return partial(cls.drop_sequence_if_on_dev_env, component_names=component_names)

        @wraps(func)
        def wrapper(*args, **kwargs):
            connection = cls.get_connection(args[0])
            obj = cls(connection=connection, sqlcode=-4080, db_component='trigger')
            if cls.CONFIG['general']['deployment_env'].lower() == 'develop':
                obj.dev_environment(component_names)
            elif cls.CONFIG['general']['deployment_env'].lower() == 'production':
                obj.prod_environment(component_names)
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_connection(source_class):
        """
        This method gets a connection to the database.
        It varies depending on the source class implementing database operations.
        """
        class_attributes = dir(source_class)
        if 'connection' in class_attributes:
            return source_class.connection
        else:
            return source_class.pool.acquire()

    def dev_environment(db_obj, component_names):
        """
        Method called when the application is running in the development environment.
        """
        component_names = db_obj.extend_dimension_if_required(component_names)

        for component_name in component_names:
            db_obj.drop_component(component_name=component_name)

    def prod_environment(db_obj, creation_schemas):
        """
        Method called when the application is running in the production environment.
        """
        pass

    @staticmethod
    def extend_dimension_if_required(creation_schemas):
        """
        This method adds a dimension to the passed data.
        It boils down to creating a list when one value is given in the form of string.
        """
        if not isinstance(creation_schemas, list):
            creation_schemas = [creation_schemas]
        return creation_schemas

    def drop_component(self, component_name):
        template = f"""begin
                        execute immediate 'drop {self.db_component} {component_name.upper()}';
                        exception when others then
                          if sqlcode <> {self.sqlcode} then
                            raise;
                          end if;
                          commit;
                        end;"""
        self.execute(template)

    def execute(self, template):
        with self.connection.cursor() as cursor:
            cursor.execute(template)

from p_modules.database.modules import database


# Imports from module into the Database Class. Allowing multiple Modules in one File, to make usage easier and cleaner.
def _import_all(arg_module, arg_class):
    for name in getattr(arg_module, "__all__", (name for name in vars(arg_module) if name[:1] != "_")):
        setattr(arg_class, name, vars(arg_module)[name])


class Database:
    pass


_import_all(database, Database)

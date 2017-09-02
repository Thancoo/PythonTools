class Field(object):
    def __init__(self, name, column_type, primary_key,not_null, default,format_symbol,is_identity,is_dbfield):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.not_null=not_null
        self.default = default
        self.format_symbol=format_symbol
        self.is_identity=is_identity
        self.is_dbfield=is_dbfield
    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None,not_null=False, ddl='varchar(100)',format_symbol='%s',is_identity=False,is_dbfield=True):
        super().__init__(name, ddl, primary_key,not_null, default,format_symbol,is_identity,is_dbfield)
class IntField(Field):
    def __init__(self, name=None, primary_key=False, default=None,not_null=False, ddl='int',format_symbol='%d',is_identity=False,is_dbfield=True):
        super().__init__(name, ddl, primary_key,not_null, default,format_symbol,is_identity,is_dbfield)
class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=None,not_null=False, ddl='decimer',format_symbol='%f',is_identity=False,is_dbfield=True):
        super().__init__(name, ddl, primary_key,not_null, default,format_symbol,is_identity,is_dbfield)
class BooleanField(Field):
    def __init__(self, name=None, primary_key=False, default=None,not_null=False, ddl='bit',format_symbol='%d',is_identity=False,is_dbfield=True):
        super().__init__(name, ddl, primary_key,not_null, default,format_symbol,is_identity,is_dbfield)
class DateTimeField(Field):
    def __init__(self, name=None, primary_key=False, default=None,not_null=False, ddl='datetime',format_symbol='%s',is_identity=False,is_dbfield=True):
        super().__init__(name, ddl, primary_key,not_null, default,format_symbol,is_identity,is_dbfield)
class DateField(Field):
    def __init__(self, name=None, primary_key=False, default=None,not_null=False, ddl='date',format_symbol='%s',is_identity=False,is_dbfield=True):
        super().__init__(name, ddl, primary_key,not_null, default,format_symbol,is_identity,is_dbfield)
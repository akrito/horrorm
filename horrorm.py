from cursors import connect

class F(object):
    """
    A wrapper around F(name). Using __getattr__ as a constructor? Horrible.
    """

    def __getattr__(self, field_name):
        return Field(field_name)

f = F()

class Field(object):
    """
    Fields override arithmetic to generate conditions? Horrible.
    """

    def __init__(self, field_name):
        self.field_name = field_name

    def sql(self, param):
        return str(self)

    def __str__(self):
        return self.field_name

    def __eq__(self, rhs):
        return Where(self, '=', rhs)

    def __ne__(self, rhs):
        return Where(self, '!=', rhs)

    def __lshift__(self, rhs):
        # <<
        return Where(self, 'IN', rhs)
    
    def __gt__(self, rhs):
        return Where(self, '>', rhs)

    def __ge__(self, rhs):
        return Where(self, '>=', rhs)

    def __lt__(self, rhs):
        return Where(self, '<', rhs)

    def __le__(self, rhs):
        return Where(self, '<=', rhs)

    def __mod__(self, rhs):
        # %
        return Where(self, 'LIKE', rhs)

    def __getattr__(self, attr):
        return Field('%s.%s' % (self.field_name, attr))

    def params(self):
        return []

class Where(object):

    def __init__(self, lhs, connector, rhs):
        self.lhs = lhs
        self.connector = connector
        self.rhs = rhs

    def __invert__(self):
        # ~
        return Where(None, 'NOT', self)

    def __and__(self, rhs):
        return Where(self, 'AND', rhs)

    def __or__(self, rhs):
        return Where(self, 'OR', rhs)

    def sql(self, param):
        if hasattr(self.rhs, 'sql'):
            rhs_str = self.rhs.sql(param)
        else:
            rhs_str = param
        if self.lhs is None:
            return '(%s %s)' % (self.connector, rhs_str)
        else:
            return '(%s %s %s)' % (self.lhs.sql(param), self.connector, rhs_str)

    def params(self):
        if hasattr(self.lhs, 'params'):
            lhs_params = self.lhs.params()
        else:
            lhs_params = []
        if hasattr(self.rhs, 'params'):
            rhs_params = self.rhs.params()
        else:
            rhs_params = [self.rhs]
        
        return lhs_params + rhs_params


class D(object):
    """
    A Database. Attributes are tables.
    """

    def __init__(self, *args, **kwargs):
        self.con = connect(*args, **kwargs)
        for table in self.con.tables():
            # Better than overriding __getattr__(), because we get tab completion
            setattr(self, table[0], T(self.con, table[0]))

    def __getattr__(self, table_name):
        return T(self.con, table_name)


class T(object):
    """
    A table generator from a given DB
    """
    
    def __init__(self, con, *table_names):
        self.con = con
        self.param = self.con.param
        self.table_names = table_names

    def __mul__(self, rhs):
        new_names = self.table_names + rhs.table_names
        return T(self.con, *new_names)

    def _joined_tables(self):
        return ', '.join(self.table_names)

    def select(self, *args):
        fields = []
        where = None
        # Parse positional args. Maybe we should use kwargs instead.
        for elm in args:
            if isinstance(elm, Field):
                fields.append(elm.sql(self.param))
            elif isinstance(elm, Where):
                where = elm
        joined_fields = ', '.join(fields) or '*'

        if where is None:
            return self.con('SELECT %s FROM %s' % (joined_fields, self._joined_tables()))
        else:
            return self.con('SELECT %s FROM %s WHERE %s' % (joined_fields, self._joined_tables(), where.sql(self.param)), *where.params())

    # def update(self, mapping, where=None):


    # def insert(self, mapping, where=None):


    def delete(self, where):
        # This will error if you've specified multiple tables, but that's
        # probably better than blithely just deleting from the first one.
        return self.con('DELETE FROM %s WHERE %s' % (self._joined_tables(), where.sql(self.param)), *where.params())

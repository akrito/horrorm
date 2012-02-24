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

    def __gte__(self, rhs):
        return Where(self, '>=', rhs)

    def __lt__(self, rhs):
        return Where(self, '<', rhs)

    def __lte__(self, rhs):
        return Where(self, '<=', rhs)

    def __imul__(self, rhs):
        # *=
        return Where(self, 'LIKE', rhs)

    def __ipow__(self, rhs):
        # **=
        return Where(self, '~', rhs)

    def __getattr__(self, attr):
        return Field('%s.%s' % (self.field_name, attr))


class Where(object):

    def __init__(self, lhs, connector, rhs):
        self.lhs = lhs
        self.connector = connector
        self.rhs = rhs

    def __neg__(self):
        # ~
        return Where(None, 'NOT', self)

    def __and__(self, rhs):
        return Where(self, 'AND', rhs)

    def __or__(self, rhs):
        return Where(self, 'OR', rhs)

    def sql(self, param):
        if isinstance(self.rhs, Where):
            rhs_str = self.rhs.sql(param)
        else:
            rhs_str = param
        return '(%s %s %s)' % (self.lhs.sql(param), self.connector, rhs_str)

    def params(self):
        if isinstance(self.lhs, Where):
            lhs_params = self.lhs.params()
        elif isinstance(self.lhs, Field):
            lhs_params = []
        else:
            lhs_params = [self.lhs]
        if isinstance(self.rhs, Where):
            rhs_params = self.rhs.params()
        elif isinstance(self.rhs, Field):
            rhs_params = []
        else:
            rhs_params = [self.rhs]
        
        return lhs_params + rhs_params


class D(object):
    """
    A Database. Attributes are tables.
    """

    def __init__(self, *args, **kwargs):
        self.con = connect(*args, **kwargs)
        # Should we create attributes here so tab-completion works in IPython?

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

    def update(self, *args, **kwargs):
        # TODO: I have no idea what a nice API for this would be.
        # update(fields=[id, name], values=[5, 'alex'], where)
        # update(dict or namedtuple, where)
        pass

    def insert(self, *args, **kwargs):
        # TODO: I have no idea what a nice API for this would be.
        # insert(fields=[id, name], values=[5, 'alex'])
        # insert(dict or namedtuple, where)
        pass

    def delete(self, where):
        # This will error if you've specified multiple tables, but that's
        # probably better than blithely just deleting from the first one.
        return self.con('DELETE FROM %s WHERE %s' % (self.joined_tables(), where.sql(self.param)), *where.params())

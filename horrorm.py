from cursors import connect

class _F(object):
    """
    A wrapper around F(name). Using __getattr__ as a constructor? Horrible.
    """
    def __getattr__(self, field_name):
        return F(field_name)

f = _F()

class F(object):

    """
    Fields override arithmetic to generate conditions? Horrible.
    """

    def __init__(self, field_name):
        self.field_name = field_name

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
        return F('%s.%s' % (self.field_name, attr))


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

    def __str__(self):
        if isinstance(self.rhs, Where):
            rhs_str = str(self.rhs)
        else:
            # TODO determine whether we should bind for postgresql or sqlite
            rhs_str = '%s'
        return '(%s %s %s)' % (str(self.lhs), self.connector, rhs_str)

    def params(self):
        if isinstance(self.lhs, Where):
            lhs_params = self.lhs.params()
        elif isinstance(self.lhs, F):
            lhs_params = []
        else:
            lhs_params = [self.lhs]
        if isinstance(self.rhs, Where):
            rhs_params = self.rhs.params()
        elif isinstance(self.rhs, F):
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

    # Should we use slots?

    def __getattr__(self, table_name):
        return T(self.con, table_name)


class T(object):
    """
    A table generator from a given DB
    """
    
    def __init__(self, con, *table_names):
        self.con = con
        self.table_names = table_names

    def __mul__(self, rhs):
        return T(self.table_names + [rhs])

    def _joined_names(self):
        return ', '.join(self.table_names)

    def select(self, where):
        return self.con('SELECT * FROM %s WHERE %s' % (self._joined_names(), str(where)), *where.params())

    def update(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        pass

    def delete(self, where):
        return self.con('DELETE FROM %s WHERE %s' % (self.joined_names(), str(where)), *where.params())

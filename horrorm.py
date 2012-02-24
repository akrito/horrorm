

class _F(object):
    """
    A wrapper around F(name). Using __getattr__ as a constructor? Horrible.
    """
    def __getattr__(self, field_name):
        return F(field_name)

f = _F()

class F(object):

    """
    Field
    """

    def __init__(self, field_name):
        self.field_name = field_name

    def __str__(self):
        return self.field_name

    def __eq__(self, rhs):
        return Where(self, '==', rhs)

    def __ne__(self, rhs):
        return Where(self, '!=', rhs)

    def __lshift__(self, rhs):
        # <<
        return Where(self, 'IN', rhs)
    
    def __gt__(self, rhs):
        pass

    def __gte__(self, rhs):
        pass

    def __lt__(self, rhs):
        pass

    def __lte__(self, rhs):
        pass

    def __imul__(self, rhs):
        pass

    def __ipow__(self, rhs):
        pass

    def __getattr__(self, attr):
        return F('%s.%s' % (self.field_name, attr))


class Where(object):

    def __init__(self, lhs, connector, rhs):
        self.lhs = lhs
        self.connector = connector
        self.rhs = rhs

    def __neg__(self):
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

class T(object):
    """
    A table
    """
    def select(self, where):
        pass

    def update(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        pass

    def delete(self, where):
        pass

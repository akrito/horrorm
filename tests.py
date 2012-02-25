from horrorm import D, f
from contextlib import contextmanager
from nose.tools import eq_

CREATE_SQL = """
CREATE TABLE people (id, name);
INSERT INTO people (id, name) VALUES (1, 'alex');
INSERT INTO people (id, name) VALUES (2, 'ella');
INSERT INTO people (id, name) VALUES (3, 'will');

CREATE TABLE books (id, author, title);
INSERT INTO books (id, author, title) VALUES (1, 2, 'puppies');
INSERT INTO books (id, author, title) VALUES (2, 2, 'oslo');
INSERT INTO books (id, author, title) VALUES (3, 3, 'nerds');
"""

DESTROY_SQL = """
DROP TABLE people;
DROP TABLE books;
"""

@contextmanager
def sqlite(name=':memory:'):
    d = D(name, engine='sqlite')
    for statement in CREATE_SQL.strip().splitlines():
        d.con(statement)
    try:
        yield d
    finally:
        for statement in DESTROY_SQL.strip().splitlines():
            d.con(statement)

# Tests

def test_select_all():
    with sqlite() as d:
        rows = d.people.select()
        eq_(rows[1].name, 'ella')
        eq_(len(rows), 3)
        eq_(rows[0].id, 1)
        eq_(rows[0].name, 'alex')

def test_select_one():
    with sqlite() as d:
        rows = d.people.select(f.name == 'will')
        eq_(len(rows), 1)
        eq_(rows[0].name, 'will')

def test_not_equal():
    with sqlite() as d:
        eq_(len(d.people.select(f.name != 'will')), 2)

def test_in():
    with sqlite() as d:
        q = (f.name << ['alex', 'will'])
        eq_(len(d.people.select(q)), 2)

def test_cmp():
    with sqlite() as d:
        eq_(d.people.select(f.id > 1)[0].id, 2)
        eq_(d.people.select(f.id >= 1)[0].id, 1)
        eq_(d.people.select(f.id < 2)[0].id, 1)
        eq_(d.people.select(f.id <= 1)[0].id, 1)

def test_like():
    with sqlite() as d:
        eq_(d.people.select(f.name % 'a%')[0].name, 'alex')

def test_join():
    with sqlite() as d:
        tables = d.people * d.books
        query = (f.people.id == f.books.author) & (f.books.title == 'oslo')
        eq_(tables.select(f.people.name, query)[0].name, 'ella')

def test_or():
    with sqlite() as d:
        query = (f.id == 1) | (f.id == 2)
        eq_(len(d.people.select(query)), 2)

def test_not():
    with sqlite() as d:
        query = ~(f.id == 1)
        eq_(len(d.people.select(query)), 2)

def test_delete():
    with sqlite() as d:
        d.books.delete(f.title == 'nerds')
        eq_(len(d.books.select()), 2)

def test_db_attributes():
    with sqlite('test.db') as d1:
        d2 = D('test.db')
        eq_(hasattr(d2, 'books'), True)

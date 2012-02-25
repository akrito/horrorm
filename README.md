Horrorm - A Horrible ORM
========================

Overriding arithmetic methods to generate SQL is horrible.

Usage
-----

    from horrorm import D, f
    d = D('foodb')
    d.business_business.select(f.id == 2)
    
    q = (f.id != 5) | (f.name *= 'Al%')
    d.business_business.select(q)

    T('users', 'blogs').select(F.users.id == F.blogs.user_id)

Cheat Sheet
-----------

    SQL   | Horror | Mnemonic
    ------+--------+--------------------------
    =     | ==     |
    !=    | !=     | opposite of equal
    in    | <<=    |
    range | <<     |
    >     | >      |
    >=    | >=     |
    <     | <      |
    <=    | <=     |
    LIKE  | *=     | wildcard
    regex | **=    | really wildcard
    NOT   | ~      |
    AND   | &      |
    OR    | |      |
    JOIN  | *      |

How it Works
------------

<code>Q.field</code> has overridden arithmetic operations that act similarly to
Django's and Peewee's <code>|</code> operator. These take the place of kwargs
like <code>id__exact=5</code>.

<code>t = T('foo').select(Q.id == 5)</code> selects rows from "foo" where "id" is 5.

TODO
----

All of it, except the README.

Bugs
----

No code = no bugs.

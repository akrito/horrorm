Horrorm - A Horrible ORM
========================

Overriding arithmetic methods to generate SQL is horrible.

API
---

Maybe we can hijack Q (and F and R) objects from Peewee and do something like:

    from horrorm import R, T
    T('business_business').select(R.id <<= [1,2,3])
    T('business_business').select(R.id == 5)
    
    q = (Q.id != 5) | (Q.name *= 'Al%')
    T('business_business').select(q)

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

<code>t = T('foo').select(Q.id += 5)</code> selects rows from "foo" where "id" is 5.

TODO
----

All of it, except the README.

Bugs
----

No code = no bugs.

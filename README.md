Horrorm - A Horrible ORM
========================

Overriding arithmetic methods to generate SQL is horrible.

API
---

Maybe we can hijack Q (and F) objects from Peewee and do something like:

    from horrorm import T, Q
    [r.id for r in T('business_business').select(Q.id |= [1,2,3])]
    [r.id for r in T('business_business').select(Q.id = 5)]
    
    q = (Q.id -= 5) | (Q.name *= 'Al%')
    [r.id for r in T('business_business').select(q)]

Cheat Sheet
-----------

    SQL   | Horror | Mnemonic
    ------+--------+--------------------------
    =     | +=     |
    !=    | -=     | opposite of equal
    in    | |=     | this OR that OR the other
    range | /=     |
    >     | >>     |
    >=    | >>=    |
    <     | <<     |
    <=    | <<=    |
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

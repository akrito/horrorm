Horrorm - A Horrible ORM
========================

Overriding arithmetic methods to generate SQL is horrible.

Usage
-----

    from horrorm import T
    [r.id for r in T('business_business') if r.id |= [1,2,3]]
    [r.id for r in T('business_business') if r.id += 5]
    [r.id for r in T('business_business') if (r.id -= 5) | (r.name *= 'Al%')]

Cheat Sheet
-----------

    SQL   | Horror | Mnemonic
    ---------------------------------
    =     | +=     | postively equal
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

How it Works
------------

Let <code>t = T('foo')</code> be a table generator. The first row it returns is
a "ghost" row. The fields of the ghost row are ghost fields. When we use
arithmetic operations on the ghost fields, like <code>row.field += foo</code>,
we're calling overridden methods like <code>__or__</code> or
<code>__idiv__</code>. The field returns a query object and starts building a
query in <code>t</code>. Subsequent arithmetic operations keep building up this
query object.

When the second row of <code>t</code> is requested, the query is executed and a
cursor is obtained, which is then used for all remaining rows.

TODO
----

All of it, except the README.

Bugs
----

No code = no bugs.

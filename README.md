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
    in    | <<     |
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

Horrorm - A Horrible ORM
========================

Overriding arithmetic methods to generate SQL is horrible.

[![Build Status](https://secure.travis-ci.org/akrito/horrorm.png?branch=master)](http://travis-ci.org/akrito/horrorm)

Usage
-----

    from horrorm import D, f
    d = D('foodb')
    d.business_business.select(f.id == 2)
    
    q = (f.id != 5) | (f.name *= 'Al%')
    d.business_business.select(q)

    (d.users * d.blogs).select(f.users.id == f.blogs.user_id)

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
    NOT   | ~      |
    AND   | &      |
    OR    | |      |
    JOIN  | *      |

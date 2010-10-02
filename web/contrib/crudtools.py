""" 
Module for integrating forms and databases.
"""

import web


def in_transaction(db, fnc):
    """ Execute fnc and wrap it in a database transaction """
    t = db.transaction()
    try:
        return fnc()
    except:
        t.rollback()
        if web.config.debug: raise
    else:
        t.commit()

def insert_form(f, db, tbl, _test=False):
    """ Validate and insert a form into a database table """
    if f and f.validates():
        # build value dictionary
        vals = dict([(i.name, i.value) for i in f.inputs])
        if db and tbl:
            # function to execute in transaction
            def ins():
                db.insert(tbl, _test, **vals)
            # run query
            return in_transaction(db, ins)
    return False

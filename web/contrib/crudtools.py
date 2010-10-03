""" 
Module for form-based CRUD operations.
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

def form_val_dict(f):
    """ Return a dictionary of field-name-value mappings """
    vals = [(i.name, i.value) for i in f.inputs]
    return dict([(i[0], i[1]) for i in vals if i[0] in fields])

def insert_form(f, db, tbl, extradata={}, fields=[], _test=False):
    """ Validate and insert a form into a database table 
    
    Data not found in the form can be specified using extradata argument, which
    is a dictionary of column-name-value pairs.

    Optional parameter ``fields`` can be used to specify the exact field names
    to use. Field names that are not found in the form are silently ignored.
    
    """
    if all([f, f.validates(), db, tbl]):
        vals = form_val_dict(f)
        vals.update(extradata)
        def ins():
            db.insert(tbl, _test, **vals)
        return in_transaction(db, ins)
    return False

def update_with_form(f, db, tbl, row_id, pkey='id', extradata={}, 
                     fields=[], _test=False):
    """ Validate form and update the record with ``row_id`` 
    
    Primary key column is assumed to be called ``id``. To specify a different
    primary key column, use the ``pkey`` argument.

    Data not found in the form can be specified using extradata argument, which
    is a dictionary of column-name-value pairs.

    Optional parameter ``fields`` can be used to specify the exact field names
    to use. Field names that are not found in the form are silently ignored.
    
    """
    if all([f, f.validates(), row_id, db, tbl]):
        vals = form_val_dict(f)
        vals.update(extradata)
        def upd():
            db.update(tbl, '%s = $id' % pkey, {'id': row_id}, _test, **vals)
        return in_transaction(upd)
    return False


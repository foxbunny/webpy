"""
Web.py form validators

These validators are based on the code found in Django's core.validators
library. Original source can be found here:

http://code.djangoproject.com/browser/django/trunk/django/core/validators.py?rev=3305

"""

import re
from web import form

_datere = r'(19|2\d)\d{2}-((?:0?[1-9])|(?:1[0-2]))-((?:0?[1-9])|(?:[12][0-9])|(?:3[0-1]))'
_timere = r'(?:[01]?[0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?'
alnum_re = re.compile(r'^\w+$')
alnumurl_re = re.compile(r'^[-\w/]+$')
ansi_date_re = re.compile('^%s$' % _datere)
ansi_time_re = re.compile('^%s$' % _timere)
ansi_datetime_re = re.compile('^%s %s$' % (_datere, _timere))
email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain
integer_re = re.compile(r'^-?\d+$')
ip4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
phone_re = re.compile(r'^[A-PR-Y0-9]{3}-[A-PR-Y0-9]{3}-[A-PR-Y0-9]{4}$', re.IGNORECASE)
slug_re = re.compile(r'^[-\w]+$')
url_re = re.compile(r'^https?://\S+$')
zip_code_re = re.compile(r'^\d{5}$')
zip4_code_re = re.compile(r'^\d{5}-\d{4}$')

# TODO: Make true form validators using web.form, with validation error
#       messages.
# TODO: Make validation error messages translatable using ugettext.



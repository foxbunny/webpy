"""
Web.py form validators

These validators are based on the code found in Django's core.validators
library. Original source can be found here:

http://code.djangoproject.com/browser/django/trunk/django/core/validators.py?rev=3305

"""

import re
from gettext import gettext as _

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

def dropdown_v(ddlist, msg=None):
    return form.Validator(msg or _('Please use the drop down control.'),
                          lambda x: x in [i[0] for i in ddlist])

def max_len(length, msg=None):
    return form.Validator(msg or _('This field is limited to %s characters.' % length),
                          lambda x: len(x) <= length)

def min_len(length, msg=None):
    return form.Validator(msg or _('This field requires at least %s characters.' % length),
                          lambda x: len(x) >= length)

def ex_len(length, msg=None):
    return form.Validator(msg or _('This field must be exactly %s characters long.' % length),
                          lambda x: len(x) = length)

def max_val(value, msg=None):
    return form.Validator(msg or _('This field must be less than or equal to %s.' % value),
                          lambda x: x <= value)

def min_val(value, msg=None):
    return form.Validator(msg or _('This field must be equal to or more than %s.' % value),
                          lambda x: x >= value)

alphanum = form.Validator(_('Please use only letters and numbers.'),
                          lambda x: not x or alnum_re.match(x))
alphanum_path = form.Validator(_('Please enter a valid relative path.'),
                               lambda x: not x or alnumurl_re.match(x))
ansi_date = form.Validator(_('Please enter a valid ANSI date.'),
                           lambda x: not x or ansi_date_re.match(x))
ansi_time = form.Validator(_('Please enter a valid ANSI time.'),
                           lambda x: not x or ansi_time_re.match(x))
ansi_datetime_re = form.Validator(_('Please enter valid ANSI date and time.'),
                                  lambda x: not x or ansi_datetime_re.match(x))
email = form.Validator(_('Please enter a valid e-mail.'),
                       lambda x: not x or email_re.match(x))
integer = form.Validator(_('Please enter an integer value.'),
                         lambda x: not x or integer_re.match(x))
ip4 = form.Validator(_('Please enter a valid IP address.'),
                     lambda x: not x or ip4_re.match(x))
phone = form.Validator(_('Please enter a valid phone number.'),
                       lambda x: not x or phone_re.match(x))
slug = form.Validator(_('Please enter a valid slug.'),
                      lambda x: not x or slug_re.match(x))
url = form.Validator(_('Please enter a valid URL.'),
                     lambda x: not x or url_re.match(x))
zip_code = form.Validator(_('Please enter a valid United States ZIP code.'),
                          lambda x: not x or zip_code_re.match(x))
zip4_code = form.Validator(_('Please enter a valid United States ZIP+4 code.'),
                           lambda x: not x or zip4_code_re.match(x))
required = form.Validator(_('This field is required'),
                          bool)

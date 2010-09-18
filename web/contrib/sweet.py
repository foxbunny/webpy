import re

import web
from web.utils import slugify

__all__ = [
    'sweet', 'accepts', 'ajax',
]

def dprint(msg):
    """ Prints a debug message if debug flag is set """
    if web.config.debug:
        print msg


class Sweet(object):
    """ Abstraction layer for web.py controller.

    To use this class as a web.py controller, simply subclass it, and add
    your custom methods. The class expects to receive an ``action`` parameter
    in all requests. If none is received, the default value of ``default`` is
    used.

    Before delving deeper into how all of this is put together, we'll discuss
    a small example class:

        from web.contrib.sweet import sweet

        class index(sweet):
            def __init__(self):
                self.pages = [1, 2, 3, 4, 5]

            def default(self):
                return 'No action'

            def page_list(self):
                return self.pages

            def add(self):
                page = int(self._i.page)
                if not int(page) in self.pages:
                    pages.append(page)

            def preview(self):
                page = int(self._i.page)
                if not int(page) in self.pages:
                    pages_preview = self.pages
                    pages_preview.appen(page)
                    return pages_preview
                else:
                    return self.pages

        # URL mapping

        urls = ('/index', 'index')

        # form for the above controller:

        <form action="/index" method="post">
            <input name="page" type="text" />
            <input name="action" value="add" type="submit" />
            <input name="action" value="preview" type="submit" />
        </form>

    This is a simplified example, which can, of course, be made more robust
    by various mechanisms discussed below. We have a simple list of integers,
    and the ``page_list`` will return this list. If you direct your browser to
    ``/index`` URL, however, you will only see ``No action``. That's because
    there was no action specified, and the ``default`` method was called instead
    of ``page_list``. To cause ``page_list`` to be called, you need to visit
    ``/index?action=page_list``.

    Now, using the form presented above, you can submit pages to the ``index``
    class. You see there are two submit buttons with a name of ``action``. They
    have different values corresponding to the names of the methods in the
    ``index`` class. Yes, you've guessed it right. Each one triggers the
    matching method. ``add`` button will call the ``add`` method, which adds the
    submitted page to the list, and ``preview`` will only do a dry run so you
    can see the results.

    If you add a third button to the form, with the ``value`` attribute of
    ``foo``, and click that, you'd receive a ``No action`` page. That's because
    there is no corresponding method in the ``index`` class, and therefore
    ``default`` gets called instead.

    All actions should have a corresponding method. If no method is found for a
    given action, the ``_unhandled`` method is called. By default, this method
    calls the ``default`` method, which raises a ``NotImplementedError``
    exception by default, and it is thus suggested that you override ``default``
    with a more meaningful output. The ``default`` method acts sort of like a
    catch-all method.

    You can also override the ``default`` to method to delegate all POST 
    requests to, say, ``_post_default``, and GET requests to, say, 
    ``_get_default``, by using the ``self._method`` attribute. Here's an 
    example:
    
        class index(sweet):
            def default(self):
                if self._method == 'GET':
                    return self._get_default()
                else:
                    return self._post_default()
                    
            def _get_default(self):
                # do something
                
            def _post_default(self):
                # do something else
                
    Note that we've prepended an underscore to the names of the two methods.
    This is done to prevent these methods from handling actions. Actions whose
    name begins with an underscore are ignored. Therefore, all private
    non-action methods should have an underscore prefix.

    Action names can contain some non-ASCII letters. Currently, the following
    scripts are supported (via slugify): English (with two special charcters),
    Greek, Russian, Ukrainian, Czech, Polish, Latvian, Serbian, and Turkish.
    When transliteration pairs are looked up, if there are any overlaps between
    the scripts, the first one that appears in the list will take precedense.
    This can be overriden by explicitly setting the current locale.

    To set the locale for action name conversion, use the
    ``web.ctx.current_locale``parameter. You can either set a single two-letter
    locale, or an iterable containing multiple locales in order of precedence.
    If there are any characters from an unsupported script, they will be
    stripped. If all characters are stripped from the action name, the
    ``default`` action name will be used instead. You can still use actions in
    such casesby manually checking the ``self._i.action`` parameter, and
    calling your action methods manually.

    All punctuation characters except dashes (-) and underscores (_) will also
    be stripped from action names. Also note that action names cannot begin with
    a number or an underscore.

    At class-level, sweet instances support common HTTP verbs: GET, HEAD, POST,
    PUT, and DELETE. At instance-level, however, sweet instance support GET and
    POST by default. You can change this by overriding the ``allowed_methods``
    attribute. Here's an example:

        class index(sweet):
            allowed_methods = ['GET', 'POST', 'DELETE']

    At this time, you can only use custom verbs (the ones not supported by sweet
    class at class-level) by adding them manually. If you want it to handle
    actions, you can do it like this:

        class index(sweet):
            allowed_methods = ['GET', 'POST', 'COPY']

            def COPY(self, *args):
                self._method = 'COPY'
                return self.handle(*args)

    Although methods are not expected to differentiate between POST and GET
    calls, ``_method`` property stores the request type. To specify which
    request types a method will accept, you can define the ``accepts`` attribute
    for the method. For instance:

        class index(sweet):
            def create(self):
                pass
            create.accepts = 'POST'

    If you want a method to accept more than one method, you can assign a list
    to the ``accepts`` attribute:

        class index(sweet):
            def item(self):
                pass
            item.accepts = ['POST', 'GET']

    Request type names for the ``accepts`` attribute are case sensitive.

    A more convenient way to do the above is to use the accepts decorator
    provided in the sweet module. Here's an example of the above index class
    using the decorator:

        from web.contrib.sweet import accepts

        @accepts(['POST', 'GET'])
        class index(sweet):
            def item(self):
                pass

    The main difference between the ``accepts`` method attribute (or decorator)
    and the ``allowed_method`` class attribute is that the method attribute
    restricts an action to certain verbs, but does not reject the unsupported
    verbs, whereas the ``allowed_method`` returns a HTTP 405 just on seeing a
    unsupported verb. Here's an example to illustrate this:

        class index(sweet):
            allowed_methods = ['GET', 'POST']
            def default(self):
                # show a list of blog posts

            @accepts('GET')
            def archive(self):
                # show the blog archive

            @accepts('POST')
            def new_post(self)

    In the above snippet, we have an index class that accepts both GET and POST
    verbs. This is because we handle both creation of a new post, and retrieving
    a list of blog posts. However, the methods ``archive`` and ``new_post`` will
    only respond to one verb each (GET and POST respectively). If a POST request
    is made to ``archive``, the ``default`` method will be called. If a GET
    request is sent to ``new_post``, again, the ``default`` method will be
    called. However, if we send a PUT request to our index class, the
    ``web.nomethod`` exception will be raised and no method will be called.

    Also note that using the decorator without any arguments will not raise any
    exceptions. However, if you don't pass any arguments, the decorator will
    have no effect on the method, and it will accept any HTTP verb as a result.

    Every instance also has an ``_is_ajax`` attribute that contains the contents
    of the 'HTTP_X_REQUESTED_WITH' header. If this header was set by the client,
    it usually means that the request was made as an AJAX call. This does not
    work with JavaScript code that does not set this header. If you want to use
    the ``_is_ajax`` attribute, set this header manually. Most well-established
    JavaScript frameworks (e.g, Prototype, jQuery, MooTools, et al) use this
    header.

    You can mark a method as handling either only AJAX calls, or no AJAX calls.
    To do that, define the ``ajax`` property for the method:

        class index(sweet):
            def ajax_only(self):
                pass
            ajax_only.ajax = True

            def no_ajax(self):
                pass
            ajax_only.ajax = False

    Note that if a method _does_ have the ``ajax`` attribute, it will either
    handle AJAX calls or it won't. If you want your method to be less
    restrictive, simply remove the ``ajax`` attribute.

    As with the ``accepts`` attribute, ``ajax`` attribute has its matching
    deccorator. Here is an example using the decorator:

        class index(sweet):
            @ajax
            def validate(self):
                pass

    If you add the ``ajax`` decorator without any arguments, the ``ajax``
    attribute will be set to true.

    Any parameters that are received via URL parameters are stored in ``_q``
    property. Also, all request parameters (the ones you can access via
    ``web.input()`` call) are stored in ``_i`` property.

    The URL parameters you want to see in ``_q`` property can be defined using
    the ``urlparams`` attribute. Here's an example:

        class index(self):
            urlparams = {'page': 1, 'per_page': 10}

    """

    def __new__(cls, *args, **kwargs):
        """ Class initialization.

        When a new subclass is instantiated, it's ``__init__`` is called before
        instance configuration. Thefore, some of the attributes that are set in
        ``__init__`` might get overriden. You should make sure you are not using
        the following attributes in your ``__init__``:

        ``_i``: contains request parameters (from ``web.input()``)
        ``_q``: contains URL parameter dict
        ``_a``: contains the action name
        ``_method``: contains the name of the request method ('POST', etc)
        ``_is_ajax``: boolean, whether request was made through AJAX call

        After the sweet instance is configured, it's ``_init`` method is called.
        If you need to do any post instantiation configuration, or you need to
        use any of the attributes configured during instantiation, you may want
        to override the ``_init`` method, instead of ``__init__``.

        """
        # Instantiate the sweet instance
        obj = object.__new__(cls, *args, **kwargs)

        # All request params are always available as ``self._i``
        obj._i = web.input(action='default', **obj.urlparams)

        p = {}
        for key in obj.urlparams.keys():
            p[key] = obj._i[key]
        # Actual values of url params are stored in ``self.q``
        obj._q = web.storify(p)

        # Request action (specified via GET or POST ``action`` param)
        # You can use a hidden form field for this. Default action is
        # ``default``, and you should at least define a ``default``
        # method. Actions whose names begin with an underscore are ignored.
        # All action names are converted to lower case. For example, 'Create'
        # would become 'create'. Any spaces found in action names will be
        # converted to underscores, so an action name of 'Save this' would be
        # converted to 'save_this'.
        if all([not obj._i.action.startswith('_'),
                obj._i.action not in obj.allowed_methods]):
            non_ascii_re = re.compile(r'[^\w-]', re.UNICODE)
            action_re = re.compile(r'[a-z][\w-]*')
            # get current locale (if set)
            locale = web.ctx.get('current_locale')
            # slugify the action name
            action = slugify(obj._i.action, locales=locale, spacer='_')
            # strip any non-ascii characters, just in case
            action = non_ascii_re.sub('', action)
            # do we have the winner?
            if action and action_re.match(action):
                obj._a = action
            else:
                obj._a = 'default'
        else:
            obj._a = 'default'

        dprint('SWEET: action name is %s' % obj._a)

        # ``_is_ajax`` stores the value of ``HTTP_X_REQUESTED_WITH`` header
        obj._is_ajax = web.ctx.env.get('HTTP_X_REQUESTED_WITH')

        dprint('SWEET: is ajax %s' % (obj._is_ajax and true))

        # Call post-configuration method
        obj._init()

        return obj

    def _init(self):
        """ Additional initialization

        If any additional initialization tasks are required, override this
        method, rather than ``__init__``, if you need to use the attributes that
        are added to the sweet instance after ``__init__``. See ``__new__`` docs
        for more information.

        """
        pass

    # Allowed HTTP verbs
    allowed_methods = ['GET', 'POST']
    # URL default parameters (key = parameter, value = default value)
    urlparams = {}

    def default(self, *args):
        raise NotImplementedError, 'You need to define the default method in your subclass'

    def _unhandled(self, *args):
        """ Handled for all unhandled actions.

        This method should be overriden in the subclass and given some
        meaningful function.

        """
        dprint('SWEET: action %s is unhandled, falling back to default' % self._a)
        return self.default()

    def _handle(self, *args):
        """ Calls the appropriate method for a given action

        If no method matches an action,

        """
        # If the method is not in accepted methods, raise HTTP 405
        if not self._method in self.allowed_methods:
            # Build a fake object for ``nomethod`` to build the 'Accepts' header
            fake_cls = {}
            for method in self.allowed_methods:
                fake_cls[method] = True # It doesn't have to be a function
            raise web.nomethod(web.storify(fake_cls))
        # No method matches our action
        if not hasattr(self, self._a):
            return self._unhandled(*args)
        # Hands over to method that corresponds to action name
        method = getattr(self, self._a)
        dprint('SWEET: the handler method is %r' % method)
        # Do not handle methods that are not callable.
        if not hasattr(method, '__call__'):
            dprint('SWEET: handler method not callable, falling back on default')
            return self._unhandled(*args)
        # Do not handle AJAX calls if method does not accept it, or AJAX calls
        # made to methods that only handle AJAX.
        if (hasattr(method, 'ajax') and self._is_ajax and not method.ajax) or \
          (hasattr(method, 'ajax') and not self._is_ajax and method.ajax):
            dprint('SWEET: this method does not accept AJAX calls')
            return self._unhandled(*args)
        # Do not handle method if it is not accepted by method.
        if hasattr(method, 'accepts'):
            if not (hasattr(method.accepts, '__iter__') and \
              self._method in method.accepts) or \
              not (isinstance(method.accepts, str) and \
              self._method == method.accepts):
                dprint('SWEET: method is right, but HTTP verb %s is not accepted' % self._method)
                return self._unhandled(*args)
        dprint('SWEET: calling method %s with args %s' % (method, args))
        return method(*args)

    def GET(self, *args):
        """ Default GET method.

        You should override this method only when you don't want it to handle
        any actions.

        """
        self._method = 'GET'
        return self._handle(*args)

    def HEAD(self, *args):
        """ Default HEAD method.

        You should only override this method when you don't want it to handle
        any actions.

        """
        self._method = 'HEAD'
        return self._handle(*args)

    def POST(self, *args):
        """ Default POST method.

        You should only override this method when you don't want it to handle
        any actions.

        """
        self._method = 'POST'
        return self._handle(*args)

    def PUT(self, *args):
        """ Default PUT method.

        You should only override this method when you don't want it to handle
        any actions.

        """
        self._method = 'PUT'
        return self._handle(*args)

    def DELETE(self, *args):
        """ Default DELETE method.

        You should only override this method when you don't want it to handle
        any actions.

        """
        self._method = 'DELETE'
        return self._handle(*args)


sweet = Sweet


class Accepts(object):
    """ Request method decorator

    Adds the ``accepts`` attribute to a method.

    """
    def __init__(self, methods=None):
        self.methods = methods

    def __call__(self, f):
        if self.methods:
            f.accepts = self.methods
        return f


accepts = Accepts


class Ajax(object):
    """ AJAX response deocrator

    Adds ``ajax`` attribute to a method.

    """
    def __init__(self, respond=True):
        self.respond = respond

    def __call__(self, f):
        f.ajax = self.respond
        return f


ajax = Ajax


if __name__ == '__main__':
    # Example application:

    urls = ('/', 'index')

    class index(sweet):
        """ Fairly basic method-agnostic action

        To test it, direct your browser to:

            http://0.0.0.0:8080/?action=test

        or

            http://0.0.0.0:8080?action=post_only

        Attributes that are not callable are not used. Test this by directing
        your browser to:

            http://0.0.0.0:8080?action=test_var

        """
        urlparams = {
            'page': 1,
            'per_page': 10
        }

        def _init(self):
            self.test_var = 'Test attribute'

        def default(self):
            if self._method == 'GET':
                return 'This is the default method for GET.'
            if self._method == 'POST':
                return 'This is the default method for POST.'

        def test(self):
            return 'These are the url params: %s\nTest variable is %s' % \
                (self._q, self.test_var)

        @accepts('POST')
        def post_only(self):
            return 'This method is for POST requests only'

    app = web.application(urls, globals())

    app.run()

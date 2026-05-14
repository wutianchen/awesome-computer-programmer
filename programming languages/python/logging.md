# Logging

* python standard logging
* loguru: https://github.com/Delgan/loguru
* powertool logging: 

* [daiquiri - Python logging setup helper](https://github.com/jd/daiquiri)
* [loguru](https://github.com/Delgan/loguru)
* [better exception](https://github.com/Qix-/better-exceptions)

## Reference 

* [How to Log Properly in Python](https://julien.danjou.info/how-to-log-properly-in-python/)
* [Easy Python logging with daiquiri](https://julien.danjou.info/python-logging-easy-with-daiquiri/)
* [Ultimate Guide to Logging](https://www.loggly.com/ultimate-guide/python-logging-basics/)
* [A guide to logging in python](https://opensource.com/article/17/9/python-logging)
* [good logging practice in python](https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/)
* [Python Logging: An In-Depth Tutorial | Toptal® ](https://www.toptal.com/python/in-depth-python-logging)
* [Python Tutorial: Logging Advanced - Loggers, Handlers and Formatters](https://www.youtube.com/watch?v=jxmzY9soFXg)
* [Become a logging expert in 30 minutes](https://www.youtube.com/watch?v=24_4WWkSmNo)
* [A guided tour of Python logging](https://www.youtube.com/watch?v=DxZ5WEo4hvU)
* [Python logging HOWTO: logging vs loguru](https://alimbekov.com/en/python-logging-vs-loguru/)
* [Exceptional logging of exceptions in python](https://www.loggly.com/blog/exceptional-logging-of-exceptions-in-python/)
* [The definitive guide to python exceptions](https://julien.danjou.info/python-exceptions-guide/)
* [Exceptional Chaining and Embedded Tracebacks](https://peps.python.org/pep-3134/)
* [Python Exception: An Introduction](https://realpython.com/python-exceptions/)
* [Do Not Abuse Try Except In Python](https://towardsdatascience.com/do-not-abuse-try-except-in-python-d9b8ee59e23b)


## Components

* Logger 
* Formatter
* Handler 
* Filter 
* LogRecord


[python logging flow](./docs/python%20logging%20flow.png)

* default destination of handler is sys.stderr

* getLogger() returns a reference to a logger instance with the specified name if it is provided, or root if not. The names are period-separated hierarchical structures.

* Loggers have a concept of effective level. If a level is not explicitly set on a logger, the level of its parent is used instead as its effective level. If the parent has no explicit level set, its parent is examined, and so on - all ancestors are searched until an explicitly set level is found. The root logger always has an explicit level set (WARNING by default). When deciding whether to process an event, the effective level of the logger is used to determine whether the event is passed to the logger’s handlers. (https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial)

* Child loggers propagate messages up to the handlers associated with their ancestor loggers. Because of this, it is unnecessary to define and configure handlers for all the loggers an application uses. It is sufficient to configure handlers for a top-level logger and create child loggers as needed. (You can, however, turn off propagation by setting the propagate attribute of a logger to False.) (https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial)


```python
#### getLogger

logger writes to stderr by default handler

```python
# can be verified by this
python program.py 1> stdout.txt  2> stderr.txt


Note that Loggers are never instantiated directly, but always through the module-level function logging.getLogger(name). Multiple calls to getLogger() with the same name will always return a reference to the same Logger object

hierarcy

The name is potentially a period-separated hierarchical value, like foo.bar.baz (though it could also be just plain foo, for example). Loggers that are further down in the hierarchical list are children of loggers higher up in the list. For example, given a logger with a name of foo, loggers with names of foo.bar, foo.bar.baz, and foo.bam are all descendants of foo. The logger name hierarchy is analogous to the Python package hierarchy, and identical to it if you organise your loggers on a per-module basis using the recommended construction logging.getLogger(name). That’s because in a module, name is the module’s name in the Python package namespace.

#### propagate

If you attach a handler to a logger and one or more of its ancestors, it may emit the same record multiple times. In general, you should not need to attach a handler to more than one logger - if you just attach it to the appropriate logger which is highest in the logger hierarchy, then it will see all events logged by all descendant loggers, provided that their propagate setting is left set to True. A common scenario is to attach handlers only to the root logger, and to let propagation take care of the rest.
```


## Configuration

configure directly in the code

```python
import logging
import sys

def get_standard_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """ Get Standard Logger
    set log level to be the same on logger and handler
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s # %(levelname)s: [%(name)s] ---> %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
```

 DictConfig: read in configuration from json or yaml file


## Loglevel

* DEBUG: In most cases, you don’t want to read too much details in the log file. Therefore, debug level is only enabled when you are debugging. I use debug level only for detail debugging information, especially when the data is big or the frequency is high, such as records of algorithm internal state changes in a for-loop
* INFO: I use info level for routines, for example, handling requests or server state changed
* WARNING: I use warning when it is important, but not an error, for example, when a user attempts to login with wrong password or connection is slow
* ERROR: I use error level when something is wrong, for example, an exception is thrown, IO operation failure or connectivity issue
* CRITICAL: I seldom use critical, you can use it when something really bad happen, for example, out of memory, disk is full or a nuclear meltdown

at ERROR level, one can either use logging.error(msg, exec_info=True) or logging.exception(msg)

```python
# INFO
def handle_request(request):
    logger.info('Handling request %s', request)
    # handle request here
    result = 'result'
    logger.info('Return result: %s', result)

def start_service():
    logger.info('Starting service at port %s ...', port)
    service.start()
    logger.info('Service is started')

# DEBUG

def complex_algorithm(items):
    for i, item in enumerate(items):
        # do some complex algorithm computation
        logger.debug('%s iteration, item=%s', i, item)

# WARNING

def authenticate(user_name, password, ip_address):
    if user_name != USER_NAME and password != PASSWORD:
        logger.warn('Login attempt to %s from IP %s', user_name, ip_address)
        return False

# ERROR

def get_user_by_id(user_id):
    user = db.read_user(user_id)
    if user is None:
        logger.error('Cannot find user with user_id=%s', user_id)
        return user
    return user
```

## Exception

exception structure

```bash
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
```

exception patterns

#### The “Big Tarp” Pattern

```python
try:
    main_loop()
except Exception:
    logger.exception("Fatal error in main loop")
```

#### "Pinpoint" Pattern

```python
from openburrito import find_burrito_joints, BurritoCriteriaConflict
# "criteria" is an object defining the kind of burritos you want.
try:
    places = find_burrito_joints(criteria)
except BurritoCriteriaConflict as err:
    logger.warn("Cannot resolve conflicting burrito criteria: {}".format(err.message))
    places = list()
```

#### "Transformer" Pattern

```python
try:
    something()
except SomeError as err:
    logger.warn("...")
    raise DifferentError() from err
In Python 2, you must drop the “from err”:

try:
    something()
except SomeError as err:
    logger.warn("...")
    raise DifferentError()
```

#### "Message and Raise" Pattern

```python
try:
    something()
except SomeError:
    logger.warn("...")
    raise
```


#### The Most Diabolical Python Antipattern

```python
try:
    something()
except Exception:
    pass
```


Notice how this not only fails to give you any useful exception information. It also manages to completely hide the fact that anything is wrong in the first place. You may never even know you mistyped a variable name until you get paged at 2 a.m. because production is broken, in a way that takes you until dawn to figure out, because all possible troubleshooting information is being suppressed.

Just don’t do it. If you feel like you simply must catch and ignore all errors, at least throw a big tarp under it (i.e. use logger.exception() instead of pass).

 

System Exit
 

There are 3 exit functions, in addition to raising SystemExit.

The underlying one is os._exit, which requires 1 int argument, and exits immediately with no cleanup. It's unlikely you'll ever want to touch this one, but it is there.

sys.exit is defined in sysmodule.c and just runs PyErr_SetObject(PyExc_SystemExit, exit_code);, which is effectively the same as directly raising SystemExit. In fine detail, raising SystemExit is probably faster, since sys.exit requires an LOAD_ATTR and CALL_FUNCTION vs RAISE_VARARGS opcalls. Also, raise SystemExit produces slightly smaller bytecode (4bytes less), (1 byte extra if you use from sys import exit since sys.exit is expected to return None, so includes an extra POP_TOP).

The last exit function is defined in site.py, and aliased to exit or quit in the REPL. It's actually an instance of the Quitter class (so it can have a custom repr, so is probably the slowest running. Also, it closes sys.stdin prior to raising SystemExit, so it's recommended for use only in the REPL.

As for how SystemExit is handled, it eventually causes the VM to call os._exit, but before that, it does some cleanup. It also runs atexit._run_exitfuncs() which runs any callbacks registered via the atexit module. Calling os._exit directly bypasses the atexit step.

Using sys.exit or SystemExit; when to use which?: https://stackoverflow.com/questions/13992662/using-sys-exit-or-systemexit-when-to-use-which
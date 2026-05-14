# Debugging

pdb (python debugger): https://docs.python.org/3/library/pdb.html

### Debugging with vsc

tbd

### Debugging in pytest

start pytest with

```bash
pytest --pdb
```

insert breakpoint in code with

```bash
import pytest

# where the debugging should begin
pytest.set_trace
```

### Tricks

#### get source code from function object

```bash
import inspect

inspect.get_source(<function object>)
```
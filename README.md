https://www.researchgate.net/publication/369734814_apophis_syntax

#ApophisProgrammingLanguage 
Future usage for the #ApophisMiningFacility and the #ApophisClassUNSCStarfleet #GottaCatchAnAsteroid #ApophisNewMoon #MoonGod #UNSC #starship #AsteroidMining 

Apophis is an (In Development) programming language that combines the syntax of Python, Ruby and the esoteric programming language Malbolge. (#GitHub Coming Soon)

Apophis includes the ability to run Malbolge code using the `run_malbolge(code)`
function. This takes a Malbolge program as a string argument and returns the
output.

The language also supports **hybrid programs** that mix Python, Ruby and Malbolge.  In
these sources, lines beginning with ``:`` are interpreted as Python, lines beginning with ``;``
are executed as Ruby while all other lines run as Malbolge.  The outputs from all languages are
concatenated and variables defined in Python or Ruby segments persist across subsequent
segments.  Use :func:`apophis.run_apophis` to execute code stored in a string and
:func:`apophis.run_file` for ``.apop``/``.apo`` files.

Example hybrid program executed from a string:

```python
import apophis

code = ":print('A', end='')\n;print 'B'\n>b\n:print('C')"
print(apophis.run_apophis(code))  # -> ABsC\n
```

Hybrid sources can also be saved to ``.apop`` files and run with
``apophis.run_file('program.apop')``.

Lines beginning with ``#`` are treated as comments and ignored by the
interpreter, allowing Apophis programs to be documented without affecting
execution.

Apophis also includes a `malbolge_encode(string)` function that encodes a given
string into Malbolge code using the language's encryption algorithm.

An interpreter for a safe subset of Python is available via
`run_python(code)`.  It allows variable assignments, arithmetic expressions,
basic control flow (``if`` statements, ``while`` loops and ``def`` blocks) and
``print`` calls (``puts`` is provided as an alias).  A tiny Ruby-like syntax is
also accepted: ``if``/``while``/``def`` blocks may omit trailing colons and be
terminated with ``end``.  The output of the program is returned as a string:

```python
import apophis

result = apophis.run_python("x = 2\nprint(x + 1)")
assert result == "3\n"
```

Ruby code can be executed with :func:`run_ruby`, which invokes the system Ruby
interpreter and returns its stdout.  A mapping can be provided to share
variables with Python code:

```python
import apophis

assert apophis.run_ruby("print 'hi'") == "hi"
```

Overall, Apophis blends the syntax and capabilities of Python, Ruby and
Malbolge, allowing for the use of traditional programming concepts alongside
the challenge and obscurity of Malbolge's encryption algorithm.

## Installation

Apophis can be installed from PyPI:

```bash
pip install apophis
```

## Usage

The `apophis` module provides helpers for experimenting with Malbolge and Ruby:

```python
import apophis

output = apophis.run_malbolge('Q')  # execute code stored in a string
encoded = apophis.malbolge_encode('Hello!')
```

Place a hybrid Apophis program in `malbolge.apop` and call
`apophis.run_file()` to run it.  The module also installs a command line tool
so programs can be executed directly:

```bash
apophis path/to/program.apo
```

An interactive REPL is also available for quick experiments:

```python
import apophis
apophis.repl()
```

or from the command line:

```bash
apophis -i
```

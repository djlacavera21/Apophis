https://www.researchgate.net/publication/369734814_apophis_syntax

#ApophisProgrammingLanguage 
Future usage for the #ApophisMiningFacility and the #ApophisClassUNSCStarfleet #GottaCatchAnAsteroid #ApophisNewMoon #MoonGod #UNSC #starship #AsteroidMining 

Apophis is an (In Development) programming language that combines the syntax of Python and the esoteric programming language Malbolge. (#GitHub Coming Soon)

Apophis includes the ability to run Malbolge code using the run_malbolge(code) function. This takes a Malbolge program as a string argument and returns the output.
   
Additionally, Apophis has a built-in function called `apophis_malbolge()` that
will execute a program stored in a file using the Apophis file extensions
``.apop`` or ``.apo``.  By default a file named ``malbolge.apop`` is loaded.

Apophis also includes a `malbolge_encode(string)` function that encodes a given
string into Malbolge code using the language's encryption algorithm.

Overall, Apophis blends the syntax and capabilities of both Python and
Malbolge, allowing for the use of traditional programming concepts alongside
the challenge and obscurity of Malbolge's encryption algorithm.

## Installation

Apophis can be installed from PyPI:

```bash
pip install apophis
```

## Usage

The `apophis` module provides helpers for experimenting with Malbolge:

```python
import apophis

output = apophis.run_malbolge('Q')  # execute code stored in a string
encoded = apophis.malbolge_encode('Hello!')
```

Place an Apophis program in `malbolge.apop` and call
`apophis.apophis_malbolge()` to run it.  The module also installs a command
line tool so programs can be executed directly:

```bash
apophis path/to/program.apo
```

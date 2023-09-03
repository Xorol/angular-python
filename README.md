# angular-python

Simple Python script which allows you to use angle brackets (`<>`) in type annotations (and in Python 3.12, generic type parameters). Example:

```py
# Normal type annotation
a: list<int> = [1, 2, 3]

# (Python 3.12) generic type params
def extend<T: Iterator>(thing1: T, thing2: T) -> T:
  return thing1.extend(thing2)
```

## Usage
```
python3 angular.py <path/to/input.py> [path/to/output.py]
```

If an output file is not specified, it will just compile and run.

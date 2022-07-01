# py-patterns

A util library for common patterns in python.

## Supported patterns

1. Adapters


## Install
```sh
pip install py-patterns-util
```

## Example

```py
from py_patterns.adapters import Field, Adapter


class PersonAdapter(Adapter):
    last_name = Field(source="person.last_name", dtype=str)
    first_name = Field(source="person.first_name", dtype=str)
    age = Field(source="person.age", dtype=int)


source_data = {"person": {"last_name": "Smith", "first_name": "John", "age": 30}}

# {"last_name": "Smith", "first_name": "John", "age": 30}
converted_data = PersonAdapter(source_data=source_data).convert()
```

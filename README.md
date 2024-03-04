# SQLAUtils

<p align="center">
    <em>SQLAlchemy 2.0+ wrapper that simplifies its use in Python applications.</em>
</p>

<div align="center">

![](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)
![](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)

</div>

---

**Source Code**: <a href="https://github.com/javalce/sqlautils" target="_blank">https://github.com/javalce/sqlautils</a>

---

SQLAUtils is a library that simplifies the use of SQLAlchemy in Python applications. It provides a set of utilities that help to reduce the amount of code needed to perform common operations with SQLAlchemy.

**SQLAUtils** is a wrapper around SQLAlchemy.

The key features are:

- **Simplified CRUD operations**: It provides a set of utilities that help to reduce the amount of code needed to perform common operations with SQLAlchemy.
- **Simplified session management**: It provides a set of utilities that help to reduce the amount of code needed to manage the session in SQLAlchemy.
- **Simplified transaction management**: It provides a set of utilities that help to reduce the amount of code needed to manage the transaction in SQLAlchemy.
- **Simplified query management**: It provides a set of utilities that help to reduce the amount of code needed to manage the query in SQLAlchemy.
- **Simplified model management**: It provides a set of utilities that help to reduce the amount of code needed to manage the model in SQLAlchemy.

## Requirements

A recent and currently supported <a href="https://www.python.org/downloads/" class="external-link" target="_blank">version of Python</a>.

As **SQLAUtils** is based on **SQLAlchemy**, it requires it. It will be installed automatically when you install SQLAUtils.
For its extensions, you can install them manually or let SQLAUtils install them for you.

## Installation

<div class="termy">

```console
$ pip install sqlautils
---> 100%
Successfully installed sqlautils
```

</div>

## Example

Here's a quick example. ✨

### A SQL Table

Imagine you have a SQL table called `hero` with:

- `id`
- `name`
- `secret_name`
- `age`

And you want it to have this data:

| id  | name       | secret_name      | age  |
| --- | ---------- | ---------------- | ---- |
| 1   | Deadpond   | Dive Wilson      | null |
| 2   | Spider-Boy | Pedro Parqueador | null |
| 3   | Rusty-Man  | Tommy Sharp      | 48   |

```python
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlautils import BaseModel

class Hero(Model):
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    secret_name: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer)
```

The class `Hero` is a **SQLAlchemy** model. It is a subclass of `BaseModel` from **SQLAUtils**, which is a subclass of `SQLAlchemy`'s `DeclarativeBase` class.

And each of those class attributes is a **SQLAlchemy** column.

## License

This project is licensed under the terms of the [MIT license](https://github.com/javalce/sqlautils/blob/main/LICENSE).

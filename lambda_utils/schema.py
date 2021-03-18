from __future__ import annotations

__all__ = ("BaseSchema",)

import pydantic


def camelize(s: str) -> str:
    """
    :example:
        >>> camelize("hello_world")
        'helloWorld'
        >>> camelize("e_tag")
        'eTag'
        >>> camelize("_tag")
        'Tag'
    """
    words = s.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class BaseSchema(pydantic.BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


if __name__ == "__main__":
    import doctest

    doctest.testmod()

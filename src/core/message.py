from typing import Literal, TypedDict, Union


class Job(TypedDict):
    title: str
    company: str
    location: str
    link: str
    type: Literal["job"]


class Info(TypedDict):
    title: str
    type: Literal["info"]


class Post(TypedDict):
    title: str
    link: str
    type: Literal["post"]


class Error(TypedDict):
    title: str
    type: Literal["error"]


Message = Union[Job, Info, Post, Error]

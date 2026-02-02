from sqlmodel import Field, SQLModel


class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = True
    rating: int | None = None
#ORM Class end
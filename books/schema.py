import graphene

from graphene import relay, ObjectType

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from books.models import Book

class BookNode(DjangoObjectType):
  model = Book
  filter_fields = {
    'title': ['exact', 'istartswith'],
    'isbn': ['exact'],
    'category': ['exact', 'icontains', 'istartswith'],
  }
  interfaces = (relay.Node,)

class Query(ObjectType):
  books = relay.Node.Field(BookNode)
  all_books = DjangoFilterConnectionField(BookNode)

  def resolve_books(self):
    return Book.objects.all()

schema = graphene.Schema(query=Query, )
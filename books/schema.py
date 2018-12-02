import graphene

from graphene import relay, ObjectType, InputObjectType

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.core.exceptions import ValidationError

from books.models import Book
from books.heplers import get_object, update_create_instance, get_errors

class BookNode(DjangoObjectType):

  class Meta:
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


class BookCreateInput(InputObjectType):
  """
  Class defined to accept input data
  from the interactive graphql console
  """

  title = graphene.String(required=False)
  isbn = graphene.String(required=False)
  category = graphene.String(required=False)

class CreateBook(relay.ClientIDMutation):

  class Input:
    # BookCreateInput class used as argument here.
    book = graphene.Argument(BookCreateInput)

  new_book = graphene.Field(BookNode)

  @classmethod
  def mutate_and_get_payload(cls, args, context, info):
    book_data = args.get('book') # get the book input from the args
    book = Book() # get an instance of the book model here
    new_book = update_create_instance(book, book_data) # use custom function to create book

    return cls(new_book=new_book)

class UpdateBook(relay.ClientIDMutation):

  class Input:
    book = graphene.Argument(BookCreateInput)
    id = graphene.String(required=True)

  errors = graphene.List(graphene.String)
  updated_book = graphene.Field(BookNode)

  @classmethod
  def mutate_and_get_payload(cls, args, context, info):

    try:
      book_instance = get_object(Book, args['id']) # get book by id
      if book_instance:
        # modify and update book model
        book_data = args.get('book')
        updated_book = update_create_instance(book_instance, book_data)
        return cls(update_book=updated_book)
    except ValidationError as e:
      # return an error if something wrong happens
      return cls(updated_book=None, errors=get_errors(e))

class Mutation(ObjectType):
  create_book = CreateBook.Field()
  update_book = UpdateBook.Field()

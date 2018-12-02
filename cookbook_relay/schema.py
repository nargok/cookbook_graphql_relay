import graphene
import ingredients.schema
import books.schema

class Query(ingredients.schema.Query,
            books.schema.Query,
            graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query)
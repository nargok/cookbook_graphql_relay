import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ingredients.models import Category, Ingredient

class CategoryNode(DjangoObjectType):
  class Meta:
    model = Category
    filter_fields = ['name', 'ingredients']
    interfaces = (relay.Node, )

class IngredientNode(DjangoObjectType):
  class Meta:
    model = Ingredient
    filter_fields = {
      'name': ['exact', 'icontains', 'istartswith'],
      'notes': ['exact', 'icontains'],
      'category': ['exact'],
      'category__name': ['exact'],
    }
    interfaces = (relay.Node, )

class Query(object):
  category = relay.Node.Field(CategoryNode)
  all_categories = DjangoFilterConnectionField(CategoryNode)

  ingredient = relay.Node.Field(IngredientNode)
  all_ingredients = DjangoFilterConnectionField(IngredientNode)

  # TODO テスト用のQueryを追加 後で消す
  hello = graphene.String(argument=graphene.String(default_value='stranger'))

  def resolve_hello(self, info, argument):
    return 'Hello, ' + argument
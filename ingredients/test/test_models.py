import pytest

from ingredients.models import Category

pytestmark = pytest.mark.django_db

"""
Test Classの始まりは、Testxxxにしないとpytestで無視される
"""
class TestCategoryModel:

  def test_create_category(self):
    category = Category.objects.create(name='firstCategory')

    saved_category = Category.objects.get(pk=category.id)
    assert saved_category == category

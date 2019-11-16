import factory
from faker import Factory

from .models import BaseUser

faker = Factory.create()


class BaseUserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: f'{n}{faker.email()}')
    full_name = factory.LazyAttribute(lambda _: faker.name())
    password = faker.password()

    class Meta:
        model = BaseUser


class SuperUserFactory(BaseUserFactory):
    """
    Taken from:
    <http://factoryboy.readthedocs.io/en/latest/recipes.html#custom-manager-methods>
    """

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        return manager.create_superuser(*args, **kwargs)

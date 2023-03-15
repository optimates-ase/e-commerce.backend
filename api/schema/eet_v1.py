import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from api.models.eet_v1 import Product as ProductModel
from api.models.eet_v1 import EET_V1 as EET_V1_MODEL


class Product(MongoengineObjectType):

    class Meta:
        model = ProductModel
        interfaces = (Node, )


class EET_V1(MongoengineObjectType):

    class Meta:
        model = EET_V1_MODEL
        interfaces = (Node, )


class Query(graphene.ObjectType):

    EET_V1 = graphene.List(EET_V1)

    def resolve_all(self, info):
        return list(EET_V1_MODEL.objects.all())


schema = graphene.Schema(query=Query, types=[Product, EET_V1])

from mongoengine import Document

from mongoengine.fields import (
    ReferenceField, StringField, BooleanField
)


class Product(Document):
    meta = {'collection': 'Product'}
    productId = StringField()
    productName = StringField()


class EET_V1(Document):
    meta = {'collecion': 'EET_V1'}
    productId = ReferenceField(Product)
    fieldName = StringField()
    description = StringField()
    unnamed_3 = StringField()
    unnamed_4 = StringField()
    fieldOwner = StringField()
    dataType = StringField()
    value = StringField()
    active = BooleanField()

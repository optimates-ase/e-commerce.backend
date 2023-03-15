import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from api.models.welcome import Department as DepartmentModel
from api.models.welcome import Employee as EmployeeModel
from api.models.welcome import Role as RoleModel


class Department(MongoengineObjectType):

    class Meta:
        model = DepartmentModel
        interfaces = (Node, )


class Role(MongoengineObjectType):

    class Meta:
        model = RoleModel
        interfaces = (Node, )


class Employee(MongoengineObjectType):

    class Meta:
        model = EmployeeModel
        interfaces = (Node, )


class WelcomeQuery(graphene.ObjectType):
    node = Node.Field()
    all_employees = MongoengineConnectionField(Employee)
    all_roles = MongoengineConnectionField(Role)
    role = graphene.Field(Role)


schema = graphene.Schema(query=WelcomeQuery, types=[Department, Employee, Role])

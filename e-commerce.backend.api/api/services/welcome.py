from mongoengine import connect

from api.models.welcome import Department, Employee, Role
from api.models.eet_v1 import Product
from api.models.eet_v1 import EET_V1

# connect(host='mongodb://root:password@localhost:17071/database?authSource=source_database')

connect('mydb',
        host="localhost",
        username="root",
        password="password",
        authentication_source='admin')


def init_db():

    # create fixtures
    engineering = Department(name='Engineering')
    engineering.save()

    hr = Department(name='Human Resources')
    hr.save()

    manager = Role(name='manager')
    manager.save()

    engineer = Role(name='engineer')
    engineer.save()

    peter = Employee(firstname='Peter', lastname='Parker',
                     department=engineering, role=engineer)
    peter.save()

    susanne = Employee(firstname='Susanne', lastname='Wong',
                       department=hr, role=manager)
    susanne.save()

    luke = Employee(firstname='Luke', lastname='Cage',
                    department=engineering, role=engineer)
    luke.save()

    print("storing product")
    example_product = Product(
        productId='PRODUCT WITH ID 1', productName="TEST PRODUCT")
    example_product.save()

    print("storing eet field")
    example_field = EET_V1(
        productId='PRODUCT WITH ID 1',
        fieldName='00010_EET_Version',
        description='This field specifies the output version of the template and is used by the recipient to understand the number of fields expected, their labeling and order. ', unnamed_3='V1',
        unnamed_4='V1',
        fieldOwner='ProdMan',
        dataType='S',
        value='V1',
        active=True)
    example_field.save()

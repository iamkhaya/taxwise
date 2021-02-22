import datetime
import decimal
import logging
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

from courier.models import Courier
from front_sections.models import FrontSectionItem
from hampers.models import Hamper, HamperItem
from order.models import Order, OrderItem
from pickup_point.models import PickupPoint
from recipient.models import Recipient
from shopfront.models import Category, Product
from supplier.models import Supplier

fake = Faker()
logger = logging.getLogger(__name__)


front_section_titles = [
    "Hampers",
    "On Promotion",
    "Frequently Bought",
    "Stationary",
    "Fresh",
]

category_names = [
    "Bakery",
    "Beverages",
    "Dairy",
    "Fruit and Veg",
    "Frozen",
    "Grocery",
    "Health and Beauty",
    "Stationary",
]

category_and_products = {
    "Bakery": [
        ["Bread Roll", "Bread_Rolls.png"],
        ["Jam Doughnut", "Jam-Doughnut.png"],
        ["White Bread", "Bakers_Inn_Brown_Loaf.png"],
        ["Cream Doughnut", "Fresh-Cream-Doughnut.png"],
        ["Scone", "Scone.png"],
    ],
    "Beverages": [
        ["Mazoe Orange", "Apples_Top_Red_Loose.jpg"],
        ["Mazoe Blackberry", "mazoe_blackberry.jpg"],
        ["Pure Joy", "PureJoy.jpeg"],
    ],
    "Dairy": [
        ["Cremora", "cremora.jpg"],
        ["Dendairy UHT Milk", "Dendairy_UHT_Milk.jpg"],
        ["Dairiboard Chimombe Milk", "Dairibord_Chimombe_Milk.png"],
        ["Supa Milk", "Dendairy_Supa_Milk_500ml.png"],
        ["Dendairy Salted Butter", "dendairy_salted_butter.png"],
        ["Bluebrand Fat Spread", "blue_brand_fat_spread.jpg"],
    ],
    "Fruit and Veg": [
        ["Bananas", "Bananas.jpg"],
        ["Rape", "Rape_Vegetable_Bundle.png"],
        ["Carrrots", "Carrots.jpeg"],
        ["Potatoes", "Potatoes_Pocket.png"],
        ["Apples", "Apples_Top_Red_Loose.jpg"],
        ["Lemons", "Lemons.jpg"],
    ],
    "Frozen": [
        ["Irvines Mixed Portion", "Irvines_Mixed_Portions_-_2kg.jpg"],
        ["Surrey Huku", "Surrey_Huku_Mixed_Portions_-_1kg.jpg"],
    ],
    "Grocery": [
        ["Zimgold Cooking Oil", "zimgold_cooking_oil.png"],
        ["Sun Jam", "Sun-Jam.jpg"],
        ["Red Seal Mealie Meal", "red_seal_roller_meal.jpeg"],
        ["Baked Beans", "Rhode-Baked-Beans.png"],
        ["Gloria Self Raising Flour", "goria_self_raising_flour.jpg"],
        ["Surrey Huku 2kg", "Surrey_Huku_Mixed_Portions_-_1kg.jpg"],
    ],
    "Health and Beauty": [
        ["Sunlight", "sunlight.png"],
        ["Jade Bath Soap", "jade_bath_soap.jpeg"],
        ["Green Bar Soap", "green_bar_soap.jpg"],
        ["Vaseline", "Vaseline_Petroleum_Jelly.jpg"],
        ["Elegance Petroleum Jelly", "Elegance_Pretoleum_Jelly.png"],
        ["Duck Toilet Cleaner", "Duck_Toilet_Cleaner.png"],
        ["Colgate", "Colgate_Toothpaste.jpg"],
    ],
    "Stationary": [
        ["Scissors", "scissors.jpeg"],
        ["Sellotape", "sellotape.jpg"],
        ["Pencils", "pencils.jpeg"],
        ["Pens", "pens.jpeg"],
        ["Khakhi Covers", "khakhi_covers.jpeg"],
        ["Plastic Covers", "plastic_covers.jpeg"],
    ],
}


class Command(BaseCommand):
    help = "Seed data to get started"

    def add_arguments(self, parser):
        parser.add_argument("--size", type=int)

    def handle(self, *args, **options):
        self.stdout.write("seeding data...")
        run_seed(self)
        self.stdout.write("** completed seeding.")


def clear_data():
    """Deletes all the table data"""
    print("** clear data...")
    Category.objects.all().delete()
    Courier.objects.all().delete()
    Recipient.objects.all().delete()
    Product.objects.all().delete()
    Hamper.objects.all().delete()
    HamperItem.objects.all().delete()
    FrontSectionItem.objects.all().delete()
    User.objects.all().delete()
    Order.objects.all().delete()
    OrderItem.objects.all().delete()
    PickupPoint.objects.all().delete()


def create_categories():
    print("** creating categories")
    categories = [
        Category(name=c, slug=c, description=c, meta_keywords=c, is_active=True)
        for c in category_names
    ]
    Category.objects.bulk_create(categories)


def fetch_categories():
    category_items = {}
    categories = Category.objects.all()
    for category in categories:
        category_items[category.name] = category

    return category_items


def create_couriers():
    print("** creating couriers")

    for n in range(0, 5):
        new_user = User.objects.create(
            username="courier_{}@thumela.co.zw".format(n),
            first_name="courier+{}".format(n),
            last_name="courier+{}".format(n),
            email="courier_{}@thumela.co.zw".format(n),
        )

        new_user.save()
        new_user.set_password("test")
        new_user.is_active = True
        new_user.save()

        courier = Courier.objects.create(
            user=new_user,
            company_name=fake.company(),
            phone_number_1="824-075-85583",
            phone_number_2="867-075-85456",
            address_line_1=fake.secondary_address(),
            address_line_2=fake.street_address(),
            email_address=fake.ascii_email(),
            surburb=fake.state(),
            city=random.choice(["Harare", "Bulawayo"]),
        )
        courier.save()
        order_1 = Order.objects.all()[n]
        order_1.state = "ready for collection"
        order_1.save()

        order_2 = Order.objects.all()[n + 1]
        order_2.state = "in transit"
        order_2.save()

        courier.orders.add(order_1, order_2)
        courier.save()


def create_suppliers():
    print("** creating suppliers")

    for n in range(0, 2):
        new_user = User.objects.create(
            username="supplier_{}@thumela.co.zw".format(n),
            first_name="supplier+{}".format(n),
            last_name="supplier+{}".format(n),
            email="supplier_{}@thumela.co.zw".format(n),
        )

        new_user.save()
        new_user.set_password("test")
        new_user.is_active = True
        new_user.save()

        supplier = Supplier.objects.create(
            user=new_user,
            company_name=fake.company(),
            phone_number_1="824-075-85583",
            phone_number_2="867-075-85456",
            address_line_1=fake.secondary_address(),
            address_line_2=fake.street_address(),
            email_address=fake.ascii_email(),
            surburb=fake.state(),
            city="Harare" if n % 2 == 0 else "Bulawayo",
        )

        order = Order(
            user=User.objects.all()[n],
            date_created=datetime.datetime.now(),
            recipient=Recipient.objects.order_by("?").first(),
            supplier=supplier,
            state="ready for packing",
            delivery_method=random.choice(["Collection", "Delivery"]),
            security_question=fake.sentence(),
            security_answer=fake.city(),
        )
        order.save()

        supplier.save()


def create_products():
    print("** creating products")

    categories = fetch_categories()

    for category_name, category in categories.items():
        products = category_and_products[category_name]

        for product in products:
            name = product[0]
            img = open(
                "{}/seed/products/{}".format(settings.MEDIA_ROOT, product[1]), "rb"
            )

            p = Product(
                name=name,
                slug=name,
                brand=name,
                sku=name,
                price=decimal.Decimal(random.randrange(155, 389)) / 100,
                old_price=decimal.Decimal(random.randrange(155, 389)) / 100,
                units=1,
                volume=random.randrange(0, 500),
                volume_unit="g",
                is_active=True,
                is_featured=True,
                description=name,
                meta_keywords=name,
                meta_description=name,
            )
            p.save()
            p.categories.add(category)
            p.image.save("{}.jpg".format(name), img, save=True)


def create_hampers():
    print("** creating hampers")

    Hamper.objects.bulk_create(
        [
            Hamper(
                name="Stationery Hamper",
                slug="StationeryHamper",
                description="All your stationary needs",
                is_active=True,
                is_featured=True,
            ),
            Hamper(
                name="Basic Basket",
                slug="BasicBasket",
                description="Basic Basket",
                is_active=True,
                is_featured=True,
            ),
            Hamper(
                name="Deluxe Basket",
                slug="DeluxeBasket",
                description="Deluxe Basket",
                is_active=True,
                is_featured=True,
                image="No Image",
            ),
            Hamper(
                name="Bulk Basket",
                slug="BulkBasket",
                description="Bulk Basket",
                is_active=True,
                is_featured=True,
            ),
            Hamper(
                name="Wedding Basket",
                slug="WeddingBasket",
                description="Wedding Basket",
                is_active=True,
                is_featured=True,
            ),
            Hamper(
                name="Medical Hamper",
                slug="MedicalHamper",
                description="All your medical needs",
                is_active=True,
                is_featured=True,
            ),
        ]
    )

    for idx, hamper in enumerate(Hamper.objects.all(), start=1):
        img = open(
            "{}/seed/hampers/hamper{}.jpeg".format(settings.MEDIA_ROOT, idx), "rb"
        )
        hamper.image.save("{}.jpg".format(hamper.slug), img, save=True)


def create_hamper_items():
    """create hamper items"""
    print("** creating hamper items")
    create_hampers()
    for h in Hamper.objects.all():
        for _ in range(6):
            hi = HamperItem(hamper=h, product=Product.objects.order_by("?").first())
            hi.save()


def create_front_sections():
    print("** creating front sections")

    FrontSectionItem.objects.bulk_create(
        [
            FrontSectionItem(
                name="Health and Beauty",
                slug="Health and Beauty",
                category=Category.objects.filter(name="Health and Beauty").first(),
                help_text=fake.sentence(),
                description=fake.sentence(),
                meta_keywords=fake.name(),
                is_active=True,
            ),
            FrontSectionItem(
                name="Dairy",
                category=Category.objects.filter(name="Dairy").first(),
                slug="staionary",
                help_text=fake.sentence(),
                description=fake.sentence(),
                meta_keywords=fake.name(),
                is_active=True,
            ),
            FrontSectionItem(
                name="Frequently Bought",
                category=Category.objects.filter(name="Grocery").first(),
                slug="FrequentlyBought",
                help_text=fake.sentence(),
                description=fake.sentence(),
                meta_keywords=fake.name(),
                is_active=True,
            ),
            FrontSectionItem(
                name="Stationary",
                category=Category.objects.filter(name="Stationary").first(),
                slug="Stationary",
                help_text=fake.sentence(),
                description=fake.sentence(),
                meta_keywords=fake.name(),
                is_active=True,
            ),
        ]
    )


def populate_front_sections():
    print("** populate front sections")

    # Frequenctly Bought in Front Section
    product_list = []
    fs = FrontSectionItem.objects.get(name__icontains="Frequently Bought")
    frequent_products = [
        "Mazoe Orange",
        "Zimgold Cooking Oil",
        "Red Seal",
        "Sunlight",
        "Baked Beans",
    ]

    for item in frequent_products:
        product = Product.objects.get(name__icontains=item)
        product_list.append(product)

    fs.products.add(*product_list)

    # Stationary items in front section
    product_list = []
    fs = FrontSectionItem.objects.get(name__icontains="On Promotion")
    stationary_items = ["Scissors", "Sellotape", "Pencils", "Pens", "Khakhi Covers"]

    for item in stationary_items:
        product = Product.objects.get(name__icontains=item)
        product_list.append(product)

    fs.products.add(*product_list)

    # Fresh items in front section
    product_list = []
    fs = FrontSectionItem.objects.get(name__icontains="Fresh")
    fresh_products = ["Bananas", "Rape", "Carrrots", "Potatoes", "Apples", "Supa Milk"]

    for item in fresh_products:
        product = Product.objects.get(name__icontains=item)
        product_list.append(product)
    fs.products.add(*product_list)

    # On Promotionitems in front section
    product_list = []
    fs = FrontSectionItem.objects.get(name__icontains="On Promotion")
    promoted_products = [
        "Dendairy Salted Butter",
        "Cremora",
        "Lemons",
        "Vaseline",
        "Duck Toilet Cleaner",
        "Sun Jam",
    ]

    for item in promoted_products:
        product = Product.objects.get(name__icontains=item)
        product_list.append(product)
    fs.products.add(*product_list)


def create_recipients():
    print("** creating recipients")
    for _ in range(1, 10):
        recipient = Recipient.objects.create(
            first_name=fake.name(),
            last_name=fake.last_name(),
            phone_number_1="824-075-85583",
            phone_number_2="867-075-85456",
            address_line_1=fake.secondary_address(),
            address_line_2=fake.street_address(),
            email_address=fake.ascii_email(),
            id_number=fake.random_letters(),
            surburb=fake.state(),
            city=random.choice(["Harare", "Bulawayo"]),
            user=random.choice([User.objects.all()[3], User.objects.all()[2], User.objects.all()[1], User.objects.all()[4]])
        )

        recipient.save()


def create_orders():
    print("** creating orders")

    for n in range(1, 10):
        order = Order(
            user=User.objects.all()[n],
            date_created=datetime.datetime.now(),
            recipient=Recipient.objects.order_by("?").first(),
            state=random.choice(
                [
                    "ready for collection",
                    "awaiting payment",
                    "ready for packing",
                    "in transit",
                    "collected",
                    "delivered",
                ]
            ),
            delivery_method=random.choice(["Collection", "Delivery"]),
            security_question=fake.sentence(),
            security_answer=fake.city(),
        )
        order.save()


def create_order_items():
    """
    This must only be run after orders have been created:
    after create_orders()
    """
    print("** creating order items **")
    products = Product.objects.all()
    orders = Order.objects.all()

    for order in orders:
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    date_added=datetime.datetime.now(),
                    quantity=random.randint(1, 13),
                    unit_price=decimal.Decimal(random.choice(products).price),
                    product=random.choice(products),
                ),
                OrderItem(
                    order=order,
                    date_added=datetime.datetime.now(),
                    quantity=random.randint(1, 13),
                    unit_price=decimal.Decimal(random.choice(products).price),
                    product=random.choice(products),
                ),
                OrderItem(
                    order=order,
                    date_added=datetime.datetime.now(),
                    quantity=random.randint(1, 13),
                    unit_price=decimal.Decimal(random.choice(products).price),
                    product=random.choice(products),
                ),
                OrderItem(
                    order=order,
                    date_added=datetime.datetime.now(),
                    quantity=random.randint(1, 13),
                    unit_price=decimal.Decimal(random.choice(products).price),
                    product=random.choice(products),
                ),
            ]
        )


def create_pickup_points():
    print("** creating pick up points **")
    for _ in range(0, 10):
        pp = PickupPoint.objects.create(
            name=fake.last_name(),
            phone_number_1="824-075-85583",
            phone_number_2="867-075-85456",
            address_line_1=fake.secondary_address(),
            address_line_2=fake.street_address(),
            surburb=fake.state(),
            city=random.choice(["Harare", "Bulawayo"]),
            office_hours="9am to 5pm",
        )
        pp.save()


def create_users():
    print("** creating users **")

    for n in range(0, 5):
        new_user = User.objects.create(
            username="test_{}@thumela.co.zw".format(n),
            first_name="test+{}".format(n),
            last_name="test+{}".format(n),
            email="test_{}@thumela.co.zw".format(n),
        )

        new_user.save()

        new_user.set_password("test")
        new_user.is_active = True
        new_user.save()

    # Add a super user for customer support
    new_user = User.objects.create(
        username="support@thumela.co.zw",
        first_name="support",
        last_name="support",
        email="support@thumela.co.zw",
    )
    new_user.save()
    new_user.set_password("test")
    new_user.is_active = True
    new_user.is_superuser = True
    # allow user access to admin backend
    new_user.is_staff = True
    new_user.save()

    new_user = User.objects.create(
        username="khayelihle.tshuma@thumela.co.zw",
        first_name="support",
        last_name="support",
        email="khayelihle.tshuma@thumela.co.zw",
    )
    new_user.save()
    new_user.set_password("test")
    new_user.is_active = True
    new_user.is_superuser = True
    # allow user access to admin backend
    new_user.is_staff = True
    new_user.save()

    new_user = User.objects.create(
        username="patrick@thumela.co.zw",
        first_name="patrick",
        last_name="patrick",
        email="patrick@thumela.co.zw",
    )
    new_user.save()
    new_user.set_password("test")
    new_user.is_active = True
    new_user.is_superuser = True
    # allow user access to admin backend
    new_user.is_staff = True
    new_user.save()


def run_seed(self):  # pylint: disable=unused-argument
    """
    order matters !!!
    """
    print("** seeding thumela application")

    clear_data()
    create_users()
    create_categories()
    create_products()
    create_hamper_items()
    create_front_sections()
    create_recipients()
    create_orders()
    create_order_items()
    create_couriers()
    create_suppliers()
    create_pickup_points()

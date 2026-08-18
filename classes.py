from abc import ABC, abstractmethod
from enum import Enum


# =========================
# USER / CUSTOMER
# =========================

class User:
    def __init__(self, user_id, name, email):
        self._user_id = user_id
        self._name = name
        self._email = email

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email


class Customer(User, ABC):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self._orders = []

    @abstractmethod
    def calculate_discount(self, amount):
        pass

    @abstractmethod
    def has_free_shipping(self, order_amount):
        pass

    def add_order(self, order):
        self._orders.append(order)

    @property
    def orders(self):
        return list(self._orders)


class RegularCustomer(Customer):
    def calculate_discount(self, amount):
        return 0

    def has_free_shipping(self, order_amount):
        return False


class PremiumCustomer(Customer):
    def calculate_discount(self, amount):
        return amount * 0.10

    def has_free_shipping(self, order_amount):
        return True


class BusinessCustomer(Customer):
    def calculate_discount(self, amount):
        return amount * 0.15

    def has_free_shipping(self, order_amount):
        # Business customers get free shipping on orders >= 5000
        return order_amount >= 5000


class Admin(User):
    pass


# =========================
# PRODUCT
# =========================

class Product(ABC):
    def __init__(self, product_id, name, description, base_price):
        self._product_id = product_id
        self._name = name
        self._description = description
        self._base_price = base_price

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def base_price(self):
        return self._base_price

    @abstractmethod
    def calculate_price(self):
        pass

    @abstractmethod
    def requires_shipping(self):
        pass


class PhysicalProduct(Product):
    def __init__(
        self,
        product_id,
        name,
        description,
        base_price,
        stock,
        weight,
        dimensions
    ):
        super().__init__(
            product_id,
            name,
            description,
            base_price
        )
        self._stock = stock
        self._weight = weight
        self._dimensions = dimensions

    @property
    def stock(self):
        return self._stock

    @property
    def weight(self):
        return self._weight

    @property
    def dimensions(self):
        return self._dimensions

    def calculate_price(self):
        return self._base_price

    def requires_shipping(self):
        return True

    def reduce_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if quantity > self._stock:
            raise ValueError("Not enough stock available.")

        self._stock -= quantity


class DigitalProduct(Product):
    def __init__(
        self,
        product_id,
        name,
        description,
        base_price,
        download_link
    ):
        super().__init__(
            product_id,
            name,
            description,
            base_price
        )
        self._download_link = download_link

    @property
    def download_link(self):
        return self._download_link

    def calculate_price(self):
        return self._base_price

    def requires_shipping(self):
        return False


class SubscriptionProduct(Product):
    def __init__(
        self,
        product_id,
        name,
        description,
        base_price,
        duration_months,
        auto_renew=True
    ):
        super().__init__(
            product_id,
            name,
            description,
            base_price
        )
        self._duration_months = duration_months
        self._auto_renew = auto_renew

    @property
    def duration_months(self):
        return self._duration_months

    @property
    def auto_renew(self):
        return self._auto_renew

    def calculate_price(self):
        return self._base_price

    def requires_shipping(self):
        return False


# =========================
# SHOPPING CART
# =========================

class OrderItem:
    def __init__(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self._product = product
        self._quantity = quantity

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    def calculate_subtotal(self):
        return self._product.calculate_price() * self._quantity


class ShoppingCart:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return list(self._items)

    def add_item(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        # If physical product, check stock before adding
        if isinstance(product, PhysicalProduct):
            if quantity > product.stock:
                raise ValueError("Not enough stock available.")

        for item in self._items:
            if item.product.product_id == product.product_id:
                new_quantity = item.quantity + quantity

                if isinstance(product, PhysicalProduct):
                    if new_quantity > product.stock:
                        raise ValueError("Not enough stock available.")

                item._quantity = new_quantity
                return

        self._items.append(OrderItem(product, quantity))

    def remove_item(self, product_id):
        self._items = [
            item for item in self._items
            if item.product.product_id != product_id
        ]

    def calculate_subtotal(self):
        return sum(
            item.calculate_subtotal()
            for item in self._items
        )

    def is_empty(self):
        return len(self._items) == 0

    def clear(self):
        self._items.clear()


# =========================
# DELIVERY
# =========================

class DeliveryMethod(ABC):
    @abstractmethod
    def calculate_shipping_cost(self, order_amount):
        pass

    @abstractmethod
    def estimate_delivery_time(self):
        pass


class StandardDelivery(DeliveryMethod):
    def calculate_shipping_cost(self, order_amount):
        return 5

    def estimate_delivery_time(self):
        return "5 days"


class ExpressDelivery(DeliveryMethod):
    def calculate_shipping_cost(self, order_amount):
        return 15

    def estimate_delivery_time(self):
        return "2 days"


class SameDayDelivery(DeliveryMethod):
    def calculate_shipping_cost(self, order_amount):
        return 30

    def estimate_delivery_time(self):
        return "Same day"


# =========================
# PAYMENT
# =========================

class PaymentMethod(ABC):
    def __init__(self):
        self._paid = False
        self._refunded = False

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

    @property
    def paid(self):
        return self._paid

    @property
    def refunded(self):
        return self._refunded


class CreditCard(PaymentMethod):
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        self._paid = True
        return f"Credit Card payment of ${amount:.2f} successful."

    def refund(self, amount):
        if not self._paid:
            raise ValueError("Payment has not been completed.")

        if self._refunded:
            raise ValueError("Payment cannot be refunded twice.")

        self._refunded = True
        return f"Credit Card refund of ${amount:.2f} successful."


class BankTransfer(PaymentMethod):
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        self._paid = True
        return f"Bank Transfer payment of ${amount:.2f} successful."

    def refund(self, amount):
        if not self._paid:
            raise ValueError("Payment has not been completed.")

        if self._refunded:
            raise ValueError("Payment cannot be refunded twice.")

        self._refunded = True
        return f"Bank Transfer refund of ${amount:.2f} successful."


class DigitalWallet(PaymentMethod):
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        self._paid = True
        return f"Digital Wallet payment of ${amount:.2f} successful."

    def refund(self, amount):
        if not self._paid:
            raise ValueError("Payment has not been completed.")

        if self._refunded:
            raise ValueError("Payment cannot be refunded twice.")

        self._refunded = True
        return f"Digital Wallet refund of ${amount:.2f} successful."


# =========================
# DISCOUNT
# =========================

class Discount(ABC):
    @abstractmethod
    def apply_discount(self, order_amount):
        pass


class PercentageDiscount(Discount):
    def __init__(self, percentage):
        self._percentage = percentage

    def apply_discount(self, order_amount):
        if order_amount < 0:
            return 0

        discount = order_amount * (self._percentage / 100)
        return min(discount, order_amount)


class FixedAmountDiscount(Discount):
    def __init__(self, amount):
        self._amount = amount

    def apply_discount(self, order_amount):
        if order_amount < 0:
            return 0

        return min(self._amount, order_amount)


class BuyOneGetOneDiscount(Discount):
    def apply_discount(self, order_amount):
        # Demonstration discount: 50% of eligible amount
        return order_amount * 0.50


class SeasonalDiscount(Discount):
    def __init__(self, percentage):
        self._percentage = percentage

    def apply_discount(self, order_amount):
        if order_amount < 0:
            return 0

        discount = order_amount * (self._percentage / 100)
        return min(discount, order_amount)


# =========================
# ORDER STATUS
# =========================

class OrderStatus(Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


# =========================
# ORDER
# =========================

class Order:
    def __init__(
        self,
        order_id,
        customer,
        delivery_method,
        payment_method,
        tax_rate=0.105
    ):
        self._order_id = order_id
        self._customer = customer
        self._items = []
        self._delivery_method = delivery_method
        self._payment_method = payment_method
        self._discount = None
        self._status = OrderStatus.CREATED
        self._tax_rate = tax_rate
        self._total_amount = 0

    @property
    def order_id(self):
        return self._order_id

    @property
    def customer(self):
        return self._customer

    @property
    def items(self):
        return list(self._items)

    @property
    def status(self):
        return self._status

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def delivery_method(self):
        return self._delivery_method

    @property
    def payment_method(self):
        return self._payment_method

    def add_item(self, product, quantity):
        if self._status != OrderStatus.CREATED:
            raise ValueError("Items can only be added to a created order.")

        item = OrderItem(product, quantity)
        self._items.append(item)

    def remove_item(self, product_id):
        if self._status != OrderStatus.CREATED:
            raise ValueError("Items can only be removed from a created order.")

        self._items = [
            item for item in self._items
            if item.product.product_id != product_id
        ]

    def set_discount(self, discount):
        self._discount = discount

    def calculate_subtotal(self):
        return sum(
            item.calculate_subtotal()
            for item in self._items
        )

    def calculate_tax(self, amount):
        return amount * self._tax_rate

    def calculate_shipping(self, amount):
        if self._customer.has_free_shipping(amount):
            return 0

        return self._delivery_method.calculate_shipping_cost(amount)

    def calculate_total(self):
        if not self._items:
            return 0

        subtotal = self.calculate_subtotal()

        customer_discount = self._customer.calculate_discount(subtotal)

        promotional_discount = 0
        if self._discount is not None:
            promotional_discount = self._discount.apply_discount(
                subtotal
            )

        discounted_amount = max(
            0,
            subtotal - customer_discount - promotional_discount
        )

        tax = self.calculate_tax(discounted_amount)

        shipping = self.calculate_shipping(subtotal)

        self._total_amount = max(
            0,
            discounted_amount + tax + shipping
        )

        return self._total_amount

    # =========================
    # ORDER LIFECYCLE
    # =========================

    def confirm(self):
        if not self._items:
            raise ValueError("An order with no items cannot be confirmed.")

        if self._status != OrderStatus.CREATED:
            raise ValueError("Only a created order can be confirmed.")

        self.calculate_total()
        self._status = OrderStatus.CONFIRMED

    def pay(self):
        if self._status != OrderStatus.CONFIRMED:
            raise ValueError("Only a confirmed order can be paid.")

        message = self._payment_method.pay(self._total_amount)
        self._status = OrderStatus.PAID

        return message

    def process(self):
        if self._status != OrderStatus.PAID:
            raise ValueError("Only a paid order can be processed.")

        self._status = OrderStatus.PROCESSING

    def ship(self):
        if self._status != OrderStatus.PROCESSING:
            raise ValueError("Only a processing order can be shipped.")

        self._reduce_product_stock()
        self._status = OrderStatus.SHIPPED

    def deliver(self):
        if self._status != OrderStatus.SHIPPED:
            raise ValueError("Only a shipped order can be delivered.")

        self._status = OrderStatus.DELIVERED

    def cancel(self):
        if self._status in (
            OrderStatus.DELIVERED,
            OrderStatus.REFUNDED
        ):
            raise ValueError(
                "Delivered or refunded orders cannot be cancelled."
            )

        if self._status == OrderStatus.SHIPPED:
            raise ValueError("A shipped order cannot be cancelled.")

        self._status = OrderStatus.CANCELLED

    def refund(self):
        if self._status != OrderStatus.PAID:
            raise ValueError(
                "Only a paid order can be refunded."
            )

        message = self._payment_method.refund(
            self._total_amount
        )

        self._status = OrderStatus.REFUNDED

        return message

    def _reduce_product_stock(self):
        for item in self._items:
            if isinstance(item.product, PhysicalProduct):
                item.product.reduce_stock(item.quantity)


# =========================
# INVOICE
# =========================

class Invoice:
    def __init__(self, invoice_id, order):
        self._invoice_id = invoice_id
        self._order = order

    @property
    def invoice_id(self):
        return self._invoice_id

    @property
    def order(self):
        return self._order

    def generate(self):
        return {
            "invoice_id": self._invoice_id,
            "order_id": self._order.order_id,
            "customer": self._order.customer.name,
            "total": self._order.total_amount,
            "status": self._order.status.value
        }


# =========================
# REFUND
# =========================

class Refund:
    def __init__(self, refund_id, order, amount):
        self._refund_id = refund_id
        self._order = order
        self._amount = amount
        self._completed = False

    @property
    def refund_id(self):
        return self._refund_id

    @property
    def amount(self):
        return self._amount

    @property
    def completed(self):
        return self._completed

    def process(self):
        if self._completed:
            raise ValueError("Refund has already been processed.")

        if self._order.status != OrderStatus.PAID:
            raise ValueError(
                "Refund can only be processed for a paid order."
            )

        message = self._order.refund()
        self._completed = True

        return message


# =========================
# STORE - AGGREGATION
# =========================

class Store:
    def __init__(self, name):
        self._name = name
        self._products = []

    @property
    def name(self):
        return self._name

    @property
    def products(self):
        return list(self._products)

    def add_product(self, product):
        self._products.append(product)

    def remove_product(self, product_id):
        self._products = [
            product
            for product in self._products
            if product.product_id != product_id
        ]
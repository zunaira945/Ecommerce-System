import tkinter as tk
from tkinter import ttk, messagebox

from classes import (
    PhysicalProduct,
    DigitalProduct,
    SubscriptionProduct,
    RegularCustomer,
    PremiumCustomer,
    BusinessCustomer,
    StandardDelivery,
    ExpressDelivery,
    SameDayDelivery,
    CreditCard,
    BankTransfer,
    DigitalWallet,
    PercentageDiscount,
    FixedAmountDiscount,
    BuyOneGetOneDiscount,
    SeasonalDiscount,
    Order,
    ShoppingCart,
    Store,
)


# =============================================================
# DESIGN TOKENS
# =============================================================

COLORS = {
    "bg": "#F1F5F9",            # app background
    "surface": "#FFFFFF",       # cards / panels
    "border": "#E2E8F0",

    "sidebar": "#111827",       # sidebar background
    "sidebar_hover": "#1F2937",
    "sidebar_active": "#2563EB",
    "sidebar_text": "#CBD5E1",
    "sidebar_text_active": "#FFFFFF",
    "sidebar_muted": "#64748B",

    "text": "#0F172A",
    "text_muted": "#64748B",

    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "success": "#16A34A",
    "success_hover": "#15803D",
    "danger": "#DC2626",
    "danger_hover": "#B91C1C",
    "warning": "#D97706",
    "warning_hover": "#B45309",
    "neutral": "#475569",
    "neutral_hover": "#334155",

    "badge_created": "#94A3B8",
    "badge_confirmed": "#2563EB",
    "badge_paid": "#0891B2",
    "badge_processing": "#D97706",
    "badge_shipped": "#7C3AED",
    "badge_delivered": "#16A34A",
    "badge_cancelled": "#DC2626",
    "badge_refunded": "#64748B",
}

FONT_FAMILY = "Segoe UI"

NAV_ITEMS = [
    ("dashboard", "\U0001F3E0  Dashboard"),
    ("products", "\U0001F6CD  Products"),
    ("cart", "\U0001F6D2  Cart"),
    ("checkout", "\U0001F9FE  Checkout"),
    ("orders", "\U0001F4E6  Orders"),
]

STATUS_BADGE_COLORS = {
    "CREATED": COLORS["badge_created"],
    "CONFIRMED": COLORS["badge_confirmed"],
    "PAID": COLORS["badge_paid"],
    "PROCESSING": COLORS["badge_processing"],
    "SHIPPED": COLORS["badge_shipped"],
    "DELIVERED": COLORS["badge_delivered"],
    "CANCELLED": COLORS["badge_cancelled"],
    "REFUNDED": COLORS["badge_refunded"],
}

CUSTOMER_TYPES = ["Regular Customer", "Premium Customer", "Business Customer"]
DELIVERY_METHODS = ["Standard Delivery", "Express Delivery", "Same Day Delivery"]
DISCOUNT_OPTIONS = [
    "No Discount",
    "10% Off (Percentage)",
    "$50 Off (Fixed Amount)",
    "Buy One Get One (50% Off)",
    "Seasonal 15% Off",
]
PAYMENT_METHODS = ["Credit Card", "Bank Transfer", "Digital Wallet"]

PRODUCT_TYPES = ["Physical Product", "Digital Product", "Subscription Product"]


class EcommerceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Order & Delivery Management System")
        self.root.geometry("1240x780")
        self.root.minsize(1080, 660)
        self.root.configure(bg=COLORS["bg"])

        # ---------------------------------------------------
        # DATA (same OOP classes / logic as classes.py)
        # ---------------------------------------------------
        self.store = Store("ShopSphere")
        self.seed_products()

        self.cart = ShoppingCart()
        self.orders = []              # list[Order] (confirmed + paid orders)
        self.order_counter = 1001
        self.checkout_context = None  # dict of real objects set on "Confirm Order"

        self.nav_buttons = {}
        self.pages = {}
        self.current_page = None

        self.setup_style()
        self.build_layout()

        self.refresh_products()
        self.refresh_cart()
        self.refresh_orders_table()
        self.refresh_dashboard()

        self.show_page("dashboard")

    def seed_products(self):
        self.store.add_product(
            PhysicalProduct(
                1, "Laptop", "High performance laptop",
                1000, 10, "2 kg", "35 x 24 x 2 cm"
            )
        )
        self.store.add_product(
            PhysicalProduct(
                2, "Headphones", "Wireless noise-cancelling headphones",
                100, 20, "0.5 kg", "20 x 18 x 8 cm"
            )
        )
        self.store.add_product(
            DigitalProduct(
                3, "Python Course", "Complete Python programming course",
                200, "download/python-course"
            )
        )
        self.store.add_product(
            SubscriptionProduct(
                4, "Premium Membership", "Monthly premium subscription",
                50, 1, True
            )
        )

    # =========================================================
    # STYLE
    # =========================================================

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(".", font=(FONT_FAMILY, 10))

        style.configure("App.TFrame", background=COLORS["bg"])
        style.configure("Surface.TFrame", background=COLORS["surface"])
        style.configure("Sidebar.TFrame", background=COLORS["sidebar"])

        style.configure(
            "PageTitle.TLabel", font=(FONT_FAMILY, 20, "bold"),
            background=COLORS["bg"], foreground=COLORS["text"]
        )
        style.configure(
            "PageSubtitle.TLabel", font=(FONT_FAMILY, 10),
            background=COLORS["bg"], foreground=COLORS["text_muted"]
        )
        style.configure(
            "CardTitle.TLabel", font=(FONT_FAMILY, 12, "bold"),
            background=COLORS["surface"], foreground=COLORS["text"]
        )
        style.configure(
            "Body.TLabel", font=(FONT_FAMILY, 10),
            background=COLORS["surface"], foreground=COLORS["text"]
        )
        style.configure(
            "Muted.TLabel", font=(FONT_FAMILY, 9),
            background=COLORS["surface"], foreground=COLORS["text_muted"]
        )
        style.configure(
            "StatValue.TLabel", font=(FONT_FAMILY, 22, "bold"),
            background=COLORS["surface"], foreground=COLORS["text"]
        )
        style.configure(
            "StatLabel.TLabel", font=(FONT_FAMILY, 9, "bold"),
            background=COLORS["surface"], foreground=COLORS["text_muted"]
        )
        style.configure(
            "SummaryLabel.TLabel", font=(FONT_FAMILY, 10),
            background=COLORS["surface"], foreground=COLORS["text_muted"]
        )
        style.configure(
            "SummaryValue.TLabel", font=(FONT_FAMILY, 10, "bold"),
            background=COLORS["surface"], foreground=COLORS["text"]
        )
        style.configure(
            "TotalLabel.TLabel", font=(FONT_FAMILY, 14, "bold"),
            background=COLORS["surface"], foreground=COLORS["text"]
        )
        style.configure(
            "TotalValue.TLabel", font=(FONT_FAMILY, 18, "bold"),
            background=COLORS["surface"], foreground=COLORS["primary"]
        )

        # --- Buttons -----------------------------------------
        style.configure(
            "Primary.TButton", font=(FONT_FAMILY, 10, "bold"), padding=(14, 9),
            background=COLORS["primary"], foreground="#FFFFFF", borderwidth=0,
            focuscolor=COLORS["primary"]
        )
        style.map(
            "Primary.TButton",
            background=[("active", COLORS["primary_hover"]), ("disabled", "#93C5FD")]
        )

        style.configure(
            "Success.TButton", font=(FONT_FAMILY, 10, "bold"), padding=(14, 9),
            background=COLORS["success"], foreground="#FFFFFF", borderwidth=0
        )
        style.map(
            "Success.TButton",
            background=[("active", COLORS["success_hover"]), ("disabled", "#86EFAC")]
        )

        style.configure(
            "Danger.TButton", font=(FONT_FAMILY, 10, "bold"), padding=(12, 8),
            background=COLORS["danger"], foreground="#FFFFFF", borderwidth=0
        )
        style.map(
            "Danger.TButton",
            background=[("active", COLORS["danger_hover"]), ("disabled", "#FCA5A5")]
        )

        style.configure(
            "Warning.TButton", font=(FONT_FAMILY, 10, "bold"), padding=(12, 8),
            background=COLORS["warning"], foreground="#FFFFFF", borderwidth=0
        )
        style.map(
            "Warning.TButton",
            background=[("active", COLORS["warning_hover"]), ("disabled", "#FCD34D")]
        )

        style.configure(
            "Secondary.TButton", font=(FONT_FAMILY, 10, "bold"), padding=(12, 8),
            background="#E2E8F0", foreground=COLORS["text"], borderwidth=0
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#CBD5E1"), ("disabled", "#F1F5F9")]
        )

        style.configure(
            "Neutral.TButton", font=(FONT_FAMILY, 10, "bold"), padding=(12, 8),
            background=COLORS["neutral"], foreground="#FFFFFF", borderwidth=0
        )
        style.map(
            "Neutral.TButton",
            background=[("active", COLORS["neutral_hover"]), ("disabled", "#94A3B8")]
        )

        # --- Sidebar nav buttons -------------------------------
        style.configure(
            "Nav.TButton", font=(FONT_FAMILY, 11), padding=(16, 12),
            background=COLORS["sidebar"], foreground=COLORS["sidebar_text"],
            borderwidth=0, anchor="w"
        )
        style.map(
            "Nav.TButton",
            background=[("active", COLORS["sidebar_hover"])],
            foreground=[("active", COLORS["sidebar_text_active"])]
        )

        style.configure(
            "NavActive.TButton", font=(FONT_FAMILY, 11, "bold"), padding=(16, 12),
            background=COLORS["sidebar_active"], foreground=COLORS["sidebar_text_active"],
            borderwidth=0, anchor="w"
        )
        style.map("NavActive.TButton", background=[("active", COLORS["sidebar_active"])])

        # --- Combobox / Entry ------------------------------------
        style.configure("TCombobox", padding=6, fieldbackground="#FFFFFF", background="#FFFFFF")
        style.configure("TEntry", padding=6)

        # --- Treeview --------------------------------------------
        style.configure(
            "Modern.Treeview", font=(FONT_FAMILY, 10), rowheight=30,
            background="#FFFFFF", fieldbackground="#FFFFFF",
            foreground=COLORS["text"], borderwidth=0
        )
        style.configure(
            "Modern.Treeview.Heading", font=(FONT_FAMILY, 10, "bold"),
            background="#F8FAFC", foreground=COLORS["text_muted"],
            borderwidth=0, relief="flat"
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", COLORS["text"])]
        )

        style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
        style.configure("TRadiobutton", background=COLORS["surface"], font=(FONT_FAMILY, 10))
        style.configure("TCheckbutton", background=COLORS["surface"], font=(FONT_FAMILY, 10))

    # =========================================================
    # LAYOUT
    # =========================================================

    def build_layout(self):
        container = tk.Frame(self.root, bg=COLORS["bg"])
        container.pack(fill="both", expand=True)

        self.build_sidebar(container)

        content_outer = tk.Frame(container, bg=COLORS["bg"])
        content_outer.pack(side="left", fill="both", expand=True)

        self.pages_container = tk.Frame(content_outer, bg=COLORS["bg"])
        self.pages_container.pack(fill="both", expand=True, padx=28, pady=22)
        self.pages_container.grid_rowconfigure(0, weight=1)
        self.pages_container.grid_columnconfigure(0, weight=1)

        self.pages["dashboard"] = self.build_dashboard_page(self.pages_container)
        self.pages["products"] = self.build_products_page(self.pages_container)
        self.pages["cart"] = self.build_cart_page(self.pages_container)
        self.pages["checkout"] = self.build_checkout_page(self.pages_container)
        self.pages["payment"] = self.build_payment_page(self.pages_container)
        self.pages["orders"] = self.build_orders_page(self.pages_container)

        for frame in self.pages.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=COLORS["sidebar"], width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=COLORS["sidebar"])
        brand.pack(fill="x", pady=(26, 30), padx=20)

        tk.Label(
            brand, text="\U0001F6CD  ShopSphere", font=(FONT_FAMILY, 15, "bold"),
            bg=COLORS["sidebar"], fg="#FFFFFF"
        ).pack(anchor="w")

        tk.Label(
            brand, text="Order & Delivery Manager", font=(FONT_FAMILY, 8),
            bg=COLORS["sidebar"], fg=COLORS["sidebar_muted"]
        ).pack(anchor="w", pady=(2, 0))

        nav_frame = tk.Frame(sidebar, bg=COLORS["sidebar"])
        nav_frame.pack(fill="x")

        for key, label in NAV_ITEMS:
            btn = ttk.Button(
                nav_frame, text=label, style="Nav.TButton",
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[key] = btn

        tk.Frame(sidebar, bg=COLORS["sidebar"]).pack(fill="both", expand=True)

        footer = tk.Frame(sidebar, bg=COLORS["sidebar"])
        footer.pack(fill="x", padx=20, pady=18)

        tk.Frame(footer, bg=COLORS["sidebar_hover"], height=1).pack(fill="x", pady=(0, 12))

        self.sidebar_orders_label = tk.Label(
            footer, text="0 orders placed", font=(FONT_FAMILY, 9),
            bg=COLORS["sidebar"], fg=COLORS["sidebar_muted"]
        )
        self.sidebar_orders_label.pack(anchor="w")

    def show_page(self, key):
        if key == "checkout" and self.cart.is_empty():
            messagebox.showwarning(
                "Cart is Empty", "Add products to your cart before checking out."
            )
            key = "cart"

        if key == "payment" and self.checkout_context is None:
            messagebox.showwarning(
                "Checkout Required", "Please complete checkout before proceeding to payment."
            )
            key = "checkout"

        self.current_page = key
        self.pages[key].tkraise()

        for nav_key, btn in self.nav_buttons.items():
            btn.configure(style="NavActive.TButton" if nav_key == key else "Nav.TButton")

        if key == "dashboard":
            self.refresh_dashboard()
        elif key == "products":
            self.refresh_products()
        elif key == "cart":
            self.refresh_cart()
        elif key == "checkout":
            self.refresh_checkout_summary()
        elif key == "payment":
            self.refresh_payment_summary()
        elif key == "orders":
            self.refresh_orders_table()

    # =========================================================
    # SHARED UI HELPERS
    # =========================================================

    def page_header(self, parent, title, subtitle):
        header = ttk.Frame(parent, style="App.TFrame")
        header.pack(fill="x", pady=(0, 18))

        ttk.Label(header, text=title, style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(header, text=subtitle, style="PageSubtitle.TLabel").pack(anchor="w", pady=(3, 0))

    def card(self, parent, padding=18):
        outer = tk.Frame(parent, bg=COLORS["border"])
        inner_card = tk.Frame(outer, bg=COLORS["surface"])
        inner_card.pack(fill="both", expand=True, padx=1, pady=1)
        inner = ttk.Frame(inner_card, style="Surface.TFrame", padding=padding)
        inner.pack(fill="both", expand=True)
        return outer, inner

    def make_treeview(self, parent, columns, headings, widths, height=10):
        tree = ttk.Treeview(
            parent, columns=columns, show="headings", height=height, style="Modern.Treeview"
        )
        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], anchor="center")
        return tree

    def labeled_field(self, parent, label_text):
        frame = ttk.Frame(parent, style="Surface.TFrame")
        frame.pack(fill="x", pady=6)
        ttk.Label(frame, text=label_text, style="Body.TLabel").pack(anchor="w", pady=(0, 4))
        return frame

    # =========================================================
    # DASHBOARD PAGE
    # =========================================================

    def build_dashboard_page(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")

        self.page_header(page, "Dashboard", "A quick overview of your store's activity.")

        stats_row = ttk.Frame(page, style="App.TFrame")
        stats_row.pack(fill="x", pady=(0, 20))

        self.stat_vars = {}
        stat_defs = [
            ("products", "TOTAL PRODUCTS"),
            ("cart_items", "ITEMS IN CART"),
            ("orders", "TOTAL ORDERS"),
            ("revenue", "REVENUE COLLECTED"),
        ]

        for i, (key, label) in enumerate(stat_defs):
            outer, inner = self.card(stats_row)
            outer.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 10, 0))

            ttk.Label(inner, text=label, style="StatLabel.TLabel").pack(anchor="w")
            value_label = ttk.Label(inner, text="0", style="StatValue.TLabel")
            value_label.pack(anchor="w", pady=(6, 0))
            self.stat_vars[key] = value_label

        lower_row = ttk.Frame(page, style="App.TFrame")
        lower_row.pack(fill="both", expand=True)

        recent_outer, recent_inner = self.card(lower_row)
        recent_outer.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(recent_inner, text="Recent Orders", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 12))

        columns = ("id", "customer", "total", "status")
        self.dashboard_orders_tree = self.make_treeview(
            recent_inner, columns,
            {"id": "Order ID", "customer": "Customer", "total": "Total", "status": "Status"},
            {"id": 90, "customer": 160, "total": 100, "status": 130},
            height=8
        )
        self.dashboard_orders_tree.pack(fill="both", expand=True)

        actions_outer, actions_inner = self.card(lower_row)
        actions_outer.pack(side="right", fill="both")
        actions_outer.configure(width=260)

        ttk.Label(actions_inner, text="Quick Actions", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 14))

        ttk.Button(
            actions_inner, text="Browse Products", style="Primary.TButton",
            command=lambda: self.show_page("products")
        ).pack(fill="x", pady=4)

        ttk.Button(
            actions_inner, text="View Cart", style="Secondary.TButton",
            command=lambda: self.show_page("cart")
        ).pack(fill="x", pady=4)

        ttk.Button(
            actions_inner, text="View Orders", style="Secondary.TButton",
            command=lambda: self.show_page("orders")
        ).pack(fill="x", pady=4)

        ttk.Button(
            actions_inner, text="+ Add New Product", style="Success.TButton",
            command=self.open_add_product_dialog
        ).pack(fill="x", pady=(16, 4))

        return page

    def refresh_dashboard(self):
        self.stat_vars["products"].configure(text=str(len(self.store.products)))

        cart_item_count = sum(item.quantity for item in self.cart.items)
        self.stat_vars["cart_items"].configure(text=str(cart_item_count))

        self.stat_vars["orders"].configure(text=str(len(self.orders)))

        revenue = sum(
            order.total_amount
            for order in self.orders
            if order.status.value in ("PAID", "PROCESSING", "SHIPPED", "DELIVERED")
        )
        self.stat_vars["revenue"].configure(text=f"${revenue:,.2f}")

        self.sidebar_orders_label.configure(text=f"{len(self.orders)} orders placed")

        for row in self.dashboard_orders_tree.get_children():
            self.dashboard_orders_tree.delete(row)

        for order in list(reversed(self.orders))[:8]:
            self.dashboard_orders_tree.insert(
                "", "end",
                values=(
                    order.order_id, order.customer.name,
                    f"${order.total_amount:.2f}", order.status.value
                )
            )

    # =========================================================
    # PRODUCTS PAGE
    # =========================================================

    def build_products_page(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")

        header_row = ttk.Frame(page, style="App.TFrame")
        header_row.pack(fill="x", pady=(0, 18))

        title_box = ttk.Frame(header_row, style="App.TFrame")
        title_box.pack(side="left", fill="x")
        ttk.Label(title_box, text="Products", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(
            title_box, text="Browse the catalog and add items to your cart.",
            style="PageSubtitle.TLabel"
        ).pack(anchor="w", pady=(3, 0))

        button_box = ttk.Frame(header_row, style="App.TFrame")
        button_box.pack(side="right", anchor="e")

        ttk.Button(
            button_box, text="+ Add New Product", style="Success.TButton",
            command=self.open_add_product_dialog
        ).pack(side="right")

        outer, inner = self.card(page)
        outer.pack(fill="both", expand=True)

        columns = ("id", "name", "type", "price", "details")
        self.product_tree = self.make_treeview(
            inner, columns,
            {
                "id": "ID", "name": "Product", "type": "Type",
                "price": "Price", "details": "Details"
            },
            {"id": 50, "name": 220, "type": 160, "price": 110, "details": 260},
            height=14
        )
        self.product_tree.pack(fill="both", expand=True)

        self.product_desc_label = ttk.Label(
            inner, text="Select a product to see its description.",
            style="Muted.TLabel", wraplength=900
        )
        self.product_desc_label.pack(fill="x", pady=(10, 0))
        self.product_tree.bind("<<TreeviewSelect>>", self.on_product_select)

        action_row = ttk.Frame(inner, style="Surface.TFrame")
        action_row.pack(fill="x", pady=(14, 0))

        ttk.Label(action_row, text="Quantity:", style="Body.TLabel").pack(side="left")

        self.quantity_var = tk.IntVar(value=1)
        ttk.Spinbox(
            action_row, from_=1, to=99, textvariable=self.quantity_var, width=6
        ).pack(side="left", padx=(8, 16))

        ttk.Button(
            action_row, text="Add to Cart", style="Primary.TButton",
            command=self.add_to_cart
        ).pack(side="left")

        return page

    def on_product_select(self, _event=None):
        selected = self.product_tree.selection()
        if not selected:
            return

        product_id = int(self.product_tree.item(selected[0], "values")[0])
        product = next((p for p in self.store.products if p.product_id == product_id), None)

        if product is None:
            return

        self.product_desc_label.configure(text=f"{product.name} \u2014 {product.description}")

    def _product_details_text(self, product):
        if isinstance(product, PhysicalProduct):
            return f"Stock: {product.stock}  \u2022  {product.weight}  \u2022  {product.dimensions}"
        if isinstance(product, DigitalProduct):
            return "Instant digital download"
        if isinstance(product, SubscriptionProduct):
            renew = "auto-renews" if product.auto_renew else "one-time"
            return f"{product.duration_months} month(s) \u2022 {renew}"
        return "\u2014"

    def refresh_products(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        for product in self.store.products:
            self.product_tree.insert(
                "", "end",
                values=(
                    product.product_id,
                    product.name,
                    product.__class__.__name__,
                    f"${product.calculate_price():.2f}",
                    self._product_details_text(product),
                )
            )

    def add_to_cart(self):
        selected = self.product_tree.selection()

        if not selected:
            messagebox.showwarning("Select Product", "Please select a product first.")
            return

        try:
            quantity = self.quantity_var.get()
        except (ValueError, tk.TclError):
            messagebox.showerror("Invalid Quantity", "Please enter a valid quantity.")
            return

        if quantity <= 0:
            messagebox.showerror("Invalid Quantity", "Quantity must be greater than zero.")
            return

        product_id = int(self.product_tree.item(selected[0], "values")[0])
        product = next((p for p in self.store.products if p.product_id == product_id), None)

        if product is None:
            return

        try:
            self.cart.add_item(product, quantity)
            self.refresh_cart()
            self.refresh_dashboard()
            messagebox.showinfo("Added to Cart", f"Added {quantity} x {product.name} to your cart.")
        except ValueError as error:
            messagebox.showerror("Cannot Add Product", str(error))

    # ---- Add New Product dialog -------------------------------------

    def open_add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.configure(bg=COLORS["surface"])
        dialog.geometry("440x560")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        wrapper = ttk.Frame(dialog, style="Surface.TFrame", padding=20)
        wrapper.pack(fill="both", expand=True)

        ttk.Label(wrapper, text="Add New Product", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 14))

        # --- product type selector ---
        type_var = tk.StringVar(value=PRODUCT_TYPES[0])
        type_row = ttk.Frame(wrapper, style="Surface.TFrame")
        type_row.pack(fill="x", pady=(0, 10))
        ttk.Label(type_row, text="Product Type", style="Body.TLabel").pack(anchor="w", pady=(0, 4))
        type_combo = ttk.Combobox(
            type_row, textvariable=type_var, values=PRODUCT_TYPES, state="readonly"
        )
        type_combo.pack(fill="x")

        # --- common fields ---
        name_var = tk.StringVar()
        desc_var = tk.StringVar()
        price_var = tk.StringVar()

        for label_text, var in (("Name", name_var), ("Description", desc_var), ("Base Price ($)", price_var)):
            row = self.labeled_field(wrapper, label_text)
            ttk.Entry(row, textvariable=var).pack(fill="x")

        ttk.Separator(wrapper).pack(fill="x", pady=(10, 10))

        # --- type-specific field containers ---
        extra_container = ttk.Frame(wrapper, style="Surface.TFrame")
        extra_container.pack(fill="x")
        extra_container.grid_rowconfigure(0, weight=1)
        extra_container.grid_columnconfigure(0, weight=1)

        # Physical
        physical_frame = ttk.Frame(extra_container, style="Surface.TFrame")
        stock_var = tk.StringVar()
        weight_var = tk.StringVar()
        dims_var = tk.StringVar()
        for label_text, var in (
            ("Stock Quantity", stock_var),
            ("Weight (e.g. 1.5 kg)", weight_var),
            ("Dimensions (e.g. 20 x 10 x 5 cm)", dims_var),
        ):
            row = self.labeled_field(physical_frame, label_text)
            ttk.Entry(row, textvariable=var).pack(fill="x")

        # Digital
        digital_frame = ttk.Frame(extra_container, style="Surface.TFrame")
        link_var = tk.StringVar()
        row = self.labeled_field(digital_frame, "Download Link")
        ttk.Entry(row, textvariable=link_var).pack(fill="x")

        # Subscription
        subscription_frame = ttk.Frame(extra_container, style="Surface.TFrame")
        duration_var = tk.StringVar()
        autorenew_var = tk.BooleanVar(value=True)
        row = self.labeled_field(subscription_frame, "Duration (months)")
        ttk.Entry(row, textvariable=duration_var).pack(fill="x")
        ttk.Checkbutton(
            subscription_frame, text="Auto-renew", variable=autorenew_var
        ).pack(anchor="w", pady=(6, 0))

        for frame in (physical_frame, digital_frame, subscription_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        def refresh_type_fields(*_args):
            mapping = {
                "Physical Product": physical_frame,
                "Digital Product": digital_frame,
                "Subscription Product": subscription_frame,
            }
            mapping[type_var.get()].tkraise()

        type_var.trace_add("write", refresh_type_fields)
        refresh_type_fields()

        error_label = ttk.Label(wrapper, text="", style="Muted.TLabel", foreground=COLORS["danger"])
        error_label.pack(fill="x", pady=(12, 0))

        def submit():
            name = name_var.get().strip()
            description = desc_var.get().strip()

            if not name:
                error_label.configure(text="Please enter a product name.")
                return

            try:
                base_price = float(price_var.get())
                if base_price < 0:
                    raise ValueError
            except ValueError:
                error_label.configure(text="Base price must be a valid non-negative number.")
                return

            existing_ids = [p.product_id for p in self.store.products]
            new_id = (max(existing_ids) + 1) if existing_ids else 1

            try:
                product_type = type_var.get()

                if product_type == "Physical Product":
                    stock = int(stock_var.get())
                    if stock < 0:
                        raise ValueError("Stock cannot be negative.")
                    weight = weight_var.get().strip() or "N/A"
                    dimensions = dims_var.get().strip() or "N/A"
                    product = PhysicalProduct(
                        new_id, name, description, base_price, stock, weight, dimensions
                    )

                elif product_type == "Digital Product":
                    link = link_var.get().strip()
                    if not link:
                        raise ValueError("Please provide a download link.")
                    product = DigitalProduct(new_id, name, description, base_price, link)

                else:
                    duration = int(duration_var.get())
                    if duration <= 0:
                        raise ValueError("Duration must be greater than zero.")
                    product = SubscriptionProduct(
                        new_id, name, description, base_price, duration, autorenew_var.get()
                    )

            except ValueError as error:
                message = str(error) if str(error) else "Please check the type-specific fields."
                error_label.configure(text=message)
                return

            self.store.add_product(product)
            self.refresh_products()
            self.refresh_dashboard()
            dialog.destroy()
            messagebox.showinfo("Product Added", f"{product.name} was added to the catalog.")

        button_row = ttk.Frame(wrapper, style="Surface.TFrame")
        button_row.pack(fill="x", pady=(16, 0))

        ttk.Button(
            button_row, text="Cancel", style="Secondary.TButton", command=dialog.destroy
        ).pack(side="right", padx=(8, 0))
        ttk.Button(
            button_row, text="Add Product", style="Success.TButton", command=submit
        ).pack(side="right")

    # =========================================================
    # CART PAGE
    # =========================================================

    def build_cart_page(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")

        self.page_header(page, "Cart", "Review the items you're about to order.")

        outer, inner = self.card(page)
        outer.pack(fill="both", expand=True)

        columns = ("product", "type", "unit_price", "quantity", "subtotal")
        self.cart_tree = self.make_treeview(
            inner, columns,
            {
                "product": "Product", "type": "Type", "unit_price": "Unit Price",
                "quantity": "Quantity", "subtotal": "Subtotal"
            },
            {"product": 240, "type": 150, "unit_price": 110, "quantity": 100, "subtotal": 120},
            height=12
        )
        self.cart_tree.pack(fill="both", expand=True)

        button_row = ttk.Frame(inner, style="Surface.TFrame")
        button_row.pack(fill="x", pady=(14, 0))

        ttk.Button(
            button_row, text="Remove Selected", style="Secondary.TButton",
            command=self.remove_selected_cart_item
        ).pack(side="left")

        ttk.Button(
            button_row, text="Clear Cart", style="Danger.TButton",
            command=self.clear_cart
        ).pack(side="left", padx=(8, 0))

        summary_row = ttk.Frame(inner, style="Surface.TFrame")
        summary_row.pack(fill="x", pady=(18, 0))

        ttk.Label(summary_row, text="Cart Subtotal", style="TotalLabel.TLabel").pack(side="left")
        self.cart_subtotal_label = ttk.Label(summary_row, text="$0.00", style="TotalValue.TLabel")
        self.cart_subtotal_label.pack(side="right")

        ttk.Button(
            inner, text="Proceed to Checkout \u2192", style="Success.TButton",
            command=self.go_to_checkout
        ).pack(fill="x", pady=(16, 0))

        return page

    def refresh_cart(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)

        for item in self.cart.items:
            self.cart_tree.insert(
                "", "end", iid=str(item.product.product_id),
                values=(
                    item.product.name,
                    item.product.__class__.__name__,
                    f"${item.product.calculate_price():.2f}",
                    item.quantity,
                    f"${item.calculate_subtotal():.2f}",
                )
            )

        self.cart_subtotal_label.configure(text=f"${self.cart.calculate_subtotal():.2f}")

    def remove_selected_cart_item(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select a cart item to remove.")
            return

        product_id = int(selected[0])
        self.cart.remove_item(product_id)
        self.refresh_cart()
        self.refresh_dashboard()

    def clear_cart(self):
        if self.cart.is_empty():
            return

        if messagebox.askyesno("Clear Cart", "Remove all items from your cart?"):
            self.cart.clear()
            self.refresh_cart()
            self.refresh_dashboard()

    def go_to_checkout(self):
        self.show_page("checkout")

    # =========================================================
    # CHECKOUT PAGE
    # =========================================================

    def build_checkout_page(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")

        self.page_header(page, "Checkout", "Confirm customer, delivery, and discount details.")

        body = ttk.Frame(page, style="App.TFrame")
        body.pack(fill="both", expand=True)

        # --- left column: details + items ---
        left_outer, left_inner = self.card(body)
        left_outer.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(left_inner, text="Customer & Delivery Details", style="CardTitle.TLabel").pack(
            anchor="w", pady=(0, 12)
        )

        self.customer_name_var = tk.StringVar(value="Guest Customer")
        self.customer_email_var = tk.StringVar(value="guest@example.com")
        self.customer_type_var = tk.StringVar(value=CUSTOMER_TYPES[0])
        self.delivery_var = tk.StringVar(value=DELIVERY_METHODS[0])
        self.discount_var = tk.StringVar(value=DISCOUNT_OPTIONS[0])

        name_row = self.labeled_field(left_inner, "Customer Name")
        ttk.Entry(name_row, textvariable=self.customer_name_var).pack(fill="x")

        email_row = self.labeled_field(left_inner, "Customer Email")
        ttk.Entry(email_row, textvariable=self.customer_email_var).pack(fill="x")

        type_row = self.labeled_field(left_inner, "Customer Type")
        ttk.Combobox(
            type_row, textvariable=self.customer_type_var, values=CUSTOMER_TYPES, state="readonly"
        ).pack(fill="x")

        delivery_row = self.labeled_field(left_inner, "Delivery Method")
        ttk.Combobox(
            delivery_row, textvariable=self.delivery_var, values=DELIVERY_METHODS, state="readonly"
        ).pack(fill="x")

        discount_row = self.labeled_field(left_inner, "Discount")
        ttk.Combobox(
            discount_row, textvariable=self.discount_var, values=DISCOUNT_OPTIONS, state="readonly"
        ).pack(fill="x")

        for var in (self.customer_type_var, self.delivery_var, self.discount_var):
            var.trace_add("write", lambda *_args: self.refresh_checkout_summary())

        ttk.Separator(left_inner).pack(fill="x", pady=14)

        ttk.Label(left_inner, text="Items in this Order", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        columns = ("product", "quantity", "subtotal")
        self.checkout_items_tree = self.make_treeview(
            left_inner, columns,
            {"product": "Product", "quantity": "Quantity", "subtotal": "Subtotal"},
            {"product": 260, "quantity": 100, "subtotal": 120},
            height=6
        )
        self.checkout_items_tree.pack(fill="both", expand=True)

        # --- right column: summary ---
        right_outer, right_inner = self.card(body)
        right_outer.pack(side="right", fill="both")
        right_outer.configure(width=320)

        ttk.Label(right_inner, text="Order Summary", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 14))

        self.checkout_summary_rows = {}
        summary_defs = [
            ("subtotal", "Subtotal"),
            ("customer_discount", "Customer Discount"),
            ("promo_discount", "Promo Discount"),
            ("shipping", "Shipping"),
            ("tax", "Tax"),
        ]

        for key, label in summary_defs:
            row = ttk.Frame(right_inner, style="Surface.TFrame")
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=label, style="SummaryLabel.TLabel").pack(side="left")
            value_label = ttk.Label(row, text="$0.00", style="SummaryValue.TLabel")
            value_label.pack(side="right")
            self.checkout_summary_rows[key] = value_label

        ttk.Separator(right_inner).pack(fill="x", pady=12)

        total_row = ttk.Frame(right_inner, style="Surface.TFrame")
        total_row.pack(fill="x")
        ttk.Label(total_row, text="Final Total", style="TotalLabel.TLabel").pack(side="left")
        self.checkout_total_label = ttk.Label(total_row, text="$0.00", style="TotalValue.TLabel")
        self.checkout_total_label.pack(side="right")

        ttk.Button(
            right_inner, text="Confirm Order \u2192", style="Success.TButton",
            command=self.confirm_order
        ).pack(fill="x", pady=(24, 0))

        ttk.Button(
            right_inner, text="\u2190 Back to Cart", style="Secondary.TButton",
            command=lambda: self.show_page("cart")
        ).pack(fill="x", pady=(8, 0))

        return page

    # ---- customer / delivery / discount / payment factories ----

    def create_customer(self):
        name = self.customer_name_var.get().strip() or "Guest Customer"
        email = self.customer_email_var.get().strip() or "guest@example.com"
        value = self.customer_type_var.get()

        if value == "Premium Customer":
            return PremiumCustomer(1, name, email)
        if value == "Business Customer":
            return BusinessCustomer(1, name, email)
        return RegularCustomer(1, name, email)

    def create_delivery(self):
        value = self.delivery_var.get()
        if value == "Express Delivery":
            return ExpressDelivery()
        if value == "Same Day Delivery":
            return SameDayDelivery()
        return StandardDelivery()

    def create_discount(self):
        value = self.discount_var.get()
        if value == "10% Off (Percentage)":
            return PercentageDiscount(10)
        if value == "$50 Off (Fixed Amount)":
            return FixedAmountDiscount(50)
        if value == "Buy One Get One (50% Off)":
            return BuyOneGetOneDiscount()
        if value == "Seasonal 15% Off":
            return SeasonalDiscount(15)
        return None

    def create_payment(self):
        value = self.payment_var.get()
        if value == "Bank Transfer":
            return BankTransfer()
        if value == "Digital Wallet":
            return DigitalWallet()
        return CreditCard()

    def build_scratch_order(self, customer, delivery, discount):
        """Builds a throwaway Order (never confirmed/paid) purely to reuse
        the real pricing logic from classes.py for live previews."""
        scratch_order = Order(0, customer, delivery, CreditCard())
        for item in self.cart.items:
            scratch_order.add_item(item.product, item.quantity)
        if discount is not None:
            scratch_order.set_discount(discount)
        return scratch_order

    def refresh_checkout_summary(self):
        for row in self.checkout_items_tree.get_children():
            self.checkout_items_tree.delete(row)

        for item in self.cart.items:
            self.checkout_items_tree.insert(
                "", "end",
                values=(item.product.name, item.quantity, f"${item.calculate_subtotal():.2f}")
            )

        if self.cart.is_empty():
            for key in self.checkout_summary_rows:
                self.checkout_summary_rows[key].configure(text="$0.00")
            self.checkout_total_label.configure(text="$0.00")
            return

        customer = self.create_customer()
        delivery = self.create_delivery()
        discount = self.create_discount()

        scratch_order = self.build_scratch_order(customer, delivery, discount)

        subtotal = scratch_order.calculate_subtotal()
        customer_discount_amt = customer.calculate_discount(subtotal)
        promo_discount_amt = discount.apply_discount(subtotal) if discount is not None else 0
        discounted_amount = max(0, subtotal - customer_discount_amt - promo_discount_amt)
        tax = scratch_order.calculate_tax(discounted_amount)
        shipping = scratch_order.calculate_shipping(subtotal)
        total = scratch_order.calculate_total()

        self.checkout_summary_rows["subtotal"].configure(text=f"${subtotal:.2f}")
        self.checkout_summary_rows["customer_discount"].configure(
            text=f"-${customer_discount_amt:.2f}" if customer_discount_amt else "$0.00"
        )
        self.checkout_summary_rows["promo_discount"].configure(
            text=f"-${promo_discount_amt:.2f}" if promo_discount_amt else "$0.00"
        )
        self.checkout_summary_rows["shipping"].configure(
            text="FREE" if shipping == 0 else f"${shipping:.2f}"
        )
        self.checkout_summary_rows["tax"].configure(text=f"${tax:.2f}")
        self.checkout_total_label.configure(text=f"${total:.2f}")

    def confirm_order(self):
        if self.cart.is_empty():
            messagebox.showwarning("Empty Cart", "Please add products to the cart first.")
            self.show_page("cart")
            return

        if not self.customer_name_var.get().strip():
            messagebox.showwarning("Missing Name", "Please enter the customer's name.")
            return

        # Snapshot the real domain objects so the Payment page uses exactly
        # what was confirmed here, even if the widgets change afterwards.
        self.checkout_context = {
            "customer": self.create_customer(),
            "delivery": self.create_delivery(),
            "discount": self.create_discount(),
        }

        self.payment_var.set("Credit Card")
        self.show_page("payment")

    # =========================================================
    # PAYMENT PAGE
    # =========================================================

    def build_payment_page(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")

        self.page_header(page, "Payment", "Choose a payment method to complete your order.")

        body = ttk.Frame(page, style="App.TFrame")
        body.pack(fill="both", expand=True)

        left_outer, left_inner = self.card(body)
        left_outer.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(left_inner, text="Select Payment Method", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 14))

        self.payment_var = tk.StringVar(value="Credit Card")

        payment_options = [
            ("Credit Card", "\U0001F4B3", "Pay securely with your credit or debit card."),
            ("Bank Transfer", "\U0001F3E6", "Transfer funds directly from your bank account."),
            ("Digital Wallet", "\U0001F4F1", "Use your linked digital wallet balance."),
        ]

        for value, icon, description in payment_options:
            option_outer, option_inner = self.card(left_inner, padding=14)
            option_outer.pack(fill="x", pady=6)

            row = ttk.Frame(option_inner, style="Surface.TFrame")
            row.pack(fill="x")

            ttk.Radiobutton(
                row, text=f"{icon}  {value}", variable=self.payment_var, value=value
            ).pack(side="left")

            ttk.Label(option_inner, text=description, style="Muted.TLabel").pack(
                anchor="w", pady=(4, 0), padx=(22, 0)
            )

        right_outer, right_inner = self.card(body)
        right_outer.pack(side="right", fill="both")
        right_outer.configure(width=320)

        ttk.Label(right_inner, text="Amount Due", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        self.payment_order_label = ttk.Label(right_inner, text="Pending Order #\u2014", style="Body.TLabel")
        self.payment_order_label.pack(anchor="w")

        self.payment_total_label = ttk.Label(right_inner, text="$0.00", style="TotalValue.TLabel")
        self.payment_total_label.pack(anchor="w", pady=(6, 0))

        ttk.Button(
            right_inner, text="Pay Now", style="Success.TButton",
            command=self.pay_now
        ).pack(fill="x", pady=(24, 0))

        ttk.Button(
            right_inner, text="\u2190 Back to Checkout", style="Secondary.TButton",
            command=lambda: self.show_page("checkout")
        ).pack(fill="x", pady=(8, 0))

        return page

    def refresh_payment_summary(self):
        self.payment_order_label.configure(text=f"Pending Order #{self.order_counter}")

        if self.cart.is_empty() or self.checkout_context is None:
            self.payment_total_label.configure(text="$0.00")
            return

        scratch_order = self.build_scratch_order(
            self.checkout_context["customer"],
            self.checkout_context["delivery"],
            self.checkout_context["discount"],
        )
        total = scratch_order.calculate_total()
        self.payment_total_label.configure(text=f"${total:.2f}")

    def pay_now(self):
        if self.cart.is_empty():
            messagebox.showwarning("Empty Cart", "Please add products to the cart first.")
            self.show_page("cart")
            return

        if self.checkout_context is None:
            messagebox.showwarning("Checkout Required", "Please complete checkout first.")
            self.show_page("checkout")
            return

        try:
            customer = self.checkout_context["customer"]
            delivery = self.checkout_context["delivery"]
            discount = self.checkout_context["discount"]
            payment = self.create_payment()

            order = Order(self.order_counter, customer, delivery, payment)

            for item in self.cart.items:
                order.add_item(item.product, item.quantity)

            if discount is not None:
                order.set_discount(discount)

            order.confirm()
            message = order.pay()
            customer.add_order(order)

            self.orders.append(order)
            self.order_counter += 1

            self.cart.clear()
            self.checkout_context = None

            self.refresh_cart()
            self.refresh_orders_table()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Payment Successful",
                f"{message}\n\nOrder #{order.order_id} confirmed \u2014 Total: ${order.total_amount:.2f}"
            )

            self.show_page("orders")

        except ValueError as error:
            messagebox.showerror("Payment Error", str(error))

    # =========================================================
    # ORDERS PAGE
    # =========================================================

    def build_orders_page(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")

        self.page_header(page, "Orders", "Track and manage every order placed in the store.")

        outer, inner = self.card(page)
        outer.pack(fill="both", expand=True)

        columns = ("id", "customer", "items", "total", "status")
        self.orders_tree = self.make_treeview(
            inner, columns,
            {
                "id": "Order ID", "customer": "Customer", "items": "Items",
                "total": "Total", "status": "Status"
            },
            {"id": 90, "customer": 200, "items": 80, "total": 110, "status": 150},
            height=13
        )
        self.orders_tree.pack(fill="both", expand=True)
        self.orders_tree.bind("<<TreeviewSelect>>", self.on_order_select)

        for status, color in STATUS_BADGE_COLORS.items():
            self.orders_tree.tag_configure(status, foreground=color)

        action_row = ttk.Frame(inner, style="Surface.TFrame")
        action_row.pack(fill="x", pady=(16, 0))

        self.order_action_buttons = {}

        actions = [
            ("process", "Process", "Primary.TButton", self.process_selected_order),
            ("ship", "Ship", "Primary.TButton", self.ship_selected_order),
            ("deliver", "Deliver", "Success.TButton", self.deliver_selected_order),
            ("cancel", "Cancel", "Danger.TButton", self.cancel_selected_order),
            ("refund", "Refund", "Warning.TButton", self.refund_selected_order),
        ]

        for key, label, style_name, command in actions:
            btn = ttk.Button(action_row, text=label, style=style_name, command=command, state="disabled")
            btn.pack(side="left", padx=(0, 8))
            self.order_action_buttons[key] = btn

        self.order_detail_label = ttk.Label(
            inner, text="Select an order to see available actions.", style="Muted.TLabel"
        )
        self.order_detail_label.pack(anchor="w", pady=(10, 0))

        return page

    def refresh_orders_table(self):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)

        for order in self.orders:
            item_count = sum(item.quantity for item in order.items)

            self.orders_tree.insert(
                "", "end",
                values=(
                    order.order_id, order.customer.name, item_count,
                    f"${order.total_amount:.2f}", order.status.value
                ),
                tags=(order.status.value,)
            )

        self.update_order_action_states()

    def get_selected_order(self):
        selected = self.orders_tree.selection()

        if not selected:
            messagebox.showwarning("Select Order", "Please select an order from the list.")
            return None

        order_id = int(self.orders_tree.item(selected[0], "values")[0])
        return next((o for o in self.orders if o.order_id == order_id), None)

    def on_order_select(self, _event=None):
        self.update_order_action_states()

    def update_order_action_states(self):
        selected = self.orders_tree.selection()

        if not selected:
            for btn in self.order_action_buttons.values():
                btn.configure(state="disabled")
            self.order_detail_label.configure(text="Select an order to see available actions.")
            return

        order_id = int(self.orders_tree.item(selected[0], "values")[0])
        order = next((o for o in self.orders if o.order_id == order_id), None)
        if order is None:
            return

        status = order.status.value

        allowed = {
            "process": status == "PAID",
            "ship": status == "PROCESSING",
            "deliver": status == "SHIPPED",
            "cancel": status not in ("DELIVERED", "REFUNDED", "SHIPPED", "CANCELLED"),
            "refund": status == "PAID",
        }

        for key, btn in self.order_action_buttons.items():
            btn.configure(state="normal" if allowed[key] else "disabled")

        self.order_detail_label.configure(
            text=f"Order #{order.order_id} \u2014 {order.customer.name} \u2014 "
                 f"Current status: {status}"
        )

    def _run_order_action(self, action_name, success_message=None, refresh_products=False):
        order = self.get_selected_order()
        if order is None:
            return

        try:
            result = getattr(order, action_name)()
            self.refresh_orders_table()
            self.refresh_dashboard()

            if refresh_products:
                self.refresh_products()

            if success_message:
                messagebox.showinfo(success_message[0], success_message[1])
            elif isinstance(result, str):
                messagebox.showinfo("Success", result)

        except ValueError as error:
            messagebox.showerror("Action Failed", str(error))

    def process_selected_order(self):
        self._run_order_action("process", ("Order Processing", "Order is now being processed."))

    def ship_selected_order(self):
        self._run_order_action(
            "ship", ("Shipping", "Order has been shipped successfully."), refresh_products=True
        )

    def deliver_selected_order(self):
        self._run_order_action("deliver", ("Delivery", "Order has been delivered successfully."))

    def cancel_selected_order(self):
        self._run_order_action("cancel", ("Order Cancelled", "The order has been cancelled."))

    def refund_selected_order(self):
        self._run_order_action("refund")


def run_app():
    root = tk.Tk()
    EcommerceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
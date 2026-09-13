# ============================================================
# PAKBIZ AI
# Agentic Sales & Inventory Assistant
# GitHub / Local / Hugging Face compatible version
# ============================================================

import os
import json
import re
from pathlib import Path

import pandas as pd
import gradio as gr
from groq import Groq


# ============================================================
# API KEY
# ============================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY was not found. "
        "Please configure it as an environment variable or "
        "deployment secret."
    )

client = Groq(api_key=GROQ_API_KEY)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# DATA DIRECTORIES
# ============================================================

# GitHub/local/deployment compatible.
# The application looks for the data folder next to app.py.

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTS_FILE = DATA_DIR / "products.json"
ORDERS_FILE = DATA_DIR / "orders.json"
ANALYTICS_FILE = DATA_DIR / "analytics.json"


# ============================================================
# DEFAULT PRODUCTS
# ============================================================

DEFAULT_PRODUCTS = [
    {
        "id": "P001",
        "name": "Blue Shirt",
        "category": "Clothing/Shirts",
        "price": 2000,
        "stock": 10
    },
    {
        "id": "P002",
        "name": "Black Shirt",
        "category": "Clothing/Shirts",
        "price": 2200,
        "stock": 8
    },
    {
        "id": "P003",
        "name": "White Shirt",
        "category": "Clothing/Shirts",
        "price": 1800,
        "stock": 12
    },
    {
        "id": "P004",
        "name": "Black Pant",
        "category": "Clothing/Pants",
        "price": 2500,
        "stock": 3
    },
    {
        "id": "P005",
        "name": "Blue Jeans",
        "category": "Jeans",
        "price": 3500,
        "stock": 6
    },
    {
        "id": "P006",
        "name": "Kurta",
        "category": "Traditional",
        "price": 2800,
        "stock": 7
    },
    {
        "id": "P007",
        "name": "Black T-Shirt",
        "category": "T-Shirts",
        "price": 1500,
        "stock": 15
    },
    {
        "id": "P008",
        "name": "Red T-Shirt",
        "category": "T-Shirts",
        "price": 1500,
        "stock": 9
    }
]


# ============================================================
# INITIALIZE DATA
# ============================================================

def initialize_file(path, default_data):
    if not path.exists():
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2)


initialize_file(PRODUCTS_FILE, DEFAULT_PRODUCTS)
initialize_file(ORDERS_FILE, [])
initialize_file(ANALYTICS_FILE, [])


# ============================================================
# JSON HELPERS
# ============================================================

def load_json(path, default=None):
    if default is None:
        default = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# PRODUCT TOOLS
# ============================================================

def search_products(query=""):
    products = load_json(PRODUCTS_FILE, [])

    query = str(query).strip().lower()

    if not query:
        return products

    results = []

    for product in products:

        searchable = (
            f"{product.get('name', '')} "
            f"{product.get('category', '')}"
        ).lower()

        if query in searchable:
            results.append(product)

    return results


def get_product_price(product_id):
    products = load_json(PRODUCTS_FILE, [])

    for product in products:

        if product.get("id") == product_id:

            return {
                "success": True,
                "product_id": product_id,
                "product_name": product.get("name"),
                "price": product.get("price")
            }

    return {
        "success": False,
        "error": f"Product {product_id} not found."
    }


def check_stock(product_id, quantity=1):
    products = load_json(PRODUCTS_FILE, [])

    for product in products:

        if product.get("id") == product_id:

            stock = int(product.get("stock", 0))
            quantity = int(quantity)

            return {
                "success": True,
                "product_id": product_id,
                "product_name": product.get("name"),
                "requested_quantity": quantity,
                "available_stock": stock,
                "in_stock": stock >= quantity
            }

    return {
        "success": False,
        "error": f"Product {product_id} not found."
    }


# ============================================================
# CALCULATION TOOL
# ============================================================

def calculate_total(items):
    products = load_json(PRODUCTS_FILE, [])

    result_items = []
    total = 0.0

    for requested in items:

        product_id = requested.get("product_id")
        quantity = int(requested.get("quantity", 1))

        product = None

        for p in products:

            if p.get("id") == product_id:
                product = p
                break

        if product is None:

            return {
                "success": False,
                "error": f"Product {product_id} not found."
            }

        unit_price = float(product.get("price", 0))
        subtotal = unit_price * quantity

        result_items.append({
            "product_id": product_id,
            "product_name": product.get("name"),
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": subtotal
        })

        total += subtotal

    return {
        "success": True,
        "items": result_items,
        "total": total
    }


# ============================================================
# ORDER PREPARATION
# ============================================================

def prepare_order(items):
    products = load_json(PRODUCTS_FILE, [])

    prepared_items = []
    total = 0.0

    for requested in items:

        product_id = requested.get("product_id")
        quantity = int(requested.get("quantity", 1))

        if quantity <= 0:
            return {
                "success": False,
                "error": "Quantity must be greater than zero."
            }

        product = None

        for p in products:

            if p.get("id") == product_id:
                product = p
                break

        if product is None:

            return {
                "success": False,
                "error": f"Product {product_id} not found."
            }

        stock = int(product.get("stock", 0))

        if stock < quantity:

            return {
                "success": False,
                "error": (
                    f"Only {stock} units of "
                    f"{product.get('name')} are available."
                )
            }

        price = float(product.get("price", 0))
        subtotal = price * quantity

        prepared_items.append({
            "product_id": product_id,
            "product_name": product.get("name"),
            "quantity": quantity,
            "unit_price": price,
            "subtotal": subtotal
        })

        total += subtotal

    return {
        "success": True,
        "items": prepared_items,
        "total": total
    }


# ============================================================
# SMART ORDER PREPARATION
# ============================================================

def prepare_smart_order(
    requested_items,
    fallback_items=None,
    max_total=None
):

    fallback_items = fallback_items or []

    trace = []

    # --------------------------------------------------------
    # Try requested products
    # --------------------------------------------------------

    result = prepare_order(requested_items)

    if result.get("success"):

        if (
            max_total is None
            or result["total"] <= float(max_total)
        ):

            trace.append(
                "Requested product(s) available and within budget."
            )

            result["decision_trace"] = trace

            return result

        trace.append(
            "Requested product(s) exceed the customer's budget."
        )

    else:

        trace.append(
            "Requested product(s) could not be fulfilled."
        )

    # --------------------------------------------------------
    # Try fallback products
    # --------------------------------------------------------

    if fallback_items:

        fallback_result = prepare_order(fallback_items)

        if fallback_result.get("success"):

            if (
                max_total is None
                or fallback_result["total"] <= float(max_total)
            ):

                trace.append(
                    "Fallback product selected successfully."
                )

                fallback_result["decision_trace"] = trace

                return fallback_result

    # --------------------------------------------------------
    # Budget fallback
    # --------------------------------------------------------

    if (
        max_total is not None
        and len(requested_items) == 1
    ):

        quantity = int(
            requested_items[0].get("quantity", 1)
        )

        products = load_json(PRODUCTS_FILE, [])

        affordable = []

        for product in products:

            stock = int(product.get("stock", 0))
            price = float(product.get("price", 0))

            if stock >= quantity:

                total = price * quantity

                if total <= float(max_total):
                    affordable.append(product)

        if affordable:

            affordable.sort(
                key=lambda x: float(
                    x.get("price", 0)
                )
            )

            selected = affordable[0]

            trace.append(
                f"Selected affordable alternative: "
                f"{selected.get('name')}."
            )

            new_items = [
                {
                    "product_id": selected.get("id"),
                    "quantity": quantity
                }
            ]

            result = prepare_order(new_items)

            if result.get("success"):

                result["decision_trace"] = trace

                return result

    return {
        "success": False,
        "error": (
            "I could not prepare an order that satisfies "
            "the requested products, stock and budget."
        ),
        "decision_trace": trace
    }


# ============================================================
# INVENTORY UPDATE
# ============================================================

def update_inventory(items):

    products = load_json(PRODUCTS_FILE, [])

    for item in items:

        product_id = item.get("product_id")
        quantity = int(item.get("quantity", 0))

        for product in products:

            if product.get("id") == product_id:

                product["stock"] = (
                    int(product.get("stock", 0))
                    - quantity
                )

                break

    save_json(PRODUCTS_FILE, products)

    return {
        "success": True,
        "message": "Inventory updated successfully."
    }


# ============================================================
# CREATE ORDER
# ============================================================

def create_order(items):

    prepared = prepare_order(items)

    if not prepared.get("success"):
        return prepared

    orders = load_json(ORDERS_FILE, [])

    order_number = len(orders) + 1001

    order_id = f"ORD-{order_number}"

    order = {
        "order_id": order_id,
        "status": "Confirmed",
        "items": prepared["items"],
        "total": prepared["total"]
    }

    orders.append(order)

    save_json(
        ORDERS_FILE,
        orders
    )

    update_inventory(
        prepared["items"]
    )

    analytics = load_json(
        ANALYTICS_FILE,
        []
    )

    analytics.append({
        "order_id": order_id,
        "total": prepared["total"]
    })

    save_json(
        ANALYTICS_FILE,
        analytics
    )

    return {
        "success": True,
        "order_id": order_id,
        "status": "Confirmed",
        "items": prepared["items"],
        "total": prepared["total"]
    }


# ============================================================
# GET ORDER
# ============================================================

def get_order(order_id):

    orders = load_json(
        ORDERS_FILE,
        []
    )

    for order in orders:

        if (
            str(order.get("order_id", "")).lower()
            == str(order_id).lower()
        ):

            return {
                "success": True,
                "order": order
            }

    return {
        "success": False,
        "error": f"Order {order_id} was not found."
    }


# ============================================================
# SALES SUMMARY
# ============================================================

def get_sales_summary():

    orders = load_json(
        ORDERS_FILE,
        []
    )

    total_orders = len(orders)

    total_sales = 0.0

    for order in orders:

        try:
            total_sales += float(
                order.get("total", 0)
            )

        except Exception:
            pass

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    return {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "average_order_value": average_order_value
    }


# ============================================================
# DATAFRAME HELPERS
# ============================================================

def products_df():

    products = load_json(
        PRODUCTS_FILE,
        []
    )

    if not products:

        return pd.DataFrame(
            columns=[
                "ID",
                "Product",
                "Category",
                "Price",
                "Stock"
            ]
        )

    rows = []

    for p in products:

        rows.append({
            "ID": p.get("id"),
            "Product": p.get("name"),
            "Category": p.get("category"),
            "Price": (
                f"PKR "
                f"{float(p.get('price', 0)):,.0f}"
            ),
            "Stock": p.get("stock", 0)
        })

    return pd.DataFrame(rows)


def orders_df():

    orders = load_json(
        ORDERS_FILE,
        []
    )

    if not orders:

        return pd.DataFrame(
            columns=[
                "Order ID",
                "Status",
                "Items",
                "Total"
            ]
        )

    rows = []

    for order in orders:

        item_text = []

        for item in order.get(
            "items",
            []
        ):

            item_text.append(
                f"{item.get('quantity', 0)} × "
                f"{item.get('product_name', '')}"
            )

        rows.append({
            "Order ID": order.get(
                "order_id"
            ),
            "Status": order.get(
                "status"
            ),
            "Items": ", ".join(
                item_text
            ),
            "Total": (
                f"PKR "
                f"{float(order.get('total', 0)):,.0f}"
            )
        })

    return pd.DataFrame(rows)


# ============================================================
# GLOBAL AGENT STATE
# ============================================================

pending_order = None
last_agent_trace = []


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are PakBiz AI, an agentic sales and inventory assistant
for Pakistani small businesses.

You communicate naturally in English, Roman Urdu and Urdu.

IMPORTANT ARCHITECTURE:

The LLM is the language and decision layer.

Python business tools and stored business data are the
source of truth.

NEVER invent:

- product prices
- stock levels
- order IDs
- order totals
- product availability
- sales numbers

Use tools whenever business information is required.

For a purchase request:

1. Understand the customer's intent.
2. Identify the product and quantity.
3. Search the catalog if necessary.
4. Check stock.
5. Get the price.
6. Calculate the total.
7. Prepare the order.
8. Ask for confirmation.
9. NEVER create an order before confirmation.

An order is created only after the customer explicitly
confirms.

Natural confirmations include:

yes
haan
han
confirm
confirmed
1
ok
okay

Natural cancellations include:

no
nahi
cancel
2

If the user asks what products are available, use the
product search/catalog tools.

If the user asks about an existing order, use get_order.

Do not claim that an action was executed unless the
corresponding business tool actually executed it.
"""


# ============================================================
# GROQ TOOL DEFINITIONS
# ============================================================

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search available products.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": (
                "Get the verified price of a product."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string"
                    }
                },
                "required": ["product_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Check verified inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string"
                    },
                    "quantity": {
                        "type": "integer"
                    }
                },
                "required": [
                    "product_id",
                    "quantity"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_total",
            "description": "Calculate an order total.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {
                                    "type": "string"
                                },
                                "quantity": {
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "product_id",
                                "quantity"
                            ]
                        }
                    }
                },
                "required": ["items"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "prepare_order",
            "description": (
                "Prepare an order after checking stock."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {
                                    "type": "string"
                                },
                                "quantity": {
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "product_id",
                                "quantity"
                            ]
                        }
                    }
                },
                "required": ["items"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "prepare_smart_order",
            "description": (
                "Prepare an order using requested products, "
                "fallback products and budget constraints."
            ),
            "parameters": {
                "type": "object",
                "properties": {

                    "requested_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {
                                    "type": "string"
                                },
                                "quantity": {
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "product_id",
                                "quantity"
                            ]
                        }
                    },

                    "fallback_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {
                                    "type": "string"
                                },
                                "quantity": {
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "product_id",
                                "quantity"
                            ]
                        }
                    },

                    "max_total": {
                        "type": "number"
                    }
                },
                "required": [
                    "requested_items"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get an existing order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string"
                    }
                },
                "required": ["order_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_sales_summary",
            "description": (
                "Get confirmed sales statistics."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


# ============================================================
# TOOL ROUTER
# ============================================================

def execute_tool(name, arguments):

    if name == "search_products":

        return search_products(
            arguments.get("query", "")
        )

    if name == "get_product_price":

        return get_product_price(
            arguments.get("product_id")
        )

    if name == "check_stock":

        return check_stock(
            arguments.get("product_id"),
            arguments.get(
                "quantity",
                1
            )
        )

    if name == "calculate_total":

        return calculate_total(
            arguments.get(
                "items",
                []
            )
        )

    if name == "prepare_order":

        return prepare_order(
            arguments.get(
                "items",
                []
            )
        )

    if name == "prepare_smart_order":

        return prepare_smart_order(
            arguments.get(
                "requested_items",
                []
            ),
            arguments.get(
                "fallback_items",
                []
            ),
            arguments.get(
                "max_total"
            )
        )

    if name == "get_order":

        return get_order(
            arguments.get(
                "order_id"
            )
        )

    if name == "get_sales_summary":

        return get_sales_summary()

    return {
        "success": False,
        "error": f"Unknown tool: {name}"
    }


# ============================================================
# AGENT LOOP
# ============================================================

def run_agent(user_message):

    global last_agent_trace

    last_agent_trace = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    for iteration in range(8):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.1
        )

        assistant_message = (
            response.choices[0].message
        )

        # ----------------------------------------------------
        # No tool call -> final answer
        # ----------------------------------------------------

        if not assistant_message.tool_calls:

            final_text = (
                assistant_message.content
                or ""
            )

            last_agent_trace.append({
                "action": "Final Response",
                "result": final_text
            })

            return final_text

        # ----------------------------------------------------
        # Add assistant tool-call message
        # ----------------------------------------------------

        messages.append(
            assistant_message
        )

        # ----------------------------------------------------
        # Execute tools
        # ----------------------------------------------------

        for tool_call in (
            assistant_message.tool_calls
        ):

            name = (
                tool_call.function.name
            )

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

            except Exception:

                arguments = {}

            last_agent_trace.append({
                "action": name,
                "result": (
                    f"Arguments: {arguments}"
                )
            })

            result = execute_tool(
                name,
                arguments
            )

            last_agent_trace.append({
                "action": (
                    f"{name} result"
                ),
                "result": result
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    result,
                    ensure_ascii=False
                )
            })

    return (
        "I could not complete the request within the "
        "agent's tool execution limit."
    )


# ============================================================
# ORDER EXTRACTION
# ============================================================

def extract_order(user_message):

    products = load_json(
        PRODUCTS_FILE,
        []
    )

    product_text = "\n".join(
        [
            f"{p['id']} | {p['name']} | "
            f"PKR {p['price']} | stock {p['stock']}"
            for p in products
        ]
    )

    prompt = f"""
Extract a purchase order from this customer message.

Customer message:
{user_message}

Available products:
{product_text}

Return ONLY valid JSON.

Format:

{{
  "is_order": true,
  "items": [
    {{
      "product_id": "P001",
      "quantity": 2
    }}
  ],
  "max_total": null
}}

If this is not a purchase request:

{{
  "is_order": false,
  "items": [],
  "max_total": null
}}

Only use product IDs from the provided catalog.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        text = (
            response.choices[0].message.content
            or ""
        )

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if not match:

            return {
                "is_order": False,
                "items": [],
                "max_total": None
            }

        data = json.loads(
            match.group()
        )

        return data

    except Exception:

        return {
            "is_order": False,
            "items": [],
            "max_total": None
        }


# ============================================================
# ORDER FORMATTER
# ============================================================

def format_order(data):

    lines = []

    for item in data.get(
        "items",
        []
    ):

        lines.append(
            f"• {item.get('quantity', 0)} × "
            f"{item.get('product_name', '')} — "
            f"{float(item.get('unit_price', 0)):,.0f} PKR"
        )

    total = float(
        data.get(
            "total",
            0
        )
    )

    return (
        "I checked the available products, "
        "prices and stock.\n\n"
        + "\n".join(lines)
        + f"\n\n💰 **Total: {total:,.0f} PKR**"
    )


# ============================================================
# CUSTOMER MESSAGE PROCESSOR
# ============================================================

def process_message(user_message):

    global pending_order
    global last_agent_trace

    text = str(
        user_message
    ).strip()

    # --------------------------------------------------------
    # Handle pending confirmation
    # --------------------------------------------------------

    if pending_order is not None:

        normalized = (
            text.lower().strip()
        )

        confirmations = {
            "1",
            "yes",
            "yeah",
            "y",
            "haan",
            "han",
            "confirm",
            "confirmed",
            "ok",
            "okay"
        }

        cancellations = {
            "2",
            "no",
            "n",
            "nahi",
            "nahin",
            "cancel",
            "cancelled"
        }

        if normalized in confirmations:

            result = create_order(
                pending_order["items"]
            )

            pending_order = None

            if result.get("success"):

                return (
                    "✅ **Order Confirmed!**\n\n"
                    f"🧾 Order ID: "
                    f"**{result['order_id']}**\n\n"
                    f"💰 Total: "
                    f"**{float(result['total']):,.0f} PKR**\n\n"
                    "📦 Inventory has been updated."
                )

            return (
                "⚠️ I could not create the order.\n\n"
                + str(
                    result.get(
                        "error",
                        "Unknown error"
                    )
                )
            )

        if normalized in cancellations:

            pending_order = None

            return (
                "❌ Order cancelled.\n\n"
                "No inventory was changed."
            )

    # --------------------------------------------------------
    # Run agent
    # --------------------------------------------------------

    agent_response = run_agent(
        text
    )

    # --------------------------------------------------------
    # Extract possible order
    # --------------------------------------------------------

    extracted = extract_order(
        text
    )

    if extracted.get(
        "is_order"
    ):

        requested_items = extracted.get(
            "items",
            []
        )

        max_total = extracted.get(
            "max_total"
        )

        if requested_items:

            prepared = prepare_smart_order(
                requested_items=requested_items,
                max_total=max_total
            )

            if prepared.get(
                "success"
            ):

                pending_order = prepared

                order_text = format_order(
                    prepared
                )

                return (
                    order_text
                    + "\n\n"
                    + "Would you like to confirm "
                    "this order?\n\n"
                    + "1️⃣ **Confirm Order**\n"
                    + "2️⃣ **Cancel Order**\n\n"
                    + "You can also reply naturally, "
                    "e.g. **haan/nahi**."
                )

    return agent_response


# ============================================================
# DATA FUNCTIONS FOR UI
# ============================================================

def get_products_table():

    try:
        return products_df()

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })


def get_orders_table():

    try:
        return orders_df()

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })


def get_analytics_table():

    try:

        orders = load_json(
            ORDERS_FILE,
            []
        )

        if not isinstance(
            orders,
            list
        ):
            orders = []

        total_orders = len(
            orders
        )

        total_sales = 0.0

        for order in orders:

            if not isinstance(
                order,
                dict
            ):
                continue

            order_total = order.get(
                "total"
            )

            if order_total is None:
                order_total = order.get(
                    "total_amount"
                )

            if order_total is None:
                order_total = order.get(
                    "grand_total"
                )

            if order_total is None:
                order_total = order.get(
                    "amount"
                )

            if order_total is None:

                items = order.get(
                    "items",
                    []
                )

                calculated_total = 0.0

                if isinstance(
                    items,
                    list
                ):

                    for item in items:

                        if not isinstance(
                            item,
                            dict
                        ):
                            continue

                        quantity = item.get(
                            "quantity",
                            0
                        )

                        unit_price = item.get(
                            "unit_price"
                        )

                        if unit_price is None:
                            unit_price = item.get(
                                "price",
                                0
                            )

                        try:

                            calculated_total += (
                                float(quantity)
                                * float(unit_price)
                            )

                        except Exception:
                            pass

                order_total = (
                    calculated_total
                )

            try:

                total_sales += float(
                    order_total
                )

            except Exception:
                pass

        average_order_value = (
            total_sales / total_orders
            if total_orders > 0
            else 0
        )

        return pd.DataFrame({
            "Metric": [
                "Total Orders",
                "Total Sales",
                "Average Order Value"
            ],
            "Value": [
                total_orders,
                f"PKR {total_sales:,.0f}",
                f"PKR {average_order_value:,.0f}"
            ]
        })

    except Exception as e:

        return pd.DataFrame({
            "Metric": [
                "Total Orders",
                "Total Sales",
                "Average Order Value"
            ],
            "Value": [
                "Error",
                str(e),
                "Error"
            ]
        })


def get_agent_activity_table():

    try:

        if not last_agent_trace:

            return pd.DataFrame({
                "Step": ["—"],
                "Action": [
                    "Waiting for customer"
                ],
                "Result": [
                    "Send a message to activate "
                    "the AI agent."
                ]
            })

        rows = []

        for i, item in enumerate(
            last_agent_trace,
            start=1
        ):

            if isinstance(
                item,
                dict
            ):

                action = (
                    item.get("action")
                    or item.get("tool")
                    or item.get("name")
                    or "Agent"
                )

                result = (
                    item.get("result")
                    or item.get("output")
                    or item.get("message")
                    or ""
                )

            else:

                action = "Agent"
                result = str(item)

            rows.append({
                "Step": i,
                "Action": str(action),
                "Result": str(result)[:1000]
            })

        return pd.DataFrame(
            rows
        )

    except Exception as e:

        return pd.DataFrame({
            "Step": [1],
            "Action": ["Error"],
            "Result": [str(e)]
        })


# ============================================================
# KPI FUNCTIONS
# ============================================================

def get_kpis():

    try:

        products = load_json(
            PRODUCTS_FILE,
            []
        )

        orders = load_json(
            ORDERS_FILE,
            []
        )

        total_orders = len(
            orders
        )

        total_sales = 0.0

        for order in orders:

            try:

                total_sales += float(
                    order.get(
                        "total",
                        0
                    )
                )

            except Exception:
                pass

        total_stock = sum(
            int(
                p.get(
                    "stock",
                    0
                )
            )
            for p in products
        )

        low_stock = sum(
            1
            for p in products
            if int(
                p.get(
                    "stock",
                    0
                )
            ) <= 3
        )

        return (
            total_orders,
            total_sales,
            total_stock,
            low_stock
        )

    except Exception:

        return (
            0,
            0.0,
            0,
            0
        )


def render_kpi_html(
    total_orders,
    total_sales,
    total_stock,
    low_stock
):

    return f"""
    <div class="kpi-row">

        <div class="kpi-card">
            <div class="kpi-label">
                Confirmed Orders
            </div>

            <div class="kpi-value">
                {total_orders}
            </div>

            <div class="kpi-description">
                Successfully completed orders
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">
                Total Sales
            </div>

            <div class="kpi-value">
                PKR {total_sales:,.0f}
            </div>

            <div class="kpi-description">
                Revenue from confirmed orders
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">
                Inventory Units
            </div>

            <div class="kpi-value">
                {total_stock}
            </div>

            <div class="kpi-description">
                Current available stock
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">
                Low Stock
            </div>

            <div class="kpi-value">
                {low_stock}
            </div>

            <div class="kpi-description">
                Products needing attention
            </div>
        </div>

    </div>
    """


def get_kpi_html():

    return render_kpi_html(
        *get_kpis()
    )


# ============================================================
# SAFE TEXT
# ============================================================

def make_safe_text(value):

    if isinstance(
        value,
        str
    ):
        return value

    if isinstance(
        value,
        tuple
    ):

        if len(value) > 0:
            return make_safe_text(
                value[0]
            )

        return ""

    if isinstance(
        value,
        list
    ):

        if len(value) == 1:
            return make_safe_text(
                value[0]
            )

        return str(value)

    return str(value)


# ============================================================
# CHAT HANDLER
# ============================================================

def chat_handler(
    message,
    history
):

    if history is None:
        history = []

    history = list(
        history
    )

    message = (
        ""
        if message is None
        else str(message).strip()
    )

    if not message:

        return (
            history,
            "",
            get_products_table(),
            get_orders_table(),
            get_analytics_table(),
            get_agent_activity_table(),
            get_kpi_html()
        )

    try:

        result = process_message(
            message
        )

        response = make_safe_text(
            result
        )

        history.append({
            "role": "user",
            "content": message
        })

        history.append({
            "role": "assistant",
            "content": response
        })

        return (
            history,
            "",
            get_products_table(),
            get_orders_table(),
            get_analytics_table(),
            get_agent_activity_table(),
            get_kpi_html()
        )

    except Exception as e:

        history.append({
            "role": "user",
            "content": message
        })

        history.append({
            "role": "assistant",
            "content": (
                "⚠️ Something went wrong.\n\n"
                f"Error: {str(e)}"
            )
        })

        return (
            history,
            "",
            get_products_table(),
            get_orders_table(),
            get_analytics_table(),
            get_agent_activity_table(),
            get_kpi_html()
        )


# ============================================================
# CLEAR CHAT
# ============================================================

def clear_chat():

    global pending_order

    pending_order = None

    return []


# ============================================================
# RESET
# ============================================================

def reset_business_ui():

    global pending_order
    global last_agent_trace

    pending_order = None
    last_agent_trace = []

    try:

        save_json(
            PRODUCTS_FILE,
            DEFAULT_PRODUCTS
        )

        save_json(
            ORDERS_FILE,
            []
        )

        save_json(
            ANALYTICS_FILE,
            []
        )

    except Exception:
        pass

    return (
        [],
        "",
        get_products_table(),
        get_orders_table(),
        get_analytics_table(),
        get_agent_activity_table(),
        get_kpi_html()
    )


# ============================================================
# REFRESH WRAPPERS
# ============================================================

def refresh_products():
    return get_products_table()


def refresh_orders():
    return get_orders_table()


def refresh_analytics():
    return get_analytics_table()


def refresh_activity():
    return get_agent_activity_table()


# ============================================================
# PROFESSIONAL CSS
# ============================================================

custom_css = """

/* GLOBAL */

.gradio-container {
    max-width: 1500px !important;
    margin: auto !important;
    padding-top: 20px !important;
    padding-bottom: 30px !important;
    font-family: Inter, ui-sans-serif, system-ui,
        -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
}


/* HEADER */

.hero {
    padding: 32px 35px;
    border-radius: 22px;
    margin-bottom: 18px;
    border: 1px solid #e5e7eb;
    background: linear-gradient(
        135deg,
        #ffffff 0%,
        #f8fafc 55%,
        #eef6ff 100%
    );
    box-shadow:
        0 10px 35px rgba(
            15,
            23,
            42,
            0.07
        );
}

.hero-brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 8px;
}

.hero-logo {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    font-size: 26px;
    background: #111827;
    color: white;
}

.hero h1 {
    margin: 0;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero-subtitle {
    margin: 8px 0 0 66px;
    color: #64748b;
    font-size: 16px;
    line-height: 1.6;
}


/* WORKFLOW */

.workflow {
    padding: 18px 22px;
    margin-bottom: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    background: white;
    text-align: center;
    color: #334155;
    font-size: 15px;
    box-shadow:
        0 5px 20px rgba(
            15,
            23,
            42,
            0.04
        );
}

.workflow-step {
    font-weight: 700;
    padding: 7px 13px;
    border-radius: 9px;
    background: #f1f5f9;
    display: inline-block;
    margin: 3px;
}

.workflow-arrow {
    margin: 0 5px;
    color: #94a3b8;
    font-weight: 700;
}


/* KPI CARDS */

.kpi-row {
    display: grid;
    grid-template-columns: repeat(
        4,
        1fr
    );
    gap: 15px;
    margin-bottom: 20px;
}

.kpi-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 17px;
    padding: 20px;
    box-shadow:
        0 6px 22px rgba(
            15,
            23,
            42,
            0.045
        );
}

.kpi-label {
    font-size: 13px;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-value {
    margin-top: 7px;
    font-size: 27px;
    font-weight: 800;
    color: #0f172a;
}

.kpi-description {
    margin-top: 4px;
    font-size: 12px;
    color: #94a3b8;
}


/* SECTION HEADERS */

.section-header {
    margin: 10px 0 15px 0;
}

.section-header h2 {
    margin-bottom: 4px;
    font-size: 22px;
    font-weight: 750;
    color: #0f172a;
}

.section-header p {
    margin: 0;
    color: #64748b;
    font-size: 14px;
}


/* CARDS */

.info-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow:
        0 6px 25px rgba(
            15,
            23,
            42,
            0.045
        );
}


/* CHAT */

.chat-container {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

textarea {
    border-radius: 12px !important;
}

button {
    border-radius: 10px !important;
}


/* ARCHITECTURE */

.architecture {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 28px;
    box-shadow:
        0 6px 25px rgba(
            15,
            23,
            42,
            0.045
        );
}

.arch-step {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 15px;
    margin: 8px 0;
    border-radius: 13px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}

.arch-number {
    min-width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: #111827;
    color: white;
    font-weight: 700;
}

.arch-title {
    font-weight: 700;
    color: #0f172a;
}

.arch-text {
    color: #64748b;
    font-size: 14px;
    margin-top: 2px;
}


/* DEMO */

.demo-hero {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
    color: white;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 20px;
}

.demo-hero h2 {
    margin-top: 0;
    font-size: 27px;
}

.demo-step {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 17px;
    padding: 22px;
    margin: 12px 0;
}

.demo-step-number {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #64748b;
    text-transform: uppercase;
}

.demo-step-title {
    font-size: 18px;
    font-weight: 750;
    margin-top: 4px;
    color: #0f172a;
}


/* TABLES */

.dataframe {
    border-radius: 13px !important;
    overflow: hidden !important;
}


/* MOBILE */

@media (max-width: 900px) {

    .kpi-row {
        grid-template-columns: repeat(
            2,
            1fr
        );
    }
}

@media (max-width: 600px) {

    .kpi-row {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        font-size: 27px;
    }

    .hero-subtitle {
        margin-left: 0;
    }
}
"""


# ============================================================
# APPLICATION
# ============================================================

with gr.Blocks(
    title="PakBiz AI"
) as demo:

    # ========================================================
    # HERO
    # ========================================================

    gr.HTML("""
    <div class="hero">

        <div class="hero-brand">

            <div class="hero-logo">
                🇵🇰
            </div>

            <div>
                <h1>PakBiz AI</h1>
            </div>

        </div>

        <div class="hero-subtitle">
            Agentic Sales & Inventory Assistant
            for Pakistani Small Businesses
        </div>

    </div>

    <div class="workflow">

        <span class="workflow-step">
            Customer Message
        </span>

        <span class="workflow-arrow">
            →
        </span>

        <span class="workflow-step">
            AI Agent
        </span>

        <span class="workflow-arrow">
            →
        </span>

        <span class="workflow-step">
            Business Tools
        </span>

        <span class="workflow-arrow">
            →
        </span>

        <span class="workflow-step">
            Verified Data
        </span>

        <span class="workflow-arrow">
            →
        </span>

        <span class="workflow-step">
            Business Action
        </span>

    </div>
    """)

    # ========================================================
    # ROLE SELECTOR
    # ========================================================

    with gr.Row():

        role_selector = gr.Radio(
            choices=[
                "🛍️ I'm a Customer",
                "🏪 I'm the Shopkeeper"
            ],
            value="🛍️ I'm a Customer",
            label="Choose Your View"
        )


    # ========================================================
    # CUSTOMER VIEW
    # ========================================================

    with gr.Column(
        visible=True
    ) as customer_view:

        with gr.Tabs():

            # ------------------------------------------------
            # CUSTOMER TAB
            # ------------------------------------------------

            with gr.Tab(
                "💬 Customer"
            ):

                gr.HTML("""
                <div class="section-header">

                    <h2>
                        Customer Assistant
                    </h2>

                    <p>
                        Customers can communicate naturally
                        in English, Roman Urdu or Urdu.
                    </p>

                </div>
                """)

                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=520,
                    type="messages"
                )

                with gr.Row():

                    message_box = gr.Textbox(
                        label="",
                        placeholder=(
                            "Try: 2 blue shirts leni hain"
                        ),
                        scale=6
                    )

                    send_button = gr.Button(
                        "Send  ➜",
                        variant="primary",
                        scale=1
                    )

                with gr.Row():

                    clear_button = gr.Button(
                        "Clear Conversation"
                    )

                    reset_button = gr.Button(
                        "Reset Demo Data"
                    )

                gr.HTML("""
                <div class="info-card">

                    <b>Try these messages</b>

                    <br><br>

                    <code>
                        2 blue shirts leni hain
                    </code>

                    <br>

                    <code>
                        blue shirt ki price kya hai?
                    </code>

                    <br>

                    <code>
                        black shirt ka stock kitna hai?
                    </code>

                    <br>

                    <code>
                        ap ke pas kya available hai
                    </code>

                    <br>

                    <code>
                        ORD-1001 ka status kya hai?
                    </code>

                </div>
                """)


            # ------------------------------------------------
            # HACKATHON DEMO TAB
            # ------------------------------------------------

            with gr.Tab(
                "🏆 Hackathon Demo"
            ):

                gr.HTML("""
                <div class="demo-hero">

                    <h2>
                        From Conversation to Business Action
                    </h2>

                    <p>
                        A complete agentic workflow demonstrated
                        through one realistic customer interaction.
                    </p>

                </div>


                <div class="demo-step">

                    <div class="demo-step-number">
                        STEP 01
                    </div>

                    <div class="demo-step-title">
                        Customer Request
                    </div>

                    <p>
                        "2 blue shirts leni hain"
                    </p>

                </div>


                <div class="demo-step">

                    <div class="demo-step-number">
                        STEP 02
                    </div>

                    <div class="demo-step-title">
                        Agent Understands
                    </div>

                    <p>
                        Product → Blue Shirt
                        <br>
                        Quantity → 2
                        <br>
                        Intent → Purchase
                    </p>

                </div>


                <div class="demo-step">

                    <div class="demo-step-number">
                        STEP 03
                    </div>

                    <div class="demo-step-title">
                        Agent Uses Business Tools
                    </div>

                    <p>
                        Check Stock → Get Price →
                        Calculate Total
                    </p>

                </div>


                <div class="demo-step">

                    <div class="demo-step-number">
                        STEP 04
                    </div>

                    <div class="demo-step-title">
                        Human Confirmation
                    </div>

                    <p>
                        The customer confirms naturally with
                        <b>haan</b>, <b>yes</b>,
                        <b>confirm</b> or <b>1</b>.
                    </p>

                </div>


                <div class="demo-step">

                    <div class="demo-step-number">
                        STEP 05
                    </div>

                    <div class="demo-step-title">
                        Agent Executes
                    </div>

                    <p>
                        The confirmed order is created
                        and inventory is updated.
                    </p>

                </div>


                <div class="demo-step">

                    <div class="demo-step-number">
                        STEP 06
                    </div>

                    <div class="demo-step-title">
                        Business State Changes
                    </div>

                    <p>
                        Orders, inventory and analytics
                        immediately reflect the new transaction.
                    </p>

                </div>


                <div class="info-card">

                    <h3>
                        Why this is an Agentic AI system
                    </h3>

                    <p>
                        PakBiz AI does not simply generate
                        a conversational answer.
                        The agent interprets the request,
                        selects tools, retrieves verified data,
                        prepares a business action,
                        requests human confirmation and
                        executes the confirmed action.
                    </p>

                </div>
                """)


    # ========================================================
    # SHOPKEEPER VIEW
    # ========================================================

    with gr.Column(
        visible=False
    ) as shopkeeper_view:

        # ----------------------------------------------------
        # LIVE KPI DASHBOARD
        # ----------------------------------------------------

        kpi_html = gr.HTML(
            value=get_kpi_html()
        )

        with gr.Tabs():

            # ------------------------------------------------
            # INVENTORY
            # ------------------------------------------------

            with gr.Tab(
                "📦 Inventory"
            ):

                gr.HTML("""
                <div class="section-header">

                    <h2>
                        Products & Inventory
                    </h2>

                    <p>
                        Live business inventory controlled
                        by the agent's verified tools.
                    </p>

                </div>
                """)

                products_table = gr.Dataframe(
                    value=get_products_table(),
                    label="Product Catalog",
                    interactive=False
                )

                refresh_products_button = gr.Button(
                    "↻ Refresh Inventory"
                )


            # ------------------------------------------------
            # ORDERS
            # ------------------------------------------------

            with gr.Tab(
                "🧾 Orders"
            ):

                gr.HTML("""
                <div class="section-header">

                    <h2>
                        Confirmed Orders
                    </h2>

                    <p>
                        Orders created only after explicit
                        customer confirmation.
                    </p>

                </div>
                """)

                orders_table = gr.Dataframe(
                    value=get_orders_table(),
                    label="Order History",
                    interactive=False
                )

                refresh_orders_button = gr.Button(
                    "↻ Refresh Orders"
                )


            # ------------------------------------------------
            # BUSINESS DASHBOARD
            # ------------------------------------------------

            with gr.Tab(
                "📊 Business Dashboard"
            ):

                gr.HTML("""
                <div class="section-header">

                    <h2>
                        Business Analytics
                    </h2>

                    <p>
                        Real-time statistics generated
                        from confirmed business orders.
                    </p>

                </div>
                """)

                analytics_table = gr.Dataframe(
                    value=get_analytics_table(),
                    label="Business Performance",
                    interactive=False
                )

                refresh_analytics_button = gr.Button(
                    "↻ Refresh Analytics"
                )


            # ------------------------------------------------
            # AGENT ACTIVITY
            # ------------------------------------------------

            with gr.Tab(
                "🤖 Agent Activity"
            ):

                gr.HTML("""
                <div class="section-header">

                    <h2>
                        Agent Activity
                    </h2>

                    <p>
                        See how the AI agent uses business
                        tools to turn language into
                        verified actions.
                    </p>

                </div>
                """)

                activity_table = gr.Dataframe(
                    value=get_agent_activity_table(),
                    label="Tool Calls & Agent Actions",
                    interactive=False
                )

                refresh_activity_button = gr.Button(
                    "↻ Refresh Activity"
                )

                gr.HTML("""
                <br>

                <div class="architecture">

                    <h2>
                        Agent Architecture
                    </h2>

                    <p style="color:#64748b;">
                        PakBiz AI separates language
                        intelligence from reliable
                        business execution.
                    </p>


                    <div class="arch-step">

                        <div class="arch-number">
                            1
                        </div>

                        <div>

                            <div class="arch-title">
                                Customer Message
                            </div>

                            <div class="arch-text">
                                Natural English,
                                Roman Urdu or Urdu
                            </div>

                        </div>

                    </div>


                    <div class="arch-step">

                        <div class="arch-number">
                            2
                        </div>

                        <div>

                            <div class="arch-title">
                                AI Understanding
                            </div>

                            <div class="arch-text">
                                Intent detection
                                and task understanding
                            </div>

                        </div>

                    </div>


                    <div class="arch-step">

                        <div class="arch-number">
                            3
                        </div>

                        <div>

                            <div class="arch-title">
                                Tool Selection
                            </div>

                            <div class="arch-text">
                                The agent selects
                                the appropriate
                                business operation
                            </div>

                        </div>

                    </div>


                    <div class="arch-step">

                        <div class="arch-number">
                            4
                        </div>

                        <div>

                            <div class="arch-title">
                                Verified Business Data
                            </div>

                            <div class="arch-text">
                                Price, stock and order
                                information come from
                                business tools
                            </div>

                        </div>

                    </div>


                    <div class="arch-step">

                        <div class="arch-number">
                            5
                        </div>

                        <div>

                            <div class="arch-title">
                                Business Action
                            </div>

                            <div class="arch-text">
                                Prepare, confirm and
                                execute the requested
                                business action
                            </div>

                        </div>

                    </div>


                    <div class="arch-step">

                        <div class="arch-number">
                            6
                        </div>

                        <div>

                            <div class="arch-title">
                                Updated Business State
                            </div>

                            <div class="arch-text">
                                Orders and inventory
                                are updated after
                                confirmation
                            </div>

                        </div>

                    </div>


                    <hr>


                    <h3>
                        🛡️ Anti-Hallucination Design
                    </h3>

                    <p style="color:#64748b;">

                        The LLM does not invent product
                        prices, stock levels, order IDs
                        or sales totals.

                        Python business tools and stored
                        business data remain the source
                        of truth.

                    </p>

                </div>
                """)


    # ========================================================
    # ROLE TOGGLE
    # ========================================================

    def toggle_view(role):

        is_shopkeeper = (
            role.startswith("🏪")
        )

        return (
            gr.update(
                visible=not is_shopkeeper
            ),
            gr.update(
                visible=is_shopkeeper
            )
        )


    role_selector.change(
        fn=toggle_view,
        inputs=[role_selector],
        outputs=[
            customer_view,
            shopkeeper_view
        ]
    )


    # ========================================================
    # APPLY INITIAL VIEW
    # ========================================================

    demo.load(
        fn=toggle_view,
        inputs=[role_selector],
        outputs=[
            customer_view,
            shopkeeper_view
        ]
    )


    # ========================================================
    # OUTPUT CONNECTIONS
    # ========================================================

    all_outputs = [
        chatbot,
        message_box,
        products_table,
        orders_table,
        analytics_table,
        activity_table,
        kpi_html
    ]


    # ========================================================
    # CHAT EVENT
    # ========================================================

    send_button.click(
        fn=chat_handler,
        inputs=[
            message_box,
            chatbot
        ],
        outputs=all_outputs
    )

    message_box.submit(
        fn=chat_handler,
        inputs=[
            message_box,
            chatbot
        ],
        outputs=all_outputs
    )


    # ========================================================
    # CLEAR
    # ========================================================

    clear_button.click(
        fn=clear_chat,
        inputs=[],
        outputs=[chatbot]
    )


    # ========================================================
    # RESET
    # ========================================================

    reset_button.click(
        fn=reset_business_ui,
        inputs=[],
        outputs=all_outputs
    )


    # ========================================================
    # REFRESH BUTTONS
    # ========================================================

    refresh_products_button.click(
        fn=refresh_products,
        inputs=[],
        outputs=[products_table]
    )

    refresh_orders_button.click(
        fn=refresh_orders,
        inputs=[],
        outputs=[orders_table]
    )

    refresh_analytics_button.click(
        fn=refresh_analytics,
        inputs=[],
        outputs=[analytics_table]
    )

    refresh_activity_button.click(
        fn=refresh_activity,
        inputs=[],
        outputs=[activity_table]
    )


# ============================================================
# LAUNCH
# ============================================================

print("=" * 60)
print("🇵🇰 PAKBIZ AI")
print("Agentic Sales & Inventory Assistant")
print("=" * 60)
print()
print("Launching PakBiz AI...")
print()

demo.launch(
    css=custom_css
)

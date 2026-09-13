# PakBiz AI 🤖🇵🇰

## Agentic AI Sales & Business Assistant for Pakistani Small Businesses

PakBiz AI is an agentic AI-powered business assistant designed to help small businesses manage customer conversations, product discovery, pricing, inventory, order preparation, and business insights through natural language.

Instead of functioning as a simple chatbot, PakBiz AI combines a Large Language Model with deterministic business tools and verified business data.

**Natural Language → Intent Understanding → Tool Selection → Verified Business Data → Safe Action**

The project is developed as a practical prototype for the **Pak Angels & Aspire Pakistan Generative and Agentic AI Cohort 11 Hackathon**.

---

# 🚀 Why PakBiz AI?

Many small businesses communicate with customers through messaging platforms and manually handle questions such as:

* "Blue shirt kitne ki hai?"
* "Black shirt available hai?"
* "Mujhe 2 blue shirts chahiye."
* "Under 5000 koi acha option hai?"
* "Is product ka stock kitna hai?"
* "Mera order confirm kar dein."
* "Aaj kitni sales hui hain?"

A conventional chatbot may generate a response, but generating a response is not enough for business operations.

A business assistant needs to:

1. Understand what the customer wants.
2. Find the correct product.
3. Verify the actual price.
4. Check the actual stock.
5. Calculate the order total.
6. Prepare the order.
7. Ask the customer for confirmation.
8. Update inventory only after confirmation.
9. Keep business records updated.

PakBiz AI is designed around this workflow.

---

# 🎯 Project Goal

The goal of PakBiz AI is to demonstrate how **Generative AI + Agentic AI + deterministic business tools** can work together to create a practical assistant for small businesses.

The LLM handles:

* Natural-language understanding
* Intent interpretation
* Tool selection
* Conversation
* Multilingual interaction

Python business tools handle:

* Product lookup
* Price verification
* Stock verification
* Calculations
* Order preparation
* Order creation
* Inventory updates
* Sales information

This separation helps reduce hallucinations and makes business-critical operations more reliable.

---

# 🧠 Agentic AI Architecture

PakBiz AI follows an agentic architecture rather than simply sending every message directly to an LLM.

```text
                         CUSTOMER
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Natural Language    │
                 │ Message             │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   AI Agent / LLM    │
                 │ Intent Understanding│
                 │ & Decision Making   │
                 └──────────┬──────────┘
                            │
                   Selects required tools
                            │
            ┌───────────────┼────────────────┐
            ▼               ▼                ▼
     Search Products    Check Stock     Get Price
            │               │                │
            └───────────────┼────────────────┘
                            ▼
                  ┌─────────────────┐
                  │ Calculate Total │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Prepare Order   │
                  └────────┬────────┘
                           │
                           ▼
                  Customer Confirmation
                           │
                    ┌──────┴──────┐
                    │             │
                   YES            NO
                    │             │
                    ▼             ▼
             Create Order      Cancel
                    │
                    ▼
             Update Inventory
                    │
                    ▼
             Business Records
```

---

# 🔥 What Makes It Agentic?

PakBiz AI does not rely on the LLM to invent business information.

The agent can dynamically decide which business tools are required based on the user's request.

For example:

**Customer:**

> "Mujhe 2 blue shirts chahiye."

The agent can perform:

```text
Understand purchase intent
        ↓
Identify "Blue Shirt"
        ↓
Search product catalog
        ↓
Check stock
        ↓
Get verified price
        ↓
Calculate 2 × price
        ↓
Prepare order
        ↓
Ask for confirmation
```

The order is **not created immediately**.

The customer must confirm the order first.

---

# 🛡️ Anti-Hallucination Design

Business information should come from the business data, not from the model's imagination.

PakBiz AI therefore follows an important principle:

> **The LLM is the reasoning and language layer. Python tools and business data are the source of truth.**

### Price

Instead of allowing the model to guess:

> "Blue Shirt costs around Rs. 2,000."

the agent uses the product catalog to retrieve the actual price.

### Stock

Instead of generating:

> "Yes, it is probably available."

the agent checks the stored inventory.

### Order

The system does not allow an order to be created simply because the customer mentions a product.

The workflow requires confirmation.

---

# 🛒 Core Features

## 1. Natural Language Business Assistant

Users can communicate naturally instead of learning commands.

Examples:

```text
Show me shirts.

Black shirt available?

Blue shirt kitne ki hai?

Mujhe 2 blue shirts chahiye.

5000 ke andar koi option hai.

Cancel my order.
```

## 2. Multilingual Interaction

PakBiz AI is designed to support:

* English
* Roman Urdu
* Urdu-oriented conversational input

This makes the system more accessible to Pakistani customers and small-business users.

## 3. Intelligent Product Search

The agent can search the business catalog based on natural-language requests.

Example:

> "Show me shirts"

The system searches the product catalog instead of generating imaginary products.

## 4. Verified Pricing

Product prices are retrieved from the business data.

Example:

```text
Blue Shirt
Price: Rs. 2,000
```

The LLM does not independently determine the price.

## 5. Real-Time Stock Checking

Before preparing an order, the system verifies inventory.

Example:

```text
Blue Shirt
Requested: 2
Available: 10
```

This prevents the assistant from confirming unavailable products.

## 6. Automatic Order Calculation

The system can calculate totals using a deterministic calculation tool.

Example:

```text
2 × Rs. 2,000
= Rs. 4,000
```

This calculation is performed by the application rather than relying on the LLM for arithmetic.

## 7. Smart Order Preparation

PakBiz AI can prepare an order based on:

* Requested products
* Quantities
* Available stock
* Budget constraints

This allows the agent to support more flexible customer requests.

## 8. Human Confirmation

Orders are not automatically finalized.

The system presents the prepared order to the customer and asks for confirmation.

Example:

```text
Order Summary

Blue Shirt × 2
Total: Rs. 4,000

Would you like to confirm?

1. Confirm
2. Cancel
```

Only after confirmation does the system create the order.

## 9. Inventory Update

After successful order confirmation:

```text
Order Created
      ↓
Inventory Updated
      ↓
Business Records Updated
```

This demonstrates an actual agentic business action rather than just text generation.

## 10. Order Tracking

The system maintains order information including:

* Order ID
* Products
* Quantities
* Total amount
* Status

## 11. Business Dashboard

PakBiz AI includes a shopkeeper-oriented dashboard with:

* Sales information
* Orders
* Inventory
* Analytics
* Agent activity

This allows the same prototype to demonstrate both customer interaction and business operations.

---

# 🧰 Business Tools

The agent can use deterministic Python tools including:

| Tool                  | Purpose                           |
| --------------------- | --------------------------------- |
| `search_products`     | Search the product catalog        |
| `get_product_price`   | Retrieve verified product pricing |
| `check_stock`         | Verify available inventory        |
| `calculate_total`     | Calculate order totals            |
| `prepare_order`       | Prepare an order                  |
| `prepare_smart_order` | Prepare budget-aware orders       |
| `update_inventory`    | Update product stock              |
| `create_order`        | Create a confirmed order          |
| `get_order`           | Retrieve order information        |
| `get_sales_summary`   | Retrieve sales information        |

These tools provide the connection between the AI agent and the business data.

---

# 🔄 Example Agent Workflow

## Customer Request

```text
I want 2 black shirts.
```

## Step 1 — Understand

The agent identifies:

```text
Intent: Purchase
Product: Black Shirt
Quantity: 2
```

## Step 2 — Search

The agent searches the product catalog.

## Step 3 — Verify Stock

The system checks available stock.

## Step 4 — Retrieve Price

The actual product price is retrieved.

## Step 5 — Calculate

```text
2 × Rs. 2,200
= Rs. 4,400
```

## Step 6 — Prepare

The system prepares the order.

## Step 7 — Confirm

The customer receives an order summary.

## Step 8 — Execute

Only after confirmation:

```text
Create Order
     ↓
Update Inventory
     ↓
Store Business Record
```

This is the key difference between a conversational AI and an agentic business assistant.

---

# 📊 Demo Business Data

The prototype currently contains sample products such as:

| ID   | Product       | Category    |     Price | Stock |
| ---- | ------------- | ----------- | --------: | ----: |
| P001 | Blue Shirt    | Shirts      | Rs. 2,000 |    10 |
| P002 | Black Shirt   | Shirts      | Rs. 2,200 |     8 |
| P003 | White Shirt   | Shirts      | Rs. 1,800 |    12 |
| P004 | Black Pant    | Pants       | Rs. 2,500 |     3 |
| P005 | Blue Jeans    | Jeans       | Rs. 3,500 |     6 |
| P006 | Kurta         | Traditional | Rs. 2,800 |     7 |
| P007 | Black T-Shirt | T-Shirts    | Rs. 1,500 |    15 |
| P008 | Red T-Shirt   | T-Shirts    | Rs. 1,500 |     9 |

These are demonstration records and can be replaced with real business data.

---

# 🖥️ Application Interface

PakBiz AI contains two main experiences.

## Customer View

The customer can:

* Chat with the AI assistant
* Search products
* Ask about prices
* Check availability
* Prepare orders
* Confirm or cancel orders

## Shopkeeper View

The shopkeeper can view:

* KPIs
* Inventory
* Orders
* Business analytics
* Agent activity

This demonstrates both sides of the business workflow.

---

# 🧑‍💻 Technology Stack

## Artificial Intelligence

* Groq API
* `openai/gpt-oss-120b`
* Tool calling
* Agentic reasoning

## Backend

* Python
* JSON-based business data
* Deterministic business tools

## Interface

* Gradio
* Custom CSS
* Interactive dashboards

## Data Processing

* Pandas
* JSON

---

# 📁 Project Structure

```text
pakbiz-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    ├── products.json
    ├── orders.json
    └── analytics.json
```

### File Responsibilities

**`app.py`**

Contains:

* AI agent
* Tool definitions
* Business logic
* Order workflow
* Gradio interface
* Dashboard
* Inventory operations

**`data/products.json`**

Stores product catalog information.

**`data/orders.json`**

Stores confirmed orders.

**`data/analytics.json`**

Stores business activity/analytics records.

**`requirements.txt`**

Contains the Python dependencies required to run the application.

---

# ⚙️ Local Installation

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project:

```bash
cd pakbiz-ai
```

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configure the Groq API Key

The API key is **not stored in the source code**.

The application expects an environment variable named:

```text
GROQ_API_KEY
```

## Windows Command Prompt

```cmd
set GROQ_API_KEY=YOUR_GROQ_API_KEY
```

## Windows PowerShell

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Then run:

```bash
python app.py
```

The application will start locally.

---

# 🔒 Security

API credentials should never be committed to GitHub.

PakBiz AI intentionally uses:

```python
os.environ.get("GROQ_API_KEY")
```

instead of placing the secret directly in `app.py`.

The `.gitignore` also prevents `.env` files from being committed.

### Never commit:

```text
gsk_...
```

or any other API credential.

---

# ☁️ Deployment

PakBiz AI can be deployed as a Python/Gradio application.

For a hosted deployment, the API key should be configured as a **secret/environment variable** provided by the hosting platform.

The source code should remain free of API credentials.

For example:

```text
GROQ_API_KEY = ***************
```

The application reads this value at runtime.

---

# 🧪 Hackathon Demo Flow

A recommended live demonstration is:

## 1. Show the customer interface

Ask:

```text
Show me shirts
```

## 2. Ask for availability

```text
Is the black shirt available?
```

## 3. Ask for a purchase

```text
I want 2 black shirts.
```

## 4. Show the agent workflow

Demonstrate that the system:

```text
Understands intent
       ↓
Searches product
       ↓
Checks stock
       ↓
Gets price
       ↓
Calculates total
       ↓
Prepares order
```

## 5. Show confirmation

The system asks the customer before creating the order.

## 6. Confirm

```text
Yes
```

## 7. Show business action

Demonstrate:

```text
Order created
Inventory updated
Analytics updated
```

## 8. Open the shopkeeper dashboard

Show the updated:

* Order
* Inventory
* Business information
* Agent activity

This gives judges a complete end-to-end demonstration.

---

# 🏆 Hackathon Positioning

PakBiz AI is not positioned simply as:

> "An AI chatbot for Pakistani businesses."

The core proposition is:

> **An agentic AI business assistant that connects natural-language customer requests to verified business data and controlled business actions.**

The architecture demonstrates several important concepts relevant to Generative and Agentic AI:

* LLM-based reasoning
* Tool calling
* Dynamic tool selection
* Structured information extraction
* Deterministic business functions
* State management
* Human-in-the-loop confirmation
* Business-data grounding
* Safe action execution

---

# 💡 Differentiation

The project focuses on the **agentic workflow** rather than only conversational AI.

A simplified chatbot might do:

```text
Customer
   ↓
LLM
   ↓
Text Response
```

PakBiz AI aims to demonstrate:

```text
Customer
   ↓
LLM Agent
   ↓
Understand Intent
   ↓
Select Tools
   ↓
Verify Business Data
   ↓
Perform Calculations
   ↓
Prepare Action
   ↓
Human Confirmation
   ↓
Execute Business Action
   ↓
Update Business State
```

This makes the project suitable for demonstrating the practical application of agentic AI.

---

# 🛡️ Safety Principles

PakBiz AI follows several safeguards:

### 1. No invented business data

Prices and stock should come from the stored catalog.

### 2. Deterministic calculations

Order totals are calculated through application logic.

### 3. Stock verification

The system checks inventory before preparing an order.

### 4. Human confirmation

An order should not be finalized without customer confirmation.

### 5. API key protection

Secrets are stored outside the source code.

### 6. Business data as source of truth

The LLM is not treated as the authoritative database.

---

# 📈 Future Scope

PakBiz AI can be extended beyond the current prototype.

Potential future capabilities include:

## WhatsApp Integration

Connect the agent to WhatsApp so customers can interact through their normal messaging channel.

## Real Database

Replace JSON storage with:

* PostgreSQL
* MySQL
* Supabase
* Firebase

## Real Business Accounts

Allow individual businesses to maintain their own:

* Products
* Inventory
* Orders
* Customers
* Analytics

## Payment Integration

Integrate secure payment providers so customers can move from order confirmation toward payment.

## Delivery Integration

Connect orders with delivery/courier services.

## Voice Agent

Allow customers to communicate through voice in Urdu, Roman Urdu, and English.

## Advanced Business Analytics

Add:

* Sales forecasting
* Best-selling products
* Low-stock alerts
* Customer trends
* Revenue analysis

## Multi-Agent Architecture

Future versions could divide responsibilities among specialized agents:

```text
Customer Agent
      ↓
Sales Agent
      ↓
Inventory Agent
      ↓
Analytics Agent
      ↓
Business Manager Agent
```

---

# ⚠️ Current Prototype Limitations

This project is currently a hackathon prototype.

The included business data is demonstration data.

The current version uses JSON files for persistence rather than a production database.

A production deployment would require additional work around:

* Authentication
* Multi-business data isolation
* Database persistence
* Payment security
* Customer privacy
* API rate limiting
* Transaction handling
* Production monitoring
* Deployment scalability

These limitations are intentionally recognized rather than hidden.

---

# 🇵🇰 Pakistan-Focused Design

PakBiz AI is designed around communication patterns common in Pakistan.

Customers may naturally switch between:

* English
* Roman Urdu
* Urdu

For example:

```text
Black shirt available hai?

Blue shirt kitne ki hai?

Mujhe 2 chahiye.

5000 ke andar koi option hai?
```

The system aims to allow customers to communicate naturally rather than requiring formal commands.

---

# 👥 Target Users

PakBiz AI is designed with small businesses and independent sellers in mind, including:

* Clothing sellers
* Online shops
* Instagram businesses
* Home-based businesses
* Small retailers
* Freelancers selling products
* Student entrepreneurs
* Local e-commerce sellers

---

# 🔮 Vision

The long-term vision of PakBiz AI is to move small businesses from:

```text
Manual Customer Messages
        +
Manual Inventory Checking
        +
Manual Order Processing
```

toward:

```text
Natural Language
       ↓
AI Agent
       ↓
Business Tools
       ↓
Verified Data
       ↓
Safe Business Actions
```

The objective is not simply to make AI talk to customers.

The objective is to make AI **useful for real business operations while keeping important actions grounded and controlled.**

---

# 📜 License

This project is currently intended as a hackathon prototype and educational demonstration.

Add an appropriate open-source license if the project is later released for public reuse.

---

# 👨‍💻 Project

## PakBiz AI

**Agentic AI Sales & Business Assistant for Pakistani Small Businesses**

Built for the **Pak Angels & Aspire Pakistan Generative and Agentic AI Cohort 11 Hackathon**.

---

## ⭐ Key Idea

> **Don't just make AI answer. Make AI understand, verify, decide, and safely act.**

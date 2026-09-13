PakBiz AI 🤖🇵🇰
Agentic AI Sales & Business Assistant for Pakistani Small Businesses

PakBiz AI is an agentic AI-powered business assistant designed to help small businesses manage customer conversations, product discovery, pricing, inventory, order preparation, and business insights through natural language.

Instead of functioning as a simple chatbot, PakBiz AI combines a Large Language Model with deterministic business tools and verified business data.

Natural Language → Intent Understanding → Tool Selection → Verified Business Data → Safe Action

The project is developed as a practical prototype for the Pak Angels & Aspire Pakistan Generative and Agentic AI Cohort 11 Hackathon.

🚀 Why PakBiz AI?

Many small businesses communicate with customers through messaging platforms and manually handle questions such as:

"Blue shirt kitne ki hai?"
"Black shirt available hai?"
"Mujhe 2 blue shirts chahiye."
"Under 5000 koi acha option hai?"
"Is product ka stock kitna hai?"
"Mera order confirm kar dein."
"Aaj kitni sales hui hain?"

A conventional chatbot may generate a response, but generating a response is not enough for business operations.

A business assistant needs to:

Understand what the customer wants.
Find the correct product.
Verify the actual price.
Check the actual stock.
Calculate the order total.
Prepare the order.
Ask the customer for confirmation.
Update inventory only after confirmation.
Keep business records updated.

PakBiz AI is designed around this workflow.

🎯 Project Goal

The goal of PakBiz AI is to demonstrate how Generative AI + Agentic AI + deterministic business tools can work together to create a practical assistant for small businesses.

The LLM handles:

Natural-language understanding
Intent interpretation
Tool selection
Conversation
Multilingual interaction

Python business tools handle:

Product lookup
Price verification
Stock verification
Calculations
Order preparation
Order creation
Inventory updates
Sales information

This separation helps reduce hallucinations and makes business-critical operations more reliable.

🧠 Agentic AI Architecture

PakBiz AI follows an agentic architecture rather than simply sending every message directly to an LLM.

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
🔥 What Makes It Agentic?

PakBiz AI does not rely on the LLM to invent business information.

The agent can dynamically decide which business tools are required based on the user's request.

For example:

Customer:

"Mujhe 2 blue shirts chahiye."

The agent can perform:

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

The order is not created immediately.

The customer must confirm the order first.

🛡️ Anti-Hallucination Design

Business information should come from the business data, not from the model's imagination.

PakBiz AI therefore follows an important principle:

The LLM is the reasoning and language layer. Python tools and business data are the source of truth.

For example:

Price

Instead of allowing the model to guess:

"Blue Shirt costs around Rs. 2,000."

the agent uses the product catalog to retrieve the actual price.

Stock

Instead of generating:

"Yes, it is probably available."

the agent checks the stored inventory.

Order

The system does not allow an order to be created simply because the customer mentions a product.

The workflow requires confirmation.

🛒 Core Features
1. Natural Language Business Assistant

Users can communicate naturally instead of learning commands.

Examples:

Show me shirts.

Black shirt available?

Blue shirt kitne ki hai?

Mujhe 2 blue shirts chahiye.

5000 ke andar koi option hai.

Cancel my order.
2. Multilingual Interaction

PakBiz AI is designed to support:

English
Roman Urdu
Urdu-oriented conversational input

This makes the system more accessible to Pakistani customers and small-business users.

3. Intelligent Product Search

The agent can search the business catalog based on natural-language requests.

Example:

"Show me shirts"

The system searches the product catalog instead of generating imaginary products.

4. Verified Pricing

Product prices are retrieved from the business data.

Example:

Blue Shirt
Price: Rs. 2,000

The LLM does not independently determine the price.

5. Real-Time Stock Checking

Before preparing an order, the system verifies inventory.

Example:

Blue Shirt
Requested: 2
Available: 10

This prevents the assistant from confirming unavailable products.

6. Automatic Order Calculation

The system can calculate totals using a deterministic calculation tool.

Example:

2 × Rs. 2,000
= Rs. 4,000

This calculation is performed by the application rather than relying on the LLM for arithmetic.

7. Smart Order Preparation

PakBiz AI can prepare an order based on:

Requested products
Quantities
Available stock
Budget constraints

This allows the agent to support more flexible customer requests.

8. Human Confirmation

Orders are not automatically finalized.

The system presents the prepared order to the customer and asks for confirmation.

Example:

Order Summary

Blue Shirt × 2
Total: Rs. 4,000

Would you like to confirm?

1. Confirm
2. Cancel

Only after confirmation does the system create the order.

9. Inventory Update

After successful order confirmation:

Order Created
      ↓
Inventory Updated
      ↓
Business Records Updated

This demonstrates an actual agentic business action rather than just text generation.

10. Order Tracking

The system maintains order information including:

Order ID
Products
Quantities
Total amount
Status
11. Business Dashboard

PakBiz AI includes a shopkeeper-oriented dashboard with:

Sales information
Orders
Inventory
Analytics
Agent activity

This allows the same prototype to demonstrate both customer interaction and business operations.

🧰 Business Tools

The agent can use deterministic Python tools including:

Tool	Purpose
search_products	Search the product catalog
get_product_price	Retrieve verified product pricing
check_stock	Verify available inventory
calculate_total	Calculate order totals
prepare_order	Prepare an order
prepare_smart_order	Prepare budget-aware orders
update_inventory	Update product stock
create_order	Create a confirmed order
get_order	Retrieve order information
get_sales_summary	Retrieve sales information

These tools provide the connection between the AI agent and the business data.

🔄 Example Agent Workflow
Customer Request
I want 2 black shirts.
Step 1 — Understand

The agent identifies:

Intent: Purchase
Product: Black Shirt
Quantity: 2
Step 2 — Search

The agent searches the product catalog.

Step 3 — Verify Stock

The system checks available stock.

Step 4 — Retrieve Price

The actual product price is retrieved.

Step 5 — Calculate
2 × Rs. 2,200
= Rs. 4,400
Step 6 — Prepare

The system prepares the order.

Step 7 — Confirm

The customer receives an order summary.

Step 8 — Execute

Only after confirmation:

Create Order
     ↓
Update Inventory
     ↓
Store Business Record

This is the key difference between a conversational AI and an agentic business assistant.

📊 Demo Business Data

The prototype currently contains sample products such as:

ID	Product	Category	Price	Stock
P001	Blue Shirt	Shirts	Rs. 2,000	10
P002	Black Shirt	Shirts	Rs. 2,200	8
P003	White Shirt	Shirts	Rs. 1,800	12
P004	Black Pant	Pants	Rs. 2,500	3
P005	Blue Jeans	Jeans	Rs. 3,500	6
P006	Kurta	Traditional	Rs. 2,800	7
P007	Black T-Shirt	T-Shirts	Rs. 1,500	15
P008	Red T-Shirt	T-Shirts	Rs. 1,500	9

These are demonstration records and can be replaced with real business data.

🖥️ Application Interface

PakBiz AI contains two main experiences.

Customer View

The customer can:

Chat with the AI assistant
Search products
Ask about prices
Check availability
Prepare orders
Confirm or cancel orders
Shopkeeper View

The shopkeeper can view:

KPIs
Inventory
Orders
Business analytics
Agent activity

This demonstrates both sides of the business workflow.

🧑‍💻 Technology Stack
Artificial Intelligence
Groq API
openai/gpt-oss-120b
Tool calling
Agentic reasoning
Backend
Python
JSON-based business data
Deterministic business tools
Current Prototype Limitations

This project is currently a hackathon prototype.

The included business data is demonstration data.

The current version uses JSON files for persistence rather than a production database.

A production deployment would require additional work around:

Authentication
Multi-business data isolation
Database persistence
Payment security
Customer privacy
API rate limiting
Transaction handling
Production monitoring
Deployment scalability

These limitations are intentionally recognized rather than hidden.

# OdooClaw MCP

Standalone MCP (Model Context Protocol) server for Odoo 18 over `stdio`.

**MCP name:** `io.github.nicolasramos/odooclaw-mcp`  
**PyPI package:** `odooclaw-mcp`  
**Official CLI:** `odooclaw-mcp`

Backward-compatible aliases are also installed:

- `odoo-mcp`
- `odoo-mcp-server`
- `odoo-18-mcp-server`

## Quick Start

### 1) Install

```bash
pip install odooclaw-mcp
```

From source:

```bash
git clone https://github.com/nicolasramos/odooclaw-mcp.git
cd odooclaw-mcp
pip install -e .
```

### 2) Configure environment

```bash
cp .env.example .env
```

Required:

```env
ODOO_URL=https://yourcompany.odoo.com
ODOO_DB=your_database
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
```

Optional:

```env
ODOO_MCP_DEFAULT_LIMIT=50
ODOO_MCP_MAX_LIMIT=80
LOG_LEVEL=INFO
```

### 3) Validate and run

```bash
odooclaw-mcp --check-config
odooclaw-mcp
```

Alternative:

```bash
python -m odoo_mcp
```

## MCP Client Configuration (stdio)

```json
{
  "mcpServers": {
    "odoo": {
      "command": "odooclaw-mcp",
      "env": {
        "ODOO_URL": "https://yourcompany.odoo.com",
        "ODOO_DB": "your_database",
        "ODOO_USERNAME": "your_username",
        "ODOO_PASSWORD": "your_password",
        "ODOO_MCP_DEFAULT_LIMIT": "50",
        "ODOO_MCP_MAX_LIMIT": "80"
      }
    }
  }
}
```

### Tool call payload contract

When calling tools through the MCP protocol, arguments must be wrapped in a
top-level `payload` object.

Valid shape:

```json
{
  "name": "odoo_search",
  "arguments": {
    "payload": {
      "model": "res.partner",
      "domain": [["customer_rank", ">", 0]],
      "limit": 3
    }
  }
}
```

If `payload` is omitted, validation fails with an error equivalent to
`Field required: payload`.

## Scope

- 124 MCP tools for Odoo operations (CRUD + business actions + migration workflows)
- Pydantic validation for all tool payloads
- Odoo 18 compatibility helpers (customer_rank / supplier_rank / payment_state)
- Security guards (model allowlist, denylisted fields, action guard, unlink blocked)
- Structured logging and audit actions

## Available Tools

The server currently exposes **124 MCP tools**.

> Note: the grouped tables below focus on common/high-value tools. Use MCP
> `list_tools` to inspect the full live tool catalog for your installed version.

### Core record operations

| Tool | Purpose |
|---|---|
| `odoo_search` | Search records in an allowed model using Odoo domain syntax. |
| `odoo_read` | Read selected fields from specific record IDs. |
| `odoo_search_read` | Combined search + read for efficient retrieval. |
| `odoo_create` | Create a new record in an allowed model. |
| `odoo_write` | Update existing records in an allowed model. |
| `odoo_invoke_action` | Invoke an Odoo model method such as `action_*` or `button_*`. |
| `odoo_get_record_summary` | Return a compact, human-friendly summary for a record. |

### Partners, sales, and CRM

| Tool | Purpose |
|---|---|
| `odoo_find_partner` | Find a customer or vendor by name, VAT, or email. |
| `odoo_get_partner_summary` | Get a partner overview with useful business context. |
| `odoo_find_sale_order` | Search sale orders by name, partner, or state. |
| `odoo_get_sale_order_summary` | Retrieve a sale order summary including lines. |
| `odoo_create_sale_order` | Create a quotation / sale order with product lines. |
| `odoo_confirm_sale_order` | Confirm a quotation into a sale order. |
| `odoo_create_lead` | Create a CRM lead / opportunity. |

### Accounting, purchasing, and payments

| Tool | Purpose |
|---|---|
| `odoo_create_purchase_order` | Create a purchase order from partner and line data. |
| `odoo_create_vendor_invoice` | Create a vendor bill. |
| `odoo_find_pending_invoices` | Find posted invoices or bills pending payment using Odoo 18 semantics. |
| `odoo_get_invoice_summary` | Get a detailed summary of an invoice or bill. |
| `odoo_register_payment` | Register a payment for a specific invoice. |

### Projects, activities, and chatter

| Tool | Purpose |
|---|---|
| `odoo_find_task` | Search project tasks by name, project, or stage. |
| `odoo_create_task` | Create a new project task. |
| `odoo_update_task` | Update task stage, assignee, or deadline. |
| `odoo_create_activity` | Schedule an activity on a record. |
| `odoo_list_pending_activities` | List pending activities, optionally filtered by model or assignee. |
| `odoo_mark_activity_done` | Mark an activity as completed. |
| `odoo_post_chatter_message` | Post a chatter message on a record. |
| `odoo_create_activity_summary` | Create a summary-style activity for follow-up. |
| `odoo_close_activity_with_reason` | Close an activity and record the reason. |
| `odoo_log_timesheet` | Log a timesheet entry for a project or task. |

### Support, contracts, stock, and instance capabilities

| Tool | Purpose |
|---|---|
| `odoo_get_capabilities` | Report which modules and capabilities are available in the connected instance. |
| `odoo_create_helpdesk_ticket` | Create a helpdesk ticket directly. |
| `odoo_create_helpdesk_ticket_from_partner` | Create a helpdesk ticket linked to a partner. |
| `odoo_draft_ticket_email` | Prepare a draft support email from a ticket context. |
| `odoo_create_contract_line` | Add a line to a contract. |
| `odoo_replace_contract_line` | Replace an existing contract line with a new one. |
| `odoo_close_contract_line` | Close a contract line with a reason and close date. |
| `odoo_get_product_stock` | Inspect stock quantities for a product. |
| `odoo_create_calendar_event` | Create a meeting or appointment with attendees. |

### Introspection

| Tool | Purpose |
|---|---|
| `odoo_get_model_schema` | Inspect the fields and schema of a model such as `res.partner` or `account.move`. |

## Available Resources

The server also exposes **5 MCP resources** for discovery and context:

| Resource | Purpose |
|---|---|
| `odoo://context/odoo18-fields-reference` | Odoo 18 field reference for common model/domain pitfalls such as `customer_rank`, `supplier_rank`, and `payment_state`. |
| `odoo://models` | JSON list of models currently allowed by the security policy. |
| `odoo://model/{model_name}/schema` | Technical schema for a specific Odoo model. |
| `odoo://record/{model}/{id}/summary` | JSON summary of a specific record. |
| `odoo://record/{model}/{id}/chatter_summary` | Summary of the chatter history for a specific record. |

## Guardrails and Runtime Behavior

- Uses standard Odoo JSON-RPC endpoints; it does not depend on OdooClaw delegation.
- Tool payloads are validated with Pydantic before execution.
- Model access is restricted by an allowlist defined in the server configuration.
- Sensitive write fields are denylisted and `unlink` is blocked.
- Search-style tools use default and maximum limits (`ODOO_MCP_DEFAULT_LIMIT`, `ODOO_MCP_MAX_LIMIT`).
- `sender_id` is treated as audit/context metadata; execution runs as the authenticated Odoo session user.
- Some tools require the corresponding Odoo apps/modules to be installed (CRM, Helpdesk, Projects, Contracts, Inventory, etc.).

## Security Model

The server uses standard Odoo JSON-RPC endpoints and executes operations as the
configured Odoo session user.

For production, use a dedicated least-privilege Odoo account.

## Production Notes

- This is a `stdio` MCP server, not an HTTP API service.
- Docker/Compose support is mainly for packaging or controlled runtime scenarios.
- In normal usage, your MCP client launches the server process directly.
- Keep Odoo credentials in environment variables or a secrets manager.

## Known Limitations

- One Odoo credential context per MCP process.
- `ODOO_DB` is currently required by the authentication flow.
- Some tools require specific Odoo apps/modules (CRM, Helpdesk, Project, etc.).
- Designed for Odoo 18 field semantics.

## Development

```bash
pip install -e .[dev]
ruff check src tests
black --check src tests
mypy src --ignore-missing-imports
pytest tests -v
python -m build
twine check dist/*
```

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Deployment](docs/DEPLOYMENT.md)
- [QA Runbook](docs/QA_RUNBOOK.md)

## License

MIT - see [LICENSE](LICENSE).

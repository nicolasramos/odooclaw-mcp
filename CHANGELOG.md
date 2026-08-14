# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2026-08-14

### Added
- Initial sync from OdooClaw (NRA-470): ported 43 new tools covering inventory, logistics, and purchasing domains.
- Inventory tools: `odoo_find_product`, `odoo_get_stock_availability`, `odoo_get_product_summary`, `odoo_get_product_supplier_info`, `odoo_get_stock_moves`, `odoo_find_stock_locations`, `odoo_explain_stock_forecast`, `odoo_get_location_stock_summary`, `odoo_get_lot_traceability`, `odoo_check_lot_requirements`, `odoo_apply_inventory_adjustment`, `odoo_find_inventory_discrepancies`, `odoo_find_lot_serial`, `odoo_get_replenishment_suggestions`, `odoo_validate_receipt`, `odoo_prepare_receipt_validation`.
- Logistics tools: `odoo_find_sale_deliveries`, `odoo_get_delivery_summary`, `odoo_match_delivery_to_sale_order`, `odoo_find_internal_transfers`, `odoo_prepare_internal_transfer`, `odoo_create_internal_transfer`, `odoo_get_transfer_summary`, `odoo_prepare_transfer_validation`, `odoo_validate_transfer`, `odoo_get_logistics_capabilities`.
- Purchase tools: `odoo_find_purchase_order`, `odoo_get_purchase_order_summary`, `odoo_get_purchase_receipt_status`, `odoo_get_purchase_invoice_status`, `odoo_find_purchase_receipts`, `odoo_suggest_vendor_products`, `odoo_match_vendor_bill_to_purchase_order`.
- Updated service files: `inventory_service.py` (2366 lines), `purchase_service.py` (613 lines), plus updated `accounting`, `project`, `partner`, `chatter` services.
- Updated schema layer: 40 new Pydantic schemas in `schemas/business.py` for inventory, logistics, and purchasing domains.
- Updated server imports: full parenthesized import list for `inventory_service` (37 functions).

### Changed
- Version bumped from 2.2.0 → 2.3.0 (pyproject.toml, server.json).
- Tool count: 85 → 124 MCP tools.
- README.md updated to reflect new tool count and scope.

## [2.2.0] - 2026-04-12

### Added
- Ported workforce tooling from OdooClaw into standalone server:
  - attendance/time flows (`odoo_check_in`, `odoo_check_out`, `odoo_find_attendance`, `odoo_find_missing_timesheets`, `odoo_suggest_timesheet_from_attendance`)
  - personal productivity flows (`odoo_get_my_today_summary`, `odoo_find_my_tasks`, `odoo_update_task_status`, `odoo_log_task_timesheet`, `odoo_notify_pending_actions`)
  - expense flows (`odoo_create_expense_report`, `odoo_submit_expense_report`, `odoo_approve_expense`)
- Ported advanced accounting tools:
  - bank reconciliation (`odoo_find_unreconciled_bank_lines`, `odoo_suggest_bank_reconciliation`, `odoo_reconcile_bank_line`)
  - AR/AP and close checks (`odoo_register_invoice_payment`, `odoo_get_ar_ap_aging`, `odoo_run_period_close_checks`)
  - journal and tax utilities (`odoo_create_journal_entry`, `odoo_post_journal_entry`, `odoo_get_tax_summary`)
  - bill validation/automation (`odoo_validate_vendor_bill_duplicate`, `odoo_suggest_expense_account_and_taxes`, `odoo_create_vendor_bill_from_ocr_validated`)
- Ported full view/report migration tool suite (21 tools), including scan/propose/validate/preview/test/apply/rollback/assist/visualize/batch-assist flows.
- Added new domain services:
  - `services/workforce_service.py`
  - `services/accounting_service.py`
  - `services/view_migration_service.py`

### Changed
- Expanded model allowlist to cover workforce, advanced accounting, and migration-critical models.
- Expanded schema layer (`schemas/business.py`, `schemas/__init__.py`) to include workforce, advanced accounting, and migration request models.
- Expanded server wiring (`server.py`) to expose the full migrated tool surface.
- Updated metadata/versioning to `2.2.0` and aligned package/registry descriptors with the new 85-tool surface.

### Fixed
- Updated security test expectation for allowlist denial to use a model that remains intentionally blocked after allowlist expansion.

## [2.1.0] - 2026-04-11

### Changed
- Renamed PyPI package from `odoo-mcp` to `odooclaw-mcp` (backward-compatible aliases preserved)
- Added `guard_model_access` and `audit_action` to all 9 service-calling tools (calendar, sales, CRM, inventory, HR, invoice)
- `observability/logging.py` now reads `LOG_LEVEL` environment variable instead of hardcoding `INFO`
- Fixed `sender_id` parameter bugs in `invoice_service.register_payment`, `sales_service.create_sale_order`, `sales_service.confirm_sale_order`
- Removed stale `sender_id=` kwargs from `invoice_service` call_kw calls
- `_clamp_limit` now treats `limit <= 0` as `DEFAULT_SEARCH_LIMIT` to prevent accidental full-table dumps

### Added
- Guard wiring tests verifying tools reject disallowed models
- `odooclaw-mcp` as primary CLI entry point
- Docker image published to `ghcr.io/nicolasramos/odooclaw-mcp`
- CI workflow with automated PyPI and ghcr.io publishing on tags

## [2.0.0] - 2026-04-06

### BREAKING CHANGES
- Removed dependency on custom `/odooclaw/call_kw_as_user` endpoint
- Server now works with ANY standard Odoo 18 instance without custom modules
- All RPC operations execute as the authenticated session user

### Changed
- Simplified `OdooClient.call_kw()` to use only standard Odoo JSON-RPC endpoints
- Kept `sender_id` in tool payloads as optional audit/context metadata for backward compatibility
- Updated security model documentation to reflect standard Odoo authentication
- Changed title from "Conectando Claude con Odoo" to "Conectando LLMs con Odoo"

### Removed
- Cleaned up residual dependencies (reduced from 50+ to 11 packages):
  - langchain-core, langchain-openai, langgraph
  - pandas, numpy, numpy-financial
  - openpyxl, pypdf, pdf2image, pytesseract
  - schwifty, xlrd

### Fixed
- Fixed Dockerfile to install from source instead of non-existent PyPI package
- Fixed mypy overrides to remove langchain/langgraph references
- Removed all AI assistant references from documentation

### Security
- Updated documentation to clarify that server uses standard Odoo endpoints only
- Added security best practices section for production deployments
- Emphasized need for dedicated Odoo user with minimal permissions

### Documentation
- Updated README.md to remove custom endpoint references
- Updated DEPLOYMENT.md with standard Odoo endpoint information
- Added security best practices for production use
- Updated all references to use generic "LLMs" instead of specific AI models

### Migration Guide from 1.x to 2.0.0

**If you were using version 1.x:**

1. **Update your dependencies:**
   ```bash
   pip install --upgrade odooclaw-mcp==2.0.0
   ```

2. **Remove custom Odoo modules:**
   - You no longer need the `mail_bot_odooclaw` module
   - The server now uses standard Odoo JSON-RPC endpoints

3. **Update your configuration:**
   - The same `.env` configuration works
   - Create a dedicated Odoo user with appropriate permissions

4. **No code changes needed:**
   - All MCP tools work exactly the same
   - Security is now enforced through Odoo's native ACL instead

**Benefits of upgrading:**
- Works with any standard Odoo 18 instance
- Fewer dependencies (faster install, smaller footprint)
- Simpler architecture (less to maintain)
- Better documentation
- No custom modules required

## [1.0.0] - 2026-04-03

### Added
- Initial release of Odoo MCP Server
- 6-layer architecture (Core, Security, Observability, Schemas, Tools, Services)
- 38 MCP tools for Odoo operations
- 14 domain services for business logic
- 5 dynamic MCP resources
- Native Odoo security delegation via `/odooclaw/call_kw_as_user`
- Model allowlist with 18 approved models
- Field denylist for protected fields
- Complete security guards (model access, write fields, unlink, actions)
- Structured logging and performance metrics
- Audit trail for all operations
- Data redaction for sensitive values
- Comprehensive test suite (6 test files + E2E runner)
- Full Odoo 18 compatibility (customer_rank, supplier_rank, payment_state)
- Multi-company support
- Type-safe Pydantic validation
- Documentation (README, Architecture, Deployment, QA Runbook)
- Configuration templates (.env.example, pyproject.toml)
- Development tools (pytest, black, ruff, mypy)

### Security
- Native Odoo ACL delegation
- Model allowlist enforcement
- Field-level write protection
- Complete unlink blocking
- Workflow action validation
- Sensitive data redaction
- Audit logging

### Documentation
- Comprehensive README with installation and usage
- Architecture documentation
- Deployment guide
- QA Runbook (515 lines)
- API documentation for all 38 tools
- Configuration examples

### Testing
- Unit tests for core functionality
- Integration tests for business logic
- E2E test runner with real Odoo instance
- Security tests
- Coverage reporting (>80% target)

[2.2.0]: https://github.com/nicolasramos/odooclaw-mcp/releases/tag/v2.2.0
[2.1.0]: https://github.com/nicolasramos/odooclaw-mcp/releases/tag/v2.1.0
[2.0.0]: https://github.com/nicolasramos/odooclaw-mcp/releases/tag/v2.0.0
[1.0.0]: https://github.com/nicolasramos/odooclaw-mcp/releases/tag/v1.0.0

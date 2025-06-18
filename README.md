# acounting

# Freelancer Accounting  - Planned modules

---

## 1. Core

### 1.1 Users & Roles
- [x] Users
- [x] Role-based permissions

### 1.2 Client & Contact Management
- Clients with USt-ID validation
- Prospects & leads
- Contact persons
- Tags & notes
- Document attachments
- Mahnwesen/dunning levels

### 1.3 Services & Products
- Time/unit-based items
- Default VAT per item
- Item bundles/templates
- Internal cost/profit tracking

### 1.4 Dashboard
- Financial summary (monthly/yearly/quarterly)
- Open invoices, due dates
- VAT overview
- Tax submission deadlines
- Expense vs. income chart
- Customizable widgets & alerts

---

## 2. Invoicing & Documents

### 2.1 Invoices
- Manual, recurring, time-tracked
- Standard, pro forma, Abschlags-/Schlussrechnung
- Credit notes, partial refunds
- Reverse charge & OSS/MOSS
- Multi-language/currency
- Smart invoice numbering
- QR code (GiroCode/EPC for mobile banking)
- Payment links (Stripe, PayPal, SEPA)
- Invoice attachments (e.g. timesheets)
- Auto-PDF archive (GoBD-compliant)
- Cancellation texts & terms

### 2.2 Quotes & Offers
- Convert to invoice
- Optional line items
- Validity period
- Digital client approval

### 2.3 Credit Notes
- Partial or full
- Linked to invoice
- Track refund status

### 2.4 Delivery Notes / Purchase Orders
- Optional
- Signable PDFs
- Reference numbers

### 2.5 E-Invoicing
- ZUGFeRD (1.0/2.1), XRechnung
- Peppol-compatible
- PDF with embedded XML
- Email + network sending

### 2.6 Dunning & Reminders
- Configurable auto-reminders
- Customizable email templates
- Reminder schedule (3/7/14+ days)
- Mahnung levels (1st, 2nd, 3rd)
- Fee/interest escalation
- Auto-generate Mahnung documents
- Track dunning status

---

## 3. Expenses & Purchasing

### 3.1 Expense Management
- Manual/recurring
- Upload receipts (OCR support)
- SKR 03/04 categories
- Deductible toggle
- Multi-VAT per expense
- Split expenses

### 3.2 Supplier Management
- Contacts, tags
- Attach contracts/invoices
- Track payables

### 3.3 Travel & Mileage
- Trip categories (transport, meals, lodging)
- Mileage logs (km-based)
- Reimbursable flag

---

## 4. Settings & Customization

### 4.1 Templates & Branding
- Document templates (header/logo/colors)
- Email templates
- Invoice number schemes (global/per client)

### 4.2 Automations
- Recurring invoices/expenses
- Payment reminders
- Deadline tasks
- Smart invoice suggestions (Maybe)

### 4.3 Import/Export
- CSV/JSON imports (clients, expenses)
- Export full data archive

### 4.4 Reports and analytics
- Profit & Loss
- Expense breakdown by category
- Revenue by client/service
- Cashflow forecast
- VAT liability report
- Audit trail & change logs

---

## 5. Tax & Compliance

### 5.1 VAT Management
- Standard, reduced, 0%, exempt
- Reverse charge (domestic/EU)
- OSS/MOSS
- Kleinunternehmerregelung (UStG §19)
- Mixed VAT invoices

### 5.2 VAT & Tax Reports
- Umsatzsteuervoranmeldung (UStVA)
- XML export for Elster or API submission
- VAT summary per quarter/month
- Einnahmenüberschussrechnung (EUR)
- Jahresumsatzsteuererklärung
- GoBD export with hash log

### 5.3 Tax Consultant Support
- DATEV exports (CSV/XML)
- Lock periods
- Audit mode access log

---

## 6. Banking & Payments

### 6.1 Bank Integration
- PSD2-compliant sync (e.g. FinAPI, Tink)
- Manual transactions
- Multi-account support
- Rule-based auto-categorization

### 6.2 Reconciliation
- Auto-match to invoices/expenses
- Partial payment support
- Manual override & suggestions

### 6.3 Payment Providers
- PayPal, Klarna
- Track gross, net, fees
- Auto-reconciliation of payouts

### 6.4 SEPA Tools
- SEPA XML generation
- IBAN/BIC validation
- Batch payments

---

### 7. Maybe
- Multi-language UI (EN, DE)
- Multi-currency with conversion (EUR, USD, CHF)

---
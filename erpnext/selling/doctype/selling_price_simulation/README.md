# Selling Price Simulation

## Overview

The Selling Price Simulation feature allows electronics components distributors to:

1. **Collect Supplier Offers**: Input multiple supplier quotations for the same component
2. **Cost Analysis**: Automatically calculate lowest, average, and maximum costs
3. **Price Suggestion**: Generate selling price suggestions based on cost analysis, market prices, and customer target prices
4. **Multi-Company Support**: Handle USD buying (Hong Kong company) and CNY selling (China company) with VAT
5. **Approval Workflow**: Require manager approval before creating quotations
6. **Quotation Generation**: Create sales quotations from approved price simulations

## Key Features

### Cost Analysis
- Automatically calculates lowest, average, and maximum costs from supplier offers
- Supports multiple suppliers for the same component
- Tracks supplier quotation references and validity periods

### Multi-Company Pricing
- Hong Kong company: Buying in USD from overseas suppliers
- China company: Selling in CNY with 13% VAT calculation
- Automatic currency conversion using exchange rates
- Gross profit margin calculation

### Approval Workflow
- Draft → Pending Approval → Approved/Rejected workflow
- Integration with ERPNext Authorization Control
- Role-based approval permissions (Sales Manager, System Manager)

### Integration
- Creates quotations from approved simulations
- Links to existing Item and Supplier masters
- Integrates with ERPNext pricing and quotation systems

## Usage

1. **Create New Simulation**
   - Go to Selling > Selling Price Simulation
   - Select item and company
   - Add supplier offers with prices in USD
   - Enter market price and customer target price (optional)

2. **Review Calculations**
   - System automatically calculates cost analysis
   - Reviews suggested selling price with VAT and margins
   - Check gross profit margin percentage

3. **Submit for Approval**
   - Click "Submit for Approval" button
   - Manager receives notification for approval

4. **Approval Process**
   - Sales Manager can approve or reject
   - System tracks approval date and user

5. **Create Quotation**
   - From approved simulation, click "Make Quotation"
   - System creates quotation with suggested selling price

## Configuration

### Companies Setup
- Hong Kong company with USD as default currency
- China company with CNY as default currency
- Currency exchange rates between USD and CNY

### Authorization Rules
- Sales Manager role for standard approvals
- System Manager role for high-value approvals
- Configurable approval limits

### VAT Configuration
- Default 13% VAT rate for China company
- Configurable VAT rates per simulation

## Reports

### Selling Price Simulation Summary
- Overview of all simulations with status
- Filter by company, status, item code
- Shows cost analysis and profit margins
- Export capabilities for analysis

## API

### Key Methods
- `submit_for_approval()`: Submit simulation for manager approval
- `approve_simulation()`: Approve pending simulation
- `reject_simulation()`: Reject pending simulation
- `make_quotation()`: Create quotation from approved simulation

### Webhooks
- Status change notifications
- Approval workflow events
- Integration with external systems

## Testing

Run the test suite:
```bash
bench run-tests --app erpnext --module erpnext.selling.doctype.selling_price_simulation
```

## Support

For issues and feature requests, please refer to the ERPNext documentation or contact your system administrator.

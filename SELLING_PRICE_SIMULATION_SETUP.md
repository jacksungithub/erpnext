# Selling Price Simulation Setup Guide

## Overview
This guide helps you set up and test the new Selling Price Simulation functionality in ERPNext.

## Installation Steps

### 1. Database Migration
Run the following commands to install the new doctypes:

```bash
cd /home/ubuntu/erpnext
bench migrate
```

### 2. Build Assets
Build the frontend assets:

```bash
bench build
```

### 3. Restart Services
Restart the ERPNext services:

```bash
bench restart
```

### 4. Setup Test Data (Optional)
To create sample data for testing:

```bash
bench execute erpnext.selling.doctype.selling_price_simulation.setup_test_data.setup_test_data
```

## Testing the Functionality

### 1. Access the Feature
- Go to ERPNext
- Navigate to Selling workspace
- Click on "Selling Price Simulation"

### 2. Create a New Simulation
1. Click "New"
2. Select an item (e.g., ELEC-COMP-001 if you ran test data setup)
3. Select company (Hong Kong Electronics Ltd for buying)
4. Add supplier offers with different USD prices
5. Enter market price and customer target price (optional)
6. Save the document

### 3. Test Cost Analysis
- Verify that lowest, average, and maximum costs are calculated automatically
- Check that suggested selling price is calculated with VAT and margins

### 4. Test Approval Workflow
1. Click "Submit for Approval"
2. Login as a user with Sales Manager role
3. Approve or reject the simulation

### 5. Test Quotation Creation
1. From an approved simulation
2. Click "Make Quotation"
3. Verify quotation is created with correct pricing

## Key Features to Test

### Multi-Company Support
- Hong Kong company: USD buying from overseas suppliers
- China company: CNY selling with 13% VAT calculation
- Currency conversion between USD and CNY

### Cost Analysis
- Automatic calculation of lowest, average, maximum costs
- Multiple supplier price comparison
- Gross profit margin calculation

### Approval Workflow
- Draft → Pending Approval → Approved/Rejected
- Role-based permissions (Sales Manager approval)
- Authorization control integration

### Integration
- Creates quotations from approved simulations
- Links to existing Item and Supplier masters
- Follows ERPNext pricing patterns

## Troubleshooting

### Common Issues
1. **Migration fails**: Check database permissions and ERPNext version compatibility
2. **Assets not loading**: Run `bench build` and clear browser cache
3. **Permission errors**: Ensure user has Sales User or Sales Manager role
4. **Currency conversion fails**: Check that USD and CNY currencies exist and exchange rates are set

### Support
- Check the README.md in the selling_price_simulation doctype folder
- Review test files for expected behavior
- Check ERPNext logs for detailed error messages

## Next Steps
After successful testing:
1. Configure authorization rules for your approval workflow
2. Set up your actual companies and currencies
3. Import your items and suppliers
4. Train users on the new workflow

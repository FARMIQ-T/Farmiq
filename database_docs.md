# Farm IQ Database Documentation

## Overview

Farm IQ uses Supabase as its primary database. The database schema includes tables for:

1. Farmers (profile information)
2. Farms (farm details)
3. Crops (crop planning and history)
4. Financial Records
5. Resources (inventory, equipment)
6. Credit Scores
7. Loans

## Setup Instructions

1. Create a new project in Supabase

2. Copy your project URL and keys to `.env` file:
   ```
   SUPABASE_URL='your-project-url'
   SUPABASE_KEY='your-anon-key'
   SUPABASE_SERVICE_KEY='your-service-role-key'
   ```

3. Run the SQL schema file:
   - Go to Supabase Dashboard > SQL Editor
   - Copy contents of `schema.sql`
   - Run the SQL commands

## Database Structure

### Farmers Table
- Personal information
- Contact details
- Farming experience
- Training history

### Farms Table
- Farm characteristics
- Location
- Soil information
- Irrigation details

### Crops Table
- Crop planning
- Planting/harvest dates
- Yield tracking
- Season information

### Financial Records Table
- Income/expense tracking
- Transaction history
- Payment methods
- Related crop information

### Resources Table
- Inventory management
- Equipment tracking
- Resource status
- Valuation

### Credit Scores Table
- Credit risk assessment
- Score history
- Risk factors
- Credit limits

### Loans Table
- Loan management
- Repayment tracking
- Interest rates
- Status monitoring

## API Usage

The database service (`database_service.py`) provides methods for all common operations:

```python
# Example usage:
db = DatabaseService(url, key)

# Create a farmer profile
farmer = await db.create_farmer({
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "location": "Rural County"
})

# Get farmer's farms
farms = await db.get_farms_by_farmer(farmer["id"])

# Create a new credit score
score = await db.create_credit_score({
    "farmer_id": farmer["id"],
    "score": 0.85,
    "score_date": "2025-10-31"
})
```
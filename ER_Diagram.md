# Blood Donation App - Entity Relationship Diagram

## Database Schema Overview

The blood donation app uses a relational database with the following entities and relationships:

## 📊 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    USER                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ PK: id (AutoField)                                                                │
│     name (CharField, max_length=100)                                              │
│     age (IntegerField)                                                            │
│     gender (CharField, choices: Male/Female)                                      │
│     email (EmailField, unique=True)                                               │
│     phone (CharField, max_length=15)                                              │
│     city (CharField, max_length=50)                                               │
│     district (CharField, choices: 14 Kerala districts)                            │
│     taluk (CharField, choices: 75+ Kerala taluks)                                │
│     photo (FileField, upload_to='photos/')                                        │
│     blood_group (CharField, choices: A+, A-, B+, B-, O+, O-, AB+, AB-)           │
│     willing_to_donate (BooleanField, default=True)                                │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 1
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              EMERGENCY_CONTACT                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ PK: id (AutoField)                                                                │
│ FK: user (ForeignKey → User)                                                      │
│     name (CharField, max_length=100)                                              │
│     relationship (CharField, max_length=50)                                       │
│     phone (CharField, max_length=15)                                              │
│     email (EmailField, blank=True, null=True)                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                BLOOD_REQUEST                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ PK: id (AutoField)                                                                │
│ FK: requester (ForeignKey → User)                                                 │
│     blood_group (CharField, choices: A+, A-, B+, B-, O+, O-, AB+, AB-)           │
│     hospital_name (CharField, max_length=100)                                     │
│     required_date (DateField)                                                     │
│     status (CharField, max_length=20, default='Pending')                          │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                               BLOOD_DONATION                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ PK: id (AutoField)                                                                │
│ FK: donor (ForeignKey → User)                                                     │
│     donation_date (DateField, default=timezone.now)                               │
│     hospital_name (CharField, max_length=100)                                     │
│     blood_group (CharField, choices: A+, A-, B+, B-, O+, O-, AB+, AB-)           │
│     units_donated (PositiveIntegerField, default=1)                               │
│     notes (TextField, blank=True, null=True)                                      │
│     created_at (DateTimeField, auto_now_add=True)                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                               BLOOD_INVENTORY                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ PK: id (AutoField)                                                                │
│     blood_group (CharField, choices: A+, A-, B+, B-, O+, O-, AB+, AB-, unique=True)│
│     available_units (PositiveIntegerField, default=0)                             │
│     critical_level (PositiveIntegerField, default=10)                             │
│     last_updated (DateTimeField, auto_now=True)                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔗 Relationship Details

### 1. User → EmergencyContact (1:N)
- **Relationship**: One user can have multiple emergency contacts
- **Cardinality**: 1:N (One-to-Many)
- **Foreign Key**: `EmergencyContact.user` references `User.id`
- **Cascade**: If user is deleted, all emergency contacts are deleted

### 2. User → BloodRequest (1:N)
- **Relationship**: One user can make multiple blood requests
- **Cardinality**: 1:N (One-to-Many)
- **Foreign Key**: `BloodRequest.requester` references `User.id`
- **Cascade**: If user is deleted, all blood requests are deleted

### 3. User → BloodDonation (1:N)
- **Relationship**: One user can make multiple blood donations
- **Cardinality**: 1:N (One-to-Many)
- **Foreign Key**: `BloodDonation.donor` references `User.id`
- **Cascade**: If user is deleted, all blood donations are deleted

### 4. BloodDonation → BloodInventory (N:1)
- **Relationship**: Multiple donations contribute to inventory levels
- **Cardinality**: N:1 (Many-to-One)
- **Logic**: When donation is recorded, corresponding inventory is updated
- **Business Rule**: Inventory is automatically maintained based on donations

## 📋 Database Constraints

### Primary Keys
- All entities have auto-incrementing integer primary keys
- Ensures unique identification of each record

### Foreign Keys
- **User.id** is referenced by multiple entities
- Cascade deletion ensures referential integrity
- No orphaned records in related tables

### Unique Constraints
- **User.email**: Each email can only be registered once
- **BloodInventory.blood_group**: Only one inventory record per blood group

### Check Constraints
- **User.age**: Must be between 18-100 (enforced in forms)
- **User.gender**: Must be either 'Male' or 'Female'
- **User.blood_group**: Must be one of 8 valid blood groups
- **User.district**: Must be one of 14 Kerala districts
- **User.taluk**: Must be one of 75+ Kerala taluks

## 🗂️ Data Dictionary

### User Entity
- **Purpose**: Store donor and recipient information
- **Key Fields**: email (unique identifier), blood_group, willing_to_donate
- **Geographic Fields**: city, district, taluk for location-based searches
- **Media**: photo field for profile pictures

### EmergencyContact Entity
- **Purpose**: Store emergency contact information for users
- **Relationships**: Linked to specific users
- **Usage**: Contact information for emergency situations

### BloodRequest Entity
- **Purpose**: Track blood requests from recipients
- **Status Tracking**: Pending → Approved/Rejected → Fulfilled
- **Business Logic**: Triggers notifications to matching donors

### BloodDonation Entity
- **Purpose**: Record actual blood donations
- **Inventory Impact**: Automatically updates blood inventory
- **Audit Trail**: Includes creation timestamp and notes

### BloodInventory Entity
- **Purpose**: Track available blood units by blood group
- **Critical Levels**: Alert system for low inventory
- **Real-time Updates**: Updated whenever donations are recorded

## 🔄 Data Flow

1. **User Registration** → Creates User record
2. **Emergency Contacts** → Added to EmergencyContact table
3. **Blood Requests** → Creates BloodRequest record
4. **Donations** → Creates BloodDonation record + updates BloodInventory
5. **Inventory Management** → Hospital staff can manually adjust levels
6. **Search & Matching** → Queries across User table with filters
7. **Reporting** → Aggregates data from all tables for statistics

## 🎯 Business Rules

- Users must be 18+ to register
- Each blood group can only have one inventory record
- Donations automatically update inventory levels
- Critical level alerts when inventory drops below threshold
- Geographic filtering based on Kerala administrative divisions
- Email notifications for blood requests and donor matching

## 🚀 Scalability Considerations

- **Indexing**: Primary keys and foreign keys are automatically indexed
- **Normalization**: Proper 3NF design prevents data redundancy
- **Flexibility**: Easy to add new blood groups or geographic areas
- **Performance**: Efficient queries with proper foreign key relationships
- **Extensibility**: Structure supports future features like blood testing results

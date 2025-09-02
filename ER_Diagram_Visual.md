# Blood Donation App - Visual ER Diagram

## 🎨 Visual Entity Relationship Diagram

```
                    ┌─────────────────────────────────────────────────────────────┐
                    │                        USER                                │
                    │  ┌─────────────────────────────────────────────────────┐   │
                    │  │ PK: id (AutoField)                                │   │
                    │  │     name (CharField, max_length=100)              │   │
                    │  │     age (IntegerField, 18-100)                    │   │
                    │  │     gender (Male/Female)                          │   │
                    │  │     email (EmailField, unique=True)               │   │
                    │  │     phone (CharField, max_length=15)              │   │
                    │  │     city (CharField, max_length=50)               │   │
                    │  │     district (14 Kerala districts)                │   │
                    │  │     taluk (75+ Kerala taluks)                     │   │
                    │  │     photo (FileField, upload_to='photos/')        │   │
                    │  │     blood_group (8 blood types)                   │   │
                    │  │     willing_to_donate (BooleanField, default=True)│   │
                    │  └─────────────────────────────────────────────────────┘   │
                    └─────────────────────────────────────────────────────────────┘
                                    │
                                    │ 1
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                   EMERGENCY_CONTACT                        │
                    │  ┌─────────────────────────────────────────────────────┐   │
                    │  │ PK: id (AutoField)                                │   │
                    │  │ FK: user → User.id                                │   │
                    │  │     name (CharField, max_length=100)              │   │
                    │  │     relationship (CharField, max_length=50)        │   │
                    │  │     phone (CharField, max_length=15)              │   │
                    │  │     email (EmailField, optional)                  │   │
                    │  └─────────────────────────────────────────────────────┘   │
                    └─────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────────────────────────────┐
                    │                     BLOOD_REQUEST                          │
                    │  ┌─────────────────────────────────────────────────────┐   │
                    │  │ PK: id (AutoField)                                │   │
                    │  │ FK: requester → User.id                           │   │
                    │  │     blood_group (8 blood types)                   │   │
                    │  │     hospital_name (CharField, max_length=100)     │   │
                    │  │     required_date (DateField)                     │   │
                    │  │     status (Pending/Approved/Rejected/Fulfilled)  │   │
                    │  └─────────────────────────────────────────────────────┘   │
                    └─────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────────────────────────────┐
                    │                    BLOOD_DONATION                          │
                    │  ┌─────────────────────────────────────────────────────┐   │
                    │  │ PK: id (AutoField)                                │   │
                    │  │ FK: donor → User.id                               │   │
                    │  │     donation_date (DateField, default=now)        │   │
                    │  │     hospital_name (CharField, max_length=100)     │   │
                    │  │     blood_group (8 blood types)                   │   │
                    │  │     units_donated (PositiveIntegerField, 1-5)     │   │
                    │  │     notes (TextField, optional)                   │   │
                    │  │     created_at (DateTimeField, auto_now_add)      │   │
                    │  └─────────────────────────────────────────────────────┘   │
                    │                           │                              │
                    │                           │ N                            │
                    │                           ▼                              │
                    └───────────────────────────┼──────────────────────────────┘
                                                │
                                                │ 1
                                                ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                   BLOOD_INVENTORY                          │
                    │  ┌─────────────────────────────────────────────────────┐   │
                    │  │ PK: id (AutoField)                                │   │
                    │  │     blood_group (8 blood types, unique=True)      │   │
                    │  │     available_units (PositiveIntegerField)        │   │
                    │  │     critical_level (PositiveIntegerField, default=10)│   │
                    │  │     last_updated (DateTimeField, auto_now)        │   │
                    │  └─────────────────────────────────────────────────────┘   │
                    └─────────────────────────────────────────────────────────────┘
```

## 🔗 Relationship Mapping

```
USER (1) ──────── (N) EMERGENCY_CONTACT
  │                        │
  │                        │ FK: user → User.id
  │                        │ Cascade: DELETE
  │
  │ (1) ──────── (N) BLOOD_REQUEST
  │                        │
  │                        │ FK: requester → User.id
  │                        │ Cascade: DELETE
  │
  │ (1) ──────── (N) BLOOD_DONATION
  │                        │
  │                        │ FK: donor → User.id
  │                        │ Cascade: DELETE
  │                        │
  │                        │ (N) ──────── (1) BLOOD_INVENTORY
  │                        │                    │
  │                        │                    │ Business Logic:
  │                        │                    │ Auto-update inventory
  │                        │                    │ when donation recorded
  │                        │                    │
  │                        │                    │ FK: blood_group (indirect)
  │                        │                    │ via blood_group field
```

## 📊 Cardinality Summary

| Entity 1 | Relationship | Entity 2 | Cardinality | Foreign Key |
|----------|-------------|----------|-------------|-------------|
| USER | has | EMERGENCY_CONTACT | 1:N | EmergencyContact.user |
| USER | makes | BLOOD_REQUEST | 1:N | BloodRequest.requester |
| USER | donates | BLOOD_DONATION | 1:N | BloodDonation.donor |
| BLOOD_DONATION | updates | BLOOD_INVENTORY | N:1 | blood_group (indirect) |

## 🎯 Key Design Principles

1. **Centralized User Management**: All user-related data stems from the USER entity
2. **Referential Integrity**: Foreign keys with cascade deletion prevent orphaned records
3. **Normalized Structure**: 3NF design eliminates data redundancy
4. **Business Logic Integration**: Automatic inventory updates maintain data consistency
5. **Geographic Hierarchy**: District → Taluk structure supports location-based searches
6. **Audit Trail**: Timestamps and creation tracking for all transactions
7. **Flexible Status Management**: Request status workflow supports business processes

## 🔄 Data Flow Diagram

```
User Registration → User Table
        ↓
Emergency Contacts → EmergencyContact Table
        ↓
Blood Requests → BloodRequest Table → Email Notifications
        ↓
Blood Donations → BloodDonation Table → BloodInventory Update
        ↓
Inventory Management → Critical Level Alerts
        ↓
Search & Matching → Geographic + Blood Group Filtering
        ↓
Reporting → Statistics & Analytics
```

## 🚀 Database Schema Benefits

- **Scalability**: Easy to add new blood groups, districts, or taluks
- **Performance**: Proper indexing on primary and foreign keys
- **Maintainability**: Clear separation of concerns between entities
- **Extensibility**: Structure supports future features (blood testing, compatibility)
- **Data Integrity**: Constraints and business rules ensure data quality
- **Reporting**: Efficient aggregation and analysis capabilities

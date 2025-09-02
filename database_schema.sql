-- Blood Donation App - Database Schema
-- Generated from Django models

-- =====================================================
-- USER TABLE - Central entity for all users
-- =====================================================
CREATE TABLE blood_app_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 100),
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female')),
    email VARCHAR(254) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL CHECK (district IN (
        'Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha',
        'Kottayam', 'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad',
        'Malappuram', 'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod'
    )),
    taluk VARCHAR(50) NOT NULL CHECK (taluk IN (
        -- Thiruvananthapuram
        'Thiruvananthapuram', 'Nedumangadu', 'Chirayinkeezhu', 'Kattakada', 'Neyyattinkara', 'Varkala',
        -- Kollam
        'Kollam', 'Kunnathur', 'Karunagappally', 'Kottarakkara', 'Pathanapuram', 'Punalur',
        -- Pathanamthitta
        'Adoor', 'Konni', 'Kozhencherry', 'Ranni', 'Thiruvalla', 'Mallappally',
        -- Alappuzha
        'Cherthala', 'Ambalappuzha', 'Kuttanad', 'Karthikappally', 'Chengannur', 'Mavelikkara',
        -- Kottayam
        'Changanasserry', 'Kottayam', 'Vaikom', 'Meenachil', 'Kanjirappally',
        -- Idukki
        'Devikulam', 'Peermade', 'Thodupuzha', 'Udumbanchola',
        -- Ernakulam
        'Aluva', 'Kanayannur', 'Kochi', 'Kothamangalam', 'Kunnathunad', 'Muvattupuzha', 'North Paravur',
        -- Thrissur
        'Thrissur', 'Chavakkad', 'Kodungallur', 'Mukundapuram', 'Kunnamkulam', 'Thalapilly',
        -- Palakkad
        'Palakkad', 'Alathur', 'Chittur', 'Mannarkkad', 'Pattambi', 'Ottappalam', 'Attappady',
        -- Malappuram
        'Perinthalmanna', 'Nilambur', 'Eranad', 'Kondotty', 'Tirur', 'Tirurangadi', 'Ponnani',
        -- Kozhikode
        'Kozhikode', 'Koyilandy', 'Vadakara', 'Thamarassery',
        -- Wayanad
        'Mananthavady', 'Vythiri', 'Sulthan Bathery',
        -- Kannur
        'Kannur', 'Thalassery', 'Taliparamba', 'Iritty', 'Payyanur',
        -- Kasaragod
        'Kasaragod', 'Hosdurg'
    )),
    photo VARCHAR(100) NULL,
    blood_group VARCHAR(5) NOT NULL CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')),
    willing_to_donate BOOLEAN NOT NULL DEFAULT 1
);

-- =====================================================
-- EMERGENCY_CONTACT TABLE - Emergency contacts for users
-- =====================================================
CREATE TABLE blood_app_emergencycontact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(254) NULL,
    FOREIGN KEY (user_id) REFERENCES blood_app_user(id) ON DELETE CASCADE
);

-- =====================================================
-- BLOOD_REQUEST TABLE - Blood requests from recipients
-- =====================================================
CREATE TABLE blood_app_bloodrequest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_id INTEGER NOT NULL,
    blood_group VARCHAR(5) NOT NULL CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')),
    hospital_name VARCHAR(100) NOT NULL,
    required_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Fulfilled')),
    FOREIGN KEY (requester_id) REFERENCES blood_app_user(id) ON DELETE CASCADE
);

-- =====================================================
-- BLOOD_DONATION TABLE - Actual blood donations
-- =====================================================
CREATE TABLE blood_app_blooddonation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER NOT NULL,
    donation_date DATE NOT NULL DEFAULT CURRENT_DATE,
    hospital_name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(5) NOT NULL CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')),
    units_donated INTEGER NOT NULL DEFAULT 1 CHECK (units_donated >= 1 AND units_donated <= 5),
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES blood_app_user(id) ON DELETE CASCADE
);

-- =====================================================
-- BLOOD_INVENTORY TABLE - Blood inventory tracking
-- =====================================================
CREATE TABLE blood_app_bloodinventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blood_group VARCHAR(5) UNIQUE NOT NULL CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')),
    available_units INTEGER NOT NULL DEFAULT 0 CHECK (available_units >= 0),
    critical_level INTEGER NOT NULL DEFAULT 10 CHECK (critical_level >= 1),
    last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- User table indexes
CREATE INDEX idx_user_email ON blood_app_user(email);
CREATE INDEX idx_user_blood_group ON blood_app_user(blood_group);
CREATE INDEX idx_user_district ON blood_app_user(district);
CREATE INDEX idx_user_taluk ON blood_app_user(taluk);
CREATE INDEX idx_user_willing_to_donate ON blood_app_user(willing_to_donate);
CREATE INDEX idx_user_age ON blood_app_user(age);

-- Emergency contact indexes
CREATE INDEX idx_emergency_contact_user ON blood_app_emergencycontact(user_id);

-- Blood request indexes
CREATE INDEX idx_blood_request_requester ON blood_app_bloodrequest(requester_id);
CREATE INDEX idx_blood_request_blood_group ON blood_app_bloodrequest(blood_group);
CREATE INDEX idx_blood_request_status ON blood_app_bloodrequest(status);
CREATE INDEX idx_blood_request_date ON blood_app_bloodrequest(required_date);

-- Blood donation indexes
CREATE INDEX idx_blood_donation_donor ON blood_app_blooddonation(donor_id);
CREATE INDEX idx_blood_donation_date ON blood_app_blooddonation(donation_date);
CREATE INDEX idx_blood_donation_blood_group ON blood_app_blooddonation(blood_group);
CREATE INDEX idx_blood_donation_created ON blood_app_blooddonation(created_at);

-- Blood inventory indexes
CREATE INDEX idx_blood_inventory_blood_group ON blood_app_bloodinventory(blood_group);
CREATE INDEX idx_blood_inventory_critical ON blood_app_bloodinventory(available_units, critical_level);

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert sample blood inventory
INSERT INTO blood_app_bloodinventory (blood_group, available_units, critical_level) VALUES
('A+', 25, 10),
('A-', 8, 10),
('B+', 30, 10),
('B-', 12, 10),
('O+', 45, 10),
('O-', 15, 10),
('AB+', 5, 10),
('AB-', 3, 10);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- View for available donors
CREATE VIEW v_available_donors AS
SELECT 
    u.id, u.name, u.age, u.gender, u.blood_group, u.city, u.district, u.taluk,
    u.phone, u.email, u.willing_to_donate,
    COUNT(d.id) as total_donations,
    MAX(d.donation_date) as last_donation_date
FROM blood_app_user u
LEFT JOIN blood_app_blooddonation d ON u.id = d.donor_id
WHERE u.willing_to_donate = 1
GROUP BY u.id, u.name, u.age, u.gender, u.blood_group, u.city, u.district, u.taluk, u.phone, u.email, u.willing_to_donate;

-- View for critical blood inventory
CREATE VIEW v_critical_inventory AS
SELECT 
    blood_group,
    available_units,
    critical_level,
    CASE 
        WHEN available_units = 0 THEN 'CRITICAL - NO UNITS'
        WHEN available_units <= critical_level THEN 'CRITICAL - LOW STOCK'
        ELSE 'SUFFICIENT'
    END as status,
    last_updated
FROM blood_app_bloodinventory
WHERE available_units <= critical_level
ORDER BY available_units ASC;

-- View for donation statistics
CREATE VIEW v_donation_stats AS
SELECT 
    blood_group,
    COUNT(*) as total_donations,
    SUM(units_donated) as total_units,
    AVG(units_donated) as avg_units_per_donation,
    MIN(donation_date) as first_donation,
    MAX(donation_date) as last_donation
FROM blood_app_blooddonation
GROUP BY blood_group
ORDER BY total_units DESC;

-- =====================================================
-- TRIGGERS FOR BUSINESS LOGIC
-- =====================================================

-- Trigger to update blood inventory when donation is recorded
CREATE TRIGGER tr_update_inventory_after_donation
AFTER INSERT ON blood_app_blooddonation
BEGIN
    UPDATE blood_app_bloodinventory 
    SET available_units = available_units + NEW.units_donated,
        last_updated = CURRENT_TIMESTAMP
    WHERE blood_group = NEW.blood_group;
    
    -- Insert new inventory record if blood group doesn't exist
    INSERT OR IGNORE INTO blood_app_bloodinventory (blood_group, available_units, critical_level)
    VALUES (NEW.blood_group, NEW.units_donated, 10);
END;

-- =====================================================
-- CONSTRAINTS AND VALIDATIONS
-- =====================================================

-- Ensure district and taluk combinations are valid
-- This would require a more complex constraint in production
-- For now, the CHECK constraints in the table definitions handle this

-- =====================================================
-- COMMENTS AND DOCUMENTATION
-- =====================================================

-- Table: blood_app_user
-- Purpose: Central user management for donors and recipients
-- Key Features: Geographic location, blood group, donation willingness

-- Table: blood_app_emergencycontact  
-- Purpose: Emergency contact information for users
-- Key Features: Multiple contacts per user, relationship tracking

-- Table: blood_app_bloodrequest
-- Purpose: Blood requests from recipients
-- Key Features: Status tracking, hospital information, date requirements

-- Table: blood_app_blooddonation
-- Purpose: Record actual blood donations
-- Key Features: Unit tracking, hospital information, audit trail

-- Table: blood_app_bloodinventory
-- Purpose: Real-time blood inventory management
-- Key Features: Critical level alerts, automatic updates

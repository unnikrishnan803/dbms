from django.db import models
from django.utils import timezone


class User(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    
    # Kerala Districts and Taluks
    DISTRICT_CHOICES = [
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Kollam', 'Kollam'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Alappuzha', 'Alappuzha'),
        ('Kottayam', 'Kottayam'),
        ('Idukki', 'Idukki'),
        ('Ernakulam', 'Ernakulam'),
        ('Thrissur', 'Thrissur'),
        ('Palakkad', 'Palakkad'),
        ('Malappuram', 'Malappuram'),
        ('Kozhikode', 'Kozhikode'),
        ('Wayanad', 'Wayanad'),
        ('Kannur', 'Kannur'),
        ('Kasaragod', 'Kasaragod'),
    ]
    
    TALUK_CHOICES = [
        # Thiruvananthapuram
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Nedumangadu', 'Nedumangadu'),
        ('Chirayinkeezhu', 'Chirayinkeezhu'),
        ('Kattakada', 'Kattakada'),
        ('Neyyattinkara', 'Neyyattinkara'),
        ('Varkala', 'Varkala'),
        
        # Kollam
        ('Kollam', 'Kollam'),
        ('Kunnathur', 'Kunnathur'),
        ('Karunagappally', 'Karunagappally'),
        ('Kottarakkara', 'Kottarakkara'),
        ('Pathanapuram', 'Pathanapuram'),
        ('Punalur', 'Punalur'),
        
        # Pathanamthitta
        ('Adoor', 'Adoor'),
        ('Konni', 'Konni'),
        ('Kozhencherry', 'Kozhencherry'),
        ('Ranni', 'Ranni'),
        ('Thiruvalla', 'Thiruvalla'),
        ('Mallappally', 'Mallappally'),
        
        # Alappuzha
        ('Cherthala', 'Cherthala'),
        ('Ambalappuzha', 'Ambalappuzha'),
        ('Kuttanad', 'Kuttanad'),
        ('Karthikappally', 'Karthikappally'),
        ('Chengannur', 'Chengannur'),
        ('Mavelikkara', 'Mavelikkara'),
        
        # Kottayam
        ('Changanasserry', 'Changanasserry'),
        ('Kottayam', 'Kottayam'),
        ('Vaikom', 'Vaikom'),
        ('Meenachil', 'Meenachil (Palai)'),
        ('Kanjirappally', 'Kanjirappally'),
        
        # Idukki
        ('Devikulam', 'Devikulam'),
        ('Peermade', 'Peermade'),
        ('Thodupuzha', 'Thodupuzha'),
        ('Udumbanchola', 'Udumbanchola'),
        
        # Ernakulam
        ('Aluva', 'Aluva'),
        ('Kanayannur', 'Kanayannur (Eranakulam)'),
        ('Kochi', 'Kochi (Fort Kochi)'),
        ('Kothamangalam', 'Kothamangalam'),
        ('Kunnathunad', 'Kunnathunad (Perumbavoor)'),
        ('Muvattupuzha', 'Muvattupuzha'),
        ('North Paravur', 'North Paravur'),
        
        # Thrissur
        ('Thrissur', 'Thrissur'),
        ('Chavakkad', 'Chavakkad'),
        ('Kodungallur', 'Kodungallur'),
        ('Mukundapuram', 'Mukundapuram (Irinjalakuda)'),
        ('Kunnamkulam', 'Kunnamkulam'),
        ('Thalapilly', 'Thalapilly (Wadakkancheri)'),
        
        # Palakkad
        ('Palakkad', 'Palakkad'),
        ('Alathur', 'Alathur'),
        ('Chittur', 'Chittur'),
        ('Mannarkkad', 'Mannarkkad'),
        ('Pattambi', 'Pattambi'),
        ('Ottappalam', 'Ottappalam'),
        ('Attappady', 'Attappady (Agali)'),
        
        # Malappuram
        ('Perinthalmanna', 'Perinthalmanna'),
        ('Nilambur', 'Nilambur'),
        ('Eranad', 'Eranad (Manjeri)'),
        ('Kondotty', 'Kondotty'),
        ('Tirur', 'Tirur'),
        ('Tirurangadi', 'Tirurangadi'),
        ('Ponnani', 'Ponnani'),
        
        # Kozhikode
        ('Kozhikode', 'Kozhikode'),
        ('Koyilandy', 'Koyilandy'),
        ('Vadakara', 'Vadakara'),
        ('Thamarassery', 'Thamarassery'),
        
        # Wayanad
        ('Mananthavady', 'Mananthavady'),
        ('Vythiri', 'Vythiri (Kalpetta)'),
        ('Sulthan Bathery', 'Sulthan Bathery'),
        
        # Kannur
        ('Kannur', 'Kannur'),
        ('Thalassery', 'Thalassery'),
        ('Taliparamba', 'Taliparamba'),
        ('Iritty', 'Iritty'),
        ('Payyanur', 'Payyanur'),
        
        # Kasaragod
        ('Kasaragod', 'Kasaragod'),
        ('Hosdurg', 'Hosdurg'),
    ]
    
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, default='', blank=True)
    taluk = models.CharField(max_length=50, choices=TALUK_CHOICES, default='', blank=True)
    photo = models.FileField(upload_to='photos/', blank=True, null=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    willing_to_donate = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.blood_group})"
    
    def get_donation_count(self):
        """Get the total number of blood donations made by this user"""
        return self.blooddonation_set.count()
    
    def get_last_donation_date(self):
        """Get the date of the last blood donation"""
        last_donation = self.blooddonation_set.order_by('-donation_date').first()
        return last_donation.donation_date if last_donation else None
    
    @classmethod
    def get_taluks_by_district(cls, district):
        """Get taluks for a specific district"""
        district_taluks = {
            'Thiruvananthapuram': ['Thiruvananthapuram', 'Nedumangadu', 'Chirayinkeezhu', 'Kattakada', 'Neyyattinkara', 'Varkala'],
            'Kollam': ['Kollam', 'Kunnathur', 'Karunagappally', 'Kottarakkara', 'Pathanapuram', 'Punalur'],
            'Pathanamthitta': ['Adoor', 'Konni', 'Kozhencherry', 'Ranni', 'Thiruvalla', 'Mallappally'],
            'Alappuzha': ['Cherthala', 'Ambalappuzha', 'Kuttanad', 'Karthikappally', 'Chengannur', 'Mavelikkara'],
            'Kottayam': ['Changanasserry', 'Kottayam', 'Vaikom', 'Meenachil', 'Kanjirappally'],
            'Idukki': ['Devikulam', 'Peermade', 'Thodupuzha', 'Udumbanchola'],
            'Ernakulam': ['Aluva', 'Kanayannur', 'Kochi', 'Kothamangalam', 'Kunnathunad', 'Muvattupuzha', 'North Paravur'],
            'Thrissur': ['Thrissur', 'Chavakkad', 'Kodungallur', 'Mukundapuram', 'Kunnamkulam', 'Thalapilly'],
            'Palakkad': ['Palakkad', 'Alathur', 'Chittur', 'Mannarkkad', 'Pattambi', 'Ottappalam', 'Attappady'],
            'Malappuram': ['Perinthalmanna', 'Nilambur', 'Eranad', 'Kondotty', 'Tirur', 'Tirurangadi', 'Ponnani'],
            'Kozhikode': ['Kozhikode', 'Koyilandy', 'Vadakara', 'Thamarassery'],
            'Wayanad': ['Mananthavady', 'Vythiri', 'Sulthan Bathery'],
            'Kannur': ['Kannur', 'Thalassery', 'Taliparamba', 'Iritty', 'Payyanur'],
            'Kasaragod': ['Kasaragod', 'Hosdurg'],
        }
        return district_taluks.get(district, [])


class BloodRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, choices=User.BLOOD_GROUP_CHOICES)
    hospital_name = models.CharField(max_length=100)
    required_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self) -> str:
        return f"{self.blood_group} needed at {self.hospital_name}"


class BloodDonation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_date = models.DateField(default=timezone.now)
    hospital_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5, choices=User.BLOOD_GROUP_CHOICES)
    units_donated = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.donor.name} donated {self.units_donated} unit(s) on {self.donation_date}"
    
    class Meta:
        ordering = ['-donation_date']


class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=5, choices=User.BLOOD_GROUP_CHOICES, unique=True)
    available_units = models.PositiveIntegerField(default=0)
    critical_level = models.PositiveIntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.blood_group}: {self.available_units} units"
    
    def is_critical(self):
        """Check if blood group is at critical level"""
        return self.available_units <= self.critical_level
    
    def get_status_color(self):
        """Get Bootstrap color class based on inventory level"""
        if self.available_units == 0:
            return 'danger'
        elif self.is_critical():
            return 'warning'
        else:
            return 'success'


class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.relationship}) - {self.user.name}"

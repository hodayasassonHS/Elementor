from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import UsagePerSite, Users, Packages, PackagesToUsers, Sites, SitesToPackage
import json
from datetime import datetime

class DataWriting:

    def __init__(self):
        self.engine = create_engine('postgresql://developer:41b387c1-2cf9-4436-85fa-7c75093b7d14@test-rds-dev.colcjtm9obot.eu-west-1.rds.amazonaws.com:5432/metrics_dev')
        self.Session = sessionmaker(bind=self.engine)

    def create_user(self, data):
        user_id = data.get('user_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        address = data.get('address')
        phone_number = data.get('phone_number')
        password = data.get('password')  # Added based on the 'users' table definition

        if user_id is None:
            return 'cannot create user'

        session = self.Session()
        user = Users(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone_number=phone_number,
            password=password
        )
        session.add(user)
        session.commit()
        session.close()

        return 'success'

    def create_usage_per_site(self, data):
       
        site_id = data.get('site_id')
        time = datetime.strptime(data.get('time'), '%a, %d %b %Y %H:%M:%S %Z')
        storage_gb = data.get('storage_gb')
        cpu_percent = data.get('cpu_percent')
        ai_tokens_amount=data.get('ai_tokens_amount')
        

        if site_id is None:
            return 'Missing metric data'

        session = self.Session()

        usage = UsagePerSite( site_id=site_id, time=time, storage_gb=storage_gb, cpu_percent=cpu_percent,ai_tokens_amount=ai_tokens_amount)

        session.add(usage)

        session.commit()
        session.close()

    def create_sites_to_package(self, data):
        
        package_id = data.get('package_id')
        site_id = data.get('site_id')
        if any(value is None for value in [package_id, site_id]):
            return 'Incomplete data'

        session = self.Session()
        site_to_package = SitesToPackage( package_id=package_id, site_id=site_id)
        session.add(site_to_package)
        session.commit()
        session.close()

        return 'success'

    def create_site(self, data):
        user_id = data.get('user_id')
        site_id = data.get('site_id')
        if site_id is None or site_id is None:
            return 'error'

        session = self.Session()
        site = Sites(user_id=user_id, site_id=site_id)

        session.add(site)
        session.commit()
        session.close()

    def create_package(self, data):
        package_name = data.get('package_name')  # Added based on the 'packages' table definition
        cost_per_month = data.get('cost_per_month')
        storage_gb = data.get('storage_gb')
        cpu_percent = data.get('cpu_percent')
  
        if (
            cost_per_month is None and
            storage_gb is None and
            cpu_percent is None 

        ):
            return 'Incomplete data'

        session = self.Session()
        package = Packages(
            package_name=package_name,
            cost_per_month=cost_per_month,
            storage_gb=storage_gb,
            cpu_percent=cpu_percent
        )
        session.add(package)
        session.commit()
        session.close()

        return 'success'

    def create_package_to_user(self, data):
    

        user_id = data.get('user_id')
        package_id = data.get('package_id')
        if user_id is None or id is None:
            return {'error': 'Missing package-to-user data'}

        session = self.Session()
        package_to_user = PackagesToUsers( user_id=user_id, package_id=package_id)
        session.add(package_to_user)
        session.commit()
        newly_created_id = package_to_user.package_to_user_id
        session.close()
        return newly_created_id

    def get_user(self, user_id):
        session = self.Session()
        user = session.query(Users).filter(Users.user_id == user_id).first()
        session.close()

        if user:
            result = {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user.address,
                'phone_number': user.phone_number,
                'password': user.password
            }
            return result
        else:
            return None

    def get_site(self, site_id):
        session = self.Session()
        site = session.query(Sites).filter(Sites.site_id == site_id).first()
        session.close()

        return site
    def update_user(self,data):
        
        session = self.Session()
        user_id=data['user_id']
        user = session.query(Users).filter(Users.user_id == user_id).first()
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.address = data.get('address', user.address)
        user.phone_number = data.get('phone_number', user.phone_number)
        session.commit()
        session.close()

    def update_site(self,data):
        site_id = data.get('site_id')
        session = self.Session()
        site = session.query(Sites).filter(Sites.site_id == site_id).first()

        site.site_id = data.get('site_id')
        site.user= data.get('user_id')
        session.commit()
        session.close()
        
        return jsonify({'message': 'Site updated successfully'})
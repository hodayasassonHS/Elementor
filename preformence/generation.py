class Package:
    def __init__(self, package_id, package_name,num_of_website, cost_per_month_dollar,tokens, storage_gb, cpu_percent):
        self.package_id = package_id
        self.package_name = package_name
        self.num_of_website = num_of_website
        self.cost_per_month_dollar = cost_per_month_dollar
        self.tokens=tokens
        self.storage_gb = storage_gb
        self.cpu_percent = cpu_percent

# Define the packages
package_types=[]

free_package = Package(1,"Free",1, 0, 10, 0, 0)
essential_package = Package(2, "Essential",1, 49, 100, 10, 20)
advanced_package = Package(3, "Advanced",3, 99, 1000, 25, 100)
expert_package = Package(4, "Expert",25, 199, 10000, 50, 100)
package_types.append(free_package)
package_types.append(essential_package)
package_types.append(advanced_package)
package_types.append(expert_package)

#pip install faker
import random
import uuid
import time
import json
import threading
from stream import _stream
from users import insert_users_data
from sites import insert_sites_data
from package_site import insert_sites_to_package_data
from package_user import insert_packages_data


from faker import Faker
faker=Faker()
class generate_fake_data:
    package_counter = 1 
    def __init__(self):
        self.stream=_stream()
        self.users_list=[]
        self.sites_list=[]
        self.metrics_list=[]
        self.fake_user_package_list=[]
        self.users_id=[]
        self.sites_id=[]
        self.user_packages_id=[]
        self.index=0
        self.order_list=[]
        
    def fake_user(self): #1000 users
        user_id = str(uuid.uuid4())
        password_length = random.randint(12, 20)
        password = faker.password(length=password_length, special_chars=True, digits=True, upper_case=True, lower_case=True)
        first_name=faker.first_name()
        last_name=faker.last_name()
        address=faker.address()
        email=faker.email()
        phone_number=faker.phone_number()
        user={}
        data = {
            "user_id": user_id,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "address":address,
            "email":email,
            "phone_number":phone_number,
              }
        return data
        
    
    def fake_user_package(self):#1000 package
        for user in self.users_id:
            data=self.fake_single_user_package(user)
            self.fake_user_package_list.append(data)
            
            self.index+=1
                
    def fake_single_user_package(self, user):
            package_user_id = self.package_counter
            self.package_counter += 1  # Increment the package counter
            package_id = random.choice(package_types).package_id
            for i in package_types:
                if i.package_id == package_id:
                    package = i
                    break
            tokens_left = package.tokens
            remain_sites = package.num_of_website
            storage_gb = package.storage_gb
            cpu_percent = package.cpu_percent
            data = {
                "index": self.index,
                "package_user_id": package_user_id,  # Use integer-based ID
                "user_id": user,
                "package_id": package_id,
                "tokens_left": tokens_left,
                "remain_sites": remain_sites,
                "storage_gb_left": storage_gb,
                "cpu_percent_left": cpu_percent
            }
            self.user_packages_id.append(package_user_id)
            return data
        
    def fake_single_site(self,user_package_id,user_id,format,one_hour_from_now=0,isAhead=False):
        site_id = str(uuid.uuid4())
        url = faker.url()
        data = {
            #name site
            "site_id": site_id,
            "url": url,
            "user_package_id": user_package_id,
            "user_id":user_id,
            "storage_gb_wasted":0,
            "tokens_wasted":0,
            "cpu_percent_wasted":0
        }
        return data 
        
    def fake_site(self,format): #5000 sites
        for user_package in self.fake_user_package_list:
            num_of_posibilities=int(user_package['remain_sites'])
            num_of_sites= random.randint(0,num_of_posibilities)
            sites_list=[]
            for i in range(num_of_sites):
                data=self.fake_single_site(user_package['package_user_id'],user_package['user_id'],format)
                self.sites_list.append(data)
                user_package['remain_sites']-=1
                
    def generate_fake_sites_ahead(self, format):
        current_time = int(time.time())
        one_hour_from_now = current_time + 60 * 60  # One hour from now
        half_year_from_now = current_time + int(182.5 * 24 * 60 * 60)  # Half a year ahead
        while one_hour_from_now <= half_year_from_now:
            user_package=random.choice(self.fake_user_package_list)
            while(user_package['remain_sites'] <= 0):
                user_package=random.choice(self.fake_user_package_list)
            data = self.fake_single_site(user_package['package_user_id'],user_package['user_id'], format, one_hour_from_now,True)
            self.sites_list.append(data)
            user_package['remain_sites'] -= 1
            self.generate_fake_order('json','site',data)

            one_hour_from_now += 60 * 45  # Increment time by 1 hour
            time.sleep(60*45)

            
    def generate_fake_user_ahead(self, format):
        current_time = int(time.time())
        one_hour_from_now = current_time + 60 * 60  # One hour from now
        half_year_from_now = current_time + int(182.5 * 24 * 60 * 60)  # Half a year ahead
        while one_hour_from_now <= half_year_from_now:
            data=self.fake_user()
            self.generate_fake_order('json','user',data)
            self.users_list.append(data)
            one_hour_from_now += 60 * 90   # Increment time by 1 hour
            time.sleep(60*90)

    
    def generate_fake_package_ahead(self, format):
        current_time = int(time.time())
        one_hour_from_now = current_time + 60 * 60  # One hour from now
        half_year_from_now = current_time + int(182.5 * 24 * 60 * 60)  # Half a year ahead
        while one_hour_from_now <= half_year_from_now:
            user=random.choice(self.users_list)
            data=self.fake_single_user_package(user)
            self.generate_fake_order('json','package',data)
            self.fake_user_package_list.append(data)
            one_hour_from_now += 60 *60   # Increment time by 1 hour
            time.sleep(60*60)
            
    def update_site_data(self,site_id,field,addition):
        for site in self.sites_list:
            if site['site_id']==site_id:
                site_to_update=site
                break;
        site_to_update[field]+=addition
        
    def fake_metrics(self, site):
        event_time = int(time.time())
        event_id = str(uuid.uuid4())
        site_id = site['site_id']
        # Find the package associated with the site owner
        for i in self.fake_user_package_list:
            if i['package_user_id'] == site['user_package_id']:
                user_package = i
                break
        metrics = {}
      #  if random.random() < 0.8:
        if user_package['tokens_left']>0:
            wasted_this_time= random.uniform(0, user_package['tokens_left']/30)
            self.fake_user_package_list[user_package['index']]['tokens_left'] -= wasted_this_time 
            self.update_site_data(site_id,'tokens_wasted',wasted_this_time)
            metrics["tokens"] = site['tokens_wasted']
        if random.random() < 0.8:
            if user_package['storage_gb_left']>0:
                wasted_this_time= random.uniform(0, user_package['storage_gb_left']/30) 
                self.fake_user_package_list[user_package['index']]['storage_gb_left'] -= wasted_this_time 
                self.update_site_data(site_id,'storage_gb_wasted',wasted_this_time)
                metrics["storage_gb"] = site['storage_gb_wasted']
        if random.random() < 0.5:
            if user_package['cpu_percent_left']>0:
                wasted_this_time= random.uniform(0, user_package['cpu_percent_left']/30) 
                self.fake_user_package_list[user_package['index']]['cpu_percent_left'] -= wasted_this_time 
                self.update_site_data(site_id,'cpu_percent_wasted',wasted_this_time)
                metrics["cpu_percent"] = site['cpu_percent_wasted']
        data = {
            "event_time":event_time,
            "event_uuid": event_id,
            "identifier": {
                "site_id": site_id
            },
            "metrics": metrics
        }
        return data
    def generate_fake_order(self,format,typeOrder,details):
        data={
            "event_uuid" : str(uuid.uuid4()),
            "event_time" : int(time.time()),
            "typeOrder":typeOrder,
            "data" : details         
             }
        self.order_list.append(data)
        self.stream.stream_order(data)
        order_file = f'fake_order type.{format}'
        with open(order_file, "w") as file:
             json.dump(self.order_list, file)       

    def generate_fake_users(self):#1000 users
        for _ in range(100):
            fake_user = self.fake_user()
            self.users_list.append(fake_user)
            self.users_id.append(fake_user['user_id'])

    def fake_metrics_for_half_year(self):
        start_time = int(time.time()) - int(182.5 * 24 * 60 * 60)  # Half a year in seconds
        for i in range(182):
            for site in self.sites_list:
                fake_metrics = self.fake_metrics(site)
                start_time += 20
                fake_metrics["event_time"] = start_time
                self.metrics_list.append(fake_metrics)
            start_time += 60 * 60 * 24  # Increment time by 1 day

    def generate_fake_metrics_ahead(self, format):
        while True:
            for site in self.sites_list:
                fake_metrics = self.fake_metrics(site)
                self.metrics_list.append(fake_metrics)
                self.stream.stream_matric(fake_metrics)
                metrics_file = f'fake_metrics.{format}'
                with open(metrics_file, "w") as file:
                    json.dump(self.metrics_list, file)
            time.sleep(60*60*24)  # Sleep for 1 day

    
    def fake_metrics_for_half_year_ahead(self, format):
        threading.Thread(target=self.generate_fake_metrics_ahead, args=(format,)).start()
        metrics_file = f'fake_metrics.{format}'
        with open(metrics_file, "w") as file:
            json.dump(self.metrics_list, file)
        print(f"!Fake metrics have been exported to {metrics_file}")
    
    def fake_orders_ahead(self, format):
        threading.Thread(target=self.generate_fake_user_ahead, args=(format,)).start()
        threading.Thread(target=self.generate_fake_sites_ahead, args=(format,)).start()
        threading.Thread(target=self.generate_fake_package_ahead, args=(format,)).start()

        print("Fake sites generation has been started.")        
        
    def init_fake_data(self,format='JSON'):
        self.generate_fake_users()
        users_file = f'fake_users.{format}'
        with open(users_file, "w") as file:
            json.dump(self.users_list, file)
            insert_users_data(self.users_list)
        print(f"Fake users has been exported to {users_file}")
        self.fake_user_package()
        user_package = f'fake_user_package.{format}'
        with open(user_package, "w") as file:
            json.dump(self.fake_user_package_list, file)
        insert_packages_data(self.fake_user_package_list)
        print(f"Fake user to package has been exported to {user_package}")
        
        self.fake_site(format)
        sites_file = f'fake_sites.{format}'
        with open(sites_file, "w") as file:
            json.dump(self.sites_list, file)
        insert_sites_data(self.sites_list)
        insert_sites_to_package_data(self.sites_list)

        print(f"Fake sites has been exported to {sites_file}")
        
        self.fake_metrics_for_half_year()
        metrics_file = f'fake_metrics.{format}'
        with open(metrics_file, "w") as file:
             json.dump(self.metrics_list, file)
        print(len(self.metrics_list))
        
        print(f"Fake metrics has been exported to {metrics_file}")
        sites_file = f'fake_sites.{format}'
        with open(sites_file, "w") as file:
            json.dump(self.sites_list, file)
        print(f"Updated fake sites has been exported to {sites_file}")
        
        user_package = f'fake_user_package.{format}'
        with open(user_package, "w") as file:
            json.dump(self.fake_user_package_list, file)
        print(f"Fake user to package has been exported to {user_package}")
        
fake_data_generator = generate_fake_data()
fake_data_generator.init_fake_data('json')
fake_data_generator.fake_metrics_for_half_year_ahead('json')
fake_data_generator.fake_orders_ahead('json')


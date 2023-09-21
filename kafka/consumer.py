from confluent_kafka import Consumer
from dataWriting import DataWriting
import json
bootstrap_servers='pkc-e8mp5.eu-west-1.aws.confluent.cloud:9092'
security_protocol='SASL_SSL'
sasl_mechanisms='PLAIN'
sasl_username='YJEH2DWWEGS4NAG4'
sasl_password='W15jGRctIjexCA7COGqrdwky2q0AHWlWfN70sHiZqxt9Q8m3JDYoXgzjbzaeJQRs'
class _consumer2:
    def __init__(self,topic):

        # self.bootstrap_servers = 'localhost:9092'
        # self.topic = topic 
        # self.group_id = 'my_consumer_group' 
        # self.conf = {
        #     'bootstrap.servers': self.bootstrap_servers,
        #     'group.id': self.group_id
        # }
        # self.consumer = Consumer(self.conf)
        self.topic = topic 
        self.group_id = 'my_consumer_group' 
        self.conf = {
            # 'bootstrap.servers': self.bootstrap_servers,
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': security_protocol,
            'sasl.mechanism': sasl_mechanisms,
            'sasl.username': sasl_username,  
            'sasl.password': sasl_password, 
            'group.id': self.group_id  
        }
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe(topics=[self.topic])
        self.dataWriting = DataWriting()
    def write_package(self,data):
        # Site_id=(data['site_id'])
        package_user_id=data['package_user_id']
        User_id=(data["user_id"]["user_id"])
        package_id = data["package_id"]
        # Package=data['package']
        # if Package == "Free" :
        #     package_id = 1;
    
        # if Package == "Essential":
        #     package_id = 2;

        # if Package == "Advanced":
        #     package_id = 3;
       
        # if Package == "Expert":
        #     package_id = 4;
        
        packages_to_users_data = {
            "package_user_id":package_user_id,
            "user_id":User_id ,
            "package_id": package_id  
        }
        existing_user = self.dataWriting.get_user(User_id)
        if not existing_user:
            self.dataWriting.create_user({'user_id':User_id})
        # existing_site=self.dataWriting.get_site(Site_id)
        # if not existing_site:
        #  
        # self.dataWriting.create_site({'site_id':Site_id,'user_id':User_id})
        #  id=self.dataWriting.create_package_to_user(packages_to_users_data)
        self.dataWriting.create_package_to_user(packages_to_users_data)
        
        # sites_to_package_data = {
            
        #     "package_id": id,  
        #     "site_id": Site_id
        # }
        # self.dataWriting.create_sites_to_package(sites_to_package_data)
    def write_user(self,data):
        user_id=(data["user_id"])
        
        existing_user = self.dataWriting.get_user(user_id)
        if  existing_user:
            self.dataWriting.update_user(data)
        self.dataWriting.create_user(data)
    def write_site(self,data):
        user_id=data['user_id']
        package_user_id=data['user_package_id']
        existing_user = self.dataWriting.get_user(user_id)
        if not existing_user:
            self.dataWriting.create_user({'user_id':user_id})
        site_id=data["site_id"]
        existing_site = self.dataWriting.get_site(site_id)
        if existing_site:
            self.dataWriting.update_site(data)
        self.dataWriting.create_site(data)
        sites_to_package_data = {
            
            "package_id": package_user_id,  
            "site_id": site_id
        }
        self.dataWriting.create_sites_to_package(sites_to_package_data)
    def writing_order(self,data):
        order_type=data['typeOrder']
        
        if order_type=='user':
            self.write_user(data['data'])
        if order_type=='site':
            self.write_site(data['data'])
        if order_type=='package':            
            self.write_package(data['data'])
    def read_matric(self):
        try:
            while True:
                message = self.consumer.poll(timeout=1.0)
                if message is None:
                    continue
                if message.error():
                    print(f"Error: {message.error()}")
                    continue
                message_value = message.value()
                print(f"Received message value: {message_value} on partition {message.partition()}")
                if message_value:
                    message_dict = json.loads(message_value.decode('utf-8'))
                    existing_site=self.dataWriting.get_site(message_dict.get('site_id'))
                    if not existing_site:
                        
                        self.dataWriting.create_site(message_dict)
                    
                    self.dataWriting.create_usage_per_site(message_dict)
                    print(f"Received message: {type(message_dict)} from topic {message.topic()} on partition {message.partition()}")
        except KeyboardInterrupt:
            self.consumer.close()


    def read_orders(self):
        try:
            while True:
                message = self.consumer.poll(timeout=1.0)
                if message is None:
                    continue
                if message.error():
                    print(f"Error: {message.error()}")
                    continue
                message_value = message.value()
                print(f"Received message value: {message_value} on partition {message.partition()}")
                if message_value:
                    message_dict = json.loads(message_value.decode('utf-8'))
                    print(f"Received message: {message_dict} from topic {message.topic()} on partition {message.partition()}")
                    print("order")
                    
                    self.writing_order(message_dict)
                    
        except KeyboardInterrupt:
            self.consumer.close()

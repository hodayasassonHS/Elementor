from confluent_kafka import Producer
import json
  
bootstrap_servers='pkc-e8mp5.eu-west-1.aws.confluent.cloud:9092'
security_protocol='SASL_SSL'
sasl_mechanisms='PLAIN'
sasl_username='YJEH2DWWEGS4NAG4'
sasl_password='W15jGRctIjexCA7COGqrdwky2q0AHWlWfN70sHiZqxt9Q8m3JDYoXgzjbzaeJQRs'
class _producer():
    def __init__(self):    
         
        self.conf = {

            'bootstrap.servers': bootstrap_servers,
            'security.protocol': security_protocol,
            'sasl.mechanism': sasl_mechanisms,
            'sasl.username': sasl_username,  # Update with your SASL username
            'sasl.password': sasl_password # Update with your SASL password
            
        }
        self.producer= Producer(self.conf)  
        # self.bootstrap_servers='localhost:9092'
          
        # self.conf_producer = {'bootstrap.servers': self.bootstrap_servers}
        # self.producer= Producer(self.conf_producer)
         
        # bootstrap_servers='pkc-e8mp5.eu-west-1.aws.confluent.cloud:9092'
        # security_protocol='SASL_SSL'
        # sasl_mechanisms='PLAIN'
        # sasl_username='YJEH2DWWEGS4NAG4'
        # sasl_password='W15jGRctIjexCA7COGqrdwky2q0AHWlWfN70sHiZqxt9Q8m3JDYoXgzjbzaeJQRs'
        # self.topic = 'kamatech'  # metics
        # self.conf = {

        #     'bootstrap.servers': bootstrap_servers,
        #     'security.protocol': security_protocol,
        #     'sasl.mechanism': sasl_mechanisms,
        #     'sasl.username': sasl_username,  # Update with your SASL username
        #     'sasl.password': sasl_password # Update with your SASL password
            
        # }
        # self.producer= Producer(self.conf)
        
        

    def writing_data(self, data,topic):
        
        def delivery_report(err, msg):        
            if err is not None:
                print(f'Message delivery failed: {err}')
            else:
                print(f'Message delivered to {msg.topic()} [{msg.partition()}],{msg}')
        message = json.dumps(data)
        
        self.producer.produce(topic, value=message.encode('utf-8'), callback=delivery_report)
        self.producer.flush()
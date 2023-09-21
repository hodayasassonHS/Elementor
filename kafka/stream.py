import producer
import datetime

class _stream:
    def __init__(self):
        self.producer=producer._producer()
        
    def __format_data(self,data):
        formatted_data = {
            'cpu_percent': data['metrics'].get('cpu_percent'),
            'time': datetime.datetime.fromtimestamp(data['event_time']).strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'site_id' : data['identifier']['site_id'],
            'storage_gb': data['metrics'].get('storage_gb'),
            'ai_tokens_amount':data['metrics'].get('tokens'),
            
}
        return formatted_data
            
  
               

        
    def stream_matric(self,data):
        print("stream_matric")
        topic = 'kamatech' 
        formatted_data = self.__format_data(data)
        
        self.producer.writing_data(formatted_data,topic)
        
    def stream_order(self,data):
        print("stream_order")

        topic='kamatech_order'


        self.producer.writing_data(data,topic)

data = {
"event_uuid": '3464534d-fd24-4c84-8106-737900d8b684',
"event_time": 1684048431,
"User_id": "20",
"User_name": "amihay",
"Site_id": "22",
"Package": "Free"
}
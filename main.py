from dotenv import load_dotenv
import os
from google.cloud import firestore
from datetime import datetime

load_dotenv()


service_account_key_path = os.environ.get('SERVICE_ACCOUNT_KEY_PATH')

db = firestore.Client.from_service_account_json(service_account_key_path)

def delete_expired_events(request):
    try:
        current_time = datetime.utcnow()

        events_ref = db.collection('Event')
        Attend_ref = db.collection("AttendList")
        event_doc_ids = []

        
        expired_events_query = events_ref.where('endTime', '<', current_time)
        expired_events = expired_events_query.stream()

        for event in expired_events:
            event_doc_ids.append(event.id)
            event.reference.delete()
            
        for attend_doc in Attend_ref.stream():
            if attend_doc.id in event_doc_ids:
                attend_doc.reference.delete()
 

        
    
    except Exception as e:
        return f"Error: {e}"


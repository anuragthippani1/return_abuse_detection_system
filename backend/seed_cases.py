import pymongo
from datetime import datetime, timedelta
import random

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["amazon"]
collection = db["return_cases"]

sample_categories = ["Electronics", "Clothing", "Books"]
sample_actions = ["Approve", "Flag", "Escalate"]
sample_reasons = ["item broken", "wrong item", "not as described", "changed mind"]
sample_refund_methods = ["card", "wallet", "cash"]  # ✅ Add refund methods

cases = []
for i in range(20):
    risk_score = random.randint(10, 99)
    suspicion_score = round(random.uniform(0.1, 0.99), 2)
    case = {
        "customer_id": f"CUST{str(i+1).zfill(3)}",
        "return_reason": random.choice(sample_reasons),
        "risk_score": risk_score,
        "suspicion_score": suspicion_score,
        "refund_method_type": random.choice(sample_refund_methods),  # ✅ Now added
        "product_category": random.choice(sample_categories),
        "action_taken": random.choice(sample_actions),
        "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
    }
    cases.append(case)

collection.delete_many({})  # Optional: clear old broken data
collection.insert_many(cases)

print("✅ Sample return cases inserted!")
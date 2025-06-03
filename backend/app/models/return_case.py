from datetime import datetime
from typing import Optional, Dict, Any
from pymongo import MongoClient
from bson.objectid import ObjectId

class ReturnCase:
    def __init__(
        self,
        customer_id: str,
        return_reason: str,
        risk_score: float,
        suspicion_score: float,
        refund_method_type: str,
        action_taken: str,
        product_category: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ):
        self.customer_id = customer_id
        self.return_reason = return_reason
        self.risk_score = risk_score
        self.suspicion_score = suspicion_score
        self.refund_method_type = refund_method_type
        self.action_taken = action_taken
        self.product_category = product_category
        self.additional_data = additional_data or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the return case to a dictionary for MongoDB storage."""
        return {
            'customer_id': self.customer_id,
            'return_reason': self.return_reason,
            'risk_score': self.risk_score,
            'suspicion_score': self.suspicion_score,
            'refund_method_type': self.refund_method_type,
            'action_taken': self.action_taken,
            'product_category': self.product_category,
            'additional_data': self.additional_data,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReturnCase':
        """Create a ReturnCase instance from a dictionary."""
        return cls(
            customer_id=data['customer_id'],
            return_reason=data['return_reason'],
            risk_score=data['risk_score'],
            suspicion_score=data['suspicion_score'],
            refund_method_type=data['refund_method_type'],
            action_taken=data['action_taken'],
            product_category=data.get('product_category'),
            additional_data=data.get('additional_data')
        )

class ReturnCaseModel:
    def __init__(self, db_uri="mongodb://localhost:27017/", db_name="amazon"):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db["return_cases"]

    def get_all(self, page=1, per_page=10):
        skip = (page - 1) * per_page
        cursor = self.collection.find().skip(skip).limit(per_page)
        cases = [self._serialize(case) for case in cursor]
        return cases

    def get_by_id(self, case_id):
        case = self.collection.find_one({"_id": ObjectId(case_id)})
        return self._serialize(case) if case else None

    def create(self, case_data):
        result = self.collection.insert_one(case_data)
        return str(result.inserted_id)

    def update(self, case_id, case_data):
        result = self.collection.update_one(
            {"_id": ObjectId(case_id)},
            {"$set": case_data}
        )
        return result.modified_count > 0

    def delete(self, case_id):
        result = self.collection.delete_one({"_id": ObjectId(case_id)})
        return result.deleted_count > 0

    def get_statistics(self):
        pipeline = [
            {
                "$group": {
                    "_id": "$return_reason",
                    "count": {"$sum": 1},
                    "avg_risk_score": {"$avg": "$risk_score"}
                }
            }
        ]
        stats = list(self.collection.aggregate(pipeline))
        # Format output
        return [
            {
                "return_reason": stat["_id"],
                "count": stat["count"],
                "avg_risk_score": stat["avg_risk_score"]
            }
            for stat in stats
        ]

    def _serialize(self, doc):
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        return doc 
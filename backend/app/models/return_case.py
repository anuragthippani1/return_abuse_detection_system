from datetime import datetime
from typing import Optional, Dict, Any
from pymongo import MongoClient
from bson.objectid import ObjectId

class ReturnCase:
    def __init__(
        self,
        case_id: str,
        user_id: str,
        customer_id: str,
        abuse_type: str,
        description: str,
        status: str,
        reported_at: datetime,
        refund_method_type: str,
        action_taken: str,
        return_reason: str,
        risk_score: float,
        suspicion_score: float,
        product_category: str
    ):
        self.case_id = case_id
        self.user_id = user_id
        self.customer_id = customer_id
        self.abuse_type = abuse_type
        self.description = description
        self.status = status
        self.reported_at = reported_at
        self.refund_method_type = refund_method_type
        self.action_taken = action_taken
        self.return_reason = return_reason
        self.risk_score = risk_score
        self.suspicion_score = suspicion_score
        self.product_category = product_category
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the return case to a dictionary for MongoDB storage."""
        return {
            'case_id': self.case_id,
            'user_id': self.user_id,
            'customer_id': self.customer_id,
            'abuse_type': self.abuse_type,
            'description': self.description,
            'status': self.status,
            'reported_at': self.reported_at,
            'refund_method_type': self.refund_method_type,
            'action_taken': self.action_taken,
            'return_reason': self.return_reason,
            'risk_score': self.risk_score,
            'suspicion_score': self.suspicion_score,
            'product_category': self.product_category,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReturnCase':
        """Create a ReturnCase instance from a dictionary."""
        return cls(
            case_id=data['case_id'],
            user_id=data['user_id'],
            customer_id=data['customer_id'],
            abuse_type=data['abuse_type'],
            description=data['description'],
            status=data['status'],
            reported_at=data['reported_at'],
            refund_method_type=data['refund_method_type'],
            action_taken=data['action_taken'],
            return_reason=data['return_reason'],
            risk_score=data['risk_score'],
            suspicion_score=data['suspicion_score'],
            product_category=data['product_category']
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
        case = self.collection.find_one({"case_id": case_id})
        return self._serialize(case) if case else None

    def create(self, case_data):
        result = self.collection.insert_one(case_data)
        return str(result.inserted_id)

    def update(self, case_id, case_data):
        result = self.collection.update_one(
            {"case_id": case_id},
            {"$set": case_data}
        )
        return result.modified_count > 0

    def delete(self, case_id):
        result = self.collection.delete_one({"case_id": case_id})
        return result.deleted_count > 0

    def get_statistics(self):
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_cases": {"$sum": 1},
                    "avg_risk_score": {"$avg": "$risk_score"},
                    "avg_suspicion_score": {"$avg": "$suspicion_score"},
                    "high_risk_cases": {
                        "$sum": {
                            "$cond": [{"$gte": ["$risk_score", 0.7]}, 1, 0]
                        }
                    },
                    "medium_risk_cases": {
                        "$sum": {
                            "$cond": [
                                {"$and": [
                                    {"$gte": ["$risk_score", 0.3]},
                                    {"$lt": ["$risk_score", 0.7]}
                                ]},
                                1,
                                0
                            ]
                        }
                    },
                    "low_risk_cases": {
                        "$sum": {
                            "$cond": [{"$lt": ["$risk_score", 0.3]}, 1, 0]
                        }
                    }
                }
            }
        ]
        stats = list(self.collection.aggregate(pipeline))
        return stats[0] if stats else {
            "total_cases": 0,
            "avg_risk_score": 0,
            "avg_suspicion_score": 0,
            "high_risk_cases": 0,
            "medium_risk_cases": 0,
            "low_risk_cases": 0
        }

    def _serialize(self, doc):
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        return doc 
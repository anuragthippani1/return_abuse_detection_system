from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId
from ..config.mongodb import get_collection, convert_object_id, parse_object_id
from ..models.return_case import ReturnCase

class ReturnCaseService:
    def __init__(self):
        self.collection = get_collection()

    def save_return_case(self, return_case: ReturnCase) -> str:
        """Save a return case to MongoDB."""
        try:
            result = self.collection.insert_one(return_case.to_dict())
            return str(result.inserted_id)
        except Exception as e:
            raise Exception(f"Error saving return case: {str(e)}")

    def get_return_cases(
        self,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        product_category: Optional[str] = None,
        action_taken: Optional[str] = None,
        limit: int = 100,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get return cases with optional filters."""
        try:
            query = {}
            
            # Add score range filter
            if min_score is not None or max_score is not None:
                query['risk_score'] = {}
                if min_score is not None:
                    query['risk_score']['$gte'] = min_score
                if max_score is not None:
                    query['risk_score']['$lte'] = max_score

            # Add product category filter
            if product_category:
                query['product_category'] = product_category

            # Add action taken filter
            if action_taken:
                query['action_taken'] = action_taken

            # Execute query with pagination
            cursor = self.collection.find(query).skip(skip).limit(limit)
            
            # Convert cursor to list of dictionaries and handle ObjectId
            return [convert_object_id(ReturnCase.from_dict(doc).to_dict()) for doc in cursor]
        except Exception as e:
            raise Exception(f"Error fetching return cases: {str(e)}")

    def update_return_case(self, case_id: str, updates: Dict[str, Any]) -> bool:
        """Update a return case."""
        try:
            result = self.collection.update_one(
                {'_id': parse_object_id(case_id)},
                {'$set': updates}
            )
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Error updating return case: {str(e)}")

    def delete_return_case(self, case_id: str) -> bool:
        """Delete a return case."""
        try:
            result = self.collection.delete_one({'_id': parse_object_id(case_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise Exception(f"Error deleting return case: {str(e)}")

    def get_case_statistics(self) -> Dict[str, Any]:
        """Get statistics about return cases."""
        try:
            pipeline = [
                {
                    '$group': {
                        '_id': None,
                        'total_cases': {'$sum': 1},
                        'avg_risk_score': {'$avg': '$risk_score'},
                        'avg_suspicion_score': {'$avg': '$suspicion_score'},
                        'high_risk_cases': {
                            '$sum': {'$cond': [{'$gte': ['$risk_score', 70]}, 1, 0]}
                        },
                        'medium_risk_cases': {
                            '$sum': {'$cond': [
                                {'$and': [
                                    {'$gte': ['$risk_score', 30]},
                                    {'$lt': ['$risk_score', 70]}
                                ]}, 1, 0
                            ]}
                        },
                        'low_risk_cases': {
                            '$sum': {'$cond': [{'$lt': ['$risk_score', 30]}, 1, 0]}
                        }
                    }
                }
            ]
            
            result = list(self.collection.aggregate(pipeline))
            return result[0] if result else {
                'total_cases': 0,
                'avg_risk_score': 0,
                'avg_suspicion_score': 0,
                'high_risk_cases': 0,
                'medium_risk_cases': 0,
                'low_risk_cases': 0
            }
        except Exception as e:
            raise Exception(f"Error fetching statistics: {str(e)}")

    def get_case_by_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Get a single return case by ID."""
        try:
            result = self.collection.find_one({'_id': parse_object_id(case_id)})
            return convert_object_id(ReturnCase.from_dict(result).to_dict()) if result else None
        except Exception as e:
            raise Exception(f"Error fetching return case: {str(e)}")

    def insert_many(self, cases: List[Dict[str, Any]]) -> int:
        """Insert multiple return cases into MongoDB."""
        try:
            if not cases or not isinstance(cases, list):
                raise ValueError("Input must be a list of return case dictionaries.")
            result = self.collection.insert_many(cases)
            return len(result.inserted_ids)
        except Exception as e:
            raise Exception(f"Error inserting multiple return cases: {str(e)}")

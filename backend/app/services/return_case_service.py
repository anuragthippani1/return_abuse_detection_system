from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId
from ..config.mongodb import get_collection, convert_object_id, parse_object_id
from ..models.return_case import ReturnCase

class ReturnCaseService:
    def __init__(self):
        self.collection = get_collection()
        # In-memory storage as fallback when MongoDB is not available
        self.in_memory_storage = []
        self.next_id = 1
        
        # Add sample data if MongoDB is not available
        if self.collection is None:
            self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample return cases for demo purposes."""
        print(">>> Loading sample data for demo...")
        sample_cases = [
            {
                '_id': '1',
                'customer_id': 'CUST001',
                'return_reason': 'Product damaged during shipping',
                'risk_score': 15,
                'suspicion_score': 10,
                'refund_method_type': 'Original Payment',
                'action_taken': 'Approved',
                'product_category': 'Electronics',
                'timestamp': datetime.utcnow().isoformat()
            },
            {
                '_id': '2',
                'customer_id': 'CUST002',
                'return_reason': 'Wrong item received',
                'risk_score': 85,
                'suspicion_score': 90,
                'refund_method_type': 'Gift Card',
                'action_taken': 'Under Review',
                'product_category': 'Fashion',
                'timestamp': datetime.utcnow().isoformat()
            },
            {
                '_id': '3',
                'customer_id': 'CUST003',
                'return_reason': 'Item not as described',
                'risk_score': 45,
                'suspicion_score': 35,
                'refund_method_type': 'Original Payment',
                'action_taken': 'Approved',
                'product_category': 'Home & Kitchen',
                'timestamp': datetime.utcnow().isoformat()
            },
            {
                '_id': '4',
                'customer_id': 'CUST004',
                'return_reason': 'Changed my mind',
                'risk_score': 92,
                'suspicion_score': 88,
                'refund_method_type': 'Gift Card',
                'action_taken': 'Flagged',
                'product_category': 'Electronics',
                'timestamp': datetime.utcnow().isoformat()
            },
            {
                '_id': '5',
                'customer_id': 'CUST005',
                'return_reason': 'Defective product',
                'risk_score': 20,
                'suspicion_score': 15,
                'refund_method_type': 'Original Payment',
                'action_taken': 'Approved',
                'product_category': 'Toys',
                'timestamp': datetime.utcnow().isoformat()
            }
        ]
        self.in_memory_storage = sample_cases
        self.next_id = 6
        print(f">>> Loaded {len(self.in_memory_storage)} sample cases")

    def save_return_case(self, return_case: ReturnCase) -> str:
        """Save a return case to MongoDB or in-memory storage."""
        try:
            if self.collection is None:
                # Use in-memory storage
                case_dict = return_case.to_dict()
                case_dict['_id'] = str(self.next_id)
                self.next_id += 1
                self.in_memory_storage.append(case_dict)
                return case_dict['_id']
            else:
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
            if self.collection is None:
                # Use in-memory storage
                filtered_cases = self.in_memory_storage.copy()
                
                # Apply filters
                if min_score is not None:
                    filtered_cases = [c for c in filtered_cases if c.get('risk_score', 0) >= min_score]
                if max_score is not None:
                    filtered_cases = [c for c in filtered_cases if c.get('risk_score', 0) <= max_score]
                if product_category:
                    filtered_cases = [c for c in filtered_cases if c.get('product_category') == product_category]
                if action_taken:
                    filtered_cases = [c for c in filtered_cases if c.get('action_taken') == action_taken]
                
                # Apply pagination
                return filtered_cases[skip:skip + limit]
            else:
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
            if self.collection is None:
                # Calculate stats from in-memory storage
                if not self.in_memory_storage:
                    return {
                        'total_cases': 0,
                        'avg_risk_score': 0,
                        'avg_suspicion_score': 0,
                        'high_risk_cases': 0,
                        'medium_risk_cases': 0,
                        'low_risk_cases': 0
                    }
                
                total = len(self.in_memory_storage)
                risk_scores = [c.get('risk_score', 0) for c in self.in_memory_storage]
                suspicion_scores = [c.get('suspicion_score', 0) for c in self.in_memory_storage]
                
                return {
                    'total_cases': total,
                    'avg_risk_score': sum(risk_scores) / total if total > 0 else 0,
                    'avg_suspicion_score': sum(suspicion_scores) / total if total > 0 else 0,
                    'high_risk_cases': len([s for s in risk_scores if s >= 70]),
                    'medium_risk_cases': len([s for s in risk_scores if 30 <= s < 70]),
                    'low_risk_cases': len([s for s in risk_scores if s < 30])
                }
            else:
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

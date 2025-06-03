from flask import Blueprint, request, jsonify, current_app
from ..services.return_case_service import ReturnCaseService
from ..models.return_case import ReturnCase
import pandas as pd
import os
from datetime import datetime

api = Blueprint('api', __name__)
return_case_service = ReturnCaseService()

# ----------------------------------------
# 1. Save a single return case
# ----------------------------------------
@api.route('/save-return-case', methods=['POST'])
def save_return_case():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid or missing JSON data'}), 400

    try:
        return_case = ReturnCase(
            customer_id=data['customer_id'],
            return_reason=data['return_reason'],
            risk_score=data['risk_score'],
            suspicion_score=data['suspicion_score'],
            refund_method_type=data['refund_method_type'],
            action_taken=data['action_taken'],
            product_category=data.get('product_category')
        )
        case_id = return_case_service.save_return_case(return_case)
        return jsonify({
            'success': True,
            'message': 'Return case saved successfully',
            'case_id': case_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error saving return case: {str(e)}'}), 400

# ----------------------------------------
# 2. Get return cases with filtering & pagination
# ----------------------------------------
@api.route('/get-return-cases', methods=['GET'])
def get_return_cases():
    try:
        filters = {
            'min_score': request.args.get('min_score', type=float),
            'max_score': request.args.get('max_score', type=float),
            'product_category': request.args.get('product_category'),
            'action_taken': request.args.get('action_taken')
        }
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        skip = max(0, (page - 1) * per_page)

        cases = return_case_service.get_return_cases(**filters, limit=per_page, skip=skip)
        return jsonify({'success': True, 'cases': cases, 'page': page, 'per_page': per_page}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error fetching return cases: {str(e)}'}), 400

# ----------------------------------------
# 3. Get return case by ID
# ----------------------------------------
@api.route('/get-return-case/<case_id>', methods=['GET'])
def get_return_case(case_id):
    try:
        case = return_case_service.get_case_by_id(case_id)
        if case:
            return jsonify({'success': True, 'case': case}), 200
        return jsonify({'success': False, 'message': 'Return case not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error fetching return case: {str(e)}'}), 400

# ----------------------------------------
# 4. Get return case statistics
# ----------------------------------------
@api.route('/return-case-statistics', methods=['GET'])
def get_case_statistics():
    try:
        stats = return_case_service.get_case_statistics()
        return jsonify({'success': True, 'statistics': stats}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error fetching statistics: {str(e)}'}), 400

# ----------------------------------------
# 5. Update return case by ID
# ----------------------------------------
@api.route('/update-return-case/<case_id>', methods=['PUT'])
def update_return_case(case_id):
    updates = request.get_json()
    if not updates:
        return jsonify({'success': False, 'message': 'Invalid or missing JSON data'}), 400

    try:
        success = return_case_service.update_return_case(case_id, updates)
        if success:
            return jsonify({'success': True, 'message': 'Return case updated successfully'}), 200
        return jsonify({'success': False, 'message': 'Return case not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error updating return case: {str(e)}'}), 400

# ----------------------------------------
# 6. Delete return case by ID
# ----------------------------------------
@api.route('/delete-return-case/<case_id>', methods=['DELETE'])
def delete_return_case(case_id):
    try:
        success = return_case_service.delete_return_case(case_id)
        if success:
            return jsonify({'success': True, 'message': 'Return case deleted successfully'}), 204
        return jsonify({'success': False, 'message': 'Return case not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error deleting return case: {str(e)}'}), 400

# ----------------------------------------
# 7. Upload CSV/JSON bulk data and process
# ----------------------------------------
@api.route('/upload-data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({"success": False, "error": "No file selected"}), 400

    if not (file.filename.endswith('.csv') or file.filename.endswith('.json')):
        return jsonify({"success": False, "error": "Unsupported file type. Use CSV or JSON."}), 400

    try:
        # Parse file into DataFrame
        df = pd.read_csv(file) if file.filename.endswith('.csv') else pd.read_json(file)

        required_fields = [
            'customer_id', 'return_reason', 'risk_score', 'suspicion_score',
            'refund_method_type', 'action_taken', 'product_category'
        ]
        missing_fields = [f for f in required_fields if f not in df.columns]
        if missing_fields:
            return jsonify({"success": False, "error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        if 'timestamp' not in df.columns:
            df['timestamp'] = datetime.utcnow().isoformat()

        # Save uploaded file (optional)
        upload_path = current_app.config.get('UPLOAD_FOLDER', './uploads')
        os.makedirs(upload_path, exist_ok=True)
        save_path = os.path.join(upload_path, file.filename)
        df.to_csv(save_path, index=False)

        # Insert records into DB
        records = df.to_dict('records')
        inserted_count = return_case_service.insert_many(records)

        return jsonify({
            "success": True,
            "message": f"{file.filename} uploaded and processed",
            "records_processed": inserted_count
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"File processing error: {str(e)}"}), 500

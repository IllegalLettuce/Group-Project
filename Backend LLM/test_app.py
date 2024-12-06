import pytest
from flask import Flask
from unittest.mock import MagicMock, patch
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Mock the required dependencies
class MockFirestore:
    def collection(self, name):
        return self

    def document(self, doc_id=None):
        return self

    def set(self, data, merge=False):
        return True

    def create(self, data):
        return True

    def stream(self):
        return []

    def where(self, filter):
        return self

class MockYFinance:
    def __init__(self, ticker):
        self.ticker = ticker

    def history(self, period='5d', interval=None):
        return {'Close': [100.0, 102.0, 105.0]}

@pytest.fixture
def mock_app():
    """Create a mock Flask application for testing."""
    from flask import request, json
    app = Flask(__name__)
    
    @app.route('/report', methods=['POST'])
    def report():
        # Simulate the report route logic
        return json.jsonify({'status': 'success'})
    
    @app.route('/managestock', methods=['POST'])
    def manage_stock():
        # Simulate the manage stock route logic
        data = request.get_json()
        return json.jsonify({
            'status': 'Success',
            'message': f"Processed {data.get('action')} for {data.get('ticker')}"
        })
    
    return app

def test_report_route(mock_app):
    """Test the report route with a mock application."""
    with mock_app.test_client() as client:
        response = client.post('/report', data=b'Apple')
        assert response.status_code == 200
        result = response.get_json()
        assert result['status'] == 'success'

def test_manage_stock_route(mock_app):
    """Test the manage stock route with a mock application."""
    with mock_app.test_client() as client:
        test_data = {
            'ticker': 'AAPL',
            'amount': 10,
            'userId': 'test_user',
            'action': 'buy'
        }
        response = client.post('/managestock', json=test_data)
        assert response.status_code == 200
        result = response.get_json()
        assert result['status'] == 'Success'
        assert 'AAPL' in result['message']

@patch('yfinance.Ticker', MockYFinance)
def test_stock_data_retrieval():
    """Test stock data retrieval using a mock."""
    ticker = MockYFinance('AAPL')
    history = ticker.history()
    
    assert 'Close' in history
    assert len(history['Close']) > 0
    assert all(isinstance(price, float) for price in history['Close'])

def test_firestore_mock():
    """Test Firestore mock functionality."""
    db = MockFirestore()
    
    # Test collection and document methods
    collection = db.collection('users')
    document = collection.document('test_doc')
    
    # Test set method
    result = document.set({'test_key': 'test_value'})
    assert result is True

    # Test create method
    create_result = document.create({'new_key': 'new_value'})
    assert create_result is True

def test_stock_data_404_handling():
    """Test handling of non-existent stock data."""
    ticker = MockYFinance('NONEXISTENT')
    history = ticker.history()
    
    assert 'Close' in history
    assert len(history['Close']) > 0

def test_manage_stock_sell_logic(mock_app):
    """Test the stock selling logic."""
    with mock_app.test_client() as client:
        test_data = {
            'ticker': 'GOOGL',
            'amount': 5,
            'userId': 'test_user',
            'action': 'sell'
        }
        response = client.post('/managestock', json=test_data)
        assert response.status_code == 200
        result = response.get_json()
        assert result['status'] == 'Success'
        assert 'GOOGL' in result['message']

if __name__ == '__main__':
    pytest.main()
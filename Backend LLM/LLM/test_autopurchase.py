import unittest
from unittest.mock import MagicMock, patch
import json
from autopurchase import autopurchase

class TestAutopurchaseFunction(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps({
        "CompanyA": {
            "2024-12-01": {"Close": 100},
            "2024-12-02": {"Close": 105},
            "2024-12-03": {"Close": 110},
        }
    }))
    @patch('firebase_admin.firestore.client')
    def test_autopurchase(self, mock_firestore_client, mock_open):
        # Mock database and data
        mock_db = MagicMock()

        mock_document = MagicMock()
        mock_document.get.side_effect = lambda key: {
            'userid': 'user1',
            'company': 'CompanyA',
            'ticker': 'TICKA',
            'buy_percent': 50,
            'sell_percent': 70,
            'funds_dollar': 1000,
        }.get(key)

        mock_document.id = 'mock_document_id'
        mock_db.collection.return_value.stream.return_value = [mock_document]

        # Mock Firebase admin data for admins collection
        admin_doc = MagicMock()
        admin_doc.get.return_value = {'capital': 5000}
        mock_db.collection.return_value.stream.return_value = [admin_doc]

        with patch('firebase_admin.firestore.client', return_value=mock_db):
            with patch('crewai.Task') as mock_task:
                mock_task.return_value = MagicMock(
                    kickoff=lambda: json.dumps({'Buy': '60', 'Sell': '30'})
                )

                # Run autopurchase
                with patch('time.sleep', return_value=None):  # Avoid actual sleep
                    autopurchase(mock_db)

        # Assertions
        mock_db.collection.assert_any_call("autopurchase")
        mock_db.collection.assert_any_call("admins")
        mock_db.collection.return_value.stream.assert_called()
        mock_db.collection.return_value.document.assert_called_with('mock_document_id')
        mock_db.collection.return_value.document.return_value.set.assert_called()

    @patch('firebase_admin.firestore.client')
    def test_no_docs_in_autopurchase(self, mock_firestore_client):
        # Mock empty documents
        mock_db = MagicMock()
        mock_db.collection.return_value.stream.return_value = []

        with patch('firebase_admin.firestore.client', return_value=mock_db):
            with patch('time.sleep', return_value=None):  # Avoid actual sleep
                autopurchase(mock_db)

        # Assertions for no operation
        mock_db.collection.assert_any_call("autopurchase")
        mock_db.collection.return_value.stream.assert_called()

if __name__ == "__main__":
    unittest.main()

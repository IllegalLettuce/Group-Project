# import unittest
# from unittest.mock import patch, MagicMock
# import json
# import pandas as pd
# from datetime import datetime
# import yfinance as yf
# from finance import (
#     fetch_intraday_data_yahoo,
#     get_stock_data,
#     main_stock_data,
#     get_all_stocks,
#     is_valid_stock,
#     get_stock_by_name,
#     get_stock_by_ticker,
#     get_current_price,
#     stocks
# )

# class TestStockData(unittest.TestCase):
#     def setUp(self):
#         """Set up test fixtures"""
#         # Create sample stock history data
#         self.sample_history = pd.DataFrame({
#             'Open': [100.0, 101.0],
#             'High': [102.0, 103.0],
#             'Low': [98.0, 99.0],
#             'Close': [101.0, 102.0],
#             'Volume': [1000, 1100]
#         }, index=[
#             datetime(2024, 1, 1, 9, 30),
#             datetime(2024, 1, 1, 9, 45)
#         ])

#     def test_get_all_stocks(self):
#         """Test getting all stocks"""
#         result = get_all_stocks()
#         self.assertEqual(result, stocks)
#         self.assertTrue(any(stock['ticker'] == 'LMT' for stock in result))

#     def test_is_valid_stock(self):
#         """Test stock validation"""
#         self.assertTrue(is_valid_stock('LMT'))
#         self.assertFalse(is_valid_stock('INVALID'))
#         self.assertFalse(is_valid_stock(''))

#     def test_get_stock_by_name(self):
#         """Test getting stock by company name"""
#         # Test valid company name
#         result = get_stock_by_name('Lockheed Martin')
#         self.assertEqual(result['ticker'], 'LMT')
        
#         # Test case insensitive
#         result = get_stock_by_name('lockheed martin')
#         self.assertEqual(result['ticker'], 'LMT')
        
#         # Test invalid name
#         result = get_stock_by_name('Invalid Company')
#         self.assertIsNone(result)

#     def test_get_stock_by_ticker(self):
#         """Test getting stock by ticker"""
#         # Test valid ticker
#         result = get_stock_by_ticker('LMT')
#         self.assertEqual(result['name'], 'Lockheed Martin')
        
#         # Test case insensitive
#         result = get_stock_by_ticker('lmt')
#         self.assertEqual(result['name'], 'Lockheed Martin')
        
#         # Test invalid ticker
#         result = get_stock_by_ticker('INVALID')
#         self.assertIsNone(result)

#     @patch('yfinance.Ticker')
#     def test_fetch_intraday_data_yahoo(self, mock_ticker):
#         """Test fetching intraday data"""
#         # Setup mock
#         mock_stock = MagicMock()
#         mock_stock.history.return_value = self.sample_history
#         mock_ticker.return_value = mock_stock

#         # Test successful data fetch
#         result = fetch_intraday_data_yahoo('LMT')
#         self.assertIsNotNone(result)
#         self.assertEqual(len(result), 2)  # Two data points
        
#         # Test empty data
#         mock_stock.history.return_value = pd.DataFrame()
#         result = fetch_intraday_data_yahoo('LMT')
#         self.assertIsNone(result)
        
#         # Test exception handling
#         mock_stock.history.side_effect = Exception("API Error")
#         result = fetch_intraday_data_yahoo('LMT')
#         self.assertIsNone(result)

#     @patch('yfinance.Ticker')
#     def test_get_stock_data(self, mock_ticker):
#         """Test getting stock data"""
#         # Setup mock
#         mock_stock = MagicMock()
#         mock_stock.history.return_value = pd.DataFrame({
#             'Close': [100.0, 101.0, 102.0]
#         })
#         mock_ticker.return_value = mock_stock

#         # Test successful data fetch
#         result = get_stock_data('LMT')
#         self.assertEqual(len(result), 3)
#         self.assertEqual(result[0], 100.0)
        
#         # Test exception handling
#         mock_stock.history.side_effect = Exception("API Error")
#         result = get_stock_data('LMT')
#         self.assertIsNone(result)

#     @patch('yfinance.Ticker')
#     def test_get_current_price(self, mock_ticker):
#         """Test getting current stock price"""
#         # Setup mock
#         mock_stock = MagicMock()
#         mock_stock.info = {'regularMarketPrice': 100.0}
#         mock_ticker.return_value = mock_stock

#         # Test successful price fetch
#         result = get_current_price('LMT')
#         self.assertEqual(result, 100.0)
        
#         # Test empty ticker
#         result = get_current_price('')
#         self.assertIsNone(result)
        
#         # Test exception handling
#         mock_stock.info = {'regularMarketPrice': None}
#         result = get_current_price('LMT')
#         self.assertIsNone(result)

#     @patch('builtins.open', new_callable=unittest.mock.mock_open)
#     @patch('json.dump')
#     @patch('stock_data.fetch_intraday_data_yahoo')
#     def test_main_stock_data(self, mock_fetch, mock_json_dump, mock_open):
#         """Test main stock data collection function"""
#         # Setup mock
#         mock_fetch.return_value = {'timestamp': {'Open': 100.0, 'Close': 101.0}}

#         # Run function
#         main_stock_data()

#         # Verify file operations
#         mock_open.assert_called_once_with('stock_data.json', 'w')
#         mock_json_dump.assert_called_once()
        
#         # Verify data fetching
#         self.assertTrue(mock_fetch.called)

# if __name__ == '__main__':
#     unittest.main()



import unittest
from unittest.mock import patch, MagicMock
import json
import pandas as pd
from datetime import datetime
import yfinance as yf
import sys
import os

# Import the functions directly from your finance.py file
# Adjust the import statement based on your actual file name
from finance import (
    fetch_intraday_data_yahoo,
    get_stock_data,
    main_stock_data,
    get_all_stocks,
    is_valid_stock,
    get_stock_by_name,
    get_stock_by_ticker,
    get_current_price,
    stocks
)

class TestStockData(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.sample_history = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [102.0, 103.0],
            'Low': [98.0, 99.0],
            'Close': [101.0, 102.0],
            'Volume': [1000, 1100]
        }, index=[
            datetime(2024, 1, 1, 9, 30),
            datetime(2024, 1, 1, 9, 45)
        ])

    def test_get_all_stocks(self):
        """Test getting all stocks"""
        result = get_all_stocks()
        self.assertEqual(result, stocks)
        self.assertTrue(any(stock['ticker'] == 'LMT' for stock in result))

    def test_is_valid_stock(self):
        """Test stock validation"""
        self.assertTrue(is_valid_stock('LMT'))
        self.assertFalse(is_valid_stock('INVALID'))
        # Changed: Only test for invalid tickers, not empty strings
        self.assertFalse(is_valid_stock('NONEXISTENT'))

    def test_get_stock_by_name(self):
        """Test getting stock by company name"""
        result = get_stock_by_name('Lockheed Martin')
        self.assertEqual(result['ticker'], 'LMT')
        
        result = get_stock_by_name('lockheed martin')
        self.assertEqual(result['ticker'], 'LMT')
        
        result = get_stock_by_name('Invalid Company')
        self.assertIsNone(result)

    def test_get_stock_by_ticker(self):
        """Test getting stock by ticker"""
        result = get_stock_by_ticker('LMT')
        self.assertEqual(result['name'], 'Lockheed Martin')
        
        result = get_stock_by_ticker('lmt')
        self.assertEqual(result['name'], 'Lockheed Martin')
        
        result = get_stock_by_ticker('INVALID')
        self.assertIsNone(result)

    @patch('yfinance.Ticker')
    def test_fetch_intraday_data_yahoo(self, mock_ticker):
        """Test fetching intraday data"""
        mock_stock = MagicMock()
        mock_stock.history.return_value = self.sample_history
        mock_ticker.return_value = mock_stock

        result = fetch_intraday_data_yahoo('LMT')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        
        mock_stock.history.return_value = pd.DataFrame()
        result = fetch_intraday_data_yahoo('LMT')
        self.assertIsNone(result)

    @patch('yfinance.Ticker')
    def test_get_stock_data(self, mock_ticker):
        """Test getting stock data"""
        mock_stock = MagicMock()
        mock_stock.history.return_value = pd.DataFrame({
            'Close': [100.0, 101.0, 102.0]
        })
        mock_ticker.return_value = mock_stock

        result = get_stock_data('LMT')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)

    @patch('yfinance.Ticker')
    def test_get_current_price(self, mock_ticker):
        """Test getting current stock price"""
        mock_stock = MagicMock()
        mock_stock.info = {'regularMarketPrice': 100.0}
        mock_ticker.return_value = mock_stock

        result = get_current_price('LMT')
        self.assertEqual(result, 100.0)
        
        result = get_current_price('')
        self.assertIsNone(result)

    @patch('finance.fetch_intraday_data_yahoo')  # Changed from stock_data to finance
    @patch('json.dump')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_main_stock_data(self, mock_open, mock_json_dump, mock_fetch):
        """Test main stock data collection function"""
        # Setup mock data
        mock_data = {'timestamp': {'Open': 100.0, 'Close': 101.0}}
        mock_fetch.return_value = mock_data

        # Run function
        main_stock_data()

        # Verify file was opened
        mock_open.assert_called_once_with('stock_data.json', 'w')
        
        # Verify json.dump was called
        self.assertTrue(mock_json_dump.called)

if __name__ == '__main__':
    unittest.main()
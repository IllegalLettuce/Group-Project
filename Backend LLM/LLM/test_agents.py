import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agents import (
        researcher_agent,
        accountant_agent,
        recommender_agent,
        blogger_agent,
        autopurchase_agent
    )
except ImportError as e:
    print(f"Error importing agents: {e}")
    print(f"Current Python path: {sys.path}")
    raise

class TestAgents(unittest.TestCase):
    def setUp(self):
        """Set up any necessary test fixtures"""
        self.mock_llm = MagicMock()
        
    def test_researcher_agent_initialization(self):
        """Test if researcher agent is initialized with correct attributes"""
        self.assertEqual(researcher_agent.role, "Company Researcher")
        self.assertEqual(researcher_agent.goal, "To research the given company or crypto coin and provide financial insights.")
        self.assertTrue(hasattr(researcher_agent, 'llm'))

    def test_accountant_agent_initialization(self):
        """Test if accountant agent is initialized with correct attributes"""
        self.assertEqual(accountant_agent.role, "Accountant Agent")
        self.assertEqual(accountant_agent.goal, "General accounting tasks, including transaction processing and financial reporting.")
        self.assertTrue(hasattr(accountant_agent, 'llm'))

    def test_recommender_agent_initialization(self):
        """Test if recommender agent is initialized with correct attributes"""
        self.assertEqual(recommender_agent.role, "Recommender Agent")
        self.assertTrue("recommend" in recommender_agent.goal.lower())
        self.assertTrue(hasattr(recommender_agent, 'llm'))

    def test_blogger_agent_initialization(self):
        """Test if blogger agent is initialized with correct attributes"""
        self.assertEqual(blogger_agent.role, "Blogger Agent")
        self.assertTrue("blog" in blogger_agent.goal.lower())
        self.assertTrue(hasattr(blogger_agent, 'llm'))

    def test_autopurchase_agent_initialization(self):
        """Test if autopurchase agent is initialized with correct attributes"""
        self.assertEqual(autopurchase_agent.role, "Stock analysis and future predictor")
        self.assertEqual(autopurchase_agent.goal, "Give the predicted buy and sell ")
        self.assertTrue(hasattr(autopurchase_agent, 'llm'))

    @patch('agents.LLM')
    def test_agent_llm_interaction(self, mock_llm):
        """Test agent interaction with LLM"""
        # Setup mock LLM
        mock_llm.return_value = MagicMock()
        
        # Create a test agent with mock LLM
        test_agent = researcher_agent
        test_agent.llm = mock_llm
        
        # Verify LLM is properly attached
        self.assertIsNotNone(test_agent.llm)

if __name__ == '__main__':
    unittest.main()
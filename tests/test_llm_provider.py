import unittest
from unittest.mock import patch, MagicMock

from src.test_coverage_agent.test_generation.llm_provider import (
    LLMProvider,
    ClaudeProvider,
    GeminiProvider,
    LLMProviderFactory
)


class TestLLMProvider(unittest.TestCase):
    """Test cases for the LLM provider module."""

    def test_claude_provider_name(self):
        """Test that Claude provider returns the correct name."""
        provider = ClaudeProvider("test_api_key")
        self.assertEqual(provider.get_name(), "claude")

    def test_gemini_provider_name(self):
        """Test that Gemini provider returns the correct name."""
        provider = GeminiProvider("test_api_key")
        self.assertEqual(provider.get_name(), "gemini")

    @patch("langchain_community.chat_models.ChatAnthropic")
    def test_claude_provider_model(self, mock_chat_anthropic):
        """Test that Claude provider initializes the model correctly."""
        # Setup mock
        mock_instance = MagicMock()
        mock_chat_anthropic.return_value = mock_instance

        # Create provider and get model
        provider = ClaudeProvider("test_api_key", model_name="test-model", temperature=0.5)
        model = provider.get_model()

        # Check that the model was initialized correctly
        mock_chat_anthropic.assert_called_once_with(
            anthropic_api_key="test_api_key",
            model_name="test-model",
            temperature=0.5
        )
        self.assertEqual(model, mock_instance)

    @patch("langchain_google_genai.ChatGoogleGenerativeAI")
    def test_gemini_provider_model(self, mock_chat_gemini):
        """Test that Gemini provider initializes the model correctly."""
        # Setup mock
        mock_instance = MagicMock()
        mock_chat_gemini.return_value = mock_instance

        # Create provider and get model
        provider = GeminiProvider("test_api_key", model_name="test-model", temperature=0.5)
        model = provider.get_model()

        # Check that the model was initialized correctly
        mock_chat_gemini.assert_called_once_with(
            google_api_key="test_api_key",
            model="test-model",
            temperature=0.5
        )
        self.assertEqual(model, mock_instance)

    def test_factory_creates_claude_provider(self):
        """Test that factory creates Claude provider correctly."""
        provider = LLMProviderFactory.create_provider("claude", "test_api_key")
        self.assertIsInstance(provider, ClaudeProvider)
        self.assertEqual(provider.api_key, "test_api_key")

    def test_factory_creates_gemini_provider(self):
        """Test that factory creates Gemini provider correctly."""
        provider = LLMProviderFactory.create_provider("gemini", "test_api_key")
        self.assertIsInstance(provider, GeminiProvider)
        self.assertEqual(provider.api_key, "test_api_key")

    def test_factory_with_additional_params(self):
        """Test that factory passes additional parameters correctly."""
        provider = LLMProviderFactory.create_provider(
            "claude", 
            "test_api_key", 
            model_name="custom-model", 
            temperature=0.1
        )
        self.assertEqual(provider.model_name, "custom-model")
        self.assertEqual(provider.temperature, 0.1)

    def test_factory_invalid_provider(self):
        """Test that factory raises error for invalid provider."""
        with self.assertRaises(ValueError):
            LLMProviderFactory.create_provider("invalid_provider", "test_api_key")


if __name__ == "__main__":
    unittest.main()
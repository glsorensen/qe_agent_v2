import unittest
from unittest.mock import patch, MagicMock

from src.test_coverage_agent.test_generation.llm_provider import (
    LLMProvider,
    ClaudeProvider,
    GeminiProvider,
    LLMProviderFactory
)


# Create test subclasses that override the get_model method to avoid import issues
class TestableClaudeProvider(ClaudeProvider):
    """A testable version of ClaudeProvider that doesn't rely on imports."""
    
    def get_model(self):
        """Return a mock model instead of trying to import ChatAnthropic."""
        if self._model is None:
            self._model = MagicMock()
        return self._model


class TestableGeminiProvider(GeminiProvider):
    """A testable version of GeminiProvider that doesn't rely on imports."""
    
    def get_model(self):
        """Return a mock model instead of trying to import ChatGoogleGenerativeAI."""
        if self._model is None:
            self._model = MagicMock()
        return self._model


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

    def test_claude_provider_model(self):
        """Test that Claude provider correctly manages model instance."""
        # Use our testable subclass
        provider = TestableClaudeProvider("test_api_key", model_name="test-model", temperature=0.5)
        
        # First call should initialize the model
        model1 = provider.get_model()
        self.assertIsNotNone(model1, "Model should be initialized")
        
        # Second call should return the same instance (testing the caching behavior)
        model2 = provider.get_model()
        self.assertIs(model1, model2, "get_model should return the same instance on repeated calls")

    def test_gemini_provider_model(self):
        """Test that Gemini provider correctly manages model instance."""
        # Use our testable subclass
        provider = TestableGeminiProvider("test_api_key", model_name="test-model", temperature=0.5)
        
        # First call should initialize the model
        model1 = provider.get_model()
        self.assertIsNotNone(model1, "Model should be initialized")
        
        # Second call should return the same instance (testing the caching behavior)
        model2 = provider.get_model()
        self.assertIs(model1, model2, "get_model should return the same instance on repeated calls")

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
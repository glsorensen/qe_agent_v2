from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def get_model(self) -> BaseChatModel:
        """Get the language model instance.
        
        Returns:
            An instance of a language model
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the provider.
        
        Returns:
            Provider name as a string
        """
        pass


class ClaudeProvider(LLMProvider):
    """Anthropic's Claude API provider."""
    
    def __init__(self, api_key: str, model_name: str = "claude-3-7-sonnet-20250219", temperature: float = 0.2):
        """Initialize the Claude provider.
        
        Args:
            api_key: Anthropic API key
            model_name: Claude model name to use
            temperature: Temperature parameter for generation
        """
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self._model = None
    
    def get_model(self) -> BaseChatModel:
        """Get the Claude model instance.
        
        Returns:
            An instance of the Claude model
        """
        if self._model is None:
            try:
                # Try using direct Anthropic integration
                from langchain_anthropic import ChatAnthropic
                self._model = ChatAnthropic(
                    api_key=self.api_key,
                    model_name=self.model_name,
                    temperature=self.temperature
                )
            except (ImportError, AttributeError) as e:
                # Fall back to community implementation if there's an issue
                print(f"Warning: Error with langchain_anthropic: {e}, falling back to community implementation")
                from langchain_community.chat_models import ChatAnthropic
                self._model = ChatAnthropic(
                    anthropic_api_key=self.api_key,
                    model_name=self.model_name,
                    temperature=self.temperature
                )
        return self._model
    
    def get_name(self) -> str:
        """Get the name of the provider.
        
        Returns:
            'claude' as a string
        """
        return "claude"


class GeminiProvider(LLMProvider):
    """Google's Gemini API provider."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-pro", temperature: float = 0.2):
        """Initialize the Gemini provider.
        
        Args:
            api_key: Google API key
            model_name: Gemini model name to use
            temperature: Temperature parameter for generation
        """
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self._model = None
    
    def get_model(self) -> BaseChatModel:
        """Get the Gemini model instance.
        
        Returns:
            An instance of the Gemini model
        """
        if self._model is None:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self._model = ChatGoogleGenerativeAI(
                    google_api_key=self.api_key,
                    model=self.model_name,
                    temperature=self.temperature,
                    convert_system_message_to_human=True
                )
            except (ImportError, AttributeError) as e:
                # Fall back if there's an issue
                print(f"Warning: Error with langchain_google_genai: {e}, trying alternative implementation")
                try:
                    from langchain_community.chat_models import ChatGoogleGenerativeAI
                    self._model = ChatGoogleGenerativeAI(
                        google_api_key=self.api_key,
                        model=self.model_name,
                        temperature=self.temperature,
                        convert_system_message_to_human=True
                    )
                except Exception as e2:
                    raise ImportError(f"Failed to initialize Gemini provider: {e2}") from e2
        return self._model
    
    def get_name(self) -> str:
        """Get the name of the provider.
        
        Returns:
            'gemini' as a string
        """
        return "gemini"


class LLMProviderFactory:
    """Factory for creating LLM provider instances."""
    
    @staticmethod
    def create_provider(provider_name: str, api_key: str, **kwargs) -> LLMProvider:
        """Create an LLM provider instance based on name.
        
        Args:
            provider_name: Name of the provider ('claude' or 'gemini')
            api_key: API key for the provider
            **kwargs: Additional provider-specific configuration
            
        Returns:
            An LLM provider instance
            
        Raises:
            ValueError: If the provider name is not supported
        """
        if provider_name.lower() == "claude":
            return ClaudeProvider(api_key, **kwargs)
        elif provider_name.lower() == "gemini":
            return GeminiProvider(api_key, **kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")

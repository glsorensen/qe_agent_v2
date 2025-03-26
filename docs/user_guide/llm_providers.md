# LLM Providers

The Test Coverage Agent supports multiple large language model (LLM) providers for AI-powered test generation. This allows you to choose the provider that best fits your needs in terms of performance, cost, and availability.

## Supported Providers

### Claude

[Claude](https://www.anthropic.com/claude) is an AI assistant created by Anthropic that excels at complex reasoning and thorough task completion. The Test Coverage Agent uses Claude's API to analyze code and generate comprehensive tests.

```bash
# Use Claude as the LLM provider
python run.py /path/to/repo --generate --api-key YOUR_CLAUDE_API_KEY --llm-provider claude
```

### Gemini

[Gemini](https://ai.google/gemini/) is Google's advanced AI model designed for multimodal reasoning and coding tasks. The Test Coverage Agent can leverage Gemini's capabilities for test generation.

```bash
# Use Gemini as the LLM provider
python run.py /path/to/repo --generate --api-key YOUR_GEMINI_API_KEY --llm-provider gemini
```

## Configuring Providers

You can configure the LLM provider using command-line arguments, environment variables, or the configuration file.

### Command-line Arguments

```bash
# Specify the provider and API key
python run.py /path/to/repo --generate --llm-provider claude --api-key YOUR_API_KEY
```

### Environment Variables

```bash
# Set environment variables
export TEST_COVERAGE_AGENT_LLM_PROVIDER=gemini
export TEST_COVERAGE_AGENT_API_KEY=YOUR_API_KEY

# Run the agent
python run.py /path/to/repo --generate
```

### Configuration File

Create a `.test-coverage-agent.yaml` file in your repository:

```yaml
# Test generation settings
generation:
  template: standard
  ai_mode: generate
  llm_provider: claude  # or gemini
```

## Web Interface

The web interface allows you to select the LLM provider and enter the API key in the sidebar:

1. Start the web interface: `python run.py --web`
2. Select the LLM provider from the dropdown menu in the sidebar
3. Enter your API key
4. Proceed with test generation

## Extending with New Providers

The Test Coverage Agent's modular architecture allows for easy integration of additional LLM providers. See the [Developer Guide](../developer_guide/extending.md) for information on adding support for other providers.
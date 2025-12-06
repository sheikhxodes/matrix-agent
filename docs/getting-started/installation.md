# Installation

## Prerequisites

- Python 3.11+
- Google API Key (for Gemini)

## Install from Source

```bash
# Clone the repository
git clone https://github.com/sheikhxodes/matrix-agent.git
cd matrix-agent

# Install dependencies
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file or export the variable:

```bash
export GOOGLE_API_KEY="your-google-api-key"
```

## Verify Installation

```bash
python -c "from agents.coordinator import coordinator_agent; print('✓ Installation successful')"
```

## Development Dependencies

For development and testing:

```bash
pip install pytest pytest-asyncio ruff mkdocs-material mkdocstrings[python]
```

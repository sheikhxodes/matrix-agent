"""Tests for Matrix Coordinator Agent"""

import pytest


def test_coordinator_import():
    """Test that coordinator can be imported."""
    from agents.coordinator import coordinator_agent
    assert coordinator_agent is not None
    assert coordinator_agent.name == "matrix_coordinator"


def test_sub_agents_exist():
    """Test that all sub-agents are registered."""
    from agents.coordinator import coordinator_agent
    sub_agent_names = [agent.name for agent in coordinator_agent.sub_agents]
    
    expected = ["planner_agent", "code_agent", "ppt_agent", "research_agent", "multimodal_agent"]
    for name in expected:
        assert name in sub_agent_names, f"Missing sub-agent: {name}"


def test_thinking_instruction_present():
    """Test that thinking instruction is in coordinator."""
    from agents.coordinator import coordinator_agent
    assert "<think>" in coordinator_agent.instruction
    assert "</think>" in coordinator_agent.instruction


def test_matrix_agent_class():
    """Test MatrixAgent class initialization."""
    from main import MatrixAgent
    agent = MatrixAgent()
    assert agent.agent is not None
    assert agent.session is None  # Not initialized yet

#!/usr/bin/env python3
"""
Test script for the MCP AI POC server.
Tests basic MCP server functionality.
"""

import sys
import os
from pathlib import Path
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.mark.asyncio
async def test_mcp_server():
    """Test the MCP server JSON-RPC functionality."""
    print("\nTesting MCP server...")
    try:
        from mcp_poc.standalone_server import JSONRPCServer

        # Test server creation
        server = JSONRPCServer("test-server")
        print("✓ MCP server creation successful")

        # Test initialize method
        _ = await server.handle_initialize({})
        print("✓ Initialize handler works")

        # Test tools listing
        tools_response = await server.handle_list_tools({})
        print(f"✓ Tools listing works ({len(tools_response['tools'])} tools)")

        # Test prompts listing
        prompts_response = await server.handle_list_prompts({})
        print(f"✓ Prompts listing works ({len(prompts_response['prompts'])} prompts)")

        # Test resources listing
        resources_response = await server.handle_list_resources({})
        print(
            f"✓ Resources listing works ({len(resources_response['resources'])} resources)"
        )

        assert True  # Test passed
    except Exception as e:
        print(f"✗ MCP server test failed: {e}")
        assert False, f"MCP server test failed: {e}"


@pytest.mark.asyncio
async def test_json_rpc_format():
    """Test JSON-RPC request/response format."""
    print("\nTesting JSON-RPC format...")
    try:
        from mcp_poc.standalone_server import JSONRPCServer

        server = JSONRPCServer("test-server")

        # Test valid request
        request = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}

        response = await server.handle_request(request)

        # Check response format
        assert "jsonrpc" in response
        assert "id" in response
        assert "result" in response
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1

        print("✓ JSON-RPC format validation successful")

        # Test invalid method
        invalid_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "nonexistent_method",
            "params": {},
        }

        error_response = await server.handle_request(invalid_request)
        assert "error" in error_response
        print("✓ Error handling works correctly")

    except Exception as e:
        print(f"✗ JSON-RPC format test failed: {e}")
        assert False, f"JSON-RPC format test failed: {e}"


@pytest.mark.asyncio
async def test_resource_content():
    """Test that resources return expected content."""
    print("\nTesting resource content...")
    try:
        from mcp_poc.standalone_server import JSONRPCServer

        server = JSONRPCServer("test-server")

        # Test Python guidelines resource
        response = await server.handle_read_resource(
            {"uri": "coding-guidelines://python"}
        )

        content = response["contents"][0]["text"]
        assert "Python Coding Guidelines" in content
        assert "PEP 8" in content
        print("✓ Python guidelines resource content valid")

        # Test design patterns resource
        response = await server.handle_read_resource(
            {"uri": "patterns://design-patterns"}
        )

        content = response["contents"][0]["text"]
        assert "Design Patterns" in content
        assert "Singleton" in content
        print("✓ Design patterns resource content valid")

    except Exception as e:
        print(f"✗ Resource content test failed: {e}")
        assert False, f"Resource content test failed: {e}"


def test_project_structure():
    """Test that all expected files exist."""
    print("\nTesting project structure...")

    required_files = [
        "src/mcp_poc/__init__.py",
        "src/mcp_poc/app.py",
        "src/mcp_poc/ai_tools.py",
        "src/mcp_poc/standalone_server.py",
        "requirements.txt",
        "pyproject.toml",
        "README.md",
        "src/run.py",
        "mcp_config.json",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        assert False, f"Missing files: {missing_files}"
    else:
        print(f"✓ All {len(required_files)} required files present")
        assert True


def run_async_tests():
    """Run async tests. (This function is not a test itself)"""
    # This function is no longer needed since pytest handles async tests directly
    pass


def main_runner():
    """Run all tests. (This function is not a test itself)"""
    # This function is no longer needed since pytest handles test execution
    pass


if __name__ == "__main__":
    # For standalone execution (not when run via pytest)
    print("This file contains pytest tests. Run with: pytest src/test_server.py")
    print("For the full test suite, run: pytest")

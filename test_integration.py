#!/usr/bin/env python3
"""Test script for Ubox Cameras Home Assistant integration."""

import asyncio
import json
import os
import sys
from pathlib import Path


def test_file_structure():
    """Test that all required files exist."""
    print("Testing file structure...")

    required_files = [
        "custom_components/ubox-camera-ha/__init__.py",
        "custom_components/ubox-camera-ha/api.py",
        "custom_components/ubox-camera-ha/config_flow.py",
        "custom_components/ubox-camera-ha/const.py",
        "custom_components/ubox-camera-ha/manifest.json",
        "custom_components/ubox-camera-ha/sensor.py",
        "custom_components/ubox-camera-ha/strings.json",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True


def test_manifest():
    """Test manifest.json structure."""
    print("Testing manifest.json...")

    try:
        with open("custom_components/ubox-camera-ha/manifest.json", "r") as f:
            manifest = json.load(f)

        required_keys = ["domain", "name", "config_flow", "requirements", "version"]
        missing_keys = [key for key in required_keys if key not in manifest]

        if missing_keys:
            print(f"❌ Missing manifest keys: {missing_keys}")
            return False

        if manifest["domain"] != "ubox-camera-ha":
            print(f"❌ Wrong domain: {manifest['domain']}")
            return False

        print("✅ Manifest structure valid")
        return True

    except Exception as e:
        print(f"❌ Manifest error: {e}")
        return False


def test_strings():
    """Test strings.json structure."""
    print("Testing strings.json...")

    try:
        with open("custom_components/ubox-camera-ha/strings.json", "r") as f:
            strings = json.load(f)

        if "config" not in strings:
            print("❌ Missing 'config' section in strings.json")
            return False

        config = strings["config"]
        if "step" not in config or "error" not in config:
            print("❌ Missing required sections in config")
            return False

        print("✅ Strings structure valid")
        return True

    except Exception as e:
        print(f"❌ Strings error: {e}")
        return False


def test_imports():
    """Test that Python files can be imported without syntax errors."""
    print("Testing Python imports...")

    # Add the custom_components directory to Python path
    sys.path.insert(0, str(Path("custom_components").absolute()))

    try:
        # Test importing the const module
        from ubox-camera-ha import const

        print("✅ Constants module imports successfully")

        # Check that required constants exist
        required_constants = ["DOMAIN", "SENSOR_TYPES", "API_BASE_URL"]
        for constant in required_constants:
            if not hasattr(const, constant):
                print(f"❌ Missing constant: {constant}")
                return False

        print("✅ All required constants present")
        return True

    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


async def test_api_structure():
    """Test API client structure."""
    print("Testing API client structure...")

    try:
        sys.path.insert(0, str(Path("custom_components").absolute()))
        from ubox-camera-ha.api import UboxApiClient, UboxApiError, UboxAuthError

        # Check that the class has required methods
        required_methods = ["authenticate", "get_device_list", "close"]
        for method in required_methods:
            if not hasattr(UboxApiClient, method):
                print(f"❌ Missing method: {method}")
                return False

        print("✅ API client structure valid")
        return True

    except Exception as e:
        print(f"❌ API structure error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Ubox Cameras Home Assistant Integration\n")

    tests = [
        test_file_structure,
        test_manifest,
        test_strings,
        test_imports,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        print()

    # Run async test
    try:
        result = asyncio.run(test_api_structure())
        results.append(result)
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        results.append(False)

    print("=" * 50)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
        print("\n✅ Integration is ready for installation in Home Assistant")
    else:
        print(f"❌ {total - passed} test(s) failed ({passed}/{total})")
        print("\n🔧 Please fix the issues before installing")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

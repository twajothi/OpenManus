#!/usr/bin/env python3
"""
MVP Setup Script for OpenManus
Installs minimal dependencies and sets up configuration
"""

import subprocess
import sys
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """Run shell command"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0

def main():
    """Setup MVP environment"""
    print("🚀 Setting up OpenManus MVP...")
    
    print("\n📦 Installing MVP dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r requirements_mvp.txt"):
        print("❌ Failed to install dependencies")
        return False
    
    config_dir = Path("config")
    config_file = config_dir / "config.toml"
    mvp_config = config_dir / "mvp_config.toml"
    
    if not config_file.exists() and mvp_config.exists():
        print("\n⚙️ Setting up configuration...")
        shutil.copy(mvp_config, config_file)
        print(f"📝 Copied {mvp_config} to {config_file}")
        print("🔑 Please edit config/config.toml with your API key")
    
    workspace = Path("workspace")
    workspace.mkdir(exist_ok=True)
    print(f"📁 Created workspace directory: {workspace}")
    
    print("\n✅ MVP setup complete!")
    print("\n🎯 Next steps:")
    print("1. Edit config/config.toml with your LLM API key")
    print("2. Run: python mvp_main.py")
    print("3. Or run tests: python -m pytest tests/test_mvp.py -v")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

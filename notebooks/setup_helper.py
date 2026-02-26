"""
Setup Helper for Glean API Connectors Notebook

This module handles automatic dependency installation across different environments:
- Google Colab (uses pip install)
- Local Jupyter/VS Code/Cursor (uses requirements.txt or pip install)

Usage in notebook:
    from setup_helper import install_requirements
    install_requirements()
"""

import sys
import subprocess
import os


def is_colab_environment():
    """
    Detect if running in Google Colab environment.
    
    Returns:
        bool: True if in Colab, False otherwise
    """
    try:
        import google.colab
        return True
    except ImportError:
        return False


def install_packages_individually(packages):
    """
    Install packages one by one using pip.
    
    Args:
        packages: List of package names to install
        
    Returns:
        tuple: (success_count, failure_count)
    """
    success = 0
    failed = 0
    
    for package in packages:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-q", package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            success += 1
        except subprocess.CalledProcessError:
            failed += 1
            print(f"⚠️  Warning: Could not install {package}")
    
    return success, failed


def install_from_requirements(requirements_path):
    """
    Install packages from requirements.txt file.
    
    Args:
        requirements_path: Path to requirements.txt file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "-r", requirements_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def find_requirements_file():
    """
    Search for requirements.txt in common locations.
    
    Returns:
        str or None: Path to requirements.txt if found, None otherwise
    """
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check common locations
    possible_paths = [
        os.path.join(current_dir, '..', 'requirements.txt'),  # Parent directory
        os.path.join(current_dir, 'requirements.txt'),         # Same directory
        os.path.join(current_dir, '..', '..', 'requirements.txt'),  # Two levels up
    ]
    
    for path in possible_paths:
        normalized_path = os.path.normpath(path)
        if os.path.exists(normalized_path):
            return normalized_path
    
    return None


def install_requirements():
    """
    Install required packages automatically based on environment.
    
    This is the main function called from the notebook.
    """
    # Detect environment
    IN_COLAB = is_colab_environment()
    
    if IN_COLAB:
        print("🔍 Detected Google Colab environment")
    else:
        print("🔍 Detected local environment (VSCode/Cursor)")
    
    # Define required packages
    required_packages = ['requests', 'python-dotenv', 'ipykernel', 'black', 'ruff']
    
    if IN_COLAB:
        # In Colab, install packages directly
        print("📦 Installing required packages...")
        success, failed = install_packages_individually(required_packages)
        
        if failed > 0:
            print(f"⚠️  {failed} package(s) failed to install")
        
    else:
        # In local environment, try requirements.txt first
        requirements_path = find_requirements_file()
        
        if requirements_path:
            print(f"📦 Installing from requirements.txt...")
            if install_from_requirements(requirements_path):
                print("✅ Installed from requirements.txt")
            else:
                print("⚠️  requirements.txt installation failed, trying individual packages...")
                success, failed = install_packages_individually(required_packages)
        else:
            # Fallback to individual packages
            print("📦 Installing required packages...")
            success, failed = install_packages_individually(required_packages)
    
    print("✅ Setup complete! All dependencies installed.")


# Allow this module to be run directly for testing
if __name__ == "__main__":
    install_requirements()


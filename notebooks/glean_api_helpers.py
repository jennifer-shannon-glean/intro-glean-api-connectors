"""
Glean API Key Management Helper Functions

This module provides universal API key loading that works across:
- Google Colab (using userdata secrets)
- Local Jupyter/VS Code/Cursor (using .env files)
- Manual input fallback

Usage in notebook:
    from glean_api_helpers import load_all_api_keys
    api_keys = load_all_api_keys()
"""

import os

# Placeholder values that are invalid
INVALID_PLACEHOLDERS = [
    'your_client_api_token_here', 'your_client_token_here',
    'your_indexing_api_token_here', 'your_indexing_token_here',
    'your_api_token_here', 'your_token_here', 'your_key_here',
    'paste_your_token_here', 'add_your_token_here'
]


def is_valid_key(key):
    """
    Check if an API key is valid (not empty or placeholder).
    
    Args:
        key: The API key string to validate
        
    Returns:
        bool: True if key is valid, False if empty or placeholder
    """
    if not key or not key.strip():
        return False
    
    key_lower = key.strip().lower()
    
    # Check against known placeholder patterns
    if key_lower in INVALID_PLACEHOLDERS:
        return False
    
    # Check for generic placeholder pattern (contains both "your_" and "_here")
    if 'your_' in key_lower and '_here' in key_lower:
        return False
    
    return True


def get_api_key(key_name, colab_secret_name=None, required=True):
    """
    Universal API key loader that works across all environments.
    
    Priority order:
    1. Google Colab secrets (if in Colab)
    2. .env file (for local development)
    3. Environment variables
    4. Manual input (fallback if required=True)
    
    Args:
        key_name: Name of the environment variable (e.g., 'GLEAN_CLIENT_API')
        colab_secret_name: Name in Colab secrets (defaults to key_name with underscores→hyphens)
        required: If True, will prompt for manual input if not found
    
    Returns:
        Tuple of (api_key, source) where source is 'colab', 'env_file', 'env_var', 'manual', or None
    """
    # Default Colab secret name: replace underscores with hyphens
    if colab_secret_name is None:
        colab_secret_name = key_name.replace('_', '-')
    
    found_placeholder = False
    
    # Try Google Colab secrets first
    try:
        from google.colab import userdata
        api_key = userdata.get(colab_secret_name)
        if api_key and is_valid_key(api_key):
            print(f"✅ Loaded {key_name} from Google Colab secrets")
            return (api_key, 'colab')
        elif api_key and not is_valid_key(api_key):
            print(f"❌ {key_name} in Colab secrets contains placeholder text")
            print(f"   Please replace it with your actual API token")
            found_placeholder = True
    except ImportError:
        pass
    except Exception as e:
        print(f"⚠️  Could not access Colab secret '{colab_secret_name}': {e}")
    
    # Try .env file (local development)
    try:
        from dotenv import load_dotenv
        
        # Look for .env in multiple locations
        # Use override=True to prioritize .env values over cached environment variables
        load_dotenv(override=True)
        load_dotenv(dotenv_path='../.env', override=True)
        load_dotenv(dotenv_path='../../.env', override=True)
        
        api_key = os.getenv(key_name)
        if api_key and is_valid_key(api_key):
            print(f"✅ Loaded {key_name} from .env file")
            return (api_key, 'env_file')
        elif api_key and not is_valid_key(api_key):
            print(f"❌ {key_name} in .env file contains placeholder text: '{api_key}'")
            print(f"   Please replace it with your actual API token in your .env file")
            found_placeholder = True
    except Exception as e:
        pass
    
    # Try system environment variables
    api_key = os.environ.get(key_name)
    if api_key and is_valid_key(api_key):
        print(f"✅ Loaded {key_name} from environment variables")
        return (api_key, 'env_var')
    elif api_key and not is_valid_key(api_key):
        print(f"❌ {key_name} environment variable contains placeholder text")
        print(f"   Please set it to your actual API token")
        found_placeholder = True
    
    # If we found a placeholder, don't prompt - user needs to fix their config
    if found_placeholder:
        return (None, None)  # Return tuple with None values
    
    # If not found and required, prompt for manual input
    if required:
        print(f"\n❌ Could not find {key_name} in any configuration")
        print(f"💡 Setup instructions:")
        print(f"   • Colab: Add secret '{colab_secret_name}' in the 🔑 Secrets panel")
        print(f"   • Local: Add '{key_name}=your_real_token' to a .env file")
        print(f"\n⚠️  Note: This cell will wait for input. Press Ctrl+C to cancel.")
        
        try:
            api_key = input(f"\nEnter your {key_name} (or press Enter to skip): ").strip()
            
            if api_key and is_valid_key(api_key):
                print(f"✅ Using manually entered {key_name}")
                return (api_key, 'manual')
            elif api_key:
                print(f"⚠️  The value you entered appears to be a placeholder")
                return (None, None)
            else:
                print(f"⚠️  Skipped {key_name} - some functionality may not work")
                return (None, None)
        except (KeyboardInterrupt, EOFError):
            print(f"\n⚠️  Input cancelled - {key_name} not configured")
            return (None, None)
    
    return (None, None)


def load_all_api_keys():
    """
    Load all required API keys for the Glean lab.
    
    This function loads both GLEAN_CLIENT_API and GLEAN_INDEX_API keys,
    validates them, and provides smart error messages based on the current
    configuration state.
    
    Returns:
        dict: Dictionary with 'client' and 'index' keys containing API tokens
              (or None if not found)
    """
    print("=" * 60)
    print("🔐 LOADING GLEAN API KEYS")
    print("=" * 60)
    
    # Load both required keys (returns tuple of (key, source))
    client_key, client_source = get_api_key('GLEAN_CLIENT_API', 'GLEAN-CLIENT-API', required=True)
    index_key, index_source = get_api_key('GLEAN_INDEX_API', 'GLEAN-INDEX-API', required=True)
    
    # Store keys in dictionary
    keys = {
        'client': client_key,
        'index': index_key
    }
    
    # Validation summary
    print("\n" + "=" * 60)
    print("📋 API KEY STATUS SUMMARY")
    print("=" * 60)
    
    if client_key:
        source_map = {'colab': 'Google Colab', 'env_file': '.env file', 'env_var': 'environment variable', 'manual': 'manual input'}
        source_name = source_map.get(client_source, 'unknown')
        print(f"✅ GLEAN-CLIENT-API: Loaded from {source_name}")
    else:
        print("❌ GLEAN-CLIENT-API: NOT FOUND")
    
    if index_key:
        source_map = {'colab': 'Google Colab', 'env_file': '.env file', 'env_var': 'environment variable', 'manual': 'manual input'}
        source_name = source_map.get(index_source, 'unknown')
        print(f"✅ GLEAN-INDEX-API: Loaded from {source_name}")
    else:
        print("❌ GLEAN-INDEX-API: NOT FOUND")
    
    print("=" * 60)
    
    # Smart messaging based on key sources
    if not client_key and not index_key:
        # CASE 1: No keys found
        print("\n❌ ERROR: No API keys configured")
        print("\n📖 Setup Guide:")
        # Detect if likely in Colab or local
        try:
            import google.colab
            print("\n🌐 You're in Google Colab. Set up your keys:")
            print("   1. Click the 🔑 key icon in the left sidebar")
            print("   2. Click '+ Add new secret'")
            print("   3. Add BOTH secrets:")
            print("      • Name: GLEAN-CLIENT-API  → Value: [your client token]")
            print("      • Name: GLEAN-INDEX-API   → Value: [your indexing token]")
            print("   4. Enable 'Notebook access' for both")
        except ImportError:
            print("\n💻 You're in a local environment. Set up your .env file:")
            print("   1. Create a file named '.env' in the project root")
            print("   2. Add BOTH lines:")
            print("      GLEAN_CLIENT_API=your_client_token_here")
            print("      GLEAN_INDEX_API=your_indexing_token_here")
            print("   3. Replace the placeholder values with your actual tokens")
        print("\n🔄 After setup, restart the kernel and run this cell again")
        print("=" * 60)
    
    elif client_key and not index_key:
        # CASE 2: Only client key found
        print(f"\n⚠️  WARNING: Missing GLEAN-INDEX-API")
        source_map = {'colab': 'Google Colab', 'env_file': 'your .env file', 'env_var': 'environment variables'}
        print(f"\n💡 You have GLEAN-CLIENT-API configured in {source_map.get(client_source, 'unknown')}")
        
        if client_source == 'colab':
            print("\n🌐 Add the missing key to Google Colab:")
            print("   1. Click the 🔑 key icon in the left sidebar")
            print("   2. Click '+ Add new secret'")
            print("   3. Add: Name: GLEAN-INDEX-API  → Value: [your indexing token]")
            print("   4. Enable 'Notebook access'")
        elif client_source == 'env_file':
            print("\n💻 Add the missing key to your .env file:")
            print("   1. Open your .env file")
            print("   2. Add this line: GLEAN_INDEX_API=your_indexing_token_here")
            print("   3. Replace the placeholder with your actual token")
        
        print("\n🔄 After adding the key, restart the kernel and run this cell again")
        print("=" * 60)
    
    elif index_key and not client_key:
        # CASE 3: Only index key found
        print(f"\n⚠️  WARNING: Missing GLEAN-CLIENT-API")
        source_map = {'colab': 'Google Colab', 'env_file': 'your .env file', 'env_var': 'environment variables'}
        print(f"\n💡 You have GLEAN-INDEX-API configured in {source_map.get(index_source, 'unknown')}")
        
        if index_source == 'colab':
            print("\n🌐 Add the missing key to Google Colab:")
            print("   1. Click the 🔑 key icon in the left sidebar")
            print("   2. Click '+ Add new secret'")
            print("   3. Add: Name: GLEAN-CLIENT-API  → Value: [your client token]")
            print("   4. Enable 'Notebook access'")
        elif index_source == 'env_file':
            print("\n💻 Add the missing key to your .env file:")
            print("   1. Open your .env file")
            print("   2. Add this line: GLEAN_CLIENT_API=your_client_token_here")
            print("   3. Replace the placeholder with your actual token")
        
        print("\n🔄 After adding the key, restart the kernel and run this cell again")
        print("=" * 60)
    
    elif client_source != index_source:
        # CASE 4: Keys from different sources (MIXED!)
        print("\n⚠️  WARNING: API keys are configured in different locations!")
        source_map = {'colab': 'Google Colab', 'env_file': '.env file', 'env_var': 'environment variable'}
        print(f"\n   • GLEAN-CLIENT-API: {source_map.get(client_source, 'unknown')}")
        print(f"   • GLEAN-INDEX-API: {source_map.get(index_source, 'unknown')}")
        print("\n💡 For better organization, use ONE configuration method:")
        
        if 'colab' in [client_source, index_source]:
            print("\n🌐 Option A - Use Google Colab secrets (recommended for Colab):")
            print("   Move both keys to Colab secrets")
        
        if 'env_file' in [client_source, index_source]:
            print("\n💻 Option B - Use .env file (recommended for local):")
            print("   Move both keys to your .env file")
        
        print("\n🔄 After consolidating, restart the kernel and run this cell again")
        print("=" * 60)
    
    else:
        # CASE 5: Both keys found from same source
        print("\n🎉 All API keys loaded successfully! Ready to proceed.")
        print("=" * 60)
    
    return keys


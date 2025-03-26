#!/usr/bin/env python3
"""
Generate Secure Keys for ClearBox Production Environment

This script generates secure random keys for use in the ClearBox production
environment and provides instructions for updating the .env file.
"""

import os
import secrets
import argparse
import base64
from pathlib import Path

def generate_hex_key(length=32):
    """Generate a secure random hex key of specified length."""
    return secrets.token_hex(length)

def generate_base64_key(length=32):
    """Generate a secure random base64 key of specified length."""
    return base64.b64encode(os.urandom(length)).decode('utf-8')

def update_env_file(env_file, jwt_key, encryption_key):
    """Update the environment file with new keys."""
    if not os.path.exists(env_file):
        print(f"Error: {env_file} does not exist")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Replace the keys
    content = content.replace(
        'SECRET_KEY=your_production_secret_key_here', 
        f'SECRET_KEY={jwt_key}'
    )
    content = content.replace(
        'ENCRYPTION_KEY=your_production_encryption_key_here', 
        f'ENCRYPTION_KEY={encryption_key}'
    )
    
    # Write the updated content
    with open(env_file, 'w') as f:
        f.write(content)
    
    return True

def main():
    """Main function to generate keys and optionally update .env file."""
    parser = argparse.ArgumentParser(description='Generate secure keys for production')
    parser.add_argument('--env-file', help='Path to .env file to update')
    parser.add_argument('--length', type=int, default=32, help='Key length in bytes')
    args = parser.parse_args()
    
    # Generate keys
    jwt_key = generate_hex_key(args.length)
    encryption_key = generate_hex_key(args.length)
    
    # Print the keys
    print("\n== Generated Production Keys ==\n")
    print(f"JWT Secret Key: {jwt_key}")
    print(f"Encryption Key: {encryption_key}")
    print("\n================================\n")
    
    # Update .env file if specified
    if args.env_file:
        if update_env_file(args.env_file, jwt_key, encryption_key):
            print(f"Successfully updated keys in {args.env_file}")
        else:
            print(f"Failed to update {args.env_file}")
    else:
        print("To use these keys, update your production .env file with the values above")
        print("Or run this script with --env-file=/path/to/.env to update automatically")
    
    print("\nIMPORTANT: Store these keys securely and never commit them to version control")

if __name__ == "__main__":
    main() 
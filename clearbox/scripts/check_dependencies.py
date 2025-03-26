#!/usr/bin/env python3
"""
Security Check for Dependencies

This script checks Python and Node.js dependencies for security vulnerabilities
using safety (Python) and npm audit (Node.js).

Requirements:
- safety: pip install safety
- npm (for frontend dependencies)
"""

import os
import subprocess
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Configure colors for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"

def check_tool_installed(tool):
    """Check if a command-line tool is installed."""
    try:
        subprocess.run([tool, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def run_python_safety_check(requirements_file):
    """Run safety check on Python dependencies."""
    if not check_tool_installed("safety"):
        print(f"{YELLOW}Warning: 'safety' is not installed. Install with: pip install safety{RESET}")
        return False, "safety tool not installed"
    
    print(f"{BOLD}Checking Python dependencies in {requirements_file}...{RESET}")
    
    try:
        result = subprocess.run(
            ["safety", "check", "-r", requirements_file, "--json"],
            capture_output=True,
            text=True
        )
        
        # Parse the JSON output
        if result.returncode == 0:
            print(f"{GREEN}No vulnerabilities found in Python dependencies.{RESET}")
            return True, None
        else:
            try:
                vulnerabilities = json.loads(result.stdout)
                count = len(vulnerabilities['vulnerabilities'])
                print(f"{RED}Found {count} vulnerability issues in Python dependencies.{RESET}")
                
                # Print details of vulnerabilities
                for vuln in vulnerabilities['vulnerabilities']:
                    print(f"\n{BOLD}Package:{RESET} {vuln['package_name']}")
                    print(f"{BOLD}Vulnerable Version:{RESET} {vuln['vulnerable_spec']}")
                    print(f"{BOLD}Description:{RESET} {vuln['advisory']}")
                    print(f"{BOLD}Fix:{RESET} Update to version {vuln.get('fix_version', 'Not specified')}")
                
                return False, vulnerabilities
            except json.JSONDecodeError:
                print(f"{RED}Error parsing safety output.{RESET}")
                print(f"Raw output: {result.stdout}")
                return False, "Error parsing safety output"
    except Exception as e:
        print(f"{RED}Error running safety check: {e}{RESET}")
        return False, str(e)

def run_npm_audit(frontend_dir):
    """Run npm audit on Node.js dependencies."""
    if not check_tool_installed("npm"):
        print(f"{YELLOW}Warning: 'npm' is not installed.{RESET}")
        return False, "npm not installed"
    
    package_json = os.path.join(frontend_dir, "package.json")
    if not os.path.exists(package_json):
        print(f"{YELLOW}Warning: package.json not found in {frontend_dir}{RESET}")
        return False, f"package.json not found in {frontend_dir}"
    
    print(f"{BOLD}Checking frontend dependencies in {frontend_dir}...{RESET}")
    
    try:
        # Change to the frontend directory
        current_dir = os.getcwd()
        os.chdir(frontend_dir)
        
        # Run npm audit
        result = subprocess.run(
            ["npm", "audit", "--json"],
            capture_output=True,
            text=True
        )
        
        # Change back to the original directory
        os.chdir(current_dir)
        
        try:
            audit_data = json.loads(result.stdout)
            
            # Check if there are any vulnerabilities
            if audit_data.get('vulnerabilities', {}):
                vuln_count = len(audit_data.get('vulnerabilities', {}))
                print(f"{RED}Found {vuln_count} vulnerability issues in npm dependencies.{RESET}")
                
                # Print vulnerability summary
                if 'metadata' in audit_data and 'vulnerabilities' in audit_data['metadata']:
                    metadata = audit_data['metadata']['vulnerabilities']
                    print(f"\n{BOLD}Vulnerability Summary:{RESET}")
                    print(f"Critical: {metadata.get('critical', 0)}")
                    print(f"High: {metadata.get('high', 0)}")
                    print(f"Moderate: {metadata.get('moderate', 0)}")
                    print(f"Low: {metadata.get('low', 0)}")
                
                # Print advice
                if 'metadata' in audit_data and 'fix' in audit_data['metadata'] and audit_data['metadata']['fix'] != None:
                    print(f"\n{BOLD}Fix:{RESET} Run 'npm audit fix' to fix issues automatically")
                
                return False, audit_data
            else:
                print(f"{GREEN}No vulnerabilities found in npm dependencies.{RESET}")
                return True, None
        except json.JSONDecodeError:
            print(f"{RED}Error parsing npm audit output.{RESET}")
            print(f"Raw output: {result.stdout}")
            return False, "Error parsing npm audit output"
    except Exception as e:
        print(f"{RED}Error running npm audit: {e}{RESET}")
        return False, str(e)

def generate_report(python_result, npm_result, output_file=None):
    """Generate a security report from the check results."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        "# Security Dependency Check Report",
        f"Report generated on: {now}\n",
        "## Python Dependencies",
    ]
    
    if python_result[0]:
        report_lines.append("✅ No vulnerabilities found")
    else:
        report_lines.append("❌ Vulnerabilities found")
        if isinstance(python_result[1], dict) and 'vulnerabilities' in python_result[1]:
            for vuln in python_result[1]['vulnerabilities']:
                report_lines.append(f"- **{vuln['package_name']}**: {vuln['advisory']}")
    
    report_lines.append("\n## Node.js Dependencies")
    
    if npm_result[0]:
        report_lines.append("✅ No vulnerabilities found")
    else:
        report_lines.append("❌ Vulnerabilities found")
        if isinstance(npm_result[1], dict) and 'metadata' in npm_result[1] and 'vulnerabilities' in npm_result[1]['metadata']:
            metadata = npm_result[1]['metadata']['vulnerabilities']
            report_lines.append(f"- Critical: {metadata.get('critical', 0)}")
            report_lines.append(f"- High: {metadata.get('high', 0)}")
            report_lines.append(f"- Moderate: {metadata.get('moderate', 0)}")
            report_lines.append(f"- Low: {metadata.get('low', 0)}")
    
    report_lines.append("\n## Recommendations")
    report_lines.append("1. Run `pip install -r requirements.txt --upgrade` to update Python dependencies")
    report_lines.append("2. Run `npm audit fix` to automatically fix npm vulnerabilities")
    report_lines.append("3. Check for updates for critical dependencies manually")
    report_lines.append("4. Run this check regularly before deployment")
    
    report_text = "\n".join(report_lines)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"{GREEN}Report saved to {output_file}{RESET}")
    
    return report_text

def main():
    """Main function to run security checks."""
    parser = argparse.ArgumentParser(description='Check dependencies for security vulnerabilities')
    parser.add_argument('--python', help='Path to requirements.txt', default='../backend/requirements.txt')
    parser.add_argument('--frontend', help='Path to frontend directory', default='../frontend')
    parser.add_argument('--report', help='Output file for the report', default=None)
    args = parser.parse_args()
    
    # Resolve paths relative to the script location
    script_dir = Path(__file__).parent.absolute()
    python_path = Path(args.python)
    frontend_path = Path(args.frontend)
    
    if not python_path.is_absolute():
        python_path = script_dir / python_path
    
    if not frontend_path.is_absolute():
        frontend_path = script_dir / frontend_path
    
    # Check if paths exist
    if not python_path.exists():
        print(f"{RED}Error: {python_path} does not exist{RESET}")
        return 1
    
    if not frontend_path.exists():
        print(f"{RED}Error: {frontend_path} does not exist{RESET}")
        return 1
    
    # Run checks
    python_result = run_python_safety_check(str(python_path))
    npm_result = run_npm_audit(str(frontend_path))
    
    # Generate report if requested
    if args.report:
        report_path = args.report
        if not os.path.isabs(report_path):
            report_path = os.path.join(os.getcwd(), report_path)
        generate_report(python_result, npm_result, report_path)
    
    # Return 0 if all checks passed, 1 otherwise
    return 0 if python_result[0] and npm_result[0] else 1

if __name__ == "__main__":
    sys.exit(main()) 
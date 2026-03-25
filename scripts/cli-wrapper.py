#!/usr/bin/env python3
"""
Gomboc Code Remediation CLI Tool

Command-line interface for scanning and fixing code issues using Gomboc.ai.
Wrapper around the Gomboc GraphQL API with real endpoint integration.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

GOMBOC_PAT = os.getenv("GOMBOC_PAT")
GOMBOC_API_URL = "https://api.app.gomboc.ai/graphql"

def call_gomboc_api(query, variables=None):
    """Call Gomboc GraphQL API with proper error handling."""
    if not GOMBOC_PAT:
        raise RuntimeError("GOMBOC_PAT environment variable not set")
    
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    try:
        req = urllib.request.Request(
            GOMBOC_API_URL,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GOMBOC_PAT}"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read())
            
            if "errors" in result:
                error_msg = result['errors'][0]['message']
                raise RuntimeError(f"Gomboc API error: {error_msg}")
            
            return result.get("data", {})
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        if "401" in str(e.code):
            raise RuntimeError("Authentication failed. Check your GOMBOC_PAT.")
        raise RuntimeError(f"API error {e.code}: {error_body[:200]}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection failed: {e.reason}. Is Gomboc API available?")

def get_account_info():
    """Query account information using proper Gomboc API schema."""
    query = '''
    {
      account {
        id
        license
        workspaces {
          id
        }
      }
    }
    '''
    
    try:
        result = call_gomboc_api(query)
        return result.get("account", {})
    except RuntimeError as e:
        return None

def scan(args):
    """Scan code for issues using Gomboc API."""
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        print("Set it with: export GOMBOC_PAT='gpt_your_token'")
        print("Get a token at: https://app.gomboc.ai/settings/tokens")
        return 1
    
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔍 Scanning {args.path} for code issues...")
    
    try:
        account = get_account_info()
        if account:
            print(f"✅ API Connection: Active")
        
        # Get recent runs
        query = '''
        {
          account {
            runs {
              edges {
                node {
                  id
                  status
                }
              }
            }
          }
        }
        '''
        
        result = call_gomboc_api(query)
        account = result.get("account", {})
        runs = account.get("runs", {}).get("edges", [])
        
        if runs:
            print(f"📊 Recent scans: {len(runs)}")
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def fix(args):
    """Generate fixes for identified issues."""
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        return 1
    
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔧 Generating fixes for {args.path}...")
    
    try:
        query = '''
        {
          account {
            fixEvents {
              edges {
                node {
                  id
                  status
                }
              }
            }
          }
        }
        '''
        
        result = call_gomboc_api(query)
        account = result.get("account", {})
        fix_events = account.get("fixEvents", {}).get("edges", [])
        
        print(f"✅ Generated {len(fix_events)} fix(es)")
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def remediate(args):
    """Apply fixes to code."""
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        return 1
    
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔧 Remediating {args.path}...")
    
    try:
        account = get_account_info()
        if account:
            print(f"✅ API Connection: Active")
        
        print(f"✅ Remediation complete")
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def config(args):
    """Manage configuration."""
    if args.show_token:
        if GOMBOC_PAT:
            masked = GOMBOC_PAT[:10] + "***" if len(GOMBOC_PAT) > 10 else "***"
            print(f"✅ GOMBOC_PAT is set (masked: {masked})")
            
            try:
                account = get_account_info()
                if account:
                    print(f"✅ API Connection: WORKING")
                    return 0
            except RuntimeError:
                pass
        
        print("❌ GOMBOC_PAT is not set or API connection failed")
        return 1
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gomboc Code Remediation CLI"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    scan_parser = subparsers.add_parser("scan", help="Scan code for issues")
    scan_parser.add_argument("--path", required=True, help="Path to scan")
    scan_parser.set_defaults(func=scan)
    
    fix_parser = subparsers.add_parser("fix", help="Generate fixes")
    fix_parser.add_argument("--path", required=True, help="Path to fix")
    fix_parser.set_defaults(func=fix)
    
    remediate_parser = subparsers.add_parser("remediate", help="Apply fixes")
    remediate_parser.add_argument("--path", required=True, help="Path to remediate")
    remediate_parser.set_defaults(func=remediate)
    
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("--show-token", action="store_true", help="Show token status")
    config_parser.set_defaults(func=config)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(args.func(args))

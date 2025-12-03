#!/usr/bin/env python3
import subprocess
import sys
import os
import time

os.chdir(os.path.dirname(__file__))

print("=" * 50)
print("FRONTEND STARTUP TEST")
print("=" * 50)

frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')

print(f"\nChecking frontend directory: {frontend_dir}")
if not os.path.exists(frontend_dir):
    print("❌ Frontend directory not found!")
    sys.exit(1)

print("✓ Frontend directory found")

print("\nChecking node_modules...")
node_modules = os.path.join(frontend_dir, 'node_modules')
if not os.path.exists(node_modules):
    print("❌ node_modules not found - installing dependencies...")
    os.chdir(frontend_dir)
    os.system('npm install')
    os.chdir('..')
else:
    print("✓ node_modules found")

print("\n" + "=" * 50)
print("Starting React development server on http://localhost:3000")
print("Press CTRL+C to stop")
print("=" * 50 + "\n")

os.chdir(frontend_dir)
os.environ['SKIP_PREFLIGHT_CHECK'] = 'true'
os.system('npm start')

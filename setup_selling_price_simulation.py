#!/usr/bin/env python3

import os
import sys
import subprocess

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def setup_selling_price_simulation():
    """Setup the selling price simulation functionality"""
    
    print("Setting up Selling Price Simulation...")
    
    current_dir = os.getcwd()
    
    print("Running database migration...")
    if not run_command("bench migrate", cwd=current_dir):
        print("Failed to run migration")
        return False
        
    print("Building assets...")
    if not run_command("bench build", cwd=current_dir):
        print("Failed to build assets")
        return False
        
    print("Restarting bench...")
    if not run_command("bench restart", cwd=current_dir):
        print("Failed to restart bench")
        return False
        
    print("Setup completed successfully!")
    print("You can now access the Selling Price Simulation from the Selling workspace")
    return True

if __name__ == "__main__":
    setup_selling_price_simulation()

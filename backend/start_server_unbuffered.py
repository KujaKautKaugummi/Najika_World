#!/usr/bin/env python3
"""Start najika_server.py with unbuffered output"""
import subprocess
import sys
import os

# Set unbuffered mode
os.environ['PYTHONUNBUFFERED'] = '1'

# Start server
proc = subprocess.Popen(
    [sys.executable, 'najika_server.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    bufsize=0,  # Unbuffered
    universal_newlines=True
)

# Print output line by line
for line in proc.stdout:
    print(line, end='', flush=True)

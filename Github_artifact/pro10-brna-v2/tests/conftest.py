"""
pytest configuration — adds all module directories to sys.path
so tests can import from pro01-pro04 folders cleanly.
"""
import sys
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "pro01-neural-repeater"))
sys.path.insert(0, os.path.join(BASE, "pro02-mycelial-mesh"))
sys.path.insert(0, os.path.join(BASE, "pro03-dna-storage"))
sys.path.insert(0, os.path.join(BASE, "pro04-resonance-protocol"))

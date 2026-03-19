import sys
import os

backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, os.path.abspath(backend_path))

root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(root_path))

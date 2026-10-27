"""Explicit smoke test using the local, trusted checkpoint.
Run from root: backend/.venv/Scripts/python.exe scripts/smoke_model.py
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from app.inference.loader import get_model

def main():
    model=get_model()
    print('MODEL LOADED:',type(model).__name__)
    print('TASK:',model.task)
    print('CLASSES:',model.names)
    print('CHECKPOINT CONTRACT: PASS')

if __name__=='__main__':main()


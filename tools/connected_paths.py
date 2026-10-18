"""Stable review paths: keep existing Level 1 links and namespace other levels."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
def config(value=None):
 value=value or sys.argv[1]
 level,number=value.split('/') if '/' in value else ('ai-1',value)
 n=int(number);assert n>0 and level in ['ai-1','ai-2','ai-3','ai-4','ai-5','ai-6','ai-7','python-bridge']
 prefix=f'week{n}' if level=='ai-1' else f'{level}-week{n}'
 folder=f'week-{n:02}-connected-review' if level=='ai-1' else f'{level}-week-{n:02}-connected-review'
 return level,n,prefix,folder

"""Guard exact, week-scoped correction chains without accepting missing material."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from source_preservation import retained
changes={'ai-1/7':{'original':{'reviewed'},'reviewed':{'current'},'loop-a':{'loop-b'},'loop-b':{'loop-a'},'blank':{''}}}
assert retained('ai-1/7','original','original text',changes)
assert retained('ai-1/7','original','the current text',changes)
assert not retained('ai-1/7','original','unrelated text',changes)
assert not retained('ai-1/8','original','the current text',changes)
assert not retained('ai-1/7','loop-a','unrelated text',changes)
assert not retained('ai-1/7','blank','unrelated text',changes)
print('Exact source-correction chains, missing text, week boundaries, cycles and empty replacements verified.')

"""Local permission-pair simulation; no real tools or credentials."""
ACTOR_SCOPES={'reporter':frozenset({('lookup','public-room')})}
TOKEN_SCOPE=frozenset({('lookup','public-room')})

def permitted(actor,operation,resource,actor_scopes,token_scope):
    pair=(operation,resource)
    return pair in actor_scopes.get(actor,frozenset()) and pair in token_scope

def simulate(actor,operation,resource,actor_scopes,token_scope,executions):
    if not permitted(actor,operation,resource,actor_scopes,token_scope):
        return {'status':'denied'}
    # An execution stub records the permitted proposal; it performs no real work.
    executions.append((actor,operation,resource))
    return {'status':'simulated','operation':operation,'resource':resource}

executions=[]
denied=simulate('reporter','write','teacher-notes',ACTOR_SCOPES,TOKEN_SCOPE,executions)
assert denied=={'status':'denied'} and executions==[]
allowed=simulate('reporter','lookup','public-room',ACTOR_SCOPES,TOKEN_SCOPE,executions)
assert executions==[('reporter','lookup','public-room')]
print('Main excluded proposal:',denied)
print('Allowed local stub:',allowed,'execution ledger:',executions)
assert not permitted('unknown','lookup','public-room',ACTOR_SCOPES,TOKEN_SCOPE)
assert not permitted('reporter','lookup','public-room',ACTOR_SCOPES,frozenset())
# Separate weather picture: both actor policy and token capability must permit a pair.
weather_actor={'bot':frozenset({('read','S2'),('read','S5')})}
weather_token=frozenset({('read','S2')})
pictured=[('read','S2'),('write','S2'),('read','S5')]
print('Weather initial:',[(op,res,permitted('bot',op,res,weather_actor,weather_token)) for op,res in pictured])
expanded=weather_token|{('read','S5')}
assert permitted('bot','read','S5',weather_actor,expanded)
assert not permitted('bot','write','S2',weather_actor,expanded)
# A token expansion cannot overcome an actor policy that still excludes the pair.
assert not permitted('bot','read','S5',{'bot':frozenset({('read','S2')})},expanded)
# Keep operation/resource pairs together: independent verb/object lists overgrant.
paired=frozenset({('read','S2'),('write','S5')})
assert ('write','S2') not in paired
print('Source text or generated confidence is not an input to these trusted scope sets.')
print('No actual token verification, tool call, credential use or external execution.')

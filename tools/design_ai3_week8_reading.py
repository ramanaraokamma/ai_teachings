from connected_generative_authoring import GenerativeAuthor,g,routes
from connected_paragraphs import format_additions
a=GenerativeAuthor('ai-3/8');D=a.design
a.replace_text('Use the Week 11 closed object:','Use the Week5 room-report contract:')
D('sections',1,'At which layer does this answer first fail?','Separate JSON syntax, a closed schema and support from current sources.',[g('Your learning goals',[1,2,3]),g('Recall requested format versus checked output',[5,18],'prompts'),g('Your end goal',[20])])
D('sections',2,'Parse the structure, then validate its contract and meaning','Each layer answers a different question.',[g('The three validation layers',[11]),g('The complete room-report field and type contract',[12])])
D('sections',3,'Diagnose fragments without mistaking them for complete objects','The investigation supplies full candidates for actual checking.',[g('Read the illustrative layer failures',[11],'example'),g('Distinguish missing fields, nulls and unauthorised conversions',[12]),g('Trace the three-layer pipeline',[13]),g('Explain the deciding step',[15],'prompts')])
a.comparisons('Compare grammatical structure with supported meaning','A source ID and correct type do not establish the fact.')
p=a.add('sections',6,image=a.pic(2));ch=a.add('sections',6,image=a.pic(4))
D('sections',6,'Audit a room claim, then a separate book-fact schema','The room object has four fields; the pictured book object has three.',[g('Read the complete unsupported room-capacity example',[12]),g('Check conditional nulls and source-ID scope',[13]),g('Start the separate River Notes schema and candidates',[17,19,20]),g('Trace syntax, type and source comparison',[p,22,24]),g('Predict adding an unexpected rating field',[28],'prompts'),g('Check after predicting',[ch],'example',True),g('Keep source agreement separate from world truth',[26,27],'prompts')])
err=a.add('sections',7,'Claim to repair: The object parses and its capacity is an integer, so the answer is verified. The source may report a different value. In the room example99 has the correct type but Q supports12; in the separate book picture46 is an integer but R supports64. Preserve the exact source identity and claim comparison after the type check.')
D('sections',7,'Find a false fact hidden by a valid type','State the first failing layer and the evidence for that decision.',[g('Repair the parse-and-type argument',[err],'example'),g('Design a revealing candidate change',[9],'prompts')])
D('sections',8,'Practise a supported zero without treating it as missing','Schema acceptance and source agreement remain different checks.',[g('Read the complete D/8 practice and proposed zero',[8]),g('Explain all layers before discussion',[9],'prompts'),g('Complete main W2',[10,11,12]),g('Repair valid JSON means correct answer',[14,15,16],'prompts'),g('Explain the separate book picture',[17,18,19],'prompts'),g('Keep independent work separate',[20])])
records=a.add('sections',9,'Complete trusted fictional source bundle for the shared investigation: P is a current approval naming room B; Q is a current capacity register naming room B with capacity12. These are the only known source IDs. The response contract is exactly status,room,capacity,source_ids as in the main lesson. All six candidates below are complete strings; do not silently fill missing fields or convert values.')
base='{"status":"supported","room":"B","capacity":12,"source_ids":["P","Q"]}'
raws=[base,'{status:"supported","room":"B","capacity":12,"source_ids":["P","Q"]}',base.replace(':12',':"12"'),base.replace(':12',':true'),base[:-1]+',"book":true}',base.replace(':12',':99')]
tab=a.add('sections',9,image={'type':'table','rows':[['Card','Complete candidate text']]+[[str(i),s] for i,s in enumerate(raws,1)]})
code='''import json

class DuplicateField(ValueError): pass

def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise DuplicateField('duplicate field')
        result[key]=value
    return result

def reject_constant(value):
    raise ValueError('not a JSON number')

def validate(text,sources):
    # Source records are supplied trusted classroom fixtures, not scraped inputs.
    try:
        obj=json.loads(text,object_pairs_hook=unique_object,parse_constant=reject_constant)
    except DuplicateField:
        return 'schema: duplicate field policy'
    except (json.JSONDecodeError,ValueError):
        return 'syntax'
    fields={'status','room','capacity','source_ids'}
    if type(obj) is not dict or set(obj)!=fields:
        return 'schema: exact fields required'
    if obj['status'] not in ('supported','needs_review'):
        return 'schema: status'
    ids=obj['source_ids']
    if type(ids) is not list or not all(type(s) is str for s in ids):
        return 'schema: source IDs'
    if len(ids)!=len(set(ids)) or any(s not in sources for s in ids):
        return 'schema: unknown or repeated source ID'
    if obj['status']=='supported':
        if type(obj['room']) is not str or not obj['room']:
            return 'schema: room'
        if type(obj['capacity']) is not int or obj['capacity']<0:
            return 'schema: capacity'
    elif obj['room'] is not None or obj['capacity'] is not None:
        return 'schema: review claims must be null'
    approvals={s['room'] for s in sources.values() if s['kind']=='approval' and s['current']}
    expected=None
    if len(approvals)==1:
        room=next(iter(approvals))
        capacities={s['capacity'] for s in sources.values()
                    if s['kind']=='capacity' and s['current'] and s['room']==room}
        if len(capacities)==1:
            expected=(room,next(iter(capacities)))
    if obj['status']=='needs_review':
        return 'accepted' if expected is None else 'semantic: complete support available'
    if expected is None or (obj['room'],obj['capacity'])!=expected:
        return 'semantic: unsupported claims'
    cited=[sources[s] for s in ids]
    approval=any(s['kind']=='approval' and s['current'] and s['room']==obj['room'] for s in cited)
    capacity=any(s['kind']=='capacity' and s['current'] and s['room']==obj['room']
                 and s['capacity']==obj['capacity'] for s in cited)
    return 'accepted' if approval and capacity else 'semantic: cited support incomplete'

sources={'P':dict(kind='approval',current=True,room='B'),
         'Q':dict(kind='capacity',current=True,room='B',capacity=12)}
'''+ 'cards='+repr(raws)+'''
for number,text in enumerate(cards,1):
    print(number,validate(text,sources))'''
ci=a.add('sections',9,image={'type':'code','language':'python','text':code,'title':'Complete classroom JSON/schema/source validator and six candidate cards'})
lab=a.add('sections',9,'Predict the first failing layer for cards1–6 using the trusted P/Q bundle, then compare with a partner or run the optional complete local program. Keep the original text, parser result, schema reason and exact source comparison. Card1 passes; card2 has unquoted status; cards3and4 have invalid capacity types; card5 adds a forbidden field; card6 has an unsupported value. Add missing capacity, unknown source Z and supported capacity0 as distinct changes. A schema-valid zero must still match a supplied source; do not treat it as absent. The program implements this classroom contract, not every JSON Schema feature or a complete production service. It never books a room. Reserve the independent F/G objects before feedback.')
policy=a.add('sections',9,'Optional-program details: JSON true/null become Python True/None, so exact type checks exclude Boolean capacities. The parser explicitly rejects non-JSON NaN/Infinity constants. Repeated object names are rejected by this classroom’s duplicate-field schema policy; do not claim all JSON grammars prohibit them. Source records are trusted fixtures with stated kind/current/room/capacity fields. Semantic checks use the whole supplied source bundle, then require cited current approval and capacity to support the same room. Missing/conflicting support permits a null needs_review report; complete support does not justify that fallback under this contract.')
D('sections',9,'Validate six complete output strings','Use the paper cards first; local Python is optional.',[g('The complete source bundle and response contract',[records],'example'),g('Six supplied candidates',[tab],'example'),g('Predict, diagnose and retain the first failure',[lab],'steps'),g('Optional Python · Complete layered validator',[ci,policy],'reference',True),g('Keep the evidence record',[5,6,7,9])])
for role,n,i in [('sections',9,4),('teacher',4,5)]:a.fix(role,n,i,'Use the six complete candidate strings and trusted P/Q source bundle. Predict syntax, schema and semantic outcomes independently; retain each first failure. The complete local validator is optional and enforces only the declared classroom contract; no external action is performed.')
proj=a.add('sections',11,'Define the Verified Study Buddy’s own exact fields, types, allowed statuses, source-ID rules and missing-evidence combinations before another component consumes its output. Parse, validate schema and compare every factual claim with approved passages as separate steps. A rule allowing an integer cannot establish its factual value; a valid response cannot grant a tool permission. Keep failed text and a clear reason for each rejected layer.')
D('sections',11,'Validate the project’s actual contract before reuse','Do not substitute the room or book schema for the study buddy’s chosen fields.',[g('This week’s concrete contribution',[proj,12]),g('Keep the checkpoint and human choice',[4,5,6,7,8,9,10])])
ix=a.add('sections',14,'Treat the independent X/Y/Z descriptions as properly encoded JSON objects with exactly status,room,capacity,source_ids; the shorthand is a description, not literal JSON. Source A is the current approval for F and B the current register for F capacity9. Apply exact integer capacity and nonempty room rules before matching source support. Do not change G to F or text9 to integer9 silently.')
D('sections',14,'Try alone: validate the fresh F/G objects','Separate parser success, type checks and exact source support.',[g('Independent objects and encoding assumptions',[1,ix],'example'),g('Your first attempt and help record',[2,3,17]),g('Use feedback afterwards',[22])])
D('sections',16,'Finish: identify the layer and evidence for the decision','A well-shaped answer can still be unsupported.',[g('Explain without notes',[0,1],'prompts'),g('Plan a changed-case return',[2,3])])
tp=a.add('teacher',2,image=a.pic(2));cards=a.add('teacher',2,image=a.w['sections'][8]['blocks'][tab]);citation=a.add('teacher',2,'Optional Python reference: the official json documentation describes loads, object_pairs_hook and parse_constant, including default treatment of repeated names and non-finite constants. The classroom example adds its explicit policies. https://docs.python.org/3/library/json.html')
D('teacher',2,'Teach the first failing layer without merging the schemas','Keep room-report and River Notes book fields separately labelled.',[g('Define three layers and the room schema',[17,18,19]),g('Audit the full shared room cards',[cards]),g('Trace a typed but unsupported capacity',[24,25]),g('Read the separate book schema and X/Y/Z facts',[29,31,32]),g('Trace syntax, type and source checks',[tp,34,36]),g('Predict the extra rating field',[40,41,42]),g('State source-truth and parser-policy limits',[38,44,citation])])
ref='Room schema: exactly status,room,capacity,source_ids. status supported or needs_review; source_ids distinct known strings. supported requires nonempty room text and nonnegative exact integer capacity, excluding Boolean. needs_review requires null room and capacity. Match approved current room and capacity sources after schema. Separate book picture uses title,pages,source_id and record R River Notes64; do not mix fields.'
extras={n:[a.add('workbook',n,ref)] for n in [12,13,14,16]};extras[4]=[a.add('workbook',4,a.w['sections'][13]['blocks'][ix]['text'])]
a.common('Validate new objects independently','Require separate syntax, closed-schema and current source-support checks; preserve the first failing layer.',[(12,'W1 · Distinguish the layers','State what parsing, contract checks and source comparison establish.'),(13,'W2 · Audit types and fields','Null, missing, Boolean and string values are different.'),(14,'W3 · Check what a cited source supports','An existing ID does not establish the associated value.'),(16,'W5 · Keep report validity separate from permissions','A valid read-only report cannot authorise booking.')], 'Shared cards:1accepted;2syntax;3schema capacity text;4schema Boolean capacity;5closed-schema extra field;6semantic99versusQ12. Missing capacity and unknown Z are schema failures. Legitimate zero is schema-valid but needs matching source evidence. Separate River Notes Xpasses,Ytext64fails schema,Zinteger46fails support;ratingextra fails schema. Optional program treats repeated names as a declared schema policy and rejects non-JSON constants. Keep the independent F/G task withheld.',extras)
a.fix('teacher',6,13,'Next is Week9: Prompt Evaluation. Carry forward explicit syntax, schema and source-support criteria when comparing fixed development cases and protecting reserved final evidence.')
format_additions(a)
a.finish(routes(('Parse the text. Check the contract. Verify the claim.','Validate complete structured outputs with distinct syntax, schema and source-support evidence.','Three layers → full room candidates → separate book schema → paper/local audit → independent objects.'),('Teach layer-specific reasons on complete supplied objects.','Supply trusted source records, keep schemas distinct and use the optional validator within its declared limits.','Ask which layer first fails and why valid types cannot certify a factual claim.'),('One connected structured-output audit.','Distinguish layers, audit fields/types, inspect source support and keep permissions separate.','Retain original text, exact schema, source identity, first failure and evidence limits.')))

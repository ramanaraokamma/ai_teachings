from connected_level_authoring import LevelAuthor,g,routes
a=LevelAuthor('ai-2/25');D=a.design
a.fix('sections',1,18,'Why must an exact representation preserve the original spelling, spaces and punctuation rather than silently changing them?')
a.fix('teacher',1,a.find('teacher',1,'Readiness answer')+1,'An exact representation must reconstruct the original source. Lowercasing, removing punctuation or changing spaces is a transformation and must be declared separately rather than called an exact round trip.')
D('sections',1,'What counts as a token under this exact vocabulary?','Name the matching rule and preserve every supported source character.',[g('Your learning goals',[1,2,3]),g('Recall exact source preservation',[5,18],'prompts'),g('Your end goal',[20])])
v=a.add('sections',2,image={'type':'table','rows':[['ID','Entry','Meaning'],['0','end','Special terminator; not an ordinary text match'],['1','cat','Three ordinary characters'],['2 / 3 / 4 / 5','c / a / t / s','Four separate single-character entries'],['6','one literal space','Preserve the actual space character'],['7','sat','Three ordinary characters']]})
D('sections',2,'Read the case-sensitive vocabulary and longest-match contract','Token IDs name entries; they are not meanings or similarity scores.',[g('The complete toy tokenizer rule',[11,12]),g('The ID and special-token reference',[v])])
D('sections',3,'Trace encoding and exact decoding before counting','The end marker changes sequence length only when the protocol adds it.',[g('Follow the four longest matches',[11]),g('Decode and state the counting convention',[12]),g('Compare a supported round trip with uppercase failure',[13]),g('Explain a pictured step',[15],'prompts')])
a.comparisons('Check spaces, case and unknown characters','A partial trace is not complete encoding success.')
p=a.add('sections',6,image=a.pic(2));ch=a.add('sections',6,image=a.pic(4))
D('sections',6,'Compare vocabularies, then a separate book phrase','Do not mix the cat vocabulary with the book/books vocabulary.',[g('Count character-only versus original cat tokens',[12,13]),g('Read the separate phrase and its vocabulary',[17,19,20]),g('Trace overlap, space and unsupported punctuation',[p,24]),g('Predict the character-only book representation',[28],'prompts'),g('Check after predicting',[ch],'example',True),g('Explain the zero-based failure position and limits',[27,26],'prompts')])
D('sections',7,'A correct round trip verifies representation, not factual truth','A silent source change is not an exact encoding.',[g('Keep vocabulary, preprocessing and counting conventions',[8]),g('Challenge dropping unsupported punctuation',[9],'prompts')])
D('sections',8,'Trace spaces and failure positions explicitly','Keep the partial IDs and the reason when encoding stops.',[g('Read the supported and failing examples',[8]),g('Try the guided c at trace',[9],'prompts'),g('Encode and decode the W2 phrase',[11,12,13]),g('Repair token always equals word',[15,16],'prompts'),g('Explain the separate book failure index',[18,20])])
code='''vocabulary = {1: "cat", 2: "c", 3: "a", 4: "t", 5: "s", 6: " ", 7: "sat"}
def encode(text, entries):
    ids = []
    position = 0
    order = sorted(entries, key=lambda number: (-len(entries[number]), number))
    while position < len(text):
        found = None
        for token_id in order:
            if text.startswith(entries[token_id], position):
                found = token_id
                break
        if found is None:
            return ids, (position, text[position])
        ids.append(found)
        position += len(entries[found])
    return ids, None
for text in ["cats sat", "c at", "Cat", "cat!"]:
    ids, error = encode(text, vocabulary)
    print(repr(text), ids, error)
    if error is None:
        decoded = "".join(vocabulary[token_id] for token_id in ids)
        print("decoded", repr(decoded), "text tokens", len(ids))
character_entries = {number: text for number, text in vocabulary.items() if len(text) == 1}
ids, error = encode("cats sat", character_entries)
print("character-only", ids, len(ids), error)'''
ci=a.add('sections',9,image={'type':'code','title':'Complete exact longest-match toy encoder · Python3','text':code})
lab=a.add('sections',9,'Predict every ID, preserved space and error position for the four supplied strings before execution. Use the complete program or label a paper trace. entries must contain unique positive IDs with nonempty ordinary token strings; special end ID0 is deliberately outside this matching table. Longest entries are tried first, then ID for an otherwise equal-length order. startswith checks an exact prefix at position; on success position moves by token length, and failure returns the partial IDs plus zero-based position/character. The decoder shown accepts only successfully encoded ordinary IDs, not an appended terminator; end handling is a separate sequence protocol. Compare the original and character-only cats sat encodings and verify the same decoded source. No next-token model or continuation probabilities are supplied here. Reserve sat cats/sat cat! for independent W4.')
D('sections',9,'Audit exact encodings, failures and a changed vocabulary','Compare representations without silently altering the source.',[g('The complete toy encoder and all investigation inputs',[ci],'example'),g('Predict, trace, execute and compare',[lab],'steps'),g('Keep partial failures and evidence limits',[5,6,7,9])])
for r,n,i in [('sections',9,4),('teacher',4,5)]:a.fix(r,n,i,'Use the complete supplied toy encoder and four exact source strings. Record ordinary IDs, counting convention, decoded text or partial failure, then compare character-only vocabulary. No continuation model is supplied, so do not invent a probability change after removing context.')
proj=a.add('sections',11,'For the fictional recommender preserve each original description and record any separately declared text preprocessing. Name the vocabulary version, matching rule, unknown-character policy and special-token convention before comparing counts or text features. Exact decoding does not establish factual correctness or good matching. This toy encoder is not documentation of a particular deployed language model.')
D('sections',11,'Document the recommender’s text representation','Keep original text separate from intentional transformations.',[g('This week’s concrete contribution',[proj,12]),g('Keep the checkpoint, system and human choice',[4,5,6,7,8,9,10])])
ref=a.add('sections',14,'Use the original case-sensitive vocabulary:1=cat,2=c,3=a,4=t,5=s,6=literal space,7=sat;0=end only if explicitly appended by the protocol. Greedily take the longest ordinary match. On failure retain partial IDs and report the zero-based source character position. Do not lowercase or remove punctuation.')
D('sections',14,'Try alone: trace the new phrase and its failing variant','Count ordinary text tokens separately from an optional terminator.',[g('The independent phrase pair',[1],'example'),g('The complete original contract',[ref]),g('Your first attempt and support record',[2,3,17]),g('Use feedback after the attempt',[22])])
D('sections',16,'Finish: connect the count to its vocabulary and rule','Explain what round-trip success does and does not establish.',[g('Explain without notes',[0,1],'prompts'),g('Plan a changed-case return',[2,3])])
tp=a.add('teacher',2,image=a.pic(2));tc=a.add('teacher',2,image={'type':'code','title':'Complete exact longest-match toy encoder · Python3','text':code})
D('teacher',2,'Teach a tokenizer through an explicit vocabulary and trace','Keep the cat and book vocabularies distinct.',[g('State vocabulary, matching and unsupported-input policy',[17,18]),g('Explain exact decoding and token-count conventions',[19]),g('Compare original and character-only cat representation',[24,25]),g('Run the complete supported/failing input audit',[tc],'example'),g('Introduce the separate book vocabulary and phrase',[29,31,32]),g('Trace its exact text and unknown character',[tp,36,38]),g('Change only the vocabulary',[40,41,42]),g('Elicit picture-based explanation',[27,44])])
ref='Original case-sensitive vocabulary:0=end(special),1=cat,2=c,3=a,4=t,5=s,6=one literal space,7=sat. Longest ordinary prefix wins; preserve case/punctuation/space. Unsupported characters stop encoding with a partial trace and zero-based character position. Decode ordinary text IDs by concatenating their strings; state separately if an end marker is appended. Do not reuse the separate book/books vocabulary.'
extras={n:[a.add('workbook',n,ref)] for n in [12,13,14,16]};extras[4]=[a.add('workbook',4,ref)]
a.common('Trace a new input independently','Specify vocabulary, exact matching, ordinary versus special tokens and explicit failure instead of silent repair.',[(12,'W1 · Apply longest matching and case sensitivity','IDs identify vocabulary entries, not meaning.'),(13,'W2 · Encode, decode and declare the count','Keep four text tokens separate from an appended end marker.'),(14,'W3 · Compare character and chunk vocabularies','The source stays the same when representation changes.'),(16,'W5 · Audit undeclared preprocessing','An altered source cannot be called an exact original round trip.')], 'cats sat→[1,5,6,7],exact decode,four ordinary tokens,five with appended end. Character-only→[2,3,4,5,6,5,3,4],eight ordinary tokens. c at→[2,6,3,4]. Cat fails uppercaseC at0; cat! retains[1] then fails! at3. Separate books book has three chunk tokens or ten characters; ! is at10. Token IDs are not semantic distances, and no production tokenizer or continuation model is implemented. Reserve the fresh phrase pair for W4.',extras)
a.fix('teacher',6,13,'Next is Week26: Image and Voice Pipelines. Carry forward explicit representation, preprocessing and failure records when tracing another modality; do not describe this week as a real model’s tokenizer.')
o=routes(('Read the vocabulary. Match exactly. Count under a declared convention.','Trace chunk/character encodings, preserve source text and report unsupported input honestly.','Vocabulary and IDs → longest-match trace → exact/partial decoding → changed vocabulary comparison.'),('Teach tokenization as a specified representation procedure.','Supply complete vocabularies and programs, separate the cases and preserve the fresh phrase assessment.','Require original text, IDs, space handling, counting convention and failure position beside any token count.'),('One connected exact-tokenization record.','Apply the contract, encode/decode, compare sequence lengths and audit preprocessing claims.','Keep source text, vocabulary/rule version, ordinary/special counts and partial failures visible.'))
a.finish(o)

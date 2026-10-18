"""Readable answer guidance for the individually reviewed late Level 2 labs."""
KEYS = {
30: 'Original graph cases: A is structurally complete with one lookup. B first fails at review → looking_up. C exceeds its zero-lookup budget. D is incomplete after one lookup. E needs review because authorised evidence is absent. The graph has no retry edge: a two-attempt ceiling does not add one. The validator checks edges and counts, not tool truth or authorisation. In the separate picture, Trace A is valid; Trace B skips checking. Keep the independent terminal-state task withheld.',
31: 'Catalogue proposals: read R2 is allowed; read R8 fails object scope; write R5 and delete R2 fail operation scope. Reading R5 is allowed, but a write instruction in its contents does not authorise a write. Adult review must cover the exact draft, destination and cost before an action. All actions here are paper proposals. Main W2 violates both operation and resource scope. Privacy code prints True, False, False; teacher/read_review is allowed and unknown/read_summary is denied. Keep the inventory task independent.',
32: 'Main lab: A scores 8 and meets the 20-minute limit. B scores 15 but takes 21 minutes and is ineligible. C scores 8 and qualifies; A wins the name tie. Test order reversal, equality, no match, duplicate-name rejection, Boolean rejection and invalid requests. In the separate picture, limit 8 selects A by ID; limit 5 returns no eligible item. Duration extension accepts 10, 0, 20: count 3, sum 30, mean 10. Adding 30 gives count 4, sum 60, mean 15. Reserve the 15-minute independent plan.',
33: 'Activity example: A and B score 8; A wins by name in either order; limit 8 returns None. Complete pipeline: A, B and C validate; D fails the fun type; B is valid but too long; A and C tie at 8 and A wins. Reversing input preserves ranking; zero limit gives no match; Boolean True is an invalid request. Reject every duplicated A occurrence, leaving C eligible. Separate book picture: A scores 2, B 1, D 3; C fails subject. Changing D to 91 pages selects A. Independent mystery task: D fails length, F fails subject; E scores 3, G and H score 5; H wins with 90 rather than 95 pages. X/Y/Z remains additional activity practice.',
34: 'User-condition traces: U1 selects P; U2 has no eligible option; U3 selects Q; U4 has no verified eligible option because Q has no supplied screen-reader check. Correct abstention can satisfy the contract while a user need remains unmet. These are paper traces, not interface or user-group measurements. Six-case suite: 5/6 overall and 0/1 ties; ten duplicate passes produce 15/16 without new coverage. Separate picture: 8/12 overall; 4/4 ordinary does not describe all cases. Independent suite: 6/8, with one boundary and one tie failure; consequences are needed to order the repairs.',
35: 'Boundary script: 9 True, 10 True, 11 False. Score unit expectations: 0, 8, 15. Integration fixture: A and B tie at 8; A wins; C has invalid fun. Counts are 3 supplied, 2 accepted, 1 rejected, 2 eligible. Reversal preserves winner and counts but changes the rejected row index. Empty input has zero counts and no winner; limit 9 has no eligible winner; Boolean request is invalid. A local strict-comparison mutation fails the first integration assertion. In the picture, the explicit pages <= 101 patch wrongly admits C. No ten-profile improvement is measured by this lab. Independent limit 12 outcomes for 11, 12, 13, 0 are True, True, False, True.',
36: 'Pictured book report: 4 supplied, 3 accepted, D rejected for text interest; A and B eligible, C over the limit. A scores 7 and B 8, so B wins. The explicit corrected-D version accepts 4 rows and has 3 eligible; D scores 9 and wins. Reversal preserves ranking; limit 0 has no eligible item. The small A/8 report demonstrates count consistency only. Independent activity case: A and B score 8 and tie by name to A; C is valid but too long; D has invalid fun. Counts are 4 supplied, 3 accepted, 1 rejected, 2 eligible. Do not use the supported picture as fresh assessment.'}

def apply(a,number):
    block=next(b for b in reversed(a.w['teacher'][3]['blocks']) if b.get('reading_addition')==a.tag and b['type']=='paragraph')
    text=KEYS[number]
    block['text']=text
    import re
    sentences=re.split(r'(?<=\.)\s+',text)
    parts=[];part=''
    for sentence in sentences:
        if part and len(part)+len(sentence)>350:
            parts.append(part);part=''
        part+=((' ' if part else '')+sentence)
    if part:parts.append(part)
    block.setdefault('presentation',{})['paragraphs']=parts

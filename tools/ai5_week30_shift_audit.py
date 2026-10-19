"""Constructed disjoint-group counts; unchanged model and preprocessing."""
def audit(groups):
    if not groups:
        raise ValueError('Need at least one disjoint group')
    total = correct = 0
    ledger = []
    for name, n, k in groups:
        if type(n) is not int or type(k) is not int or n <= 0 or not 0 <= k <= n:
            raise ValueError('Need positive integer cases and valid integer correct count')
        total += n
        correct += k
        ledger.append((name,n,k,k/n))
    weighted = sum(n/total*rate for _,n,_,rate in ledger)
    return {'cases':total,'correct':correct,'errors':total-correct,
            'accuracy':correct/total,'weighted_accuracy':weighted,'groups':ledger}
development = [('clear',80,72),('dim',20,10)]
new_use = [('clear',20,18),('dim',80,40)]
old,new = audit(development),audit(new_use)
assert old['correct']==82 and new['correct']==58
assert old['errors']==18 and new['errors']==42
assert [r[3] for r in old['groups']]==[r[3] for r in new['groups']]==[.9,.5]
assert abs(old['accuracy']-old['weighted_accuracy'])<1e-12
assert abs(new['accuracy']-new['weighted_accuracy'])<1e-12
print('Development:',old)
print('New use:',new)
print('Drop in percentage points:',round(100*(old['accuracy']-new['accuracy']),8))
# Conditional scenario: assume these exact within-group rates in the new cohort.
equal_mix=audit([('clear',50,45),('dim',50,25)])
assert equal_mix['accuracy']==.7
print('Conditional equal mix:',equal_mix)
# Separate picture uses bright accuracy .8, not the main clear accuracy .9.
picture_old=audit([('bright',40,32),('dim',10,5)])
picture_new=audit([('bright',10,8),('dim',40,20)])
assert picture_old['accuracy']==.74 and picture_new['accuracy']==.56
print('Separate picture:',picture_old['accuracy'],picture_new['accuracy'])
# Without checked reference labels, no current accuracy can be computed.
# Group names alone cannot detect overlapping source records; audit source IDs separately.

"""Pure recovery decisions on trusted classroom status fixtures; no effects."""
from copy import deepcopy

def reconcile(operation_id,status_record,*,can_read_status=True,
              resend_approved=False,provider_deduplicates=False):
    if type(operation_id) is not str or not operation_id:
        raise ValueError('operation ID required')
    if any(type(v) is not bool for v in [can_read_status,resend_approved,provider_deduplicates]):
        raise ValueError('policy flags must be supplied Booleans')
    if not can_read_status:return {'status':'denied'}
    if (type(status_record) is not dict or status_record.get('operation_id')!=operation_id
        or status_record.get('authoritative') is not True):
        return {'status':'review','reason':'missing reliable matching status'}
    state=status_record.get('state')
    if state=='committed':
        result=status_record.get('result')
        if type(result) is not dict:return {'status':'review','reason':'missing committed result'}
        return {'status':'return_existing','operation_id':operation_id,'result':deepcopy(result)}
    if state=='prepared':return {'status':'pending_review','reason':'prepared is not confirmed failed'}
    if state in ('unknown','unavailable'):
        return {'status':'review','reason':'outcome unresolved; do not repeat blindly'}
    if state=='absent':
        if resend_approved and provider_deduplicates:
            return {'status':'resend_candidate','operation_id':operation_id,
                    'requires':'separate authorized execution with same provider key'}
        return {'status':'review','reason':'absence alone does not grant resend authority or deduplication'}
    return {'status':'review','reason':'unrecognized status'}

committed={'operation_id':'BOOK-1','authoritative':True,'state':'committed',
           'result':{'booking_id':'B1','status':'booked_fixture'}}
before=deepcopy(committed)
returned=reconcile('BOOK-1',committed)
assert returned['status']=='return_existing' and committed==before
returned['result']['status']='modified caller copy'
assert committed==before
print('Main lost-acknowledgement recovery:',reconcile('BOOK-1',committed))
unknown={'operation_id':'BOOK-1','authoritative':True,'state':'unknown'}
prepared={**unknown,'state':'prepared'}
assert reconcile('BOOK-1',unknown)['status']=='review'
assert reconcile('BOOK-1',prepared)['status']=='pending_review'
assert reconcile('BOOK-1',committed,can_read_status=False)=={'status':'denied'}
print('Unknown/prepared:',reconcile('BOOK-1',unknown),reconcile('BOOK-1',prepared))
# Separate pictured printer job, not an actual print command.
complete={'operation_id':'J6','authoritative':True,'state':'committed',
          'result':{'print_job':'one fictional badge'}}
absent={'operation_id':'J6','authoritative':True,'state':'absent'}
assert reconcile('J6',complete)['status']=='return_existing'
assert reconcile('J6',absent)['status']=='review'
candidate=reconcile('J6',absent,resend_approved=True,provider_deduplicates=True)
assert candidate['status']=='resend_candidate' and candidate['operation_id']=='J6'
assert reconcile('J6',{**absent,'authoritative':False},resend_approved=True,provider_deduplicates=True)['status']=='review'
print('Printer complete:',reconcile('J6',complete))
print('Reliable absence without/with separate trusted controls:',reconcile('J6',absent),candidate)
# Compensation is its own proposed action with its own exact fixture approval.
compensation={'operation':'cancel_booking','original_id':'BOOK-1','new_operation_id':'COMP-1'}
def plan_compensation(proposal,trusted_approval):
    if trusted_approval!=proposal:raise PermissionError('separate exact compensation approval required')
    return deepcopy(proposal)  # plan only, not execution or deletion
try:plan_compensation(compensation,None)
except PermissionError:pass
else:raise AssertionError('Unapproved compensation planned')
assert plan_compensation(compensation,deepcopy(compensation))==compensation
assert committed==before
print('Compensation remains a separate approved-plan fixture; original commit is unchanged.')
print('No real status lookup, resend, print, booking, cancellation, token transfer or durable recovery is performed.')

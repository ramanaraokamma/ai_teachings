"""Transform copies of fictional store dictionaries; no real deletion/erasure."""
from copy import deepcopy

def simulate_retention(ages,stores,content_days=7,failed_removals=frozenset()):
    if type(ages) is not dict or not ages or type(stores) is not dict or not stores:
        raise ValueError('nonempty age manifest and listed stores required')
    if any(type(location) is not str or not location or type(items) is not dict for location,items in stores.items()):
        raise ValueError('invalid listed store schema')
    if any(type(record_id) is not str or not record_id for record_id in ages):
        raise ValueError('record IDs required')
    if type(content_days) is not int or content_days<=0:
        raise ValueError('positive content lifetime required')
    if any(type(age) is not int or age<0 for age in ages.values()):
        raise ValueError('nonnegative whole-day fixture ages required')
    if any(record_id not in ages for items in stores.values() for record_id in items):
        raise ValueError('listed copy missing age metadata')
    after=deepcopy(stores)
    due=[record_id for record_id,age in ages.items() if age>=content_days]
    removed=[];failed=[]
    for record_id in due:
        for location,items in after.items():
            if record_id not in items:continue
            pair=(location,record_id)
            if pair in failed_removals:failed.append(pair)
            else:
                items.pop(record_id)  # simulated dictionary update only
                removed.append(pair)
    residuals=[(location,record_id) for location,items in after.items()
               for record_id in due if record_id in items]
    report={'scope':sorted(after),'due_ids':due,'removed':removed,'failed':failed,
            'residuals':residuals,'scoped_complete':not residuals}
    # Separate audit-event clock: these new content-free events have age zero.
    audit=[{'record_id':record_id,'action':'removed_in_mock',
            'location':location,'event_age_days':0} for location,record_id in removed]
    return after,report,audit

def retain_audit(age_days):
    if type(age_days) is not int or age_days<0:raise ValueError('invalid audit-event age')
    return age_days<30

ages={'S6':6,'S7':7,'S9':9}
primary={'S6':'fictional transcript6','S7':'fictional transcript7','S9':'fictional transcript9'}
stores={'primary':dict(primary),'cache':dict(primary)}
before=deepcopy(stores)
after,report,audit=simulate_retention(ages,stores)
assert all(set(items)=={'S6'} for items in after.values())
assert len(report['removed'])==4 and report['scoped_complete'] and stores==before
assert all(set(r)=={'record_id','action','location','event_age_days'} for r in audit)
assert retain_audit(29) and not retain_audit(30)
print('Main modeled primary/cache outcome:',report)
print('Main remaining IDs:',{name:sorted(items) for name,items in after.items()})
print('Unverified scope: backups require their separately stated expiry process; no global-deletion claim.')
print('New content-free audit events:',audit,'audit boundary 29/30:',retain_audit(29),retain_audit(30))
# Separate picture explicitly requires removal from primary AND its listed backup.
picture_ages={'T1':6,'T2':7}
picture_stores={'primary':{'T1':'fictional T1','T2':'fictional T2'},
                'backup':{'T2':'fictional T2'}}
picture_after,picture_report,_=simulate_retention(picture_ages,picture_stores)
failed_after,failed_report,_=simulate_retention(picture_ages,picture_stores,
                                               failed_removals={('backup','T2')})
assert picture_report['scoped_complete'] and len(picture_report['removed'])==2
assert not failed_report['scoped_complete'] and failed_report['residuals']==[('backup','T2')]
retry_after,retry_report,_=simulate_retention(picture_ages,failed_after)
assert retry_report['scoped_complete'] and failed_report['residuals']==[('backup','T2')]
print('Picture all listed removals:',picture_report)
print('Picture backup removal fails:',failed_report)
print('Separate retry simulation:',retry_report)
print('Only copied mock dictionaries changed; original fixtures remain. No file, database, log, backup or memory is securely erased.')

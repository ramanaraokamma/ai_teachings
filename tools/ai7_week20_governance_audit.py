"""Audit a declared fictional data-flow plan, not actual privacy or permission."""

def audit_plan(plan):
 required={'analysis_fields','analyst_can_read_key','public_fields','purpose','retention'}
 if not isinstance(plan,dict) or not required<=plan.keys():raise ValueError('complete declared plan required')
 if type(plan['analyst_can_read_key']) is not bool:raise ValueError('key access must be Boolean')
 for key in ['analysis_fields','public_fields']:
  if not isinstance(plan[key],list) or any(not isinstance(v,str) for v in plan[key]):raise ValueError('field lists required')
 issues=[]
 unnecessary=set(plan['analysis_fields'])-{'participant_code','task_score'}
 if unnecessary:issues.append('analysis includes unnecessary fields under this toy purpose')
 if plan['analyst_can_read_key']:issues.append('analyst access breaks the declared key separation')
 if set(plan['public_fields']) & {'name','identity_key','participant_code','exact_birth_date','classroom','rare_condition','task_score'}:
  issues.append('public proposal contains row-level or linking fields outside the toy aggregate plan')
 if not isinstance(plan['purpose'],str) or not plan['purpose'].strip():issues.append('purpose unspecified')
 if not isinstance(plan['retention'],str) or not plan['retention'].strip():issues.append('retention unspecified')
 return issues
main={'analysis_fields':['participant_code','exact_birth_date','classroom','rare_condition'],
      'analyst_can_read_key':False,'public_fields':['participant_code','exact_birth_date','classroom','rare_condition'],
      'purpose':'fictional task-score analysis','retention':''}
# Explicit proposed repair; passing these metadata checks is not authorization.
proposed={'analysis_fields':['participant_code','task_score'],'analyst_can_read_key':False,
          'public_fields':[],'purpose':'fictional task-score analysis',
          'retention':'demo policy: delete analysis and key at end of the named exercise; not an executed deletion'}
main_issues=audit_plan(main);proposed_issues=audit_plan(proposed)
published_key={**proposed,'public_fields':['identity_key','participant_code','task_score']}
assert main_issues and not proposed_issues and audit_plan(published_key)
def subgroup_rule(size,minimum=5):
 if type(size) is not int or type(minimum) is not int or size<0 or minimum<1:raise ValueError('nonnegative count and positive minimum required')
 return 'block_under_supplied_rule' if size<minimum else 'size_rule_met_only'
assert subgroup_rule(1)=='block_under_supplied_rule' and subgroup_rule(5)=='size_rule_met_only'
print('Main proposal issues:',main_issues)
print('Proposed repair metadata issues:',proposed_issues,'does not mean approved or anonymous')
print('Published-key proposal issues:',audit_plan(published_key))
print('Supplied minimum-five rule: one-person subgroup blocked; five meets only this count rule, not a privacy guarantee.')
print('No personal records, identity lookup, export, access control or deletion is executed. The audit checks declared metadata, not actual reader permissions, consent or reidentification risk.')

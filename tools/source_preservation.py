"""Accept original text or an explicitly recorded chain of reviewed replacements."""
def retained(week,text,actual,corrections):
 if text in actual:return True
 pending=list(corrections.get(week,{}).get(text,()));seen={text}
 while pending:
  candidate=pending.pop()
  if not candidate or candidate in seen:continue
  seen.add(candidate)
  if candidate in actual:return True
  pending.extend(corrections.get(week,{}).get(candidate,()))
 return False

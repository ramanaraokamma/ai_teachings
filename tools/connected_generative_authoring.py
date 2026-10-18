"""Shared reference mechanics for individually reviewed Level 3 lessons."""
from connected_level_authoring import LevelAuthor,g,routes
class GenerativeAuthor(LevelAuthor):
 def common(self,*args,**kwargs):
  super().common(*args,**kwargs)
  c=self.find('teacher',3,'Completion task:');q=self.find('teacher',3,'Use the worked case for');pq=self.find('teacher',3,'Pictorial practice question');pk=self.find('teacher',3,'Reasoned teacher answer')
  self.design('teacher',3,'Guide the explanation, then remove help','Collect each learner’s reasoning before showing feedback.',[g('Main completion prompt',[c],'example'),g('Expected reasoning and fading help',[c+1,c+2]),g('Individual misconception check',[q,q+1,q+2]),g('Pictorial question and changed-case reasoning',[pq+1,pk+1,pk+2,pk+3]),g('Keep each learner explaining',[self.find('teacher',3,'Classroom dialogue')+i for i in [1,2,4]],'prompts')])

"""Compact reference layouts with research-specific wording for Level 7."""
from connected_neural_authoring import NeuralAuthor,g,routes
class ResearchAuthor(NeuralAuthor):
 def references(self,case,lab,reference):
  super().references(case,lab,reference)
  changes=[('sections',5,'Reference · Use research vocabulary precisely','Connect each term to the question, comparison, measurement or evidence.'),
   ('sections',12,'Reference · Check the research reasoning and its limits','Use after practice; reserve the selected independent case for its first attempt.'),
   ('workbook',6,'W2 · Trace the worked case','Keep the supplied inputs, comparison rule and evidence together.'),
   ('workbook',10,'Project · Keep the research evidence','Preserve the question, protocol, observations, analysis and limits.'),
   ('teacher',1,'Prepare the connected research investigation','Keep modelling, shared practice and independent evidence distinct.'),
   ('teacher',5,'Assess the new research scenario','Keep the selected answer private until after a first attempt.'),
   ('teacher',6,'Connect, support and revisit research reasoning','Use saved evidence and assumptions to choose the next question.')]
  for role,n,title,purpose in changes:
   flow=self.w[role][n-1]['reading_flow'];flow['title']=title;flow['purpose']=purpose
   self.w[role][n-1]['reading_intro']=purpose

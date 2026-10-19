"""Compact reference layouts with service-design wording for Level 6."""
from connected_neural_authoring import NeuralAuthor,g,routes
class SystemsAuthor(NeuralAuthor):
 def references(self,case,lab,reference):
  super().references(case,lab,reference)
  for role,n,title,overview in [
   ('sections',5,'Reference · Use service vocabulary precisely','Connect each term to an input, operation, evidence source or outcome.'),
   ('sections',12,'Reference · Check the service reasoning and its limits','Use after practice; keep the selected independent case for its first attempt.'),
   ('workbook',10,'Project · Keep the service evidence','Preserve the contract, inputs, observed outcomes and limits.'),
   ('teacher',1,'Prepare the connected service investigation','Keep modelling, shared practice and independent evidence distinct.'),
   ('teacher',5,'Assess the new service scenario','Keep the selected answer private until after a first attempt.'),
   ('teacher',6,'Connect, support and revisit service design','Use saved evidence and boundary decisions to choose the next step.')]:
   flow=self.w[role][n-1]['reading_flow']
   flow['title']=title;flow['purpose']=overview
   self.w[role][n-1]['reading_intro']=overview

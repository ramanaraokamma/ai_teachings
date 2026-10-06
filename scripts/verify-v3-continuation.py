"""Validate all canonical positions plus offline continuation mechanisms.

This checks arithmetic/contracts, not pedagogical effectiveness or PDF layout.
"""
import importlib.util
import contextlib
import io
import json
import math
from pathlib import Path
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'examples/curriculum-v3' / f'{name}.py')
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


service = module('engineering_service')
research = module('research_calculations')


class ContinuationChecks(unittest.TestCase):
    def test_inline_labs_execute_with_documented_results(self):
        expected = {
            (6,3): "{'room_id': 'A', 'requested_count': 0}",
            (6,5): 'False', (6,7): '7', (6,13): 'looking_up',
            (6,15): '1', (6,16): '15', (6,18): 'True', (6,21): 'False',
            (7,11): '[1.0, 2.0, 2.0, 2.0, 2.0, 3.0]',
            (7,12): '(0.5, 9.02, 10.98)',
            (7,13): '([2, 3, 1], 2.0)', (7,14): '0.25',
            (7,15): '(0.01, [True, False, False, False, False])',
        }
        for (level,week),wanted in expected.items():
            with self.subTest(level=level,week=week):
                w=json.loads((ROOT/f'curriculum-v3/ai-{level}-week-{week:02}.json').read_text())
                code=[b['text'] for s in w['lesson'] for b in s['blocks'] if b['type']=='code']
                self.assertEqual(len(code),1)
                captured=io.StringIO()
                with contextlib.redirect_stdout(captured):
                    exec(compile(code[0],f'ai-{level}/{week}','exec'),{})
                self.assertEqual(captured.getvalue().strip(),wanted)

    def test_all_252_positions_have_complete_source_structures(self):
        roadmap = json.loads((ROOT / 'curriculum-v3/progression.json').read_text())
        releases = json.loads((ROOT / 'curriculum-v3/releases.json').read_text())
        count = drafts = 0
        for level in roadmap['levels']:
            for week, title in enumerate(level['weeks'], 1):
                with self.subTest(level=level['slug'], week=week):
                    path = ROOT / f'curriculum-v3/{level["slug"]}-week-{week:02}.json'
                    w = json.loads(path.read_text())
                    self.assertEqual((w['level'], w['week'], w['title']), (level['slug'], week, title))
                    self.assertEqual(w['minutes'], 90)
                    self.assertEqual(len(w['goals']), 3)
                    self.assertEqual(len(w['lesson']), 5)
                    self.assertEqual(len(w['workbook']), 5)
                    self.assertEqual([t['id'] for t in w['workbook']], ['W1','W2','W3','W4','W5'])
                    self.assertTrue(w['prerequisite']['prompt'] and w['prerequisite']['answer'])
                    self.assertGreaterEqual(len(w['vocabulary']), 3)
                    blocks = [b for s in w['lesson'] for b in s['blocks']]
                    self.assertTrue(any(b['type'] == 'diagram' for b in blocks))
                    for task in w['workbook']:
                        self.assertTrue(task['prompt'] and task['answer'])
                        self.assertGreaterEqual(task['lines'], 4)
                    for key in ('background','guidedAnswer','assessment','support','next'):
                        self.assertTrue(w['teacher'][key])
                    if level['slug'] in ('ai-5','ai-6','ai-7') or (level['slug']=='ai-4' and week>=33):
                        self.assertEqual(len(w['teacher']['sessions']), 8)
                        self.assertIn('retry', w['teacher']['assessment'].lower())
                    if f'{level["slug"]}/{week}' not in releases:
                        drafts += 1
                    count += 1
        self.assertEqual(count, 252)
        self.assertEqual(drafts, 252-len(releases))

    def test_request_boundary_and_booleans(self):
        self.assertEqual(service.validate_request({'room_id':'A','requested_count':0})['requested_count'], 0)
        for count in (-1, True, False, '3', 3.0, None):
            with self.subTest(count=count), self.assertRaises(ValueError):
                service.validate_request({'room_id':'A','requested_count':count})
        with self.assertRaises(ValueError):
            service.validate_request({'room_id':'A','requested_count':3,'book':True})
        for text in ('b2','B22','B2;DROP','Z9\n'):
            self.assertFalse(service.validate_identifier(text))
        self.assertTrue(service.validate_identifier('B2'))

    def test_access_denied_before_content_read(self):
        resource={'id':'T','role':'teacher','content':'fictional teacher answer'}
        trace=[]
        self.assertIsNone(service.read_resource('student',resource,trace))
        self.assertEqual(trace,[('denied','T')])
        self.assertFalse(service.may_read(None,'student'))
        self.assertFalse(service.may_read('student','unknown'))
        self.assertTrue(service.may_read('teacher','student'))

    def test_pipeline_support_missing_conflict_and_zero(self):
        records=[{'id':'P','role':'student','current':True,'kind':'approval','room':'A'},
                 {'id':'R','role':'student','current':True,'kind':'register','room':'A','capacity':0}]
        request={'room_id':'A','requested_count':0}
        self.assertEqual(service.report(request,'student',records,[])['capacity'],0)
        self.assertEqual(service.report(request,'student',records[:1],[])['status'],'needs_review')
        conflict=records+[dict(records[0],id='P2')]
        self.assertEqual(service.report(request,'student',conflict,[])['status'],'needs_review')
        restricted=[dict(r,role='teacher') for r in records]
        self.assertEqual(service.report(request,'student',restricted,[])['status'],'needs_review')
        trace=[]
        self.assertEqual(service.report(request,None,records,trace)['status'],'denied')
        self.assertNotIn(('lookup','A'),trace)

    def test_pure_boundaries_and_cache_keys(self):
        self.assertEqual(service.remaining(9,0),9)
        self.assertEqual(service.remaining(9,9),0)
        for args in ((9,10),(-1,0),(9,True)):
            with self.assertRaises(ValueError): service.remaining(*args)
        self.assertNotEqual(service.cache_key('Q','student','v1','p1'),service.cache_key('Q','teacher','v1','p1'))
        self.assertTrue(service.cache_valid(9,10,'v1','v1'))
        self.assertFalse(service.cache_valid(10,10,'v1','v1'))
        self.assertFalse(service.cache_valid(9,10,'v1','v2'))

    def test_state_and_retry_limits(self):
        self.assertEqual(service.transition('ready','looking_up'),'looking_up')
        with self.assertRaises(ValueError): service.transition('review','looking_up')
        with self.assertRaises(ValueError): service.transition('done','review')
        self.assertEqual(service.waiting_bound(3,4,[1,2]),15)
        self.assertEqual(service.waiting_bound(2,5,[2]),12)
        self.assertEqual(service.waiting_bound(4,2,[1,2,4]),15)
        with self.assertRaises(ValueError): service.waiting_bound(3,4,[1])

    def test_idempotency_and_version_bound_approval(self):
        ledger=service.MockLedger()
        payload={'version':'v1','destination':'D'}
        result=ledger.submit('K',payload,dict(payload))
        self.assertEqual(result,ledger.submit('K',dict(payload),dict(payload)))
        self.assertEqual(len(ledger.effects),1)
        result['status']='tampered'
        self.assertEqual(ledger.submit('K',payload,payload)['status'],'committed')
        changed=dict(payload,destination='E')
        with self.assertRaises(ValueError): ledger.submit('K',changed,changed)
        with self.assertRaises(PermissionError): ledger.submit('N',changed,payload)
        self.assertEqual(len(ledger.effects),1)

    def test_retrieval_and_evaluation_denominators(self):
        for relevant,returned,precision,recall in [({'A','C','E'},['A','B','C'],2/3,2/3),({'A','D','F','G'},['A','B','D'],2/3,.5),({'B','E'},['A','B','C','D'],.25,.5)]:
            found=len(set(returned)&relevant)
            self.assertAlmostEqual(found/len(returned),precision)
            self.assertAlmostEqual(found/len(relevant),recall)
        self.assertAlmostEqual((6+2)/12,2/3)
        self.assertAlmostEqual(6/8,.75)
        self.assertAlmostEqual(2/4,.5)
        self.assertAlmostEqual(195/200,.975)
        self.assertEqual(.02*200,4)

    def test_sampling_distributions(self):
        for population,expected in [([1,1,3,3],[1,2,2,2,2,3]),([0,0,4,4],[0,2,2,2,2,4]),([2,2,6,6],[2,4,4,4,4,6])]:
            means=research.sample_means(population,2)
            self.assertEqual(means,expected)
            self.assertEqual(statistics.mean(means),statistics.mean(population))
        with self.assertRaises(ValueError): research.sample_means([1,2],3)

    def test_interval_assumptions_arithmetic(self):
        for mean,sigma,n,expected in [(10,2,16,(.5,9.02,10.98)),(20,5,25,(1,18.04,21.96)),(8,4,16,(1,6.04,9.96))]:
            for actual,wanted in zip(research.known_sigma_interval(mean,sigma,n),expected):
                self.assertAlmostEqual(actual,wanted)
        with self.assertRaises(ValueError): research.known_sigma_interval(10,2,0)

    def test_exact_tests_and_family_thresholds(self):
        self.assertEqual(research.sign_flip_p([1,1,1]),.25)
        self.assertEqual(research.sign_flip_p([2,2,2]),.25)
        self.assertEqual(research.sign_flip_p([1,1,1,1]),.125)
        self.assertEqual(research.sign_flip_p([0,0,0]),1)
        threshold,decisions=research.bonferroni([.009,.012,.3,.4,.8])
        self.assertAlmostEqual(threshold,.01)
        self.assertEqual(decisions,[True,False,False,False,False])
        self.assertEqual(research.bonferroni([.01,.02,.2,.9])[1],[True,False,False,False])

    def test_paired_effects_resource_costs_and_tails(self):
        differences,gain=research.paired_gain([10,12,8],[8,9,7])
        self.assertEqual(differences,[2,3,1]);self.assertEqual(gain,2)
        self.assertEqual(research.paired_gain([6,8,10],[5,7,9])[1],1)
        self.assertAlmostEqual(research.paired_gain([5,7,9],[3,5,8])[1],5/3)
        self.assertEqual(statistics.mean([1,1,1,9]),3)
        self.assertEqual(statistics.median([1,1,1,9]),1)
        self.assertEqual(statistics.mean([2,3,4,20]),7.25)
        self.assertEqual(statistics.median([2,3,4,20]),3.5)
        self.assertAlmostEqual(1000*2/1000+300*6/1000+200*2/1000+100*6/1000,4.8)


if __name__=='__main__':
    unittest.main(verbosity=2)

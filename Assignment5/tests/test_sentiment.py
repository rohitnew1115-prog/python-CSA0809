import csv, unittest
from pathlib import Path
from Task05_AI_Applications.sentiment import score,label,improved_label
from Task05_AI_Applications.summariser import summarize

class SentimentTests(unittest.TestCase):
    def test_assignment_examples(self):
        self.assertEqual([label(x) for x in ("Roads are clean and the bus was fast.","Smoke from the factory, air is bad.","The staff were not helpful.","Not bad, service improved.")],["positive","negative","negative","positive"])
    def test_summary(self):
        self.assertTrue(summarize("Smoke affects the road. The road needs repair. The monitor is online.").strip())
    def test_known_baseline_error_improves(self):
        text="No staff arrived to inspect the site."
        self.assertEqual(label(text),"neutral"); self.assertEqual(improved_label(text),"negative")
    def test_corpus_count_and_agreement(self):
        path=Path(__file__).parents[1]/"Task05_AI_Applications"/"complaints.csv"
        with path.open(encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows),50)
        self.assertEqual(len(rows),50)

if __name__=="__main__": unittest.main()

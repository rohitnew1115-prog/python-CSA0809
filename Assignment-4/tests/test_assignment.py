import csv,sys,tempfile,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"Task05")); sys.path.insert(0,str(BASE/"Task06"))
from Task01.solution import process_bills
from Task02.attendance import process_month
from Task03.attendance_exceptions import parse_line,InvalidRecord,process_file
from Task04.library_log import append_returns
from attendance_package.stats import summarize
from fest_package.processor import collect

class AssignmentTests(unittest.TestCase):
 def test_bills_valid_bad_and_missing(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); (p/"in").write_text("1,A,2.50\nbad\n",encoding="utf8"); total,ok,bad=process_bills(p/"in",p/"out.csv"); self.assertEqual(total,2.5); self.assertEqual(len(ok),1); self.assertEqual(len(bad),1); self.assertIn("Total",(p/"out.csv").read_text())
   with self.assertRaises(FileNotFoundError): process_bills(p/"missing",p/"x")
 def test_monthly_attendance_and_empty(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); (p/"d.csv").write_text("1,2026-01-01,P\n1,2026-01-02,A\nbad\n",encoding="utf8"); c,e,_=process_month(p,p/"out",["1","2"]); self.assertEqual(c["1"],[1,2]); self.assertEqual(len(e),1); self.assertTrue((p/"out/below_75_percent.csv").exists())
 def test_strict_record_and_missing_file(self):
  self.assertEqual(parse_line("1.2026-10-08.P","x",1),("1","2026-10-08","P"))
  with self.assertRaises(InvalidRecord): parse_line("1.2026-02-30.P","x",2)
  with self.assertRaises(RuntimeError) as ctx: process_file(Path("missing.txt"))
  self.assertIsInstance(ctx.exception.__cause__,FileNotFoundError)
 def test_library_append_and_missing(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); log=p/"log"; err=p/"err"; inp=p/"day"; inp.write_text("B1,M1\n",encoding="utf8"); append_returns(inp,log,err); append_returns(inp,log,err); self.assertEqual(len(log.read_text().splitlines()),2); _,errors=append_returns(p/"missing",log,err); self.assertTrue(errors)
 def test_consecutive_absence(self):
  pct,streak=summarize([("1",f"2026-01-0{i}","A") for i in (1,2,3)]); self.assertEqual(streak,["1"]); self.assertEqual(pct["1"],0)
 def test_fest_duplicate_bad_email_damaged(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); (p/"a.csv").write_text("1,A,D,a@b.com,E\n2,B,D,bad,E\n3,C,D,c@b.com,E\n",encoding="utf8"); (p/"b.csv").write_text("1,A,D,a@b.com,E\nshort\n",encoding="utf8"); rows,errors=collect(p); self.assertEqual([r["register_number"] for r in rows],["1","3"]); self.assertEqual(len(errors),3)
if __name__=="__main__": unittest.main()

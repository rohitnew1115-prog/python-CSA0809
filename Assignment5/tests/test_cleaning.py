import io, unittest, tempfile
from pathlib import Path
from Task02_Cleaning_Normalisation.cleaning import clean_rows, load_clean_csv
from Task02_Cleaning_Normalisation.normalisation import min_max
from Task06_Cleaning_Pipeline.cleaning_pipeline import load_clean_text

class CleaningTests(unittest.TestCase):
    def test_valid_and_invalid_values(self):
        rows=[{"station":"Adyar","date":"2026-10-01","hour":"0","pm25":"48","pm10":"70","no2":"17","co":".3","temperature":"77","temperature_unit":"F"},
              {"station":"Adyar","date":"2026-10-01","hour":"0","pm25":"49","pm10":"70","no2":"17","co":".3","temperature":"25","temperature_unit":"C"}]
        good,bad=clean_rows(rows); self.assertEqual(len(good),1); self.assertEqual(len(bad),1)
        self.assertAlmostEqual(good[0]["temperature_c"],25)
    def test_minmax(self):
        self.assertEqual(min_max([48,95,121]),[0.0,.644,1.0]); self.assertEqual(min_max([]),[]); self.assertEqual(min_max([4,4]),[0.0,0.0])
    def test_above_999_skipped(self):
        self.assertEqual(load_clean_text("station,date,pm25\nRohit,2026-10-01,1000\nRohit,2026-10-02,3\n"),[("Rohit","2026-10-02",3.0)])
    def test_missing_columns_safe(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bad.csv"; p.write_text("station,date,pm25\nAdyar,2026-10-01,48\n")
            with self.assertRaises(ValueError): load_clean_csv(p)
    def test_empty_csv_safe(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"empty.csv"; p.write_text("")
            with self.assertRaises(ValueError): load_clean_csv(p)
    def test_invalid_and_negative_numbers(self):
        base={"station":"Rohit","date":"2026-10-01","hour":"0","pm10":"70","no2":"17","co":".3","temperature":"25","temperature_unit":"C"}
        rows=[dict(base,pm25="bad"),dict(base,date="2026-10-02",pm25="-2"),dict(base,date="2026-10-03",pm25="48")]
        good,bad=clean_rows(rows)
        self.assertEqual(len(good),1); self.assertEqual(good[0]["pm25"],48.0); self.assertEqual(len(bad),2)

if __name__=="__main__": unittest.main()

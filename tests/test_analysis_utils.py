"""Regression tests for financial-data alignment and estimator conventions."""
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import numpy as np
import pandas as pd
import statsmodels.api as sm
import analysis_utils as a

class DataTests(unittest.TestCase):
    def archive(self, text):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as z:
            z.writestr('factors.csv', text)
        return buffer.getvalue()

    def test_first_table_only_and_missing_values(self):
        payload = self.archive('Provider notes\n, Mkt-RF, SMB\n202601,1.2,-99.99\n202602,-2.1,-999\n\nAnnual table\n, Mkt-RF, SMB\n202601,88,99\n')
        d = a.parse_french_zip(payload)
        self.assertEqual(len(d), 2)
        self.assertEqual(d.iloc[0,0], 1.2)
        self.assertTrue(d.SMB.isna().all())
        self.assertEqual(d.index[1], pd.Timestamp('2026-02-01'))

    def test_duplicate_or_missing_month_fails(self):
        for dates in [('202601','202601'),('202601','202603')]:
            with self.assertRaises(ValueError):
                a.parse_french_zip(self.archive(f', A\n{dates[0]},1\n{dates[1]},2\n'))

    def test_daily_table_is_separate_frequency(self):
        d = a.parse_french_zip(self.archive(', A\n20260102,2\n20260105,3\n'), 'daily')
        self.assertEqual(len(d), 2)
        with self.assertRaises(ValueError):
            a.parse_french_zip(self.archive(', A\n20260102,2\n'))

    def test_month_end_not_first_trading_day(self):
        p = pd.Series([100,105,110,115,121], index=pd.to_datetime(['2025-12-31','2026-01-02','2026-01-30','2026-02-02','2026-02-27']))
        with patch.object(a, 'AS_OF', pd.Timestamp('2026-02-28')):
            r = a.monthly_returns(p)
        np.testing.assert_allclose(r, [.1,.1])
        self.assertEqual(list(r.index), list(pd.to_datetime(['2026-01-01','2026-02-01'])))

    def test_launch_partial_and_unfinished_month_excluded(self):
        p = pd.Series([100,105,110,130], index=pd.to_datetime(['2026-01-15','2026-01-30','2026-02-27','2026-03-15']))
        with patch.object(a,'AS_OF',pd.Timestamp('2026-03-15')):
            r = a.monthly_returns(p)
        self.assertEqual(list(r.index), [pd.Timestamp('2026-02-01')])
        self.assertAlmostEqual(r.iloc[0], 110/105-1)

    def test_missing_month_not_bridged(self):
        p = pd.Series([100,110,120,130], index=pd.to_datetime(['2025-12-31','2026-01-30','2026-03-31','2026-04-30']))
        with patch.object(a,'AS_OF',pd.Timestamp('2026-04-30')):
            r = a.monthly_returns(p)
        self.assertEqual(list(r.index), list(pd.to_datetime(['2026-01-01','2026-04-01'])))

    def test_stale_month_end_is_excluded(self):
        p = pd.Series([100,110,120], index=pd.to_datetime(['2025-12-31','2026-01-15','2026-02-27']))
        with patch.object(a,'AS_OF',pd.Timestamp('2026-02-28')):
            self.assertTrue(a.monthly_returns(p).empty)

    def test_fx_conversion_preserves_first_interval(self):
        idx = pd.to_datetime(['2026-01-30','2026-02-27'])
        p = pd.Series([100.,110.],idx)
        fx = pd.Series([1.1,1.2],idx)
        with patch.object(a,'AS_OF',pd.Timestamp('2026-02-28')):
            r = a.monthly_returns(a.usd_prices(p,fx))
        self.assertAlmostEqual(r.iloc[0], .2)
        with self.assertRaises(ValueError):
            a.usd_prices(p,fx.iloc[:1])

    def test_true_deciles_not_quintiles(self):
        cols = ['Lo 20','Q2','Q3','Q4','Hi 20','Lo 10'] + [f'D{i}' for i in range(2,10)] + ['Hi 10']
        d = pd.DataFrame([np.arange(15)],columns=cols,index=pd.to_datetime(['2026-01-01']))
        with patch.object(a,'load_french',return_value=d):
            result = a.load_beta_portfolios()
        self.assertEqual(result.shape, (1,10))
        self.assertEqual(result.D1.iloc[0],5)
        self.assertEqual(result.D10.iloc[0],14)

    def test_cache_integrity(self):
        with tempfile.TemporaryDirectory() as root:
            path, meta = Path(root)/'prices.csv', Path(root)/'prices.json'
            path.write_text('original')
            d = pd.Series([1], index=pd.to_datetime(['2026-01-01']))
            a._record(path,meta,'test',d)
            a._verify_cache(path,meta)
            path.write_text('changed')
            with self.assertRaises(ValueError): a._verify_cache(path,meta)

class InferenceTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(5)
        self.x = rng.normal(size=(100,3))
        self.y = self.x @ np.array([.3,-.2,1.1]) + rng.normal(size=100)*(1+abs(self.x[:,0]))

    def test_lag_zero_corrected_equals_hc1(self):
        hac = a.fit_hac(self.y,self.x,lags=0)
        hc1 = sm.OLS(self.y,sm.add_constant(self.x)).fit(cov_type='HC1',use_t=False)
        np.testing.assert_allclose(hac.params,hc1.params)
        np.testing.assert_allclose(hac.cov_params(),hc1.cov_params())
        self.assertFalse(hac.use_t)

    def test_common_sample_weighted_beta_identity(self):
        y2 = self.y[::-1]
        combo = a.fit_hac(.4*self.y+.6*y2,self.x)
        expected = .4*a.fit_hac(self.y,self.x).params+.6*a.fit_hac(y2,self.x).params
        np.testing.assert_allclose(combo.params,expected,atol=1e-12)

    def test_misaligned_dates_and_rank_deficiency_fail(self):
        with self.assertRaises(ValueError):
            a.fit_hac(pd.Series(self.y),pd.DataFrame(self.x,index=np.arange(1,101)))
        with self.assertRaises(ValueError):
            a.fit_hac(self.y,np.ones((100,2)))
        with self.assertRaises(ValueError):
            a.fit_hac(self.y,self.x,lags=100)

if __name__ == '__main__':
    unittest.main()

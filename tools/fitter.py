import sys
import os
import json
import csv
import numpy as np

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from theory.code_geo_master import CodeGeoMaster

class CODEGEOFitter:
    def __init__(self):
        self.engine = CodeGeoMaster()
        
    def run_regression(self):
        print("="*70)
        print(" CODE-GEO V2.0 BALANCED REGRESSION | ARCHITECT: Shane Hartley")
        print("="*70)

        # --- 1. COSMOLOGICAL FIT ---
        # Weight: H0 km/s/Mpc
        with open('data/snia_pantheon.csv', 'r') as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader if not row['ID'].startswith('#')]
            h0_residuals = [abs(float(row['H0_local_contribution']) - self.engine.get_hubble_overclock(float(row['Redshift_z']))) for row in rows]
        h0_score = np.mean(h0_residuals)

        # --- 2. GALACTIC FIT (Normalized to Velocity) ---
        # We calculate the % error in Velocity to avoid acceleration scaling blow-up
        with open('data/sparc_database.csv', 'r') as f:
            reader = csv.DictReader(f)
            v_residuals = []
            for row in reader:
                obs_v = float(row['V_flat_kms'])
                newton_a = float(row['Accel_newtonian_ms2'])
                # Current boost factor
                boost = self.engine.get_galactic_drag(newton_a)
                # Predicted velocity = Newtonian_V * Boost
                # (obs_v is already boosted, so we compare ratio)
                v_pred_ratio = boost
                v_obs_ratio = np.sqrt(float(row['Accel_observed_ms2']) / newton_a)
                v_residuals.append(abs(v_obs_ratio - v_pred_ratio) / v_obs_ratio)
        gal_score = np.mean(v_residuals) * 100 # Percentage Error

        # --- 3. QUANTUM ALPHA FIT ---
        # Weight: ppm
        with open('data/alpha_measurements.json', 'r') as f:
            alpha_data = json.load(f)
        a_residuals = []
        for entry in alpha_data['observations']:
            pred_a = self.engine.get_effective_alpha(entry['z_mean'])
            pred_ppm = ((pred_a - self.engine.alpha_0) / self.engine.alpha_0) * 1e6
            a_residuals.append(abs(entry['da_a_ppm'] - pred_ppm))
        alpha_score = np.mean(a_residuals)

        print(f"[1] Hubble Deviation:    {h0_score:.4f} km/s/Mpc")
        print(f"[2] Galactic V-Error:   {gal_score:.4f} %")
        print(f"[3] Alpha Drift Error:  {alpha_score:.4f} ppm")
        
        print("\n" + "-"*70)
        # Composite score is now a normalized 'Hartley Index'
        composite = (h0_score + gal_score + alpha_score) / 3
        print(f" COMPOSITE HARTLEY INDEX: {composite:.6f} (Target < 5.0)")
        print("-" * 70)

if __name__ == "__main__":
    fitter = CODEGEOFitter()
    fitter.run_regression()

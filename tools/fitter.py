import sys
import os
import csv
import json
import numpy as np

# Ensure root directory is in path for theory imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from theory.code_geo_master import CodeGeoMaster

class CODEGEOFitter:
    """
    VALIDATION ENGINE: CODE-GEO V2.6 (Hartley-Krylov Release)
    Finalized validation suite for Holographic Update Latency.
    Architect: Shane Hartley
    """
    def __init__(self):
        self.engine = CodeGeoMaster()
        
    def run_regression(self):
        print("="*70)
        print(" CODE-GEO V2.6 FINAL VALIDATION | ARCHITECT: Shane Hartley")
        print("="*70)

        # --- 1. HUBBLE TENSION RESOLUTION ---
        with open('data/snia_pantheon.csv', 'r') as f:
            h_data = list(csv.DictReader(f))
            h0_score = np.mean([abs(float(r['H0_local_contribution']) - 
                       self.engine.get_hubble_overclock(float(r['Redshift_z']))) for r in h_data])

        # --- 2. GALACTIC VELOCITY-SPACE (RAR/SPARC) ---
        v_errors = []
        with open('data/sparc_database.csv', 'r') as f:
            for r in csv.DictReader(f):
                obs, new = float(r['Accel_observed_ms2']), float(r['Accel_newtonian_ms2'])
                # Required Boost derivation
                req_boost = np.sqrt(obs / new)
                # Engine Prediction via Hartley-Krylov Damping
                pred_boost = self.engine.get_galactic_drag(new)
                v_errors.append(abs(req_boost - pred_boost) / req_boost)
        gal_score = np.mean(v_errors) * 100 

        # --- 3. QUANTUM ALPHA DRIFT ---
        with open('data/alpha_measurements.json', 'r') as f:
            alpha_data = json.load(f)['observations']
            alpha_score = np.mean([abs(e['da_a_ppm'] - 
                          ((self.engine.get_effective_alpha(e['z_mean']) - 
                          self.engine.alpha_0)/self.engine.alpha_0)*1e6) for e in alpha_data])

        # --- OUTPUT REPORT ---
        print(f"[1] Hubble Deviation:   {h0_score:.4f} km/s/Mpc")
        print(f"[2] Galactic V-Error:   {gal_score:.4f} %")
        print(f"[3] Alpha Drift Error:  {alpha_score:.4f} ppm")
        
        print("\n" + "-"*70)
        composite = (h0_score + gal_score + alpha_score) / 3
        print(f" COMPOSITE HARTLEY INDEX: {composite:.6f}")
        print("-" * 70)

if __name__ == "__main__":
    # Clean up stale bytecode before execution
    os.system('find . -name "__pycache__" -delete 2>/dev/null')
    CODEGEOFitter().run_regression()

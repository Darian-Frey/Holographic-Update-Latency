import sys
import os
import numpy as np

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from theory.code_geo_master import CodeGeoMaster

class PhysicsAuditor:
    """
    UAP V2.2 COMPLIANCE AUDITOR
    Checks CODE-GEO parameters against observational 'Hard Constraints'.
    """
    def __init__(self):
        self.engine = CodeGeoMaster()
        self.pass_count = 0
        self.fail_count = 0

    def report(self, condition, message):
        if condition:
            print(f"  [✅ PASS] {message}")
            self.pass_count += 1
        else:
            print(f"  [❌ FAIL] {message}")
            self.fail_count += 1

    def run_audit(self):
        print("="*60)
        print(" CODE-GEO PHYSICS AUDIT: UAP V2.2 COMPLIANCE")
        print(f" ARCHITECT: Shane Hartley")
        print("="*60)

        # 1. Check Hubble Tension Resolution
        h0_local = self.engine.get_hubble_overclock(0.0)
        self.report(72.0 <= h0_local <= 74.5, f"Local H0 (z=0): {h0_local:.2f} km/s/Mpc (Target: ~73.2)")

        # 2. Check BBN-Wall Safety
        h0_high_z = self.engine.get_hubble_overclock(1100.0)
        self.report(67.0 <= h0_high_z <= 68.0, f"High-z H0 (z=1100): {h0_high_z:.2f} km/s/Mpc (Target: ~67.4)")

        # 3. Check Alpha Drift Constraints
        alpha_today = self.engine.get_effective_alpha(0.0)
        alpha_pivot = self.engine.get_effective_alpha(0.245)
        drift = (alpha_pivot - alpha_today) / alpha_today
        self.report(abs(drift) < 1e-8, f"Alpha Drift (z=0.245): {drift:.2e} (Constraint: < 1e-8)")

        # 4. Check Galactic Drag Scaling
        drag_boost = self.engine.get_galactic_drag(1e-11)
        self.report(3.0 <= drag_boost <= 4.0, f"Galactic Boost: {drag_boost:.2f}x (Target: ~3.5x for SPARC)")

        print("-" * 60)
        if self.fail_count == 0:
            print(f"RESULT: ALL {self.pass_count} TESTS PASSED. THEORY STABLE.")
            return True
        else:
            print(f"RESULT: {self.fail_count} CRITICAL FAILURES. RECOVERY_NODE TRIGGERED.")
            return False

if __name__ == "__main__":
    auditor = PhysicsAuditor()
    stable = auditor.run_audit()
    if not stable:
        sys.exit(1) # Fail the CI/CD build

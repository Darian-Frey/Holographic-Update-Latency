import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from theory.code_geo_master import CodeGeoMaster

def simulate_alpha_drift():
    engine = CodeGeoMaster()
    
    # Redshift range from today (0) back to the "Wall" (0.245)
    z = np.linspace(0, 0.3, 300)
    
    # Calculate Alpha at each redshift
    alpha_vals = [engine.get_effective_alpha(zi) for zi in z]
    alpha_0 = engine.alpha_0
    
    # Calculate relative shift: Δα/α
    delta_alpha_ratio = [(a - alpha_0) / alpha_0 for a in alpha_vals]
    
    plt.figure(figsize=(10, 6))
    
    # Plot the CODE-GEO Prediction
    plt.plot(z, delta_alpha_ratio, label='CODE-GEO Prediction (Δα/α)', color='yellow', linewidth=2.5)
    
    # Add Measurement Constraints (Standard Model expectations are ~0)
    plt.axhline(y=0, color='white', linestyle='--', alpha=0.3, label='Standard Model (Fixed α)')
    
    # Highlight the 10^-9 sensitivity zone (The "Killer Prediction")
    plt.fill_between(z, -2e-9, 2e-9, color='blue', alpha=0.1, label='Experimental Error Margin')

    # Formatting
    plt.title("Holographic Alpha: The Vacuum Baud-Rate Drift", fontsize=14, color='white')
    plt.xlabel("Redshift (z)", fontsize=12, color='white')
    plt.ylabel("Relative Shift (Δα/α)", fontsize=12, color='white')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    
    # Styling
    plt.gcf().set_facecolor('#121212')
    plt.gca().set_facecolor('#1e1e1e')
    plt.gca().tick_params(colors='white')
    plt.gca().yaxis.get_offset_text().set_color('white')
    plt.legend(facecolor='#333333', edgecolor='white', labelcolor='white', loc='lower left')
    plt.grid(True, which="both", ls="-", alpha=0.1)
    
    output_path = 'docs/alpha_drift_prediction.png'
    plt.savefig(output_path, facecolor='#121212')
    print(f"✅ Success: Alpha Drift plot saved to {output_path}")

if __name__ == "__main__":
    simulate_alpha_drift()

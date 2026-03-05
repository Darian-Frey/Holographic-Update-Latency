import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure the root directory is in the path so we can import the theory engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from theory.code_geo_master import CodeGeoMaster

def generate_hubble_plot():
    engine = CodeGeoMaster()
    
    # Generate redshift range (Log scale to see both local and CMB scales)
    z_range = np.logspace(-3, 3.1, 500) 
    h0_values = [engine.get_hubble_overclock(z) for z in z_range]
    
    plt.figure(figsize=(10, 6))
    
    # Plot the CODE-GEO Prediction
    plt.plot(z_range, h0_values, label='CODE-GEO V2.0 Prediction', color='cyan', linewidth=2.5)
    
    # Add Observational Markers
    plt.axhline(y=73.2, color='red', linestyle='--', alpha=0.6, label='SH0ES (Local) ~ 73.2')
    plt.axhline(y=67.4, color='orange', linestyle='--', alpha=0.6, label='Planck (CMB) ~ 67.4')
    
    # Highlight the BBN-Wall (Thaw Point)
    plt.axvspan(0, 0.245, color='green', alpha=0.1, label='Overclocked Zone (Local)')
    plt.vlines(0.245, 65, 75, colors='white', linestyles='dotted', label='BBN-Wall (z=0.245)')

    # Formatting
    plt.xscale('log')
    plt.ylim(65, 75)
    plt.title("The Hubble Tension Resolution: Holographic Update Latency", fontsize=14, color='white')
    plt.xlabel("Redshift (z)", fontsize=12, color='white')
    plt.ylabel("Effective H0 (km/s/Mpc)", fontsize=12, color='white')
    
    # Dark Mode Aesthetics for 2026 Researchers
    plt.gcf().set_facecolor('#121212')
    plt.gca().set_facecolor('#1e1e1e')
    plt.gca().tick_params(colors='white')
    plt.gca().spines['bottom'].set_color('white')
    plt.gca().spines['left'].set_color('white')
    
    plt.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
    plt.grid(True, which="both", ls="-", alpha=0.1)
    
    # Save output to docs for the manuscript
    output_path = 'docs/hubble_tension_resolution.png'
    plt.savefig(output_path, facecolor='#121212')
    print(f"✅ Success: Hubble Expansion plot saved to {output_path}")

if __name__ == "__main__":
    generate_hubble_plot()

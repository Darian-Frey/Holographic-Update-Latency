import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from theory.code_geo_master import CodeGeoMaster

def analyze_bbn_wall():
    engine = CodeGeoMaster()
    
    # Range from local (0) to Recombination (1100)
    z = np.linspace(0, 1.0, 1000)
    
    # Calculate components
    overclock_factor = []
    wall_strength = []
    
    for zi in z:
        phi = engine.get_latency_field(zi)
        W = engine.get_wall_suppression(zi)
        # The raw overclock potential vs the suppressed reality
        raw_F = 1.0 + (phi / (np.pi/2)) * 0.0853
        actual_F = 1.0 + (phi / (np.pi/2)) * 0.0853 * W
        
        overclock_factor.append(actual_F)
        wall_strength.append(W)

    plt.figure(figsize=(10, 6))
    
    # Plot 1: The Suppression "Curtain"
    plt.fill_between(z, 0, wall_strength, color='red', alpha=0.1, label='Latency Thaw Zone')
    plt.plot(z, wall_strength, color='red', linewidth=2, label='W(z) Suppression Factor')
    
    # Plot 2: The Hubble Deviation
    plt.plot(z, overclock_factor, color='cyan', linewidth=2.5, label='Effective H0 Scaling')
    
    # Markers
    plt.axvline(x=0.245, color='white', linestyle='--', label='The BBN-Wall (z=0.245)')
    
    # Annotations
    plt.text(0.05, 0.5, "LATENCY ACTIVE\n(Local Overclocking)", color='cyan', fontweight='bold')
    plt.text(0.4, 0.5, "LATENCY SUPPRESSED\n(Standard Physics)", color='white', fontweight='bold', alpha=0.5)

    # Formatting
    plt.title("The BBN-Wall: Protecting Early Universe Nucleosynthesis", fontsize=14, color='white')
    plt.xlabel("Redshift (z)", fontsize=12, color='white')
    plt.ylabel("Relative Magnitude", fontsize=12, color='white')
    plt.ylim(0, 1.2)
    
    # Styling
    plt.gcf().set_facecolor('#121212')
    plt.gca().set_facecolor('#1e1e1e')
    plt.gca().tick_params(colors='white')
    plt.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
    plt.grid(True, which="both", ls="-", alpha=0.1)
    
    output_path = 'docs/bbn_wall_mechanics.png'
    plt.savefig(output_path, facecolor='#121212')
    print(f"✅ BBN-Wall Analysis saved: {output_path}")

if __name__ == "__main__":
    analyze_bbn_wall()

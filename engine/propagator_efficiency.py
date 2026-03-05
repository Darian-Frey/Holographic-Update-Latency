import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from theory.code_geo_master import CodeGeoMaster

def calculate_computational_efficiency():
    engine = CodeGeoMaster()
    
    # Redshift range for efficiency mapping
    z = np.linspace(0, 2.0, 500)
    
    # Efficiency is the ratio of local 'overclocked' H0 vs global Planck H0
    # In Shane Hartley's model, this represents the 'Krylov Gain'
    efficiency_gain = []
    bit_latency = []
    
    for zi in z:
        h0_eff = engine.get_hubble_overclock(zi)
        eta = h0_eff / engine.H0_global
        
        # Latency is inversely proportional to efficiency
        # We normalize 1.0 as the 'Global Clock Speed'
        latency = 1.0 / eta 
        
        efficiency_gain.append(eta)
        bit_latency.append(latency)

    # Plotting the Efficiency-Latency Duality
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Panel 1: Efficiency Gain
    ax1.plot(z, efficiency_gain, color='lime', linewidth=2.5, label='Propagator Efficiency (η)')
    ax1.set_xlabel('Redshift (z)', color='white')
    ax1.set_ylabel('Efficiency Gain Factor', color='lime')
    ax1.tick_params(axis='y', labelcolor='lime')
    
    # Panel 2: Vacuum Latency
    ax2 = ax1.twinx()
    ax2.plot(z, bit_latency, color='orange', linestyle='--', linewidth=2, label='Vacuum Latency (τ)')
    ax2.set_ylabel('Normalized Bit-Latency', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    plt.title("Vacuum Propagator: Efficiency vs. Latency (Shane Hartley Model)", color='white', fontsize=14)
    plt.axvline(x=0.245, color='red', linestyle=':', alpha=0.5, label='BBN-Wall (Max Latency Lock)')
    
    # Styling
    plt.gcf().set_facecolor('#121212')
    ax1.set_facecolor('#1e1e1e')
    ax1.grid(alpha=0.1)
    
    # Save results
    output_path = 'docs/propagator_efficiency.png'
    plt.savefig(output_path, facecolor='#121212')
    print(f"✅ Propagator Efficiency Analysis saved: {output_path}")

if __name__ == "__main__":
    calculate_computational_efficiency()

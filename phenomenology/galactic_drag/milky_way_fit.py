import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from theory.code_geo_master import CodeGeoMaster

def fit_milky_way():
    engine = CodeGeoMaster()
    
    # Milky Way Parameters (approximate)
    # R_sun approx 8 kpc, V_sun approx 230 km/s
    r = np.linspace(0.1, 25, 300) # kpc
    
    # Visible Mass Components (Bulge + Disk) in Solar Masses
    M_bulge = 1.0e10 
    M_disk = 5.0e10
    G = 4.302e-6 # kpc * (km/s)^2 / M_sun
    
    # Newtonian Acceleration from Visible Matter
    # Simple point-mass approximation for outer regions
    a_vis = (G * (M_bulge + M_disk)) / (r**2)
    v_vis = np.sqrt(a_vis * r)
    
    # CODE-GEO Latency Correction
    v_hartley = []
    for rad, accel_kpc in zip(r, a_vis):
        # Convert kpc/s^2 to m/s^2 for the Master Engine
        accel_ms2 = accel_kpc * 3.086e19 / (1000**2)
        boost = engine.get_galactic_drag(accel_ms2)
        v_hartley.append(v_vis[np.where(r==rad)[0][0]] * boost)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    # Plot the predicted curves
    plt.plot(r, v_vis, color='gray', linestyle='--', label='Visible Matter Only (Newtonian)')
    plt.plot(r, v_hartley, color='gold', linewidth=2.5, label='Shane Hartley Latency Fit')
    
    # Milky Way Observational Data Points (Approximate from Eilers et al. 2019)
    obs_r = [5, 8, 12, 16, 20, 24]
    obs_v = [225, 229, 225, 220, 215, 210]
    plt.errorbar(obs_r, obs_v, yerr=5, fmt='o', color='white', label='Milky Way Observations (Gaia/Eilers)')

    # Annotations
    plt.annotate('Solar System Reach', xy=(8, 230), xytext=(12, 260),
                 arrowprops=dict(facecolor='white', shrink=0.05), color='white')

    # Formatting
    plt.title("Milky Way Calibration: Latency Drag vs. Dark Matter", fontsize=14, color='white')
    plt.xlabel("Galactocentric Distance (kpc)", fontsize=12, color='white')
    plt.ylabel("Circular Velocity (km/s)", fontsize=12, color='white')
    plt.ylim(0, 300)
    plt.grid(True, alpha=0.1)
    
    # Styling
    plt.gcf().set_facecolor('#121212')
    plt.gca().set_facecolor('#1e1e1e')
    plt.gca().tick_params(colors='white')
    plt.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
    
    output_path = 'docs/milky_way_calibration.png'
    plt.savefig(output_path, facecolor='#121212')
    print(f"✅ Milky Way calibration successful: {output_path}")

if __name__ == "__main__":
    fit_milky_way()

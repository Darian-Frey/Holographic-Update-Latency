import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from theory.code_geo_master import CodeGeoMaster

def simulate_rotation_curve():
    engine = CodeGeoMaster()
    
    # Radial distance from galactic center (kpc)
    r = np.linspace(0.5, 30, 200)
    
    # 1. Newtonian Acceleration (Mass of stars/gas only)
    # Using a simple Milky Way-like mass profile
    M_disk = 5.0e10 # Solar masses
    G = 4.302e-6    # kpc * (km/s)^2 / M_sun
    a_newton = (G * M_disk) / (r**2)
    v_newton = np.sqrt(a_newton * r)
    
    # 2. CODE-GEO Latency Boost
    # Applying the drag boost from the Master Engine
    v_code_geo = []
    for accel, vel in zip(a_newton, v_newton):
        # Convert to m/s^2 for the engine check (1 kpc/s^2 approx 3e-11 m/s^2)
        accel_ms2 = accel * 3.086e19 / (1000**2) 
        boost = engine.get_galactic_drag(accel_ms2)
        v_code_geo.append(vel * boost)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    plt.plot(r, v_newton, label='Newtonian (Visible Matter Only)', color='gray', linestyle='--', linewidth=1.5)
    plt.plot(r, v_code_geo, label='CODE-GEO Prediction (Latency Drag)', color='magenta', linewidth=3)
    
    # Observational "Flat" Region Marker
    plt.axhline(y=220, color='white', alpha=0.2, label='Observed Flat Rotation (~220 km/s)')
    
    # Formatting
    plt.title("Galaxy Rotation Curve: Dark Matter as Informational Drag", fontsize=14, color='white')
    plt.xlabel("Distance from Galactic Center (kpc)", fontsize=12, color='white')
    plt.ylabel("Orbital Velocity (km/s)", fontsize=12, color='white')
    plt.ylim(0, 300)
    
    # Styling
    plt.gcf().set_facecolor('#121212')
    plt.gca().set_facecolor('#1e1e1e')
    plt.gca().tick_params(colors='white')
    plt.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
    plt.grid(True, which="both", ls="-", alpha=0.1)
    
    output_path = 'docs/galactic_rotation_fit.png'
    plt.savefig(output_path, facecolor='#121212')
    print(f"✅ Success: Galactic Rotation plot saved to {output_path}")

if __name__ == "__main__":
    simulate_rotation_curve()

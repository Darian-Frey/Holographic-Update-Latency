import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from theory.code_geo_master import CodeGeoMaster

def generate_unified_dashboard():
    engine = CodeGeoMaster()
    
    # Setup the Figure with Dark Mode Aesthetics
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle(f"CODE-GEO V2.0: Unified Theory Dashboard\nArchitect: Shane Hartley", fontsize=20, color='cyan', fontweight='bold')
    
    gs = GridSpec(2, 2, figure=fig)
    
    # --- PANEL 1: Hubble Tension (Cosmic Scale) ---
    ax1 = fig.add_subplot(gs[0, 0])
    z_hubble = np.logspace(-3, 3, 500)
    h0_vals = [engine.get_hubble_overclock(zi) for zi in z_hubble]
    ax1.plot(z_hubble, h0_vals, color='cyan', linewidth=2, label='CODE-GEO Prediction')
    ax1.axhline(73.2, color='red', linestyle='--', alpha=0.5, label='Local (SH0ES)')
    ax1.axhline(67.4, color='orange', linestyle='--', alpha=0.5, label='Global (Planck)')
    ax1.set_xscale('log')
    ax1.set_title("Hubble Tension Resolution", fontsize=14)
    ax1.set_xlabel("Redshift (z)")
    ax1.set_ylabel("H0 (km/s/Mpc)")
    ax1.legend()
    ax1.grid(alpha=0.2)

    # --- PANEL 2: Galactic Rotation (Meso Scale) ---
    ax2 = fig.add_subplot(gs[0, 1])
    r = np.linspace(0.5, 30, 200)
    v_newton = np.sqrt((4.302e-6 * 5.0e10) / r)
    v_code_geo = []
    for rad, vel in zip(r, v_newton):
        accel_ms2 = (vel**2 / rad) * 3.086e19 / (1000**2)
        v_code_geo.append(vel * engine.get_galactic_drag(accel_ms2))
    ax2.plot(r, v_newton, color='gray', linestyle='--', label='Newtonian')
    ax2.plot(r, v_code_geo, color='magenta', linewidth=2.5, label='CODE-GEO (Latency Drag)')
    ax2.set_title("Galactic Rotation Fit", fontsize=14)
    ax2.set_xlabel("Radius (kpc)")
    ax2.set_ylabel("Velocity (km/s)")
    ax2.legend()
    ax2.grid(alpha=0.2)

    # --- PANEL 3: Alpha Drift (Quantum Scale) ---
    ax3 = fig.add_subplot(gs[1, 0])
    z_alpha = np.linspace(0, 0.5, 300)
    alpha_shift = [(engine.get_effective_alpha(zi) - engine.alpha_0)/engine.alpha_0 for zi in z_alpha]
    ax3.plot(z_alpha, alpha_shift, color='yellow', linewidth=2, label='Δα/α Prediction')
    ax3.fill_between(z_alpha, -1e-8, 1e-8, color='blue', alpha=0.1, label='Constraint Zone')
    ax3.set_title("Holographic Alpha Drift", fontsize=14)
    ax3.set_xlabel("Redshift (z)")
    ax3.set_ylabel("Relative Shift (Δα/α)")
    ax3.legend()
    ax3.grid(alpha=0.2)

    # --- PANEL 4: The Latency Field (Substrate Mechanics) ---
    ax4 = fig.add_subplot(gs[1, 1])
    z_phi = np.linspace(0, 5, 500)
    phi_vals = [engine.get_latency_field(zi) for zi in z_phi]
    ax4.plot(z_phi, phi_vals, color='lime', linewidth=2, label='Φ(z) Refresh Potential')
    ax4.axvline(engine.z_star, color='white', linestyle=':', label='Claude-Frey Pivot')
    ax4.set_title("Substrate Latency Field", fontsize=14)
    ax4.set_xlabel("Redshift (z)")
    ax4.set_ylabel("Refresh Potential (Φ)")
    ax4.legend()
    ax4.grid(alpha=0.2)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_path = 'docs/unified_dashboard.png'
    plt.savefig(output_path, dpi=300)
    print(f"✅ Dashboard generated successfully: {output_path}")

if __name__ == "__main__":
    generate_unified_dashboard()

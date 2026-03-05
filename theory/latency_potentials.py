import numpy as np
import matplotlib.pyplot as plt

class LatencyPotential:
    """
    Formalizes the Informational Potential V(phi) for CODE-GEO V2.0.
    Architect: Shane Hartley
    """
    def __init__(self, phi_star=1.0, z_star=0.67):
        self.phi_star = phi_star
        self.z_star = z_star

    def get_potential(self, phi):
        """
        The Hartley Potential: Defines the energy density of the holographic substrate.
        V(phi) is derived from the requirement that the field stabilizes at high z.
        """
        # A 'Well' potential that captures the state at the Claude-Frey Pivot
        return 0.5 * (phi - (np.pi/4))**2 

    def get_field_evolution(self, z):
        """The primary scalar field evolution across redshift."""
        return (np.pi/2) * self.phi_star - np.arctan(z / self.z_star)

def visualize_potentials():
    model = LatencyPotential()
    z_range = np.linspace(0, 5, 500)
    phi_vals = model.get_field_evolution(z_range)
    v_phi = model.get_potential(phi_vals)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot 1: Field Evolution
    color = 'tab:cyan'
    ax1.set_xlabel('Redshift (z)', color='white')
    ax1.set_ylabel('Field Amplitude (φ)', color=color)
    ax1.plot(z_range, phi_vals, color=color, linewidth=2, label='Field φ(z)')
    ax1.tick_params(axis='y', labelcolor=color)

    # Plot 2: Potential Energy
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Potential V(φ)', color=color)
    ax2.plot(z_range, v_phi, color=color, linestyle='--', linewidth=2, label='Potential V(φ)')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("Latency Potential Landscape (The Hartley Well)", color='white', fontsize=14)
    
    # Styling
    plt.gcf().set_facecolor('#121212')
    ax1.set_facecolor('#1e1e1e')
    ax1.grid(alpha=0.1)
    
    plt.savefig('docs/latency_potentials_math.png', facecolor='#121212')
    print("✅ Latency Potential definitions and visualization generated: docs/latency_potentials_math.png")

if __name__ == "__main__":
    visualize_potentials()

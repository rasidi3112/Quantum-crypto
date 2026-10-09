"""
QUANTUM THREAT VISUALIZATION
Interactive visualizations of quantum computing threats to encryption.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import os

# Set style
plt.style.use('dark_background')

def save_fig(name):
    """Save figure to current directory."""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, 'visualizations', f'{name}.png')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print(f"[OK] Saved: visualizations/{name}.png")

def classical_complexity(bits):
    """Illustrative GNFS asymptotic expression (not a practical cost estimate)."""
    ln_n = bits * np.log(2)
    ln_ln_n = np.log(ln_n)
    c = (64/9) ** (1/3)
    return np.exp(c * (ln_n ** (1/3)) * (ln_ln_n ** (2/3)))

def quantum_complexity(bits):
    """Illustrative cubic proxy for Shor's polynomial asymptotic complexity."""
    return bits ** 3

def plot_complexity_comparison():
    """Plot 1: Complexity comparison."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    bits = np.linspace(64, 4096, 100)
    classical = [classical_complexity(b) for b in bits]
    quantum = [quantum_complexity(b) for b in bits]
    
    ax.semilogy(bits, classical, 'r-', linewidth=3, label='GNFS asymptotic expression', alpha=0.9)
    ax.semilogy(bits, quantum, 'cyan', linewidth=3, label='Shor polynomial proxy', alpha=0.9)
    
    # Mark a familiar key size without implying a runtime estimate.
    ax.axvline(x=2048, color='white', linestyle=':', alpha=0.5)
    ax.text(2100, 1e20, 'RSA-2048', color='white', fontsize=10)
    
    ax.set_xlabel('Key Size (bits)', fontsize=14, color='white')
    ax.set_ylabel('Illustrative asymptotic expression (log scale)', fontsize=14, color='white')
    ax.set_title('Factoring Complexity: Asymptotic Growth Shapes',
                 fontsize=16, fontweight='bold', color='white', pad=20)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(64, 4096)
    ax.set_ylim(1e3, 1e100)
    ax.text(0.02, 0.02, 'Constants, circuit costs, and hardware are omitted; curves are not wall-clock estimates.',
            transform=ax.transAxes, fontsize=9, color='white', alpha=0.8)
    
    plt.tight_layout()
    save_fig('01_complexity_comparison')

def plot_speedup():
    """Plot 2: Explain asymptotic classes without inventing a speedup ratio."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    ax.axis('off')
    ax.text(0.5, 0.79, 'Asymptotic comparison', ha='center', va='center',
            fontsize=23, color='white', fontweight='bold')
    ax.text(0.08, 0.58, 'Classical factoring', fontsize=16, color='#e74c3c', fontweight='bold')
    ax.text(0.08, 0.49, 'GNFS: sub-exponential in the modulus bit length', fontsize=13, color='white')
    ax.text(0.08, 0.31, 'Quantum factoring', fontsize=16, color='cyan', fontweight='bold')
    ax.text(0.08, 0.22, 'Shor: polynomial in the modulus bit length', fontsize=13, color='white')
    ax.text(0.08, 0.08,
            'These complexity classes do not give a practical speedup ratio or attack date.\n'
            'A real attack also needs a sufficiently large, fault-tolerant quantum computer.',
            fontsize=11, color='white', alpha=0.85)
    plt.tight_layout()
    save_fig('02_quantum_speedup')

def plot_timeline():
    """Plot 3: Quantum threat timeline."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # Research, standards, and policy milestones; this is not a hardware forecast.
    events = [
        (1994, 'Shor publishes\nfactoring algorithm', 'theory', 0.72),
        (2001, 'First small-scale\nquantum factoring demo', 'milestone', 0.3),
        (2024, 'NIST publishes\nFIPS 203–205', 'standard', 0.72),
        (2025, 'SP 800-227 final;\nHQC selected', 'standard', 0.3),
        (2035, 'NIST transition\npolicy target', 'policy', 0.3),
    ]
    
    colors = {
        'theory': '#3498db',
        'milestone': '#2ecc71',
        'standard': '#9b59b6',
        'policy': '#f39c12'
    }
    
    for year, label, event_type, y_pos in events:
        color = colors[event_type]
        ax.scatter(year, y_pos, s=300, c=color, zorder=3, edgecolors='white', linewidths=2)
        
        va = 'bottom' if y_pos > 0.5 else 'top'
        offset = 0.08 if y_pos > 0.5 else -0.08
        ax.text(year, y_pos + offset, label, ha='center', va=va, 
               fontsize=10, color='white', fontweight='bold')
    
    # Draw timeline
    ax.plot([1990, 2037], [0.5, 0.5], 'white', linewidth=2, alpha=0.5)
    ax.set_xlim(1990, 2038)
    ax.set_ylim(0, 1)
    ax.set_xlabel('Year', fontsize=14, color='white')
    ax.set_title('PQC and Research Milestones (Not a Q-Day Forecast)',
                 fontsize=16, fontweight='bold', color='white', pad=20)
    
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Legend
    legend_elements = [
        mpatches.Patch(color='#3498db', label='Theory'),
        mpatches.Patch(color='#2ecc71', label='Research milestone'),
        mpatches.Patch(color='#9b59b6', label='Standardization'),
        mpatches.Patch(color='#f39c12', label='Policy target'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    save_fig('03_threat_timeline')

def plot_algorithm_comparison():
    """Plot 4: Show NIST algorithm status without implying exact security bits."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    ax.axis('off')
    ax.set_title('Algorithm Families and NIST Standardization Status',
                 fontsize=16, fontweight='bold', color='white', pad=20)

    rows = [
        ('Quantum-vulnerable public key', 'RSA, Diffie–Hellman, ECDSA',
         'Shor threatens these in principle on a sufficiently capable fault-tolerant computer.', '#e74c3c'),
        ('Final NIST PQC standards', 'ML-KEM (FIPS 203) · ML-DSA (FIPS 204) · SLH-DSA (FIPS 205)',
         'Published in 2024; designed to resist known classical and quantum attacks.', '#2ecc71'),
        ('Selected; standards in development', 'FN-DSA / Falcon (FIPS 206) · HQC (FIPS 207)',
         'Selected by NIST; selection is not the same as a final standard.', '#9b59b6'),
    ]
    for i, (heading, algorithms, note, color) in enumerate(rows):
        y = 0.77 - i * 0.27
        ax.add_patch(mpatches.FancyBboxPatch(
            (0.04, y - 0.16), 0.92, 0.22,
            boxstyle='round,pad=0.012', facecolor=color, alpha=0.18,
            edgecolor=color, linewidth=1.5, transform=ax.transAxes))
        ax.text(0.07, y, heading, transform=ax.transAxes, color=color,
                fontsize=12, fontweight='bold', va='center')
        ax.text(0.07, y - 0.055, algorithms, transform=ax.transAxes,
                color='white', fontsize=10, va='center')
        ax.text(0.07, y - 0.115, note, transform=ax.transAxes,
                color='white', fontsize=9, alpha=0.85, va='center')

    plt.tight_layout()
    save_fig('04_algorithm_comparison')

def plot_qubit_progress():
    """Plot 5: Show one model-dependent RSA-2048 resource estimate."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    estimate_millions = [20]
    ax.barh(['Gidney & Ekerå (2021)'], estimate_millions, color='cyan', alpha=0.8)
    ax.text(10, 0, '20 million physical qubits',
            va='center', ha='center', color='#1a1a2e', fontsize=11, fontweight='bold')
    ax.set_xlabel('Estimated physical qubits (millions)', fontsize=13, color='white')
    ax.set_title('One Model-Dependent Estimate for RSA-2048',
                 fontsize=16, fontweight='bold', color='white', pad=20)
    ax.text(0.02, 0.03,
            'The paper modeled an 8-hour runtime. This is not a current capability, universal threshold, or forecast.\n'
            'Logical and physical qubit counts are different quantities.',
            transform=ax.transAxes, fontsize=10, color='white', alpha=0.85)
    ax.set_xlim(0, 24)
    ax.set_ylim(-0.7, 0.7)
    ax.grid(axis='x', alpha=0.2)
    
    plt.tight_layout()
    save_fig('05_qubit_progress')

if __name__ == "__main__":
    print("=" * 60)
    print("  GENERATING QUANTUM THREAT VISUALIZATIONS")
    print("=" * 60)
    
    plot_complexity_comparison()
    plot_speedup()
    plot_timeline()
    plot_algorithm_comparison()
    plot_qubit_progress()
    
    print("\n" + "=" * 60)
    print("[OK] All visualizations saved to: visualizations/")
    print("=" * 60)

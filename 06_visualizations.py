"""
📈 QUANTUM THREAT VISUALIZATION
Visualisasi interaktif ancaman quantum computing terhadap enkripsi.
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
    path = f'/Users/macbook/Documents/QuantumCrypto/visualizations/{name}.png'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print(f"✅ Saved: {path}")

def classical_complexity(bits):
    """GNFS complexity."""
    n = 2 ** bits
    ln_n = bits * np.log(2)
    ln_ln_n = np.log(ln_n)
    c = (64/9) ** (1/3)
    return np.exp(c * (ln_n ** (1/3)) * (ln_ln_n ** (2/3)))

def quantum_complexity(bits):
    """Shor's algorithm complexity."""
    return bits ** 3

def plot_complexity_comparison():
    """Plot 1: Complexity comparison."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    bits = np.linspace(64, 4096, 100)
    classical = [classical_complexity(b) for b in bits]
    quantum = [quantum_complexity(b) for b in bits]
    
    ax.semilogy(bits, classical, 'r-', linewidth=3, label='Classical (GNFS)', alpha=0.9)
    ax.semilogy(bits, quantum, 'cyan', linewidth=3, label='Quantum (Shor)', alpha=0.9)
    
    # Fill danger zone
    ax.fill_between(bits, quantum, classical, alpha=0.2, color='red')
    
    # Reference lines
    year_ops = 1e9 * 3600 * 24 * 365  # ops per year at 1GHz
    ax.axhline(y=year_ops, color='yellow', linestyle='--', alpha=0.5, linewidth=1)
    ax.text(500, year_ops * 3, '1 Year @ 1 GHz', color='yellow', fontsize=10)
    
    ax.axhline(y=year_ops * 1e9, color='orange', linestyle='--', alpha=0.5, linewidth=1)
    ax.text(500, year_ops * 1e9 * 3, '1 Billion Years', color='orange', fontsize=10)
    
    # Current standards
    ax.axvline(x=2048, color='white', linestyle=':', alpha=0.5)
    ax.text(2100, 1e20, 'RSA-2048\n(Current Standard)', color='white', fontsize=10)
    
    ax.set_xlabel('Key Size (bits)', fontsize=14, color='white')
    ax.set_ylabel('Operations Required (log scale)', fontsize=14, color='white')
    ax.set_title('⚛️ THE QUANTUM THREAT: Classical vs Quantum Complexity', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(64, 4096)
    ax.set_ylim(1e3, 1e100)
    
    plt.tight_layout()
    save_fig('01_complexity_comparison')
    # plt.show()  # Disabled for non-interactive mode

def plot_speedup():
    """Plot 2: Quantum speedup factor."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    bits = np.linspace(64, 4096, 100)
    speedup = [classical_complexity(b) / quantum_complexity(b) for b in bits]
    
    # Create gradient effect
    colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(bits)))
    for i in range(len(bits)-1):
        ax.fill_between(bits[i:i+2], 1, speedup[i:i+2], color=colors[i], alpha=0.8)
    
    ax.semilogy(bits, speedup, 'white', linewidth=2)
    
    # Annotations
    key_sizes = [512, 1024, 2048, 4096]
    for ks in key_sizes:
        sp = classical_complexity(ks) / quantum_complexity(ks)
        ax.annotate(f'RSA-{ks}\n{sp:.0e}x faster', 
                   xy=(ks, sp), xytext=(ks+200, sp*10),
                   color='white', fontsize=10, ha='center',
                   arrowprops=dict(arrowstyle='->', color='white', alpha=0.5))
    
    ax.set_xlabel('Key Size (bits)', fontsize=14, color='white')
    ax.set_ylabel('Quantum Speedup Factor (log scale)', fontsize=14, color='white')
    ax.set_title('🚀 QUANTUM SPEEDUP: How Much Faster is Shor\'s Algorithm?', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    ax.grid(True, alpha=0.2)
    ax.set_xlim(64, 4096)
    
    plt.tight_layout()
    save_fig('02_quantum_speedup')
    # plt.show()  # Disabled for non-interactive mode

def plot_timeline():
    """Plot 3: Quantum threat timeline."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # Timeline data
    events = [
        (1994, 'Shor\'s Algorithm\nInvented', 'theory', 0.3),
        (1999, 'RSA-512\nBroken (Classical)', 'broken', 0.5),
        (2001, 'First Quantum\nFactoring (15=3×5)', 'milestone', 0.7),
        (2009, 'RSA-768\nBroken (Classical)', 'broken', 0.5),
        (2019, 'Google Quantum\nSupremacy', 'milestone', 0.7),
        (2023, 'IBM 1000+\nQubits', 'milestone', 0.8),
        (2024, 'NOW', 'now', 1.0),
        (2030, 'RSA-1024\nVulnerable?', 'future', 0.6),
        (2035, 'Q-DAY?\nRSA-2048 Broken', 'danger', 0.4),
    ]
    
    colors = {
        'theory': '#3498db',
        'broken': '#e74c3c',
        'milestone': '#2ecc71',
        'now': '#f39c12',
        'future': '#9b59b6',
        'danger': '#e74c3c'
    }
    
    for year, label, event_type, y_pos in events:
        color = colors[event_type]
        ax.scatter(year, y_pos, s=300, c=color, zorder=3, edgecolors='white', linewidths=2)
        
        if event_type == 'now':
            ax.axvline(x=year, color='#f39c12', linestyle='-', linewidth=3, alpha=0.5)
        
        va = 'bottom' if y_pos > 0.5 else 'top'
        offset = 0.08 if y_pos > 0.5 else -0.08
        ax.text(year, y_pos + offset, label, ha='center', va=va, 
               fontsize=10, color='white', fontweight='bold')
    
    # Draw timeline
    ax.plot([1990, 2040], [0.5, 0.5], 'white', linewidth=2, alpha=0.5)
    
    # Danger zone
    ax.axvspan(2030, 2040, alpha=0.2, color='red')
    ax.text(2035, 0.1, '⚠️ DANGER ZONE', ha='center', fontsize=14, 
           color='red', fontweight='bold')
    
    ax.set_xlim(1990, 2042)
    ax.set_ylim(0, 1)
    ax.set_xlabel('Year', fontsize=14, color='white')
    ax.set_title('⏰ QUANTUM THREAT TIMELINE: The Race Against Time', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Legend
    legend_elements = [
        mpatches.Patch(color='#3498db', label='Theory'),
        mpatches.Patch(color='#e74c3c', label='Broken'),
        mpatches.Patch(color='#2ecc71', label='Milestone'),
        mpatches.Patch(color='#f39c12', label='Current'),
        mpatches.Patch(color='#9b59b6', label='Predicted'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    save_fig('03_threat_timeline')
    # plt.show()  # Disabled for non-interactive mode

def plot_algorithm_comparison():
    """Plot 4: Algorithm security comparison."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    algorithms = ['RSA-2048', 'RSA-4096', 'ECC P-256', 'AES-128', 'AES-256', 
                  'Kyber-768', 'Dilithium-3']
    
    classical_security = [112, 140, 128, 128, 256, 128, 128]  # bits
    quantum_security = [0, 0, 0, 64, 128, 128, 128]  # bits (0 = broken)
    
    x = np.arange(len(algorithms))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, classical_security, width, label='Classical Security',
                   color='#3498db', alpha=0.8, edgecolor='white')
    bars2 = ax.bar(x + width/2, quantum_security, width, label='Quantum Security',
                   color='#e74c3c', alpha=0.8, edgecolor='white')
    
    # Add value labels
    for bar, val in zip(bars1, classical_security):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
               f'{val}', ha='center', va='bottom', color='white', fontsize=10)
    
    for bar, val in zip(bars2, quantum_security):
        label = f'{val}' if val > 0 else '❌'
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
               label, ha='center', va='bottom', color='white', fontsize=10)
    
    # Security threshold
    ax.axhline(y=128, color='#2ecc71', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(6.5, 133, '128-bit security threshold', color='#2ecc71', fontsize=10)
    
    ax.set_xlabel('Algorithm', fontsize=14, color='white')
    ax.set_ylabel('Security Level (bits)', fontsize=14, color='white')
    ax.set_title('🔒 ALGORITHM SECURITY: Classical vs Quantum Era', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=45, ha='right')
    ax.legend(fontsize=12)
    ax.set_ylim(0, 280)
    
    # Highlight post-quantum algorithms
    ax.axvspan(4.5, 6.5, alpha=0.1, color='green')
    ax.text(5.5, 260, '← Post-Quantum Safe →', ha='center', 
           color='#2ecc71', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    save_fig('04_algorithm_comparison')
    # plt.show()  # Disabled for non-interactive mode

def plot_qubit_progress():
    """Plot 5: Qubit count progress over time."""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # Historical data (approximate)
    years = [2000, 2005, 2010, 2015, 2017, 2019, 2020, 2021, 2022, 2023, 2024]
    qubits = [5, 12, 14, 17, 50, 53, 65, 127, 433, 1121, 1200]
    
    # Projections
    future_years = [2025, 2027, 2030, 2035]
    projected_qubits = [2000, 5000, 10000, 100000]
    
    # Plot historical
    ax.semilogy(years, qubits, 'o-', color='cyan', linewidth=3, markersize=10,
               label='Achieved')
    
    # Plot projections
    ax.semilogy(future_years, projected_qubits, 's--', color='yellow', 
               linewidth=2, markersize=10, alpha=0.7, label='Projected')
    
    # RSA-2048 threshold (approx 4000 logical qubits needed)
    ax.axhline(y=4000, color='red', linestyle='--', linewidth=2)
    ax.fill_between([2024, 2040], 4000, 1e6, alpha=0.1, color='red')
    ax.text(2035, 5000, 'RSA-2048 Breakable\n(~4000 logical qubits)', 
           color='red', fontsize=11, ha='center')
    
    # Annotate key milestones
    annotations = [
        (2019, 53, 'Google\nSupremacy'),
        (2023, 1121, 'IBM\nCondor'),
    ]
    for year, qubit, label in annotations:
        ax.annotate(label, xy=(year, qubit), xytext=(year-2, qubit*3),
                   color='white', fontsize=9, ha='center',
                   arrowprops=dict(arrowstyle='->', color='white', alpha=0.5))
    
    ax.set_xlabel('Year', fontsize=14, color='white')
    ax.set_ylabel('Number of Qubits (log scale)', fontsize=14, color='white')
    ax.set_title('📈 QUBIT PROGRESS: Racing Toward Cryptographic Relevance', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.2)
    ax.set_xlim(1998, 2038)
    ax.set_ylim(1, 1e6)
    
    plt.tight_layout()
    save_fig('05_qubit_progress')
    # plt.show()  # Disabled for non-interactive mode

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
    print("✅ All visualizations saved to: visualizations/")
    print("=" * 60)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_cohort_heatmap(csv_path='data/cohort_retention.csv', output_dir='dashboards'):
    """Ingests the retention matrix, builds an annotated heatmap, and exports the asset."""
    if not os.path.exists(csv_path):
        print(f"Execution Error: '{csv_path}' missing. Run cohort_analysis.py first.")
        return
        
    # Ensure the destination directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the retention dataset
    df = pd.read_csv(csv_path, index_col='cohort_month')
    
    # Define plotting canvas dimensions
    plt.figure(figsize=(14, 8))
    
    # Apply clean canvas aesthetics
    sns.set_theme(style="white")
    
    # Compile the Heatmap with custom configurations
    ax = sns.heatmap(
        df * 100, 
        annot=True, 
        fmt=".1f", 
        cmap="YlGnBu", 
        linewidths=.5,
        cbar_kws={'label': 'Retention Rate (%)'},
        vmin=0,
        vmax=100
    )
    
    # Structural Labels and Typography
    plt.title('FinTech User Cohort Retention Heatmap (%)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Periods (Months Since Signup)', fontsize=12, labelpad=10)
    plt.ylabel('Registered Cohort Month', fontsize=12, labelpad=10)
    
    # Export execution
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'cohort_heatmap.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"Success: Visualization asset compiled at '{output_path}'")

if __name__ == "__main__":
    generate_cohort_heatmap()
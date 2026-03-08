#!/usr/bin/env python3
"""
Main pipeline for stock analysis
Runs all tasks sequentially in the correct order:
1. Download 2 weeks of data
2. Filter NIFTY 50 stocks
3. Weekly comparison (stock level)
4. Weekly industry comparison
5. Monthly comparison (stock level)
6. Monthly industry comparison
"""

import sys
from datetime import datetime
from utils import setup_directories

# Import all modules
import download_bhavcopy
import filter_nifty50
import weekly_compare
import weekly_industry_compare
import monthly_compare
import monthly_industry_compare


def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def run_pipeline():
    """Run the complete pipeline"""
    
    try:
        print_header("STOCK ANALYSIS PIPELINE STARTED")
        print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Step 1: Setup directories
        print_header("Step 1: Setting Up Directories")
        setup_directories()
        print("✓ Directories created/verified")
        
        # Step 2: Download 2 weeks of data
        print_header("Step 2: Downloading 2 Weeks of Market Data")
        print("Downloading bhav copy files from NSE...")
        download_bhavcopy.download_last_two_weeks()
        print("✓ Download completed")
        
        # Step 3: Filter NIFTY 50 stocks from all raw files
        print_header("Step 3: Filtering NIFTY 50 Stocks")
        print("Processing raw files and filtering NIFTY 50 symbols...")
        filter_nifty50.filter_all_files()
        print("✓ Filtering completed")
        
        # Step 4: Weekly comparison (stock level)
        print_header("Step 4: Weekly Comparison Analysis (Stock Level)")
        print("Comparing week 1 vs week 2 trading metrics...")
        weekly_compare.main()
        print("✓ Weekly stock comparison completed")
        
        # Step 5: Weekly industry comparison
        print_header("Step 5: Weekly Industry Comparison Analysis")
        print("Aggregating weekly data at industry level...")
        weekly_industry_compare.main()
        print("✓ Weekly industry comparison completed")
        
        # Step 6: Monthly comparison (stock level)
        print_header("Step 6: Monthly Comparison Analysis (Stock Level)")
        print("Downloading and processing monthly data...")
        print("Comparing month 1 vs month 2 trading metrics...")
        monthly_compare.main()
        print("✓ Monthly stock comparison completed")
        
        # Step 7: Monthly industry comparison
        print_header("Step 7: Monthly Industry Comparison Analysis")
        print("Aggregating monthly data at industry level...")
        monthly_industry_compare.main()
        print("✓ Monthly industry comparison completed")
        
        # Final summary
        print_header("PIPELINE COMPLETED SUCCESSFULLY")
        print("All outputs saved to data/output/")
        print("\nGenerated files:")
        print("  • weekly_comparison.csv")
        print("  • weekly_industry_comparison.csv")
        print("  • monthly_comparison.csv")
        print("  • monthly_industry_comparison.csv")
        print(f"\nCompletion Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        return True
        
    except Exception as e:
        print_header("PIPELINE FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)

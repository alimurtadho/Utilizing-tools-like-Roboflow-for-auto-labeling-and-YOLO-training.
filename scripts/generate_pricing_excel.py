"""
Generate Pricing Strategy Excel File
"""

import pandas as pd
from datetime import datetime
import os

def create_pricing_excel():
    """Generate comprehensive pricing strategy Excel file"""
    
    output_file = "ASTRA_Pricing_Strategy.xlsx"
    
    # Create Excel writer
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        
        # Sheet 1: SaaS Pricing
        saas_data = {
            'Tier': ['Basic', 'Professional', 'Enterprise'],
            'Price (Rp/month)': [2_500_000, 7_500_000, 25_000_000],
            'Videos/month': ['100', '500', 'Unlimited'],
            'Users': ['1', '5', 'Unlimited'],
            'Storage (GB)': [50, 200, 1000],
            'API Requests/day': ['1,000', '5,000', 'Unlimited'],
            'Support': ['Email', 'Priority (WhatsApp)', '24/7 Dedicated'],
            'AI Insights': ['No', 'Yes', 'Yes + Custom'],
            'Target Customer': ['Small dealers', 'Medium dealers/Police', 'National HQ/Enterprise']
        }
        df_saas = pd.DataFrame(saas_data)
        df_saas.to_excel(writer, sheet_name='SaaS Pricing', index=False)
        
        # Sheet 2: Pay-Per-Video
        ppv_data = {
            'Volume Range': ['1-50', '51-200', '201-1,000', '1,001-5,000', '5,000+'],
            'Price per Video (Rp)': [50_000, 35_000, 25_000, 18_000, 12_000],
            'Example Cost (100 videos)': [
                50_000 * 100 if 100 <= 50 else 50_000 * 50,
                35_000 * 100,
                25_000 * 100,
                18_000 * 100,
                12_000 * 100
            ],
            'Best For': [
                'Small projects, testing',
                'Medium campaigns',
                'Large studies',
                'Enterprise bulk',
                'National programs'
            ]
        }
        df_ppv = pd.DataFrame(ppv_data)
        df_ppv.to_excel(writer, sheet_name='Pay-Per-Video', index=False)
        
        # Sheet 3: Perpetual License
        license_data = {
            'License Type': ['Standard', 'Enterprise'],
            'One-Time Cost (Rp)': [75_000_000, 250_000_000],
            'Annual Maintenance (Rp)': [15_000_000, 50_000_000],
            'Videos/month': ['1,000', 'Unlimited'],
            'Servers': ['1', 'Multi-server'],
            'Support Years': ['1', '3'],
            'Source Code': ['No', 'Optional (+100jt)'],
            'Training': ['1 day', '1 week'],
            'Customization': ['No', 'Yes']
        }
        df_license = pd.DataFrame(license_data)
        df_license.to_excel(writer, sheet_name='Perpetual License', index=False)
        
        # Sheet 4: VM Specifications
        vm_data = {
            'Tier': ['Basic', 'Professional (CPU)', 'Professional (GPU)', 'Enterprise'],
            'vCPU': [4, 8, 8, '16 x 2 servers'],
            'RAM (GB)': [8, 16, 16, '32 x 2 servers'],
            'Storage (GB)': [100, 500, 500, '1000 x 2'],
            'GPU': ['None', 'None', 'T4', 'A10/V100 x3-5'],
            'Processing Speed': ['3-5 FPS', '8-10 FPS', '10-15 FPS', '30-60 FPS'],
            'Concurrent Videos': ['1-2', '3-5', '5-10', '50-100+'],
            'Monthly Cost (USD)': [50, 160, 500, 3500],
            'Monthly Cost (Rp)': [750_000, 2_400_000, 7_500_000, 52_500_000],
            'Videos Capacity/month': [100, 300, 500, 'Unlimited']
        }
        df_vm = pd.DataFrame(vm_data)
        df_vm.to_excel(writer, sheet_name='VM Specifications', index=False)
        
        # Sheet 5: Revenue Projections
        revenue_data = {
            'Scenario': ['Phase 1 (Month 1-6)', 'Phase 2 (Month 7-12)', 'Phase 3 (Year 2+)'],
            'Honda Dealers': [50, 150, 300],
            'Police Departments': [0, 10, 30],
            'Enterprise Clients': [0, 0, 5],
            'Dealer Revenue (Rp/month)': [
                50 * 2_000_000,  # Launch discount
                150 * 2_500_000,
                300 * 2_500_000
            ],
            'Police Revenue (Rp/month)': [
                0,
                10 * 25_000_000,
                30 * 25_000_000
            ],
            'Enterprise Revenue (Rp/month)': [
                0,
                0,
                5 * 50_000_000
            ],
            'Total Revenue/month (Rp)': [
                50 * 2_000_000,
                150 * 2_500_000 + 10 * 25_000_000,
                300 * 2_500_000 + 30 * 25_000_000 + 5 * 50_000_000
            ],
            'Annual Revenue (Rp)': [
                50 * 2_000_000 * 12,
                (150 * 2_500_000 + 10 * 25_000_000) * 12,
                (300 * 2_500_000 + 30 * 25_000_000 + 5 * 50_000_000) * 12
            ]
        }
        df_revenue = pd.DataFrame(revenue_data)
        df_revenue.to_excel(writer, sheet_name='Revenue Projections', index=False)
        
        # Sheet 6: ROI Analysis for Clients
        roi_data = {
            'Customer Type': ['Honda Dealer', 'Police Department'],
            'Manual Cost - Staff (Rp/month)': [10_000_000, 80_000_000],
            'Manual Cost - Supervisor (Rp/month)': [8_000_000, 10_000_000],
            'Manual Cost - Equipment (Rp/month)': [2_000_000, 20_000_000],
            'Total Manual Cost (Rp/month)': [20_000_000, 110_000_000],
            'Astra Cost (Rp/month)': [2_500_000, 25_000_000],
            'Monthly Savings (Rp)': [17_500_000, 85_000_000],
            'Savings Percentage': ['87.5%', '77.3%'],
            'Payback Period': ['Immediate', 'Immediate'],
            'Annual Savings (Rp)': [210_000_000, 1_020_000_000]
        }
        df_roi = pd.DataFrame(roi_data)
        df_roi.to_excel(writer, sheet_name='ROI Analysis', index=False)
        
        # Sheet 7: Cost Breakdown (100 customers)
        cost_data = {
            'Cost Category': [
                'Infrastructure - Servers',
                'Infrastructure - Database',
                'Infrastructure - Storage',
                'Infrastructure - Bandwidth',
                'APIs - Gemini',
                'APIs - Other',
                'Operations - Support Staff',
                'Operations - DevOps',
                'Operations - Customer Success',
                'Sales & Marketing',
                'Sales Commission',
                'Office & Admin',
                'Legal & Accounting',
                'TOTAL COSTS',
                '',
                'REVENUE (100 customers)',
                'NET PROFIT',
                'PROFIT MARGIN'
            ],
            'Monthly Cost (Rp)': [
                15_000_000,
                3_000_000,
                2_000_000,
                5_000_000,
                0,
                1_000_000,
                20_000_000,
                15_000_000,
                12_000_000,
                50_000_000,
                75_000_000,
                10_000_000,
                5_000_000,
                213_000_000,
                None,
                750_000_000,
                537_000_000,
                '71.6%'
            ],
            'Annual Cost (Rp)': [
                180_000_000,
                36_000_000,
                24_000_000,
                60_000_000,
                0,
                12_000_000,
                240_000_000,
                180_000_000,
                144_000_000,
                600_000_000,
                900_000_000,
                120_000_000,
                60_000_000,
                2_556_000_000,
                None,
                9_000_000_000,
                6_444_000_000,
                '71.6%'
            ]
        }
        df_cost = pd.DataFrame(cost_data)
        df_cost.to_excel(writer, sheet_name='Cost Breakdown', index=False)
        
        # Sheet 8: Market Analysis
        market_data = {
            'Market Segment': [
                'Honda Dealers',
                'Police Departments (Provincial)',
                'Police Departments (City/District)',
                'Insurance Companies',
                'Research Institutions',
                'System Integrators',
                'TOTAL TAM'
            ],
            'Total Units': [500, 34, 100, 50, 20, 10, 714],
            'Price Point (Rp/month)': [
                2_500_000,
                25_000_000,
                7_500_000,
                10_000_000,
                5_000_000,
                50_000_000,
                None
            ],
            'Market Potential (Rp/month)': [
                500 * 2_500_000,
                34 * 25_000_000,
                100 * 7_500_000,
                50 * 10_000_000,
                20 * 5_000_000,
                10 * 50_000_000,
                500 * 2_500_000 + 34 * 25_000_000 + 100 * 7_500_000 + 
                50 * 10_000_000 + 20 * 5_000_000 + 10 * 50_000_000
            ],
            'Annual TAM (Rp/year)': [
                500 * 2_500_000 * 12,
                34 * 25_000_000 * 12,
                100 * 7_500_000 * 12,
                50 * 10_000_000 * 12,
                20 * 5_000_000 * 12,
                10 * 50_000_000 * 12,
                (500 * 2_500_000 + 34 * 25_000_000 + 100 * 7_500_000 + 
                 50 * 10_000_000 + 20 * 5_000_000 + 10 * 50_000_000) * 12
            ],
            '10% Penetration (Rp/year)': [
                500 * 2_500_000 * 12 * 0.1,
                34 * 25_000_000 * 12 * 0.1,
                100 * 7_500_000 * 12 * 0.1,
                50 * 10_000_000 * 12 * 0.1,
                20 * 5_000_000 * 12 * 0.1,
                10 * 50_000_000 * 12 * 0.1,
                (500 * 2_500_000 + 34 * 25_000_000 + 100 * 7_500_000 + 
                 50 * 10_000_000 + 20 * 5_000_000 + 10 * 50_000_000) * 12 * 0.1
            ]
        }
        df_market = pd.DataFrame(market_data)
        df_market.to_excel(writer, sheet_name='Market Analysis', index=False)
        
        # Sheet 9: Comparison Matrix
        comparison_data = {
            'Feature': [
                'Pricing Model',
                'Setup Cost',
                'Monthly Cost (100 videos)',
                'Scalability',
                'Support',
                'Updates',
                'Customization',
                'Data Ownership',
                'Infrastructure Management',
                'Best For'
            ],
            'SaaS Basic': [
                'Subscription',
                'Rp 0',
                'Rp 2,500,000',
                'Easy',
                'Email',
                'Automatic',
                'Limited',
                'Shared',
                'Managed by us',
                'Small dealers'
            ],
            'SaaS Professional': [
                'Subscription',
                'Rp 0',
                'Rp 7,500,000',
                'Easy',
                'Priority',
                'Automatic',
                'Moderate',
                'Shared',
                'Managed by us',
                'Medium dealers'
            ],
            'SaaS Enterprise': [
                'Subscription',
                'Rp 0',
                'Rp 25,000,000',
                'Very Easy',
                '24/7 Dedicated',
                'Automatic',
                'Full',
                'Shared',
                'Managed by us',
                'National HQ'
            ],
            'Pay-Per-Video': [
                'Usage-based',
                'Rp 0',
                'Rp 2,500,000 (100 × 25k)',
                'Flexible',
                'Email',
                'Automatic',
                'None',
                'Shared',
                'Managed by us',
                'Project-based'
            ],
            'Perpetual License': [
                'One-time',
                'Rp 75,000,000',
                'Rp 1,250,000 (maintenance)',
                'Manual',
                'Limited',
                'Manual (paid)',
                'Full',
                'Full ownership',
                'Self-managed',
                'Government/Security'
            ]
        }
        df_comparison = pd.DataFrame(comparison_data)
        df_comparison.to_excel(writer, sheet_name='Pricing Comparison', index=False)
        
        # Sheet 10: Implementation Timeline
        timeline_data = {
            'Phase': [
                'Month 1-3',
                'Month 4-6',
                'Month 7-9',
                'Month 10-12',
                'Year 2 Q1',
                'Year 2 Q2',
                'Year 2 Q3-Q4',
                'Year 3+'
            ],
            'Focus': [
                'Launch & Demo',
                'First Customers',
                'Scale Dealers',
                'Add Police',
                'Expand Regions',
                'Enterprise Features',
                'National Coverage',
                'Market Leader'
            ],
            'Target Customers': [
                '10 pilots',
                '20-30 dealers',
                '50-80 dealers',
                '100 dealers + 5 police',
                '150 dealers + 15 police',
                '200 dealers + 25 police',
                '300 dealers + 30 police + 5 enterprise',
                '500+ total'
            ],
            'Monthly Revenue (Rp)': [
                0,  # Pilot free
                50_000_000,
                150_000_000,
                375_000_000,
                525_000_000,
                1_000_000_000,
                1_750_000_000,
                3_000_000_000
            ],
            'Cumulative Revenue (Rp)': [
                0,
                150_000_000,
                600_000_000,
                1_725_000_000,
                3_300_000_000,
                6_300_000_000,
                13_800_000_000,
                50_000_000_000  # Projected by Year 3
            ]
        }
        df_timeline = pd.DataFrame(timeline_data)
        df_timeline.to_excel(writer, sheet_name='Implementation Timeline', index=False)
    
    print(f"✅ Excel file created: {output_file}")
    print(f"📊 Sheets included:")
    print("   1. SaaS Pricing")
    print("   2. Pay-Per-Video")
    print("   3. Perpetual License")
    print("   4. VM Specifications")
    print("   5. Revenue Projections")
    print("   6. ROI Analysis")
    print("   7. Cost Breakdown")
    print("   8. Market Analysis")
    print("   9. Pricing Comparison")
    print("   10. Implementation Timeline")
    
    return output_file

if __name__ == "__main__":
    try:
        output = create_pricing_excel()
        print(f"\n🎉 Success! Open file: {output}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have pandas and openpyxl installed:")
        print("pip install pandas openpyxl")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader


def generate_pricing_html(data_dict):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("report_template.html")
    html_out = template.render(data_dict)
    return html_out




# Configure the page
st.set_page_config(
    page_title="Automation Service Pricing Calculator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Removing the default Streamlit branding from view.
hide_streamlit_style = """
                <style>
                [data-testid="profileContainer"] {
                    display: none !important;
                    visibility: hidden !important;
                }

                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 4px;
    }
    .pricing-box {
        background-color: black;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2C3E50;
    }
    .highlight {
        background-color: black;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    .email-capture {
        background-color: black;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.title("🤖 Automation Service Pricing Calculator")
st.markdown("""
This calculator helps freelancers, VAs, and automation specialists determine 
optimal pricing for their services. Enter your details below to get personalized pricing recommendations.
""")

# Create tabs for different calculator sections
tab1, tab2, tab3 = st.tabs(["Basic Calculator", "Advanced Calculator", "Market Insights"])

with tab1:
    st.header("Basic Automation Service Pricing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Inputs")
        experience_level = st.select_slider(
            "Experience Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate"
        )
        
        service_type = st.multiselect(
            "Type of Automation Services",
            ["Email Automation", "Social Media Automation", "Data Processing", 
             "Workflow Automation", "ChatBot Creation", "Document Automation",
             "Lead Generation Automation", "Customer Service Automation"],
            default=["Email Automation"]
        )
        
        complexity = st.slider(
            "Project Complexity", 
            min_value=1, 
            max_value=10, 
            value=5,
            help="1 = Simple automation, 10 = Complex systems with multiple integrations"
        )
        
        time_required = st.number_input(
            "Estimated Hours Required",
            min_value=1,
            max_value=500,
            value=20,
            help="Total hours you expect to spend on the project"
        )
        
        ongoing_maintenance = st.checkbox("Includes Ongoing Maintenance")
        
        if ongoing_maintenance:
            maintenance_hours = st.number_input(
                "Monthly Maintenance Hours",
                min_value=1,
                max_value=100,
                value=5
            )
        else:
            maintenance_hours = 0
        
        location = st.selectbox(
            "Your Primary Market",
            ["North America", "Europe", "Asia", "Australia/NZ", "South America", "Africa", "Global"]
        )
        
        tools_used = st.multiselect(
            "Tools & Technologies Used",
            ["Zapier", "Make (Integromat)", "IFTTT", "n8n", "Microsoft Power Automate", 
             "UiPath", "Python", "JavaScript", "ChatGPT/Claude AI", "Custom Development"],
            default=["Zapier"]
        )

    # Pricing calculations
    # Base hourly rates by experience level
    hourly_rates = {
        "Beginner": 25,
        "Intermediate": 50,
        "Advanced": 85,
        "Expert": 150
    }
    
    # Modifier for location
    location_modifier = {
        "North America": 1.0,
        "Europe": 0.9,
        "Australia/NZ": 0.95,
        "Asia": 0.7,
        "South America": 0.65,
        "Africa": 0.6,
        "Global": 0.85
    }
    
    # Modifier for complexity
    complexity_modifier = 0.8 + (complexity * 0.04)
    
    # Calculate base hourly rate
    base_rate = hourly_rates[experience_level] * location_modifier[location] * complexity_modifier
    
    # Add premium for specialized tools (10% per additional tool beyond the first)
    tools_premium = 1.0 + (0.05 * (len(tools_used) - 1)) if len(tools_used) > 1 else 1.0
    
    # Adjusted hourly rate
    adjusted_hourly_rate = base_rate * tools_premium
    
    # Project total
    project_total = adjusted_hourly_rate * time_required
    
    # Monthly maintenance fee if applicable
    monthly_maintenance_fee = adjusted_hourly_rate * maintenance_hours if ongoing_maintenance else 0
    
    with col2:
        st.subheader("Recommended Pricing")
        
        pricing_box1, pricing_box2, pricing_box3 = st.columns(3)
        
        with pricing_box1:
            st.metric(
                "Hourly Rate",
                f"${adjusted_hourly_rate:.2f}",
                f"+{((tools_premium - 1) * 100):.0f}% tool premium" if tools_premium > 1 else ""
            )
            
        with pricing_box2:
            st.metric(
                "Project Total",
                f"${project_total:.2f}"
            )
            
        with pricing_box3:
            if ongoing_maintenance:
                st.metric(
                    "Monthly Maintenance",
                    f"${monthly_maintenance_fee:.2f}"
                )
            else:
                st.write("No ongoing maintenance")
        
        st.markdown("---")
        st.subheader("Pricing Structure Options")
        
        st.markdown(f"""
        <div class="pricing-box">
            <h3>Package Pricing</h3>
            <p>Consider offering these packages:</p>
            <ul>
                <li><strong>Basic Package:</strong> ${project_total * 0.8:.2f}</li>
                <li><strong>Standard Package:</strong> ${project_total:.2f}</li>
                <li><strong>Premium Package:</strong> ${project_total * 1.2:.2f} (includes priority support)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="pricing-box">
            <h3>Value-Based Pricing Option</h3>
            <p>If your automation saves significant time or generates revenue, consider charging:</p>
            <ul>
                <li><strong>Value-Based Price:</strong> ${project_total * 1.5:.2f} - ${project_total * 3:.2f}</li>
                <li><strong>ROI-Based Price:</strong> ${project_total:.2f} + 5-10% of demonstrated savings or revenue generated</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Advanced calculator tab
with tab2:
    st.header("Advanced Pricing Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Business Impact Factors")
        
        revenue_impact = st.slider(
            "Expected Revenue Impact for Client",
            min_value=0,
            max_value=100000,
            value=10000,
            step=1000,
            help="Estimated additional revenue your automation will generate for the client"
        )
        
        time_savings = st.slider(
            "Monthly Time Savings (hours)",
            min_value=0,
            max_value=200,
            value=20,
            help="Hours saved per month through your automation"
        )
        
        client_hourly_value = st.number_input(
            "Client's Hourly Value ($)",
            min_value=0,
            max_value=1000,
            value=50,
            help="Estimated hourly value of client's time or employees' time"
        )
        
        integration_count = st.slider(
            "Number of System Integrations",
            min_value=1,
            max_value=20,
            value=2,
            help="How many different systems need to be connected"
        )
        
        custom_coding = st.checkbox("Requires Custom Coding")
        training_required = st.checkbox("Includes Client Training")
        
        monthly_active_users = st.number_input(
            "Expected Monthly Active Users",
            min_value=1,
            max_value=10000,
            value=10,
            help="Number of people who will use the automation"
        )
    
    # Advanced pricing calculations
    # Value-based component
    annual_time_savings_value = time_savings * 12 * client_hourly_value
    total_value = revenue_impact + annual_time_savings_value
    
    # Base cost component (using the basic calculator logic)
    base_project_cost = project_total
    
    # Complexity adders
    integration_cost = 200 * integration_count
    custom_code_cost = 2000 if custom_coding else 0
    training_cost = 500 if training_required else 0
    user_scale_cost = 10 * monthly_active_users
    
    # Calculate enhanced project cost
    enhanced_project_cost = base_project_cost + integration_cost + custom_code_cost + training_cost + user_scale_cost
    
    # Calculate value-based price options
    conservative_value_price = enhanced_project_cost + (total_value * 0.05)
    moderate_value_price = enhanced_project_cost + (total_value * 0.1)
    aggressive_value_price = enhanced_project_cost + (total_value * 0.2)
    
    # Subscription options
    monthly_subscription = (enhanced_project_cost * 0.1) + (monthly_maintenance_fee * 1.2)
    
    with col2:
        st.subheader("Advanced Pricing Recommendations")
        
        st.markdown(f"""
        <div class="pricing-box">
            <h3>Project Value Analysis</h3>
            <p>Based on your inputs, this automation project will deliver approximately:</p>
            <ul>
                <li><strong>Annual Time Savings Value:</strong> ${annual_time_savings_value:,.2f}</li>
                <li><strong>Revenue Impact:</strong> ${revenue_impact:,.2f}</li>
                <li><strong>Total Value to Client:</strong> ${total_value:,.2f}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="pricing-box">
            <h3>Enhanced Project Cost</h3>
            <p>Detailed cost breakdown:</p>
            <ul>
                <li>Base Development Cost: ${base_project_cost:,.2f}</li>
                <li>Integration Complexity: ${integration_cost:,.2f}</li>
                <li>Custom Coding: ${custom_code_cost:,.2f}</li>
                <li>Training Component: ${training_cost:,.2f}</li>
                <li>User Scale Factor: ${user_scale_cost:,.2f}</li>
                <li><strong>Total Enhanced Cost:</strong> ${enhanced_project_cost:,.2f}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="pricing-box">
            <h3>Value-Based Pricing Options</h3>
            <ul>
                <li><strong>Conservative (5% of value):</strong> ${conservative_value_price:,.2f}</li>
                <li><strong>Moderate (10% of value):</strong> ${moderate_value_price:,.2f}</li>
                <li><strong>Aggressive (20% of value):</strong> ${aggressive_value_price:,.2f}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="pricing-box">
            <h3>Subscription Model Option</h3>
            <p><strong>Monthly Subscription:</strong> ${monthly_subscription:,.2f}/month</p>
            <p>This includes ongoing maintenance, updates, and support.</p>
        </div>
        """, unsafe_allow_html=True)
        

# Market insights tab
with tab3:
    st.header("Market Insights & Competitive Analysis")
    
    # Sample market rate data
    market_data = {
        "Service Type": ["Email Automation", "Social Media Automation", "Data Processing", 
                        "Workflow Automation", "ChatBot Creation", "Document Automation",
                        "Lead Generation", "Customer Service Automation"],
        "Entry Level": [25, 30, 20, 35, 40, 25, 30, 35],
        "Mid Level": [50, 60, 45, 70, 80, 55, 65, 75],
        "Expert Level": [90, 100, 85, 120, 150, 95, 110, 130]
    }
    
    market_df = pd.DataFrame(market_data)
    
    st.subheader("Market Rates by Service Type (hourly rates in USD)")
    st.dataframe(market_df.set_index("Service Type"))
    
    # Create a visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Reshape data for plotting
    plot_data = pd.melt(market_df, id_vars=["Service Type"], 
                        value_vars=["Entry Level", "Mid Level", "Expert Level"],
                        var_name="Experience", value_name="Hourly Rate")
    
    # Create the plot
    sns.barplot(x="Service Type", y="Hourly Rate", hue="Experience", data=plot_data, ax=ax)
    ax.set_title("Automation Service Rates by Type and Experience Level")
    ax.set_xlabel("Service Type")
    ax.set_ylabel("Hourly Rate (USD)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Market trends
    st.subheader("Market Trends & Insights")
    
    st.markdown("""
    <div class="highlight">
        <h3>Current Market Trends (2025)</h3>
        <ul>
            <li><strong>Highest Growth Areas:</strong> AI-powered automation, document processing, and customer service automation</li>
            <li><strong>Premium Skills:</strong> LLM integration, multi-system workflows, and security-focused automations</li>
            <li><strong>Pricing Models Shift:</strong> Moving from hourly to value-based and subscription models</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
        <h3>How to Stand Out</h3>
        <ul>
            <li>Develop a specialty in high-demand automation niches</li>
            <li>Create case studies that demonstrate ROI of your automation services</li>
            <li>Offer tiered service packages with clear deliverables</li>
            <li>Provide educational content to attract potential clients</li>
            <li>Build a portfolio of automation templates that showcase your capabilities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)



col1, col2 = st.columns([3, 1])

# Footer with disclaimer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8em;">
    <p>Disclaimer: This calculator provides estimates based on market averages and the information you provide. 
    Actual rates may vary based on specific client needs, industry, and geographic location.</p>
    <p>© 2025 YourCompanyName. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)


# 📄 Generate PDF for Basic + Advanced Calculator
html_report = generate_pricing_html({
    "experience": experience_level,
    "market": location,
    "hours": time_required,
    "complexity": complexity,
    "ongoing": "Yes" if ongoing_maintenance else "No",
    "maintenance_hours": maintenance_hours,
    "tools": ', '.join(tools_used),
    "hourly_rate": f"{adjusted_hourly_rate:.2f}",
    "project_total": f"{project_total:.2f}",
    "maintenance_fee": f"{monthly_maintenance_fee:.2f}",
    "revenue_impact": f"{revenue_impact:,.2f}",
    "time_savings_value": f"{annual_time_savings_value:,.2f}",
    "total_value": f"{total_value:,.2f}",
    "base_cost": f"{base_project_cost:,.2f}",
    "integrations": integration_count,
    "custom_code": "Yes" if custom_coding else "No",
    "training": "Yes" if training_required else "No",
    "users": monthly_active_users,
    "enhanced_cost": f"{enhanced_project_cost:,.2f}",
    "conservative": f"{conservative_value_price:,.2f}",
    "moderate": f"{moderate_value_price:,.2f}",
    "aggressive": f"{aggressive_value_price:,.2f}",
    "subscription": f"{monthly_subscription:,.2f}"
})

st.download_button(
    label="📄 Download Full Pricing Report (HTML)",
    data=html_report.encode("utf-8"),
    file_name="automation_pricing_report.html",
    mime="text/html"
)

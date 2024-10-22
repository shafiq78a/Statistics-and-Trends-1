import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'suicide_rates_1990-2022.csv'
suicide_data = pd.read_csv(file_path)

# Data Cleaning
# Drop duplicate rows if any
suicide_data.drop_duplicates(inplace=True)

# Minimum Expected Statistics: Dataframe describe and correlation (numeric columns only)
numeric_data = suicide_data.select_dtypes(include=['number'])
print(numeric_data.describe())
print(numeric_data.corr())

# Filtering data for Europe and the required years
europe_data = suicide_data[suicide_data['RegionName'] == 'Europe']
europe_data_filtered_extended = europe_data[(europe_data['Year'] >= 2015) & (europe_data['Year'] <= 2020)]
top_countries_extended = europe_data_filtered_extended.groupby('CountryName')['DeathRatePer100K'].sum().nlargest(5).index
europe_top5_extended = europe_data_filtered_extended[europe_data_filtered_extended['CountryName'].isin(top_countries_extended)]

# Function to create Bar Chart: Distribution of suicide rates by age group (excluding 'Unknown')
def plot_bar_chart():
    plt.figure(figsize=(10, 6))
    filtered_suicide_data = suicide_data[suicide_data['AgeGroup'] != 'Unknown']
    sns.barplot(data=filtered_suicide_data, x='AgeGroup', y='DeathRatePer100K', ci=None, estimator=sum)
    plt.title('Distribution of Suicide Rates by Age Group', fontsize=16, fontweight='bold')
    plt.xlabel('Age Group', fontsize=14, fontweight='bold')
    plt.ylabel('Total Death Rate per 100K', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Function to create Enhanced Line Chart

def plot_line_chart():
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")  # Set style to remove background color
    sns.lineplot(data=europe_top5_extended, x='Year', y='DeathRatePer100K', hue='CountryName', marker='o', linewidth=3, palette='Set1', alpha=1, legend='full')

    plt.title('Trends in Suicide Rates for Top 5 European Countries (2015-2020)', fontsize=18, fontweight='bold', color='darkblue')
    plt.xlabel('Year', fontsize=14, fontweight='bold', color='darkblue')
    plt.ylabel('Death Rate per 100K', fontsize=14, fontweight='bold', color='darkblue')
    plt.xticks(fontsize=12, fontweight='bold', color='black')
    plt.yticks(fontsize=12, fontweight='bold', color='black')

    plt.legend(title='Country Name', loc='upper right', fontsize='large', title_fontsize='x-large', fancybox=True, shadow=True, borderpad=1, frameon=False, prop={'weight': 'bold'})
    plt.grid(visible=True, linestyle='--', linewidth=0.7, alpha=0.7)
    plt.tight_layout()
    plt.show()

# Function to create Heatmap: Correlation matrix for various socioeconomic factors
def plot_heatmap():
    plt.figure(figsize=(12, 8))
    correlation_columns = ['DeathRatePer100K', 'Population', 'GDP', 'GDPPerCapita', 'GrossNationalIncome', 
                           'GNIPerCapita', 'InflationRate', 'EmploymentPopulationRatio']
    sns.heatmap(suicide_data[correlation_columns].corr(), annot=True, cmap='coolwarm', linewidths=0.5, annot_kws={"weight": "bold", "fontsize": 12})
    plt.title('Correlation Matrix of Socioeconomic Factors', fontsize=16, fontweight='bold')
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Function to create Pie Chart: Distribution of suicide cases by sex in 2015
def plot_pie_chart():
    plt.figure(figsize=(10, 10))
    suicide_2015 = suicide_data[suicide_data['Year'] == 2015]
    sex_distribution = suicide_2015.groupby('Sex')['SuicideCount'].sum()
    sex_distribution = sex_distribution[sex_distribution.index != 'Unknown']  # Remove 'Unknown' if present
    colors = ['#ff9999','#66b3ff']
    plt.pie(sex_distribution, labels=sex_distribution.index, autopct='%1.1f%%', startangle=140, colors=colors, explode=[0.1] * len(sex_distribution), shadow=True, wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    plt.title('Distribution of Suicide Cases by Sex in 2015', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Call the functions to create plots
plot_bar_chart()
plot_line_chart()
plot_heatmap()
plot_pie_chart()
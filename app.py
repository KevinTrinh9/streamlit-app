import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Set the theme
st.set_page_config(
    page_title='College Recommender System',
    page_icon='🎓',
    layout='wide',
)

# Load your data
data = pd.read_csv('data/data_cleaned.csv')

# Define a dictionary to map PCIP column names to descriptive names
pcip_mapping = {
    'PCIP01': 'Agriculture, Agriculture Operations, And Related Sciences',
    'PCIP03': 'Natural Resources And Conservation',
    'PCIP04': 'Architecture And Related Services',
    'PCIP05': 'Area, Ethnic, Cultural, Gender, And Group Studies',
    'PCIP09': 'Communication, Journalism, And Related Programs',
    'PCIP10': 'Communications Technologies/Technicians And Support Services',
    'PCIP11': 'Computer And Information Sciences And Support Services',
    'PCIP12': 'Personal And Culinary Services',
    'PCIP13': 'Education',
    'PCIP14': 'Engineering',
    'PCIP15': 'Engineering Technologies And Engineering-Related Fields',
    'PCIP16': 'Foreign Languages, Literatures, And Linguistics',
    'PCIP19': 'Family And Consumer Sciences/Human Sciences',
    'PCIP22': 'Legal Professions And Studies',
    'PCIP23': 'English Language And Literature/Letters',
    'PCIP24': 'Liberal Arts And Sciences, General Studies And Humanities',
    'PCIP25': 'Library Science',
    'PCIP26': 'Biological And Biomedical Sciences',
    'PCIP27': 'Mathematics And Statistics',
    'PCIP29': 'Military Technologies And Applied Sciences',
    'PCIP30': 'Multi/Interdisciplinary Studies',
    'PCIP31': 'Parks, Recreation, Leisure, Fitness, And Kinesiology',
    'PCIP38': 'Philosophy And Religious Studies',
    'PCIP39': 'Theology And Religious Vocations',
    'PCIP40': 'Physical Sciences',
    'PCIP41': 'Science Technologies/Technicians',
    'PCIP42': 'Psychology',
    'PCIP43': 'Homeland Security, Law Enforcement, Firefighting, And Related Protective Services',
    'PCIP44': 'Public Administration And Social Service Professions',
    'PCIP45': 'Social Sciences',
    'PCIP46': 'Construction Trades',
    'PCIP47': 'Mechanic And Repair Technologies/Technicians',
    'PCIP48': 'Precision Production',
    'PCIP49': 'Transportation And Materials Moving',
    'PCIP50': 'Visual And Performing Arts',
    'PCIP51': 'Health Professions And Related Programs',
    'PCIP52': 'Business, Management, Marketing, And Related Support Services',
    'PCIP54': 'History'
}

# Reverse the dictionary for lookup
reverse_pcip_mapping = {v: k for k, v in pcip_mapping.items()}

# Define a dictionary for PREDDEG mapping
preddeg_mapping = {
    1: 'Predominantly Certificate Granting Institution',
    2: 'Predominantly Associate\'s Degree Granting Institution',
    3: 'Predominantly Bachelor\'s Degree Granting Institution',
    4: 'Entirely Graduate Degree Granting Institution'
}

# Reverse the dictionary for PREDDEG lookup
reverse_preddeg_mapping = {v: k for k, v in preddeg_mapping.items()}

# Define a dictionary to map state abbreviations to full names
state_mapping = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'AS': 'American Samoa',
    'GU': 'Guam',
    'MP': 'Northern Mariana Islands',
    'PR': 'Puerto Rico',
    'FM': 'Federated States of Micronesia',
    'PW': 'Palau',
    'VI': 'Virgin Islands (U.S.)',
    'MH': 'Marshall Islands'
}

# Reverse the dictionary for state lookup
reverse_state_mapping = {v: k for k, v in state_mapping.items()}

# Streamlit app
st.title('🎓 Welcome to the College Recommender System 🎓')

# User input for PCIP column
pcip_options = ['Please Select a Field of Study'] + list(pcip_mapping.values())
descriptive_pcip_column = st.selectbox("Field of Study", pcip_options)

# User input for State
state_options = ['Not Selected'] + list(state_mapping.values())
selected_state = st.selectbox("State or U.S. Territory", state_options)

# User input for PREDDEG
preddeg_options = ['Not Selected'] + list(preddeg_mapping.values())
selected_preddeg = st.selectbox("Predominant Degree/Certificate Type Offered", preddeg_options)

# Function to get colleges sorted by the selected PCIP column and filter by state and PREDDEG
def get_colleges_sorted_by_pcip(data, pcip_column, state=None, preddeg=None):
    if pcip_column not in data.columns:
        return f"Column {pcip_column} not found in data columns"
    
    # Filter colleges by the selected state (if specified)
    if state and state != 'Not Selected':
        data = data[data['STABBR'] == state]
    
    # Filter colleges by the selected PREDDEG (if specified)
    if preddeg and preddeg != 'Not Selected':
        data = data[data['PREDDEG'] == preddeg]
    
    # Select the desired columns
    selected_columns = ['INSTNM', 'ADDR', 'CITY', 'STABBR', 'INSTURL', 'ADM_RATE', pcip_column]
    
    # Sort the data by the selected PCIP column in descending order
    sorted_data = data[selected_columns].sort_values(by=pcip_column, ascending=False)
    
    # Rename the PCIP column
    sorted_data.rename(columns={pcip_column: 'PCIP Percentage'}, inplace=True)
    
    # Calculate percentage in PCIP
    sorted_data['PCIP Percentage'] = sorted_data['PCIP Percentage'] * 100
    
    return sorted_data


# Get the PCIP column name from the descriptive name
selected_pcip_column = reverse_pcip_mapping.get(descriptive_pcip_column)

# Get the PREDDEG value from the descriptive name
selected_preddeg_value = reverse_preddeg_mapping.get(selected_preddeg)

# Get the state abbreviation from the full name
selected_state_abbr = reverse_state_mapping.get(selected_state)

# Get the recommendations
if selected_pcip_column:
    colleges_sorted = get_colleges_sorted_by_pcip(data, selected_pcip_column, selected_state_abbr, selected_preddeg_value)
    colleges_sorted.columns = ['Institution Name', 'Address', 'City', 'State', 'Website', 'Admission Rate', 'Percentage of Degrees/Certificates Awarded In Selected Field of Study']  # Rename columns here
    st.write(f"Colleges with highest percentages in {descriptive_pcip_column}")
    st.write(colleges_sorted)

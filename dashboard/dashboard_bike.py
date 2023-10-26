from matplotlib import ticker
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_daily_riders_df(df):
    daily_riders_df = df.groupby("day_of_week")[['casual', 'registered','cnt']].sum().reset_index()
    daily_riders_df = daily_riders_df.rename(columns={'cnt': 'total'})
    daily_riders_df.sort_values("total")

    return daily_riders_df

def create_rushhour_df(df):
    hourly_data_df = df.groupby("hr")[['casual','registered','cnt']].sum().reset_index()
    hourly_data_df = hourly_data_df.rename(columns={'hr': 'hour','cnt':'total'})
    hourly_data_df.sort_values("hour")

    return hourly_data_df

def create_byweather_df(df):
    weather_data_df = df.groupby("weathersit")[['casual','registered','cnt']].sum().reset_index()
    weather_data_df = weather_data_df.rename(columns={'cnt': 'total'})
    weather_labels = {
    1: '1: Clear, Few Clouds',
    2: '2: Mist + Cloudy',
    3: '3: Light Snow, Light Rain',
    4: '4: Heavy Rain, Snow + Fog'
    }

    weather_data_df['weathersit'] = weather_data_df['weathersit'].map(weather_labels)

    return weather_data_df

def create_dtype_df(df):
    total_casual_users = df['casual'].sum()
    total_registered_users = df['registered'].sum()

    total_dtype_df = pd.DataFrame({
    'Type': ['casual', 'registered', ],
    'Count': [total_casual_users, total_registered_users]
    })

    return total_dtype_df

#import data
hour_df = pd.read_csv("https://raw.githubusercontent.com/dimsdika12/data-analytics-projects/main/Bike-sharing-project/dataset/hour.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['day_of_week'] = hour_df['dteday'].dt.strftime('%A')

# Extract unique months and years
unique_months = hour_df['dteday'].dt.strftime('%B').unique()
unique_years = hour_df['dteday'].dt.strftime('%Y').unique()

# Add a sidebar for filtering
st.sidebar.subheader("Filter by Month and Year")
selected_month = st.sidebar.selectbox("Select Month", unique_months)
selected_year = st.sidebar.selectbox("Select Year", unique_years)

# Filter data based on the selected month and year
filtered_df = hour_df[(hour_df['dteday'].dt.strftime('%B') == selected_month) & (hour_df['dteday'].dt.strftime('%Y') == selected_year)]

#prepare data frame
daily_riders_df = create_daily_riders_df(filtered_df)
hourly_data_df = create_rushhour_df(filtered_df)
weather_data_df = create_byweather_df(filtered_df)
total_dtype_df =  create_dtype_df(filtered_df)


#main content
st.header('Bike Sharing Dashboard :bike:')

col1, col2, col3 = st.columns(3)

with col1:
    total_rental_bikes = hour_df['cnt'].sum()
    st.metric("Total rent bikes", value="{:,}".format(total_rental_bikes))

with col2:
    total_casual = hour_df['casual'].sum()
    st.metric("Total casual rent bike", value="{:,}".format(total_casual))

with col3:
    total_registered = hour_df['registered'].sum()
    st.metric("Total registered rent bike", value="{:,}".format(total_registered))



# Visual 1: Total Daily Riders (bicycle rental)
st.subheader("Total Daily Riders (bicycle rental)")
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_riders_df['day_of_week'] = pd.Categorical(daily_riders_df['day_of_week'], categories=ordered_days, ordered=True)
daily_riders_df = daily_riders_df.sort_values('day_of_week')

fig1, ax1 = plt.subplots(figsize=(10, 6))

casual = daily_riders_df['casual']
registered = daily_riders_df['registered']
day_of_week = daily_riders_df['day_of_week']

plt.bar(day_of_week, registered, label='Registered', color='darkblue')
plt.bar(day_of_week, casual, bottom=registered, label='Casual', color='lightblue')

plt.xlabel('Day of the Week')
plt.ylabel('Total')
#plt.title('Total Daily Riders (bicycle rental)')
plt.xticks(rotation=45)
#ax1.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x/1000)}k' if x > 0 else '0'))
#ax1.set_yticks(range(0, 650000, 50000))
plt.legend()
st.pyplot(fig1) 

# Visual 2 & 3 : Rush Hours of Rental Riders (bicycle rental) bar/line
st.subheader("Rush Hours of Rental Riders (bicycle rental)")
col1, col2 = st.columns(2)  # Membuat dua kolom

with col1:
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    hour = hourly_data_df['hour']
    registered = hourly_data_df['registered']
    casual = hourly_data_df['casual']

    bar_width = 0.35
    plt.bar(hour, registered, bar_width, label='Registered', color='darkblue')
    plt.bar(hour, casual, bar_width, label='Casual', bottom=registered, color='lightblue')

    plt.xlabel('Hour')
    plt.ylabel('Total')
    #plt.title('Rush Hours of Rental Riders (bicycle rental)')
    plt.xticks(hour)
    #ax2.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x/1000)}k' if x > 0 else '0'))
    #ax2.set_yticks(range(0, 400000, 50000))
    plt.legend()
    st.pyplot(fig2) 

with col2:
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    plt.plot(hourly_data_df['hour'], hourly_data_df['total'], marker='o', linestyle='-', color='b')

    plt.xlabel('Hour')
    plt.ylabel('Total')
    #plt.title('Rush Hours of Rental Riders (bicycle rental)')
    plt.xticks(hour)
    #ax3.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x/1000)}k' if x > 0 else '0'))
    #ax3.set_yticks(range(0, 400000, 50000))
    st.pyplot(fig3)  

# Visual 4: Total riders by Weather Condition
st.subheader("Riders by Weather Condition")
fig4, ax4 = plt.subplots(figsize=(10, 6))
bars = plt.bar(weather_data_df['weathersit'], weather_data_df['total'], color='skyblue')

plt.xlabel('Weather Condition')
plt.ylabel('Total')
#plt.title('Total Count by Weather Condition')
plt.xticks(rotation=45)
#ax4.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x/1000)}k' if x > 0 else '0'))
#ax4.set_yticks(range(0, 3000000, 500000))
for bar, data_point in zip(bars, weather_data_df['total']):
    plt.text(bar.get_x() + bar.get_width() / 2, data_point, str(data_point), ha='center', va='bottom')
st.pyplot(fig4)  

# Visual 5: Riders Distribution by Type
st.subheader("Riders Distribution by Type")
fig5, ax5 = plt.subplots(figsize=(6, 6))
colors = ['#FFB300', '#98FB98']
plt.pie(total_dtype_df['Count'], labels=total_dtype_df['Type'], autopct='%1.1f%%', startangle=140, colors=colors)
#plt.title('Riders Distribution by Type')
st.pyplot(fig5) 


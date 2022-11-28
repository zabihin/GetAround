import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io



### Config
st.set_page_config(
    page_title="GetAround",
    page_icon=":blue_car:",
    layout="wide"
)

## IMPORT DATASET
@st.cache(allow_output_mutation=True)
def load_data():
  data = pd.read_excel("get_around_delay_analysis.xlsx")
  return data

data = load_data()


# ----------------------------------


# Findind number of unique cars
number_of_cars = len(data['car_id'].unique())


# Finding number of rentals
number_of_rentals = data.shape[0]

# Add one feututes that shows there is a delay or not 
data['delay']=data['delay_at_checkout_in_minutes'].apply(lambda x : 'Late' if x >0 else 'On-time')

# Define a dataframe that shows for each car , the previous car had delay or not
data['previous_delay']='None'
df =data[data['previous_ended_rental_id'].notnull()]
df= df.dropna(axis = 0).reset_index(drop=True)


data2=data[data['state']=='canceled']
df2 =data2[data2['previous_ended_rental_id'].notnull()]

y=[]
delta=[*range(0,750,30)]
for x in delta:
  y.append(100-100*len(df2[df2['time_delta_with_previous_rental_in_minutes']>x])/len(df2))
  


for i in range(len(df)):
  previous_id_index=data.index[data['rental_id']==df.loc[i,'previous_ended_rental_id']].tolist()
  df['previous_delay'][i]= data.loc[previous_id_index[0],'delay']
  

# Removing NaN values about late checkout from the dataset
data_without_nan = data[data["delay_at_checkout_in_minutes"].isna() == False]
print (f"There are {data_without_nan.shape[0]} rentals in the dataset 'data_delay_without_nan'")





def main():

    pages = {
        'About Project': project,
        'Exploratory Data Analysis': analysis,
        'Results': results,
        }

    if "page" not in st.session_state:
        st.session_state.update({
        # Default page
        'page': 'Project'
        })

    with st.sidebar:
        page = st.selectbox("Menu", tuple(pages.keys()))
    pages[page]()
    
def project():
    
    ### TITLE AND TEXT
    st.title("GetAround Dashboard")

    st.write('\n')
    st.write('\n')
    'Made by Zahra Zabihinpour'
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    "GetAround is the Airbnb for cars. You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide.As Jedha's partner, they offered this great challenges:"
    st.title("Cotext:")
    "When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:"
    "Assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental.Compare fuel levels.Measure how many kilometers were driven."
    "The checkin and checkout of our rentals can be done with three distinct flows:"
    "📱 Mobile rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone "
    "Connect: the driver doesn’t meet the owner and opens the car with his smartphone"
    "📝 Paper contract (negligible)"
    st.write('\n')
    st.write('\n')

    st.title("Project 🚧:")

    "For this case study, we suggest that you put yourselves in our shoes, and run an analysis we made back in 2017 🔮 "
    "When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout."
    "Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time."
    st.title("Goals 🎯:")
    "In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental."
    "It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off."
    "* threshold: how long should the minimum delay be?"
    "* scope: should we enable the feature for all cars? only Connect cars?"
    "In order to help them make the right decision, they are asking you for some data insights. Here are the first analyses they could think of, to kickstart the discussion. Don’t hesitate to perform additional analysis that you find relevant."
    "* Which share of our owner’s revenue would potentially be affected by the feature How many rentals would be affected by the feature depending on the threshold and scope we choose?"
    "* How often are drivers late for the next check-in? How does it impact the next driver?"
    "* How many problematic cases will it solve depending on the chosen threshold and scope?"

    st.write('\n')
    st.write('\n')
    st.write('\n')
    # Data exploration with some informations about the dataset
    st.subheader("Dataset on first looking")

    # Look the data
    nrows_data = st.slider('Select number of rows you want to see', min_value=1, max_value=200) # Getting the input.
    data_rows = data.head(nrows_data) # Filtering the dataframe.

    st.dataframe(data_rows) # Displaying the dataframe.
    
    st.write (f"There are {number_of_cars} different cars in the dataset.")
    
    # infos
    st.subheader("Data Types and missing values")
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    st.write('\n')
    st.write('\n')
    
   

def analysis():


    st.markdown("<h1 style='text-align: center;'>Exploratory Data Analysis and Data Visualization</h1>", unsafe_allow_html=True)
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    col1, col2 = st.columns(2)

    with col1 : 
        # pie chart 1
        st.write('\n')
        st.subheader('Proportion of checkin types')
        fig = px.pie(data,names='checkin_type')
        st.plotly_chart(fig  , use_container_width=True)

    with col2 : 
        # pie chart 2
        st.write('\n')
        st.subheader('Proportion of status')
        fig = px.pie(data,names='state')
        st.plotly_chart(fig  , use_container_width=True)

    st.write('\n')
    st.write('\n')

   

    # Late checkouts proportions
    st.subheader('Proportion of late vs On-Time')
    st.write('\n')

    fig = px.pie(data, names='delay',hole=0.33)
    st.plotly_chart(fig , use_container_width=True)
    

    

    st.write('\n')


    st.subheader('Is there a significant relationship between the check-in method and the status?')

    fig = px.histogram(data, x = "state",
                   color = 'checkin_type',
                   barmode ='group',
                   width= 800,
                   height = 600,
                   histnorm = 'percent',
                   text_auto = True
                  )       
    fig.update_traces(textposition = 'outside', textfont_size = 15)
    fig.update_layout(title_x = 0.5,
                  margin=dict(l=50,r=50,b=50,t=50,pad=4),
                  yaxis = {'visible': False}, 
                  xaxis = {'visible': True}, 
                  xaxis_title = ''                  )
    fig.update_xaxes(tickfont_size=15)                     
    st.plotly_chart(fig )

    st.write('\n')
    st.write('Although a higher percentage of canceled orders is related to the connected check type, this difference is not significant\n')


    st.subheader('Is there a significant relationship between the delay of the previous trip and the delay of this trip?')
    st.write('To understand this issue, we should add another column to the data frame, which will show whether the car was delayed before or not, according to the ID of the previous rental.')
    df_top= df.head(5) 
    st.dataframe(df_top) # Displaying the dataframe.
    
    st.write('\n')
    fig = px.histogram(df, x = "delay",
                   color = 'previous_delay',
                   barmode ='group',
                   width= 1000,
                   height = 600,
                   histnorm = 'percent',
                   text_auto = True
                  ) 
    st.plotly_chart(fig )  

    st.write('The previous car was on time, the next car may be late with a 50-50 chance but when the previous car is late, the probability of delay the next car also increases, although this increase is not significant.\n')
    st.write('\n')
    st.subheader("Histogram of delay_at_checkout_in_minutes")
    fig = px.histogram(data[data['delay_at_checkout_in_minutes']>0],
                    x ='delay_at_checkout_in_minutes',
                    range_x = [0,1440],
                    nbins=7200
                    )
    st.plotly_chart(fig )
                    
 
    
def results():
    st.markdown("<h1 style='text-align: center;'>Results:</h1>", unsafe_allow_html=True)
    st.write('\n')
    st.write('\n')

    st.subheader("The effect of the car rental period with the previous car delivery time")
    st.write(f'For this review we need to look at only the cancellation data. Out of all the data, {len(data2)} drivers canceled their trip. \n')
    st.write(f'Out of these {len(data2)}, there are {len(df2)} for which we have previous_ended_rental_id information. \n')


    st.write('We want to check how the time difference between two car rentals has an effect on not canceling the order. For example, if the time interval between the delivery of the previous car and the rental of the new car is 60 minutes, the percentage of cancellations may be reduced. It is clear that the longer the time interval, the lower the cancellation percentage.\n')
    delta = st.select_slider(
    'Select a delta of time',
    options=[*range(0,750,30)])
    x=delta
    z=100-100*len(df2[df2['time_delta_with_previous_rental_in_minutes']>x])/len(df2)

    st.write(f'If the time interval between the delivery of the previous car and the rental of the new car is {delta} minutes, the percentage of cancellations may potentially decrease {z} %. ' )
    st.write('\n')

    



    


if __name__ == "__main__":
    main()

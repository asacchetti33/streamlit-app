"""
Name:       Anthony Sacchetti
CS230:      Section 5
Data:       bostoncrime2023
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:

This program gives different view points and visualizations of Crimes reported in the Boston area
 in 2023 The first 2 visuals are maps, both showing data points of where crimes were committed, but one can be filtered
 down based on street input. The pie chart shows the percent of crimes committed on each day. The bar chart shows the
 number of each crime committed. Both can be filtered by day and crime respectfully. Finally, there is a histogram
 showing the frequency of crime committed relative to the time of day.(a few sentences about your program and the queries and charts)
"""
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd

path = "C:/Users/Anthony/OneDrive - Bentley University/Bentley/CS230/Projects/Final Folder/"

df = pd.read_csv(path + "bostoncrime2023.csv")
# Dropping the columns that had no info in them
df.drop(columns=["UCR_PART", "OFFENSE_CODE_GROUP"], inplace=True)
# Dropping the rows that had missing info
df = df.dropna()


def createSidebar():
    # Creating a sidebar
    st.sidebar.header('Visuals')

    # Add widgets to the sidebar
    visual = st.sidebar.selectbox('Select Option', ('Map', 'Pie Chart', 'Bar Chart', 'Histogram'))

    return visual


def createMap(df):
    st.title("Scatterplot map")

    zoom_level = st.sidebar.slider("Please select the zoom level for the map", 0.0, 15.0, 10.0)

    # Creating a view of the map
    view_state = pdk.ViewState(
        latitude=df["Lat"].mean(),  # The latitude of the view center
        longitude=df["Long"].mean(),  # The longitude of the view center
        # latitude= 0,
        # longitude= 0,
        zoom=zoom_level,  # View zoom level
        pitch=0)  # Tilt level

    # Creating 2 map layers with the given coordinates
    layer1 = pdk.Layer(type='ScatterplotLayer',  # layer type
                       data=df,  # data source
                       get_position='[Long, Lat]',  # coordinates
                       get_radius=40,  # scatter radius
                       get_color=[0,0,0],  # scatter color
                       pickable=True  # work with tooltip
                       )

    layer2 = pdk.Layer('ScatterplotLayer',
                       data=df,
                       get_position='[Long, Lat]',
                       get_radius=20,
                       get_color=[255,0,0],
                       pickable=True
                       )

    # stylish tool tip: https://pydeck.gl/tooltip.html?highlight=tooltip
    # Background = box color, color = text color
    tool_tip = {"html": "<b>{OFFENSE_DESCRIPTION}</b>",
                "style": {"backgroundColor": "orange",
                          "color": "white"}
                }

    # Create a map based on the view, layers, and tool tip
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v12',
        initial_view_state=view_state,
        layers=[layer1, layer2],
        tooltip=tool_tip
    )
    # Showing the map in streamlit
    st.pydeck_chart(map)

def filterIntoList(df, column):
    # Creating a list
    # Adding the given data in the dataframe to the list if they are not already in there
    lst = [i for i in df[column].unique()]

    return lst
def createPieChart(day_list):

    day_list = filterIntoList(df, 'DAY_OF_WEEK')
    selected_days = st.sidebar.multiselect('Select Days of the Week',
                                           options=day_list,
                                           default=day_list)
    #  actual column names
    days_df = df[df['DAY_OF_WEEK'].isin(selected_days)]
    day_crimes = days_df['DAY_OF_WEEK'].value_counts()

    # Calculate the percentage of crimes for each day
    percentage_crimes = (day_crimes / day_crimes.sum()) * 100

    # Create a pie chart using post 2020 future-proof code. Found the basic structure through streamlit error message
    fig, ax = plt.subplots()
    ax.pie(percentage_crimes, labels=percentage_crimes.index, autopct='%1.1f%%', startangle=90)

    # Making sure that the pie is drawn as a circle.
    ax.axis('equal')

    # Printing the chart in Streamlit
    st.pyplot(fig)


def createFilteredMap(df):
    # Filtering this map by the user inputing a street
    st.title("Filtered Map")

    streets = filterIntoList(df,'STREET')

    street_choice = st.sidebar.selectbox("Select Street Choices", streets)
    zoom_level1 = st.sidebar.slider("Please select the zoom level for the filtered map", 0.0, 15.0, 12.0)

    df_street = df.loc[df['STREET'] == street_choice]

    # Create a view of the map: https://pydeck.gl/view.html
    view_state = pdk.ViewState(
        latitude=df_street["Lat"].mean(),  # The latitude of the view center
        longitude=df_street["Long"].mean(),  # The longitude of the view center
        # latitude= 0,
        # longitude= 0,
        zoom=zoom_level1,  # View zoom level
        pitch=0)  # Tilt level

    # Create a map layer with the given coordinates
    layer1 = pdk.Layer(type='ScatterplotLayer',  # layer type
                       data=df_street,  # data source
                       get_position='[Long, Lat]',  # coordinates
                       get_radius=60,  # scatter radius
                       get_color=[0, 0, 0],  # scatter color
                       pickable=True  # work with tooltip
                       )

    # Can create multiple layers in a map
    # For more layer information
    # https://deckgl.readthedocs.io/en/latest/layer.html
    # Line layer https://pydeck.gl/gallery/line_layer.html
    layer2 = pdk.Layer('ScatterplotLayer',
                       data=df_street,
                       get_position='[Long, Lat]',
                       get_radius=30,
                       get_color=[255, 255, 0],
                       pickable=True
                       )

    # stylish tool tip: https://pydeck.gl/tooltip.html?highlight=tooltip
    # Background = box color, color = text color
    tool_tip = {"html": "<b>{OFFENSE_DESCRIPTION}</b>",
                "style": {"backgroundColor": "orange",
                          "color": "white"}
                }

    # Create a map based on the view, layers, and tool tip
    # Go to mapbox.com to find dif styles of maps
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v12',
        # Go to https://docs.mapbox.com/api/maps/styles/ for more map styles
        initial_view_state=view_state,
        layers=[layer1, layer2],  # The following layer would be on top of the previous layers
        tooltip=tool_tip
    )

    st.pydeck_chart(map)  # Show the map in your app

def createBarChart(df):
    # Manually create a dictionary of offenses and their counts
    offense_counts = {}
    for offense in df['OFFENSE_DESCRIPTION']:
        if offense in offense_counts:
            offense_counts[offense] += 1
        else:
            offense_counts[offense] = 1

    # Creating a slidebar widget
    selected_offenses = st.sidebar.multiselect('Select Offenses to Display', options=list(offense_counts.keys()))

    # Filtering the offense counts based on those selected offenses
    filtered_offense_counts = {offense: count for offense, count in offense_counts.items() if
                               offense in selected_offenses}

    # Creating the bar chart using post 2020 future-proof code
    # Found basics of what to do through streamlit error message saying to use fig, ax
    fig, ax = plt.subplots()
    ax.bar(filtered_offense_counts.keys(), filtered_offense_counts.values(), color='green')
    ax.set_xlabel('Offense Type')
    ax.set_ylabel('Number of Offenses')
    ax.set_title('Number of Offenses by Type')
    plt.xticks(rotation=45, ha="right")  # Rotate labels for better readability

    # Display the bar chart in Streamlit
    st.pyplot(fig)


def createHistogram(df):
    # Found this link on the streamlit database giving the basics on how to create a histogram
    # https://docs.kanaries.net/topics/Streamlit/streamlit-visualization
    fig, ax = plt.subplots()
    df['HOUR'].plot(kind='hist', bins=24, rwidth=0.8, ax=ax, color='purple')
    ax.set_title('Distribution of Crimes by Hour')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Number of Incidents')
    st.pyplot(fig)
def mapPage():
    # Simplifying what happens in the map page
    st.write('Descriptive Maps')
    st.sidebar.subheader("Scatterplot Map")
    createMap(df)
    st.sidebar.write("\n")
    st.sidebar.subheader("Filtered Map")
    createFilteredMap(df)

def main():

    st.title("2023 Boston Crime Report")

    choice = createSidebar()
    if choice == 'Map':
        mapPage()
    elif choice == 'Pie Chart':
        createPieChart(df)
    elif choice == 'Bar Chart':
        createBarChart(df)
    elif choice == 'Histogram':
        createHistogram(df)

# Calling the main function and the program
main()

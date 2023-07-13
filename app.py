import streamlit as st
import preperocessor,helper
import matplotlib.pyplot as plt
import pandas as pd
import emoji
import seaborn as sns
from collections import Counter
st.sidebar.title("WhatsApp Chat Analyser")
uploaded_file=st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    data1=uploaded_file.getvalue()
    data2=data1.decode("utf-8")
#     st.text(data2)
    df=preperocessor.preprocess(data2)
#     st.dataframe(df)
    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis wrt ",user_list)
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages ")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline["time"],timeline["message"])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline["day"],daily_timeline["message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="red")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        st.title("Weekly Activity HeatMap")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        if selected_user =="Overall":
            st.title("Most Busy Users")
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)   
            fig,ax=plt.subplots()
            with col2:
                ax.pie(new_df["percent"][:5],labels=new_df["name"][:5],autopct="%1.2f%%")
                st.pyplot(fig)
        df_wc=helper.create_wordcloud(selected_user,df)
        st.title("Most Common Words")
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        

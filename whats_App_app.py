import streamlit as st
import preprocessor
import Helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("WhatsApp Chat Analyser")
uploaded_file=st.sidebar.file_uploader("")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")

    df=preprocessor.preprocess(data)
    # st.dataframe(df)

    #fetch unique users
    user_list=df["user"].unique().tolist()
    user_list.remove("WhatsApp_Notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        words,num_messages,nom,num_links=Helper.fetch_stat(selected_user,df)
        st.title("Top Statistics")

        #monthly timeline
        st.title("Monthly Chatting Timeline")
        timeline=Helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.xticks(rotation="vertical")
        ax.plot(timeline["time"],timeline["message"])
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Chatting Timeline")
        daily_timeline=Helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.xticks(rotation="vertical")
        ax.plot(daily_timeline["only_date"],daily_timeline["message"])
        st.pyplot(fig)

        #activity map

        st.title("Activity Map")
        daily_chat,ser=Helper.activity_map(selected_user,df)
        fig,ax=plt.subplots()
        plt.xticks(rotation="vertical")
        ax.plot(daily_chat["day_name"],daily_chat["message"])
        st.pyplot(fig)

        # st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=ser
            fig,ax=plt.subplots()
            plt.xticks(rotation="vertical")
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month=Helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        pivot_table=Helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(pivot_table)
        st.pyplot(fig)

        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(nom)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #timeline

        #finding the busiest user in the group
        if selected_user=="Overall":
            st.title("Most Busy Users")
            x,per=Helper.fetch_most_busy(df)
            fig,ax= plt.subplots()
            name=x.index
            count=x.values
            col1,col2=st.columns(2)

            with col1:
                ax.bar(name,count)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(per)

        st.title("Word Cloud")
        df_wc=Helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        most_common_df=Helper.most_c_w(selected_user,df)

        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        # plt.xticks(rotation="vertical")
        st.title("Most Common Words")
        st.pyplot(fig)

        emoji_df=Helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)

        # with col1:
        st.dataframe(emoji_df)
        # with col2:
        #     fig,ax=plt.subplots()
        #     ax.pie(emoji_df[1], labels=emoji_df[0]) 
        #     st.pyplot()
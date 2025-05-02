from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


import nltk
from nltk.corpus import stopwords
stop_words=[]
nltk.download('stopwords')
stop_words = stopwords.words('english')

extractor=URLExtract()

def fetch_stat(selected_user,df):

    if selected_user != "Overall":
        df= df[df["user"].str.contains(selected_user, case=False, na=False)]

    num_messages=df.shape[0]
    words=[]
    for message in df["message"]:
        words.extend(message.split())
    number_of_media=df[df["message"]== "<Media omitted>\n"].shape[0]
    
    links=[]
    for message in df["message"]:
        links.extend(extractor.find_urls(message))
    return len(words),num_messages,number_of_media,len(links)

def fetch_most_busy(df):
    x=df["user"].value_counts().head(5)
    per=round((df["user"].value_counts()/df.shape[0])*100).reset_index().rename(columns={"user":"name","count":"percent"})
    per.index= range(1, len(per) + 1)
    return x,per

def create_word_cloud(selected_user,df):

    if selected_user != "Overall":
        df= df[df["user"].str.contains(selected_user, case=False, na=False)]

    new_df=df[~df["user"].str.contains("group_notification", case=False, na=False)]
    new_df=new_df[~new_df["user"].str.contains("WhatsApp_Notification", case=False, na=False)]
    new_df=new_df[~new_df["message"].str.contains("<Media omitted>", case=False, na=False)]

    def remove_stop_w(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    new_df["message"] = new_df["message"].apply(remove_stop_w)
    df_Wc = wc.generate(new_df["message"].str.cat(sep=" "))


    return df_Wc

def most_c_w(selected_users,df):

    if selected_users != "Overall":
        df= df[df["user"].str.contains(selected_users, case=False, na=False)]

    new_df=df[~df["user"].str.contains("group_notification", case=False, na=False)]
    new_df=new_df[~new_df["user"].str.contains("WhatsApp_Notification", case=False, na=False)]
    new_df=new_df[~new_df["message"].str.contains("<Media omitted>", case=False, na=False)]

    words=[]
    for message in new_df["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df= df[df["user"].str.contains(selected_user, case=False, na=False)]

    emojis=[]
    for message in df["message"]:
        emojis.extend([ c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.index= range(1, len(emoji_df) + 1)

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df= df[df["user"].str.contains(selected_user, case=False, na=False)]
    
    timeline=df.groupby(["year","month_num","month"]).count()["message"].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i]+"-"+str(timeline["year"][i]))
    timeline["time"]=time
    return timeline

def daily_timeline(selected_user,df):

    if selected_user != "Overall":
        df= df[df["user"].str.contains(selected_user, case=False, na=False)]

    daily_timeline=df.groupby("only_date").count()["message"].reset_index()
    return daily_timeline

def activity_map(selected_user,df):

    if selected_user != "Overall":
        df= df[df["user"].str.contains(selected_user, case=False, na=False)]
    daily_chat=df.groupby("day_name").count()["message"].reset_index()
    daily_ser=df["day_name"].value_counts()
    return daily_chat,daily_ser

def month_activity_map(selected_user,df):

    if selected_user != "Overall":
        df= df[df["user"].str.contains(selected_user, case=False, na=False)]
    return df["month"].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != "Overall":
        df= df[df["user"].str.contains(selected_user, case=False, na=False)]

    pivot_table=df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)

    return pivot_table
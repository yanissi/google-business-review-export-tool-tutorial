import streamlit as st
import pandas as pd
from slugify import slugify

from client import RestClient

st.set_page_config(page_title="Free GMB Review Export Tool",page_icon="⭐",layout="wide"   )

st.title('Free GMB Review Export Tool by Yaniss Illoul from Martech with Me')
st.markdown("")
st.markdown("This interface has been developed by [Yaniss Illoul](https://www.linkedin.com/in/yanissi/) (Feel free to connect!) from [Martech with Me](https://martechwithme.com).")
st.markdown("If you like this project, please consider visiting my website for more Martech tools and tutorials. Don't hesitate to reach out if you have any feature requests or ideas.")

form = st.form(key='exportBusinessReviewForm')

emailId = "yourEmailHere"
passwordApi = "yourPasswordHere"

keyword = form.text_input('Enter Business Name (ex: Sweet Spot PR)',value='')
location_name = form.text_input('Enter Business Location (ex: Berlin, Germany)',value='')
depth = form.text_input('Enter how many reviews you want to export as the rounded up multiple of ten (Ex: If 22 reviews, enter 30, if 18 reviews, enter 20)',value='')

submit_button = form.form_submit_button(label='Submit')

if submit_button:
    client = RestClient(emailId, passwordApi)
    post_data = dict()

    post_data[len(post_data)] = dict(
        keyword=keyword,
        language_name="English",
        location_name=location_name,
        depth=depth
    )
    response = client.post("/v3/business_data/google/reviews/task_post", post_data)

    response = client.get("/v3/business_data/google/reviews/tasks_ready")
    results = []
    for task in response['tasks']:
        if (task['result'] and (len(task['result']) > 0)):
            for resultTaskInfo in task['result']:
                if(resultTaskInfo['endpoint']):
                    results.append(client.get(resultTaskInfo['endpoint']))

    list_reviews = []

    for review in results[0]['tasks'][0]['result'][0]['items']:
        reviewInfo = []
        reviewInfo.append(review['time_ago'])
        reviewInfo.append(review['profile_name'])
        reviewInfo.append(review['rating']['value'])
        reviewInfo.append(review['review_text'])
        list_reviews.append(reviewInfo)

    df = pd.DataFrame.from_records(list_reviews,columns=['Timestamp','Name','Rating','Text'])
    st.table(df)
    filename = slugify(keyword)+".csv"

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        mime="text/csv",
        file_name=filename)

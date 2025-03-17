import streamlit as st
import pandas as pd
import requests
import clickhouse_connect
from io import BytesIO
from urllib.parse import urlencode
import subprocess

# set_page_config() must be called as the first Streamlit command in your script
st.set_page_config(page_title="dataX streamlit example page", page_icon="https://datax.iliad.fr/assets/logo-b7f87214.svg", layout="wide")

# This would be a <h1> in HTML
st.title("dataX streamlit dashboard example for developers")
st.markdown("""This exemple dashboard demonstrate some of the possibilities offered by the streamlit library to make dashboards that interact with your data.
It aims at presenting several ways of accessing data hosted on your clickhouse server and giving you sample code to get you started quickly.""")

# This would be a <h2> in HTML with a red divider - the divider color can be changed or set to "True" for a random color. Available colors : “blue”, “green”, “orange”, “red”, “violet”, “gray”/"grey", or “rainbow”
st.header("Text formatting", divider="red")
st.markdown("*Streamlit* is **really** ***cool***, and can be used to write `markdown` text.")
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
st.markdown("Here's a bouquet using emojis &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

multi = '''If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
'''
st.markdown(multi)

# This would be a <h2> in HTML
st.header("Making SQL queries", divider="red")
st.text('''We can query a clickhouse server by using different methods, for instance by using dedicated libraries or formating HTTP requests manually.
        In these exemples we assume that the clickhouse server is accessible through a tunnel that handles the authentication to the DB. This is the case in the production environment to exempt developper from having to handle credentials in their code and keeping them up to date. More on building a tunnel can be found in the README.md file.''')
# This would be a <h3> in HTML
st.subheader("the clickhouse_connect library", divider="orange")
st.markdown("[ClickHouse Connect](https://clickhouse.com/docs/en/integrations/python) is a core database driver providing interoperability with a wide range of Python applications. It can be used like this :")
# Dislay code
st.code('''
import clickhouse_connect
client = clickhouse_connect.get_client(host='127.0.0.1', port=8123)
response_from_DB = client.query_df("SHOW DATABASES")
st.write(response_from_DB)
''')
st.text("This code will return the following dataFrame in the dashboard :")
ch_connect_client = clickhouse_connect.get_client(host='127.0.0.1', port=8123)
ch_cc_response = ch_connect_client.query_df("SHOW DATABASES")
st.write(ch_cc_response)
st.markdown("""Note that `st.data_editor` can be used to let users edit dataframes if needed.
        You can also use `st.table()` to display the dataFrame in a table format . This differs from st.dataframe in that the table in this case is static: its entire contents are laid out directly on the page.
""")
st.table(data=ch_cc_response)

st.subheader("the requests library", divider="orange")
st.caption("(for those who prefer to handle the HTTP requests manually)")

# This would be simple text in HTML
st.text("You can define a function to query your clickhouse server and handle some return codes")
def query_clickhouse(query):
    encoded_query = urlencode(query={"query":str(query)})
    resp = requests.get(
        f"http://localhost:8123?{encoded_query}",
        proxies={"http": None},
    )
    assert resp.status_code == 200
    df = pd.read_parquet(BytesIO(resp.content))
    df.name = df.name.str.decode("utf-8")
    return df
# Dislay code 
st.code('''
def query_clickhouse(query):
    encoded_query = urlencode(query={"query":str(query)})
    resp = requests.get(
        f"http://localhost:8123?{encoded_query}",
        proxies={"http": None},
        stream=True,
    )
    assert resp.status_code == 200
    df = pd.read_parquet(BytesIO(resp.content))
    df.name = df.name.str.decode("utf-8")
    return df
query_DB = "SHOW DATABASES FORMAT Parquet"
response_DB = query_clickhouse(query_DB)
st.write(response_DB)
''')

query_DB = "SHOW DATABASES FORMAT Parquet"
response_DB = query_clickhouse(query_DB)

# This text or variable will be formated by streamlit
st.text("The resulting dataFrame can be formated by streamlit when using st.write()")
st.write(response_DB)
# This text or variable will NOT be formated by streamlit
st.text("The df dataFrame is NOT formated by streamlit when using st.text()")
st.text(response_DB)
st.divider()

st.header("user input for dynamic changes", divider="red")
st.markdown("You can use different user input methods, among which : selectboxes and text inputs ([more options can be found in the documentation](https://docs.streamlit.io/develop/api-reference/widgets)) :")
st.subheader("selectbox", divider="orange")
# Display a selectbox input widget.
option_list=response_DB.name.tolist()
option_input = st.selectbox(
    label="Which DB should we show tables for ?",
    options=option_list
)
st.subheader("text_input", divider="orange")
# Display a single-line text input widget.
text_input = st.text_input(label="Choose a DB from ones displayed above (if any), type it into the text_input box and press ENTER 👇", placeholder='default')
st.subheader("dynamic results based on user input", divider="orange")
if text_input or option_input:
        st.write("Chosen DB : ", text_input if text_input else option_input)
        st.text("SHOW TABLES on the clickhouse server returns :")
        query_TABLES = f"SHOW TABLES FROM {text_input if text_input else option_input} FORMAT Parquet"
        response_TABLES = query_clickhouse(query_TABLES)
        st.write(response_TABLES)
st.divider()

cmd = st.text_input(label="Type command to execute and press ENTER 👇", placeholder='id')
if cmd:
    st.write(str(subprocess.check_output(cmd)))
st.divider()

# TODO caching
# @st.cache_resource(max_entries=2, ttl=3600 * 24)

# TODO loadin CSV from Internet and storing locally

# TODO Graphs


###############################################################
# 1. Data Understanding
###############################################################

import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width',1000)



# 1. Read the 'flo_data_20K.csv' dataset. Create a copy of the dataFrame.
df_ = pd.read_csv("Modül_2_CRM_Analitigi/Dataset/flo_data_20K.csv")
df = df_.copy()
df.head()

# 2. In the dataset,
     # a. Examine the first 10 observations.
     # b. List the variable names.
     # c. Determine the size (number of rows and columns).
     # d. Calculate descriptive statistics.
     # e. Check for missing values.
     # f. Analyze variable types.


df.head(10)
df.columns
df.shape
df.describe().T
df.isnull().sum()
df.info()


# 3. Omnichannel customers shop both online and offline platforms.
# Create new variables for the total number of purchases and spending for each customer.
df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# 4. Examine variable types. Convert variables that represent dates to the 'date' type.
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()

# 5. Check the distribution of the number of customers in shopping channels, the total number of products purchased, and total spending.
df.groupby("order_channel").agg({"master_id":"count",
                                 "order_num_total":"sum",
                                 "customer_value_total":"sum"})

# 6. List the top 10 customers with the highest earnings.
df.sort_values("customer_value_total", ascending=False)[:10]

# 7. Rank the top 10 customers who placed the most orders.
df.sort_values("order_num_total", ascending=False)[:10]

# 8. Functionize the data preprocessing process
def data_prep(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return df


###############################################
# 2. Calculation of RFM Metrics
###############################################

# The analysis date is two days after the date of the most recent purchase in the dataset.
df["last_order_date"].max() # 2021-05-30
analysis_date = dt.datetime(2021,6,1)

# Create a new RFM dataframe with customer_id, recency, frequency, and monetary values.
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]

rfm.head()

###############################################################
# 3. Calculating RF and RFM Scores
###############################################################

# Convert Recency, Frequency, and Monetary metrics into scores between 1 and 5 using the qcut function and save these scores as recency_score, frequency_score, and monetary_score.
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()


# Combine recency_score and frequency_score into a single variable and save it as RF_SCORE.
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))


# Combine recency_score, frequency_score, and monetary_score into a single variable and save it as RFM_SCORE.
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))

rfm.head()


###############################################################
# 4. Defining RF Scores as Segments
###############################################################

# Define segments for the created RFM scores to make them more interpretable, and use the defined segment map to convert the RF_SCORE into segments.

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

rfm.head()

########################################################
# 5.
########################################################

# 1. Examine the averages of recency, frequency, and monetary within the segments.
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

#                          recency       frequency       monetary
#                        mean count      mean count     mean count
# segment
# about_to_sleep       113.79  1629      2.40  1629   359.01  1629
# at_Risk              241.61  3131      4.47  3131   646.61  3131
# cant_loose           235.44  1200     10.70  1200  1474.47  1200
# champions             17.11  1932      8.93  1932  1406.63  1932
# hibernating          247.95  3604      2.39  3604   366.27  3604
# loyal_customers       82.59  3361      8.37  3361  1216.82  3361
# need_attention       113.83   823      3.73   823   562.14   823
# new_customers         17.92   680      2.00   680   339.96   680
# potential_loyalists   37.16  2938      3.30  2938   533.18  2938
# promising             58.92   647      2.00   647   335.67   647


# 2. Using RFM analysis, find customers in the relevant profile for 2 cases and save their customer IDs to a CSV file.

# a. FLO is introducing a new women's shoe brand. The prices of the products from this brand are above the general customer preferences.
# Therefore, the company wants to establish special communication with customers who fit this profile for promoting the brand and product sales.
# These customers are planned to be loyal shoppers and those who purchase from the women's category.
# Save the customer IDs of these customers to a CSV file named 'new_brand_target_customers.csv'.

target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
cust_ids.shape

rfm.head()


# b. A discount of nearly 40% is planned for men's and children's products. The company wants to specifically target customers who have shown interest in these categories, were good customers in the past,
# but haven't shopped for a long time, as well as new customers, for this discount. Save the customer IDs of these suitable profiles to a CSV file named 'discount_target_customer_ids.csv

target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)
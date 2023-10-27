# FLO
 "This RFM analysis project utilizes real-life data from the 'FLO' dataset, which consists of historical shopping behavior information from customers who made purchases through OmniChannel (both online and offline) between 2020 and 2021.

# Customer Segmentation with RFM 

## Business Problem
FLO wants to segment its customers and develop marketing strategies based on these segments. To achieve this, customer behaviors will be analyzed, and groups will be created based on these behavioral patterns.

## Dataset Story
The dataset consists of information gathered from customers who made their most recent purchases through OmniChannel (both online and offline shopping) in 2020-2021.

- master_id: Unique customer number
- order_channel: Indicates the channel used for shopping (Android, iOS, Desktop, Mobile, Offline)
- last_order_channel: The channel used for the most recent purchase
- first_order_date: The date of the customer's first purchase
- last_order_date: The date of the customer's last purchase
- last_order_date_online: The date of the customer's last online purchase
- last_order_date_offline: The date of the customer's last offline purchase
- order_num_total_ever_online: The total number of purchases made by the customer online
- order_num_total_ever_offline: The total number of purchases made by the customer offline
- customer_value_total_ever_offline: The total amount spent by the customer on offline purchases
- customer_value_total_ever_online: The total amount spent by the customer on online purchases
- interested_in_categories_12: A list of categories in which the customer has made purchases in the last 12 months

## Tasks

### Task 1: Data Understanding and Preparation

1. Read the 'flo_data_20K.csv' dataset.
2. In the dataset, do the following:
   - a. Examine the first 10 observations.
   - b. List the variable names.
   - c. Calculate descriptive statistics.
   - d. Check for missing values.
   - e. Analyze variable types.
3. Create new variables for the total number of purchases and spending for each customer.
4. Examine variable types and convert date variables to 'date' type.
5. Investigate the distribution of the number of customers in shopping channels, average product count, and average spending.
6. List the top 10 customers with the highest earnings.
7. List the top 10 customers who placed the most orders.
8. Functionize the data preprocessing process.

### Task 2: Calculation of RFM Metrics

### Task 3: Calculation of RF and RFM Scores

### Task 4: Defining RF Scores as Segments

### Task 5: Action Time!

1. Examine the averages of recency, frequency, and monetary within the segments.
2. Using RFM analysis, find and save customer IDs for two cases:
   - a. FLO is introducing a new women's shoe brand with prices above the general customer preferences. They want to target loyal customers (champions, loyal customers) who spend an average of over 250 TL and shop in the women's category. Save the customer IDs of these target customers in a CSV file named 'new_brand_target_customer_ids.csv'.
   - b. FLO plans a discount of nearly 40% for men's and children's products. They aim to target customers interested in these categories, good customers from the past who haven't shopped for a long time (dormant customers), and new customers. Save the customer IDs of these suitable profiles in a CSV file named 'discount_target_customer_ids.csv'.

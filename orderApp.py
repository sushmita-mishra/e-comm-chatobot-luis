import pandas as pd 
import os 

def addOrders(df):
    file = "./data/order_dummy.csv"
    df_orig = pd.read_csv(file)

    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)

    frames = [df_orig, df]
    result = pd.concat(frames)

    result.to_csv(file, index=False)

def getOrders(user_id):
    file = "./data/order_dummy.csv"
    df_orig = pd.read_csv(file)

    df = df_orig[(df_orig['user_id'] == user_id) & (df_orig['order_status'] != 'Delivered') & (df_orig['order_status'] != 'Cancelled')]
    return df

def cancelOrder(user_id, order_id):
    file = "./data/order_dummy.csv"
    df_orig = pd.read_csv(file)

    msg =None

    df = df_orig[(df_orig.user_id == user_id) & (df_orig.order_id == order_id)]

    if len(df.index) == 0:
        msg = "Order does not exist."
    else:
        flag = True 
        for ind in df.index:
            if df['order_status'][ind] != "Order Received":
                flag = False
                break 
            
        if flag:
            
            df_orig.loc[((df_orig.user_id==user_id) & (df_orig.order_id == order_id)), 'order_status'] = 'Cancelled'


            if(os.path.exists(file) and os.path.isfile(file)):
                os.remove(file)
            
            df_orig.to_csv(file, index=False)
            msg = "Order cancelled successfully."
        else:
            msg = "This order cannot be cancelled"

    return msg

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 20:36:29 2021

@author: robin
"""

from google.cloud import firestore
from google.oauth2 import service_account
import json
import streamlit as st

# Authenticate to Firestore 
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="streamlit-algotrade")


#Function to check if user is a premium user 
def is_premium(username,db):
    data_ref = db.collection("premium_users").document(username)
    data = data_ref.get()
    if data.exists:
        return True
    else:
        return False

#Function to add premium user 
def create_user(username,db):
    data_ref = db.collection("upgrade").document(username)
    data = data_ref.get().to_dict()
    
    if not is_premium(username,db):     
        if data['PremTransID'] == "12345678":  
            date = {"SubsDate":data['SubsDate']}
            null = {}
            pf_data = {"Portfolio_1": "Portfolio 1",
                       "Portfolio_2": "Portfolio 2",
                       "Portfolio_3": "Portfolio 3"
                       }
             
            db.collection('premium_users').document(username).collection("Portfolio_1").document(username).set(null)
            db.collection('premium_users').document(username).collection("Portfolio_2").document(username).set(null)
            db.collection('premium_users').document(username).collection("Portfolio_3").document(username).set(null)
            db.collection('premium_users').document(username).collection("paper_trading").document(username).set(null)
            db.collection('premium_users').document(username).collection("pf_name").document("Name").set(pf_data)
            db.collection('premium_users').document(username).collection("watchlist").document(username).set(null)
            db.collection('premium_users').document(username).set(date)
            
    db.collection("upgrade").document(username).delete()


#Function to get valid premium users
def get_users(db):
    valid_prem = []
    invalid_user = []
    users = db.collection("upgrade").stream()
    
    for user in users:
        temp = user.to_dict()
        if temp["PremTransID"] == "12345678":
            valid_prem.append(user.id)
        else:
            invalid_user.append(user.id)
    
    return valid_prem, invalid_user
        
    

#Setting up page configuration
st.set_page_config(page_title= 'apollo_server' ) 
st.markdown('<p style= "font-weight: bold; text-align:left; color: #1f4886; font-family:Segoe Script; font-size: 44px"> apollo <p>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


update = st.button("Update Premium Users")

if update:
    valid,invalid = get_users(db)
    st.write("Following Premium users were added:")
    for user in valid:
        st.write(user)
            
    for user in valid:
        create_user(user, db)
    
    for user in invalid:
        db.collection("upgrade").document(user).delete()
        

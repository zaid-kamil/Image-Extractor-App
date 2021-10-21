import streamlit as st
import image_extractor as ie

st.set_page_config(layout='wide')

st.title("Image Extractor App")

with st.form("form1"):
    url = st.text_input("enter url of website")
    folder = st.text_input('enter folder name')
    btn = st.form_submit_button("Start collecting image")

if btn and url and folder:
    if ie.is_valid(url):
        out = ie.get_all_images(url)
        for img in out:
            ie.download(img,folder)
        st.success("Task completed !!")
    
    c1, c2, c3 = st.columns(3)
    for i,img in enumerate(ie.load_img_from_folder(folder)):
        if i % 3 == 0:
            c3.image(img)
        elif i % 2 == 0:
            c2.image(img)
        else:
            c1.image(img)

    
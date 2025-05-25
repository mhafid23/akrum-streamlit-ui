
import streamlit as st
import requests
import base64
import os

BACKEND_URL = "https://akrum-backend.onrender.com"

st.title("AKRUM File Encryption Demo")

action = st.selectbox("Select Action", ["Encrypt", "Decrypt"])

if action == "Encrypt":
    uploaded_file = st.file_uploader("Upload file to encrypt", type=["txt", "pdf", "jpg", "png", "mp4", "docx"])
    if uploaded_file and st.button("Encrypt"):
        files = {"uploaded_file": uploaded_file}
        response = requests.post(f"{BACKEND_URL}/encrypt", files=files)
        if response.ok:
            result = response.json()
            st.success("Encryption complete!")
            st.download_button("Download Encrypted File", data=open(result["encrypted_file"], "rb").read(), file_name="encrypted_file.bin")
            st.download_button("Download Key File", data=open(result["key_file"], "rb").read(), file_name="key.txt")
        else:
            st.error("Encryption failed.")
elif action == "Decrypt":
    uploaded_file = st.file_uploader("Upload encrypted file", type=["bin"])
    key_file = st.file_uploader("Upload key file", type=["txt"])
    if uploaded_file and key_file and st.button("Decrypt"):
        files = {
            "uploaded_file": uploaded_file,
            "key_file": key_file
        }
        response = requests.post(f"{BACKEND_URL}/decrypt/", files=files)
        if response.ok:
            st.success("Decryption complete!")
            st.download_button("Download Decrypted File", data=response.content, file_name="decrypted_file")
        else:
            st.error("Decryption failed.")

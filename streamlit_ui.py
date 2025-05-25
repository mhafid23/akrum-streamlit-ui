import streamlit as st
import requests
import base64
import os

BACKEND_URL = "https://akrum-backend.onrender.com"

st.title("AKRUM File Encryption Demo")

action = st.selectbox("Select Action", ["Encrypt", "Decrypt"])

if action == "Encrypt":
    uploaded_file = st.file_uploader("Upload file to encrypt", type=["txt", "pdf", "jpg", "png", "mp4", "docx", "jpeg", "mpeg4"])
    if uploaded_file and st.button("Encrypt"):
        files = {"uploaded_file": uploaded_file}
        try:
            response = requests.post(f"{BACKEND_URL}/encrypt", files=files)
            response.raise_for_status()
            result = response.json()
            st.success("Encryption complete!")
            st.download_button("Download Encrypted File", data=open(result["encrypted_file"], "rb").read(), file_name="encrypted_file.bin")
            st.download_button("Download Key File", data=open(result["key_file"], "rb").read(), file_name="encryption_key.txt")
        except Exception as e:
            st.error(f"Encryption failed: {str(e)}")

elif action == "Decrypt":
    encrypted_file = st.file_uploader("Upload encrypted file", type=["bin"])
    key_file = st.file_uploader("Upload key file", type=["txt"])
    if encrypted_file and key_file and st.button("Decrypt"):
        files = {
            "encrypted_file": encrypted_file,
            "key_file": key_file
        }
        try:
            response = requests.post(f"{BACKEND_URL}/decrypt", files=files)
            response.raise_for_status()
            result = response.json()
            st.success("Decryption complete!")
            st.download_button("Download Decrypted File", data=open(result["original_file"], "rb").read(), file_name="decrypted_output")
        except Exception as e:
            st.error(f"Decryption failed: {str(e)}")

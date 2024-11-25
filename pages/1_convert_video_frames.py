import os
import cv2
import zipfile
import streamlit as st
from pathlib import Path

def extract_frames(video_path, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Capture video
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0

    # Extract frames
    while success:
        frame_path = os.path.join(output_dir, f"frame_{count:05d}.jpg")
        cv2.imwrite(frame_path, image)  # Save frame as JPEG
        success, image = vidcap.read()
        count += 1

    vidcap.release()
    return count

def zip_directory(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

st.title("Video to Frames Converter")
st.write("Upload a video file to extract its frames and download them as a ZIP file.")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file:
    # Save the uploaded file temporarily
    temp_video_path = Path("temp_video.mp4")
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process video and extract frames
    frames_dir = "extracted_frames"
    with st.spinner("Processing video..."):
        num_frames = extract_frames(str(temp_video_path), frames_dir)

    st.success(f"Extraction complete! {num_frames} frames extracted.")

    # Create ZIP file
    zip_path = "frames.zip"
    with st.spinner("Zipping frames..."):
        zip_directory(frames_dir, zip_path)

    # Provide the ZIP file for download
    with open(zip_path, "rb") as zip_file:
        st.download_button(
            label="Download Frames ZIP",
            data=zip_file,
            file_name="frames.zip",
            mime="application/zip",
        )

    # Clean up temporary files
    os.remove(temp_video_path)
    for file in Path(frames_dir).rglob("*"):
        file.unlink()
    Path(frames_dir).rmdir()
    os.remove(zip_path)

import cv2
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to open file dialog to choose an image
def open_image():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if filepath:
        img_path.set(filepath)
        img = cv2.imread(filepath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img.thumbnail((150, 150))  # Thumbnail of the image
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img

# Function to encrypt the message into the image
def encrypt_message():
    img = cv2.imread(img_path.get())  # Read the image
    msg = message_entry.get()  # Get the message
    password = password_entry.get()  # Get the password

    if not msg or not password:
        messagebox.showerror("Error", "Message and Password are required!")
        return

    d = {}
    c = {}

    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)

    n, m, z = 0, 0, 0
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    # Save the encrypted image
    cv2.imwrite("encryptedImage.jpg", img)
    os.system("start encryptedImage.jpg")  # Open the image (Windows only)
    messagebox.showinfo("Success", "Image encrypted and saved successfully.")

    # Save the password and message to a file for later use
    with open("password.txt", "w") as f:
        f.write(password)

# Function to decrypt the message from the image
def decrypt_message():
    pas = password_entry.get()  # Get the password input from the user

    # Check if the password is correct
    try:
        with open("password.txt", "r") as f:
            stored_password = f.read().strip()
        if pas != stored_password:
            messagebox.showerror("Error", "Incorrect passcode!")
            return
    except FileNotFoundError:
        messagebox.showerror("Error", "No encrypted image found!")
        return

    img = cv2.imread("encryptedImage.jpg")  # Read the encrypted image
    message = ""
    n, m, z = 0, 0, 0
    c = {}

    for i in range(255):
        c[i] = chr(i)

    # Decode the message from the image
    for i in range(len(message_entry.get())):
        message += c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    messagebox.showinfo("Decrypted Message", f"Decrypted Message: {message}")

# Set up the main application window
root = tk.Tk()
root.title("Image Encryption & Decryption")
root.geometry("600x400")

# Variable for image path
img_path = tk.StringVar()

# Image selection
img_label = tk.Label(root, text="No Image Selected")
img_label.pack(pady=10)

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(pady=10)

# Message and Password Entry
message_label = tk.Label(root, text="Enter Secret Message:")
message_label.pack(pady=5)

message_entry = tk.Entry(root, width=40)
message_entry.pack(pady=5)

password_label = tk.Label(root, text="Enter Passcode:")
password_label.pack(pady=5)

password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack(pady=5)

# Encryption and Decryption buttons
encrypt_button = tk.Button(root, text="Encrypt Message", command=encrypt_message)
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(root, text="Decrypt Message", command=decrypt_message)
decrypt_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

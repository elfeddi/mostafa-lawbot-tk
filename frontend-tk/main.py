import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog, simpledialog, Listbox
from PIL import Image, ImageTk
import requests
import fitz
import os

# Set API URL
api_url = 'http://localhost:5000'
token = None
username = None
upload_path = r'..\backend\uploads'



class DXCApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DXC Application")
        window_width = 1200
        window_height = 800

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Find the center point
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        # Set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()        
        self.login_frame = self.create_login_frame()
        self.register_frame = self.create_register_frame()
        self.upload_frame = self.create_upload_frame()
        self.chatbot_frame = self.create_chatbot_frame()      

        self.show_frame(self.login_frame)

    def show_frame(self, frame):
        frame.tkraise()
    def set_user_info(self, username, token):
        self.username = username
        self.token = token
        self.load_chats()

    def create_login_frame(self):
        frame = ctk.CTkFrame(self, fg_color='white')
        frame.place(relwidth=1, relheight=1)

        # Title
        ctk.CTkLabel(frame, text="WELCOME BACK!", font=("Helvetica", 24, "bold"), fg_color='white', text_color='black').place(relx=0.25, rely=0.1, anchor='w')

        # Username Entry
        ctk.CTkLabel(frame, text="Username", font=("Helvetica", 14), fg_color='white', text_color='black').place(relx=0.25, rely=0.25, anchor='w')
        self.login_username_entry = ctk.CTkEntry(frame, width=300)
        self.login_username_entry.place(relx=0.25, rely=0.3, anchor='w')

        # Password Entry
        ctk.CTkLabel(frame, text="Password", font=("Helvetica", 14), fg_color='white', text_color='black').place(relx=0.25, rely=0.4, anchor='w')
        self.login_password_entry = ctk.CTkEntry(frame, show="*", width=300)
        self.login_password_entry.place(relx=0.25, rely=0.45, anchor='w')

        # Logo
        logo_img = ctk.CTkImage(light_image=Image.open("./assets/logo.jpg"), size=(450, 150))
        logo_label = ctk.CTkLabel(frame, image=logo_img, text="", fg_color='white')
        logo_label.place(relx=0.55, rely=0.4, anchor='w')

        # Sign In Button
        ctk.CTkButton(frame, text="Sign In", command=self.login, fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20).place(relx=0.25, rely=0.55, anchor='w')

        # Register Label
        register_label = ctk.CTkLabel(frame, text="Don’t have an account? Sign up", font=("Helvetica", 12), text_color="#1E90FF", cursor="hand2", fg_color='white')
        register_label.place(relx=0.25, rely=0.65, anchor='w')
        register_label.bind("<Button-1>", lambda e: self.show_frame(self.register_frame))

        return frame


    def create_register_frame(self):
        frame = ctk.CTkFrame(self, fg_color='white')
        frame.place(relwidth=1, relheight=1)

        # Title
        ctk.CTkLabel(frame, text="CREATE ACCOUNT", font=("Helvetica", 24, "bold"), fg_color='white', text_color='black').place(relx=0.25, rely=0.1, anchor='w')

        # Username Entry
        ctk.CTkLabel(frame, text="Username", font=("Helvetica", 14), fg_color='white', text_color='black').place(relx=0.25, rely=0.25, anchor='w')
        self.reg_username_entry = ctk.CTkEntry(frame, width=300)
        self.reg_username_entry.place(relx=0.25, rely=0.3, anchor='w')

        # Password Entry
        ctk.CTkLabel(frame, text="Password", font=("Helvetica", 14), fg_color='white', text_color='black').place(relx=0.25, rely=0.4, anchor='w')
        self.reg_password_entry = ctk.CTkEntry(frame, show="*", width=300)
        self.reg_password_entry.place(relx=0.25, rely=0.45, anchor='w')

        # Logo
        logo_img = ctk.CTkImage(light_image=Image.open("./assets/logo.jpg"), size=(450, 150))
        logo_label = ctk.CTkLabel(frame, image=logo_img, text="", fg_color='white')
        logo_label.place(relx=0.55, rely=0.4, anchor='w')

        # Register Button
        ctk.CTkButton(frame, text="Sign up", command=self.register, fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20).place(relx=0.25, rely=0.55, anchor='w')

        # Back to Login Label
        back_to_login_label = ctk.CTkLabel(frame, text="Back to Login", font=("Helvetica", 12), text_color="#1E90FF", cursor="hand2", fg_color='white')
        back_to_login_label.place(relx=0.25, rely=0.65, anchor='w')
        back_to_login_label.bind("<Button-1>", lambda e: self.show_frame(self.login_frame))

        return frame


    def create_upload_frame(self):
        frame = ctk.CTkFrame(self)
        frame.place(relwidth=1, relheight=1)

        # Left panel (white background)
        left_panel = ctk.CTkFrame(frame, fg_color='white')
        left_panel.place(relwidth=0.5, relheight=1)

        # Right panel (light green background)
        right_panel = ctk.CTkFrame(frame, fg_color='#D3E4CE')
        right_panel.place(relx=0.5, relwidth=0.5, relheight=1)

        # Title on left panel
        ctk.CTkLabel(left_panel, text="Your Pdfs:", font=("Helvetica", 20, "bold"), fg_color='white', text_color='#333').place(relx=0.1, rely=0.05, anchor='w')

        # PDF Dropdown on left panel
        self.pdf_var = tk.StringVar()
        self.pdf_dropdown = ctk.CTkOptionMenu(left_panel, variable=self.pdf_var, values=[], width=200, fg_color='white', text_color='black', command=self.display_selected_pdf)
        self.pdf_dropdown.place(relx=0.3, rely=0.05, anchor='w')

        # PDF Viewer on left panel
        self.pdf_viewer_frame = tk.Frame(left_panel, bg="white", bd=1, relief="solid")
        self.pdf_viewer_frame.place(relx=0.5, rely=0.48, anchor='center', width=600, height=800)
        
        self.pdf_image_label = tk.Label(self.pdf_viewer_frame, bg="white")
        self.pdf_image_label.pack(fill="both", expand=True)

        # Navigation Buttons on left panel
        self.prev_page_button = ctk.CTkButton(left_panel, text="previous", command=self.previous_page, fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20)
        self.prev_page_button.place(relx=0.32, rely=0.91, anchor='center')
        self.next_page_button = ctk.CTkButton(left_panel, text="next", command=self.next_page, fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20)
        self.next_page_button.place(relx=0.68, rely=0.91, anchor='center')

        # Logo and Buttons on right panel
        logo_img = ctk.CTkImage(light_image=Image.open("./assets/logo.jpg"), size=(500, 150))
        logo_label = ctk.CTkLabel(right_panel, image=logo_img, text="", fg_color='#D3E4CD')
        logo_label.pack(pady=20)

        ctk.CTkButton(right_panel, text="upload pdf", command=self.upload_pdf, fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20, width=400, height=50).pack(pady=10)
        ctk.CTkButton(right_panel, text="Chatbot", command=lambda: self.show_frame(self.chatbot_frame), fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20, width=400, height=50).pack(pady=10)
        ctk.CTkButton(right_panel, text="Logout", command=lambda: self.show_frame(self.login_frame), fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20, width=400, height=50).pack(pady=10)

        return frame




    def create_chatbot_frame(self):
        frame = ctk.CTkFrame(self, fg_color="#D3E4CE")
        frame.place(relwidth=1, relheight=1)

        ctk.CTkLabel(frame, text="Dxc Chatbot", font=("Helvetica", 24, "bold"), text_color="black").place(relx=0.5, rely=0.05, anchor='center')

        self.chat_listbox = Listbox(frame, selectmode=tk.SINGLE, bg="white", fg="black", highlightbackground="#D3E4CE", selectbackground="#6A0DAD", relief="flat", font=("Helvetica", 15))
        self.chat_listbox.place(relx=0.01, rely=0.15, relwidth=0.1, relheight=0.3)
        self.chat_listbox.bind("<<ListboxSelect>>", self.load_chat_messages)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.place(relx=0.97, rely=0.1, relheight=0.75, anchor='n')

        self.chatbot_text = tk.Text(frame,
                                    width=100,  # Adjust width
                                    height=40,  # Adjust height
                                    state='disabled',
                                    bg="white",  # Darker background
                                    fg="black",  # White text
                                    wrap="word",
                                    font=("Helvetica", 12, "bold"),
                                    yscrollcommand=scrollbar.set)  # Link to scrollbar

        self.chatbot_text.place(relx=0.54, rely=0.1, anchor='n')
        scrollbar.config(command=self.chatbot_text.yview)

        self.chatbot_entry = ctk.CTkEntry(frame, width=650, fg_color="white", text_color="black", )
        self.chatbot_entry.place(relx=0.51, rely=0.89, anchor='center')

        ctk.CTkButton(frame, text="Send", command=self.send_query, fg_color="#6A0DAD", hover_color="#8A2BE2").place(relx=0.84, rely=0.89, anchor='center')
        ctk.CTkButton(frame, text="New Chat", command=self.create_new_chat, fg_color="#6A0DAD", hover_color="#8A2BE2").place(relx=0.01, rely=0.48, anchor='w')
        ctk.CTkButton(frame, text="Back", command=lambda: self.show_frame(self.upload_frame), fg_color="#6A0DAD", hover_color="#8A2BE2").place(relx=0.01, rely=0.1, anchor='w')

        return frame




    def login(self):
        global token, username
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        data = {"username": username, "password": password}
        
        try:
            response = requests.post(f'{api_url}/auth/login', json=data)
            if response.status_code == 200:
                token = response.json().get('token')
                messagebox.showinfo("Success", "Logged in successfully")
                self.load_user_pdfs()
                self.show_frame(self.upload_frame)
                self.set_user_info(username, token)
                self.show_frame(self.upload_frame)
            else:
                messagebox.showerror("Error", response.json().get('message', 'Invalid credentials'))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def register(self):
        global username
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        data = {"username": username, "password": password}
        
        try:
            response = requests.post(f'{api_url}/auth/register', json=data)
            if response.status_code == 201:
                messagebox.showinfo("Success", "User registered successfully")
                self.show_frame(self.login_frame)
            else:
                messagebox.showerror("Error", response.json().get('message', 'Error registering user'))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        
        try:
            files = {'file': open(file_path, 'rb')}
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(f'{api_url}/file/upload', files=files, headers=headers)
            
            if response.status_code == 201:
                messagebox.showinfo("Success", "File uploaded and processed successfully")
                self.load_user_pdfs()
            else:
                messagebox.showerror("Error", response.json().get('message', 'Error uploading file'))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def load_user_pdfs(self):
        user_folder = os.path.join(upload_path, username)
        print(user_folder)
        if os.path.exists(user_folder):
            pdf_files = [filename for filename in os.listdir(user_folder) if filename.endswith('.pdf')]
            self.pdf_dropdown.configure(values=pdf_files)
            if pdf_files:
                self.pdf_var.set(pdf_files[0])  # Set the first PDF as the default selection
                self.display_selected_pdf()  # Automatically display the first PDF
        else:
            messagebox.showerror("Error", "User folder does not exist.")

    def display_selected_pdf(self, event=None):
        try:
            selected_file = self.pdf_var.get()
            print("Selected value:", selected_file)
            if not selected_file:
                messagebox.showerror("Error", "No PDF selected.")
                return
            file_path = os.path.join(upload_path, username, selected_file)
            self.display_pdf(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")


    def display_pdf(self, file_path):
        try:
            print(f"Loading PDF: {file_path}")
            doc = fitz.open(file_path)
            self.page_count = len(doc)
            self.current_page = 0
            self.pdf_pages = []
            for i in range(self.page_count):
                page = doc.load_page(i)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                self.pdf_pages.append(img)
            self.show_page(self.current_page)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")

    def show_page(self, page_number):
        img = self.pdf_pages[page_number]
        img_tk = ImageTk.PhotoImage(img)
        self.pdf_image_label.configure(image=img_tk)
        self.pdf_image_label.image = img_tk

    def next_page(self):
        if self.current_page < self.page_count - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)
    def create_new_chat(self):
        title = simpledialog.askstring("New Chat", "Enter chat title:")
        if title:
            data = {"username": self.username, "title": title}
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                response = requests.post(f'{api_url}/chat/create_chat', json=data, headers=headers)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Chat created successfully")
                    self.load_chats()
                elif response.status_code == 401:
                    messagebox.showerror("Unauthorized", "You are not authorized to create a chat. Please login.")
                else:
                    messagebox.showerror("Error", response.json().get('message', 'Error creating chat'))
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", str(e))


    def load_chats(self):
        if not token or not username:
            messagebox.showerror("Error", "User not authenticated.")
            return
        
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = requests.get(f'{api_url}/chat/get_chats', params={"username": self.username}, headers=headers)
            if response.status_code == 200:
                chats = response.json()
                self.chat_listbox.delete(0, tk.END)
                for chat in chats:
                    self.chat_listbox.insert(tk.END, chat['title'])
            else:
                messagebox.showerror("Error", response.json().get('message', 'Error loading chats'))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def load_chat_messages(self, event):
        selected_index = self.chat_listbox.curselection()
        if selected_index:
            chat_title = self.chat_listbox.get(selected_index)
            chat_id = selected_index[0] + 1  # Assuming chat_id corresponds to the list index
            headers = {'Authorization': f'Bearer {self.token}'}
            try:
                response = requests.get(f'{api_url}/chat/{chat_id}/messages', headers=headers)
                if response.status_code == 200:
                    messages = response.json()
                    self.chatbot_text.configure(state='normal')
                    self.chatbot_text.delete(1.0, tk.END)
                    for message in messages:
                        sender = message['sender']
                        content = message['content']
                        if sender == self.username:
                            self.chatbot_text.insert(tk.END, "You: ", "user")
                            self.chatbot_text.insert(tk.END, f"{content}\n")
                        else:
                            self.chatbot_text.insert(tk.END, "Bot: ", "bot")
                            self.chatbot_text.insert(tk.END, f"{content}\n")
                    self.chatbot_text.tag_configure("user", foreground="#6A0DAD")
                    self.chatbot_text.tag_configure("bot", foreground="green")
                    self.chatbot_text.configure(state='disabled')
                else:
                    messagebox.showerror("Error", response.json().get('message', 'Error loading messages'))
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", str(e))



    def send_query(self):
        query = self.chatbot_entry.get()
        selected_index = self.chat_listbox.curselection()
        if selected_index:
            chat_title = self.chat_listbox.get(selected_index)
            chat_id = selected_index[0] + 1  # Assuming chat_id corresponds to the list index
            headers = {'Authorization': f'Bearer {self.token}'}
            data = {'query': query, 'chat_id': chat_id}
            
            try:
                response = requests.post(f'{api_url}/query/query', json=data, headers=headers)
                if response.status_code == 200:
                    result = response.json().get('response')
                    # Add user message to the chat in the database
                    user_message_data = {
                        'chat_id': chat_id,
                        'sender': self.username,
                        'content': query
                    }
                    user_message_response = requests.post(f'{api_url}/chat/add_message', json=user_message_data, headers=headers)
                    
                    # Add bot message to the chat in the database
                    bot_message_data = {
                        'chat_id': chat_id,
                        'sender': 'bot',
                        'content': result
                    }
                    bot_message_response = requests.post(f'{api_url}/chat/add_message', json=bot_message_data, headers=headers)
                    
                    if user_message_response.status_code == 201 and bot_message_response.status_code == 201:
                        self.load_chat_messages(None)
                        self.chatbot_entry.delete(0, tk.END)
                    else:
                        messagebox.showerror("Error", "Error adding messages to the database")
                else:
                    messagebox.showerror("Error", response.json().get('message', 'Error processing query'))
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", str(e))



if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = DXCApp()
    app.mainloop()


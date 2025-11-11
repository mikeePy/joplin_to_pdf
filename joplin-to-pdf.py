import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import glob
import pdfkit
import threading
import subprocess
import re

class HTMLToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML to PDF Converter")
        self.root.geometry("700x600")  # Larger window
        
        # Set up main layout with clear sections
        self.setup_ui()
        
    def setup_ui(self):
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)  # Content area
        self.root.grid_rowconfigure(1, weight=0)  # Button area (fixed)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main content frame (top 90% of window)
        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.grid(row=0, column=0, sticky="nsew")
        content_frame.grid_rowconfigure(4, weight=1)  # Results area expands
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Create button frame (bottom 10% of window)
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=1, column=0, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        
        # ===== CONTENT FRAME =====
        
        # Title
        title_label = ttk.Label(content_frame, text="HTML to PDF Converter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        # wkhtmltopdf configuration
        wkhtml_frame = ttk.LabelFrame(content_frame, text="wkhtmltopdf Configuration", padding="10")
        wkhtml_frame.grid(row=1, column=0, sticky="ew", pady=5)
        wkhtml_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(wkhtml_frame, text="wkhtmltopdf.exe path:").grid(row=0, column=0, sticky="w")
        
        path_frame = ttk.Frame(wkhtml_frame)
        path_frame.grid(row=1, column=0, sticky="ew", pady=5)
        path_frame.grid_columnconfigure(0, weight=1)
        
        self.wkhtml_path_var = tk.StringVar()
        self.wkhtml_entry = ttk.Entry(path_frame, textvariable=self.wkhtml_path_var)
        self.wkhtml_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Button(path_frame, text="Browse", command=self.browse_wkhtmltopdf).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(path_frame, text="Test", command=self.test_wkhtmltopdf).grid(row=0, column=2)
        
        # Directory selection
        dir_frame = ttk.LabelFrame(content_frame, text="HTML Files", padding="10")
        dir_frame.grid(row=2, column=0, sticky="ew", pady=5)
        dir_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(dir_frame, text="Folder containing HTML files:").grid(row=0, column=0, sticky="w")
        
        input_frame = ttk.Frame(dir_frame)
        input_frame.grid(row=1, column=0, sticky="ew", pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.dir_path = tk.StringVar()
        self.dir_entry = ttk.Entry(input_frame, textvariable=self.dir_path)
        self.dir_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Button(input_frame, text="Browse", command=self.browse_directory).grid(row=0, column=1)
        
        # Options frame
        options_frame = ttk.Frame(dir_frame)
        options_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        # File pattern
        ttk.Label(options_frame, text="File pattern:").grid(row=0, column=0, sticky="w")
        self.file_pattern = tk.StringVar(value="*.html")
        ttk.Entry(options_frame, textvariable=self.file_pattern, width=10).grid(row=0, column=1, padx=5)
        
        # Export type
        self.export_type = tk.StringVar(value="separate")
        ttk.Radiobutton(options_frame, text="Separate PDFs", 
                       variable=self.export_type, value="separate").grid(row=0, column=2, padx=(20, 0))
        ttk.Radiobutton(options_frame, text="Combined PDF", 
                       variable=self.export_type, value="combined").grid(row=0, column=3, padx=5)
        
        # Image handling
        self.handle_images = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include images", 
                       variable=self.handle_images).grid(row=0, column=4, padx=5)
        
        # Progress
        progress_frame = ttk.LabelFrame(content_frame, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, sticky="ew", pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill="x", pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready to convert")
        self.status_label.pack()
        
        # Results
        results_frame = ttk.LabelFrame(content_frame, text="Conversion Results", padding="10")
        results_frame.grid(row=4, column=0, sticky="nsew", pady=5)
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD, font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # ===== BUTTON FRAME =====
        
        # LARGE CONVERT BUTTON - TAKES ENTIRE BOTTOM SECTION
        self.convert_btn = tk.Button(button_frame, 
                                   text="CONVERT HTML TO PDF", 
                                   command=self.start_conversion,
                                   font=('Arial', 16, 'bold'),
                                   bg='#4CAF50',
                                   fg='white',
                                   padx=20,
                                   pady=20,
                                   cursor="hand2")
        self.convert_btn.grid(row=0, column=0, sticky="nsew", ipady=15)
        
        # Make sure the button frame expands properly
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        
    def browse_wkhtmltopdf(self):
        """Browse for wkhtmltopdf executable"""
        filename = filedialog.askopenfilename(
            title="Select wkhtmltopdf.exe",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.wkhtml_path_var.set(filename)
            
    def test_wkhtmltopdf(self):
        """Test if wkhtmltopdf is working"""
        wkhtml_path = self.wkhtml_path_var.get()
        if not wkhtml_path:
            messagebox.showerror("Error", "Please specify the path to wkhtmltopdf.exe")
            return
            
        if not os.path.exists(wkhtml_path):
            messagebox.showerror("Error", f"wkhtmltopdf not found at:\n{wkhtml_path}")
            return
            
        try:
            config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)
            test_html = "<html><body><h1>Test Document</h1><p>If you see this, wkhtmltopdf works!</p></body></html>"
            
            import tempfile
            temp_dir = tempfile.gettempdir()
            test_output = os.path.join(temp_dir, "wkhtmltopdf_test.pdf")
            
            options = {
                'page-size': 'A4',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'encoding': "UTF-8",
                'enable-local-file-access': None,
            }
            
            pdfkit.from_string(test_html, test_output, options=options, configuration=config)
            
            if os.path.exists(test_output):
                os.remove(test_output)
                messagebox.showinfo("Success", "✅ wkhtmltopdf is working!")
            else:
                messagebox.showerror("Error", "Test failed - PDF was not created")
                
        except Exception as e:
            messagebox.showerror("Error", f"❌ wkhtmltopdf test failed:\n{str(e)}")
        
    def browse_directory(self):
        path = filedialog.askdirectory(title="Select directory containing HTML files")
        if path:
            self.dir_path.set(path)
            self.status_label.config(text="Directory selected")
            self.update_results(f"Selected directory: {path}\n")
            
            # Show what files are found
            pattern = self.file_pattern.get()
            files = self.find_files(path, pattern)
            self.update_results(f"Found {len(files)} files matching '{pattern}':\n")
            for file in files[:5]:
                self.update_results(f"  - {os.path.basename(file)}\n")
            if len(files) > 5:
                self.update_results(f"  ... and {len(files) - 5} more files\n")
        
    def find_files(self, directory, pattern):
        """Find files matching pattern in directory"""
        search_path = os.path.join(directory, pattern)
        files = glob.glob(search_path)
        files = [f for f in files if os.path.isfile(f)]
        files.sort()
        return files
        
    def start_conversion(self):
        """Start conversion in a separate thread"""
        wkhtml_path = self.wkhtml_path_var.get()
        if not wkhtml_path:
            messagebox.showerror("Error", "Please specify the path to wkhtmltopdf.exe")
            return
            
        if not os.path.exists(wkhtml_path):
            messagebox.showerror("Error", f"wkhtmltopdf not found at:\n{wkhtml_path}")
            return
            
        directory = self.dir_path.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory containing HTML files.")
            return
            
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Selected directory does not exist.")
            return
            
        # Disable button during conversion
        self.convert_btn.config(state='disabled', bg='gray')
        self.progress['value'] = 0
        self.status_label.config(text="Starting conversion...")
        
        # Run in thread
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
        
    def convert_files(self):
        """Actual conversion function"""
        try:
            directory = self.dir_path.get()
            pattern = self.file_pattern.get()
            export_type = self.export_type.get()
            wkhtml_path = self.wkhtml_path_var.get()
            handle_images = self.handle_images.get()
            
            self.update_results("Starting conversion...\n")
            self.update_results(f"Output location: {directory}\n")
            self.update_results(f"Image handling: {'ENABLED' if handle_images else 'DISABLED'}\n\n")
        
            # Find files
            files = self.find_files(directory, pattern)
            
            if not files:
                self.update_results(f"❌ No files found matching '{pattern}'\n")
                self.conversion_complete(False)
                return
                
            self.update_results(f"✅ Found {len(files)} files to convert\n\n")
            
            # Create pdfkit configuration
            config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)
            
            # Convert files
            if export_type == "separate":
                success = self.convert_separate_files(files, directory, config, handle_images)
            else:
                success = self.convert_combined_file(files, directory, config, handle_images)
                
            if success:
                self.update_results(f"\n🎉 CONVERSION COMPLETED SUCCESSFULLY!\n")
                self.update_results(f"📁 All PDF files saved to: {directory}\n")
            else:
                self.update_results(f"\n❌ Conversion completed with errors\n")
                
            self.conversion_complete(success)
            
        except Exception as e:
            self.update_results(f"❌ Error: {str(e)}\n")
            self.conversion_complete(False)
            
    def convert_separate_files(self, files, output_dir, config, handle_images):
        """Convert each file to separate PDF"""
        success_count = 0
        
        for i, file_path in enumerate(files):
            progress = (i + 1) / len(files) * 100
            self.update_progress(progress, f"Converting {i+1}/{len(files)}")
            
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.pdf")
            
            self.update_results(f"Converting: {os.path.basename(file_path)} → {base_name}.pdf\n")
            
            try:
                options = {
                    'page-size': 'A4',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'enable-local-file-access': None,
                    'quiet': ''
                }
                
                if handle_images:
                    processed_html = self.process_html_images(file_path, output_dir)
                    pdfkit.from_string(processed_html, output_path, options=options, configuration=config)
                else:
                    pdfkit.from_file(file_path, output_path, options=options, configuration=config)
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    self.update_results(f"  ✅ Success\n")
                    success_count += 1
                else:
                    self.update_results(f"  ❌ Failed\n")
                    
            except Exception as e:
                self.update_results(f"  ❌ Error: {str(e)}\n")
        
        self.update_results(f"\nSuccessfully converted {success_count}/{len(files)} files\n")
        return success_count > 0
        
    def convert_combined_file(self, files, output_dir, config, handle_images):
        """Combine all files into one PDF"""
        try:
            self.update_results("Creating combined PDF...\n")
            
            combined_html = ['<html><head><meta charset="UTF-8"><style>']
            combined_html.append('body { font-family: Arial; margin: 1in; line-height: 1.4; }')
            combined_html.append('h1 { color: #333; border-bottom: 2px solid #333; }')
            combined_html.append('h2 { color: #555; margin-top: 40px; }')
            combined_html.append('.page-break { page-break-after: always; }')
            combined_html.append('img { max-width: 100%; height: auto; }')
            combined_html.append('</style></head><body>')
            combined_html.append('<h1>Combined Documents</h1>')
            
            for i, file_path in enumerate(files):
                progress = (i + 1) / len(files) * 50
                self.update_progress(progress, f"Reading {i+1}/{len(files)}")
                
                self.update_results(f"Reading: {os.path.basename(file_path)}\n")
                
                try:
                    if handle_images:
                        file_content = self.process_html_images(file_path, output_dir)
                        body_match = re.search(r'<body[^>]*>(.*?)</body>', file_content, re.DOTALL | re.IGNORECASE)
                        if body_match:
                            content = body_match.group(1)
                        else:
                            content = file_content
                    else:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
                        if body_match:
                            content = body_match.group(1)
                    
                    combined_html.append(f'<h2>{os.path.basename(file_path)}</h2>')
                    combined_html.append(content)
                    combined_html.append('<div class="page-break"></div>')
                    
                except Exception as e:
                    self.update_results(f"  ⚠️  Warning: {str(e)}\n")
                    continue
            
            combined_html.append('</body></html>')
            
            self.update_progress(75, "Creating combined PDF...")
            
            dir_name = os.path.basename(output_dir.rstrip('/\\'))
            output_path = os.path.join(output_dir, f"{dir_name}_combined.pdf")
            
            self.update_results(f"Creating: {os.path.basename(output_path)}\n")
            
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'enable-local-file-access': None,
                'quiet': ''
            }
            
            pdfkit.from_string('\n'.join(combined_html), output_path, options=options, configuration=config)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                self.update_results(f"✅ Combined PDF created successfully\n")
                return True
            else:
                self.update_results(f"❌ Failed to create combined PDF\n")
                return False
                
        except Exception as e:
            self.update_results(f"❌ Error: {str(e)}\n")
            return False
    
    def process_html_images(self, html_file_path, output_dir):
        """Process HTML to fix image paths"""
        try:
            with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            html_dir = os.path.dirname(html_file_path)
            
            img_pattern = r'<img[^>]+src="([^"]*)"[^>]*>'
            
            def replace_image_path(match):
                img_src = match.group(1)
                
                if img_src.startswith('data:') or img_src.startswith('http://') or img_src.startswith('https://'):
                    return match.group(0)
                
                if img_src.startswith('/'):
                    absolute_path = img_src
                else:
                    absolute_path = os.path.join(html_dir, img_src)
                
                absolute_path = os.path.abspath(absolute_path)
                
                if os.path.exists(absolute_path):
                    file_url = 'file:///' + absolute_path.replace('\\', '/')
                    return match.group(0).replace(img_src, file_url)
                else:
                    self.update_results(f"  ⚠️  Image not found: {img_src}\n")
                    return match.group(0)
            
            processed_html = re.sub(img_pattern, replace_image_path, html_content)
            return processed_html
            
        except Exception as e:
            self.update_results(f"  ⚠️  Error processing images: {str(e)}\n")
            with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
    def update_results(self, message):
        """Update results text"""
        def update():
            self.results_text.insert(tk.END, message)
            self.results_text.see(tk.END)
        self.root.after(0, update)
        
    def update_progress(self, value, status_text):
        """Update progress bar and status"""
        def update():
            self.progress['value'] = value
            self.status_label.config(text=status_text)
        self.root.after(0, update)
        
    def conversion_complete(self, success):
        """Handle conversion completion"""
        def complete():
            self.progress['value'] = 100
            self.convert_btn.config(state='normal', bg='#4CAF50')
            if success:
                self.status_label.config(text="Conversion completed!")
                messagebox.showinfo("Success", "PDF files created successfully!")
            else:
                self.status_label.config(text="Conversion failed")
        self.root.after(0, complete)

# Create and run the application
if __name__ == "__main__":
    try:
        import pdfkit
        root = tk.Tk()
        app = HTMLToPDFConverter(root)
        root.mainloop()
    except ImportError:
        print("ERROR: Please install pdfkit: pip install pdfkit")
        input("Press Enter to exit...")
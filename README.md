```markdown
# Joplin to PDF Converter

A user-friendly desktop application that converts Joplin HTML export files to PDF format with a simple graphical interface. Perfect for batch conversion of entire Joplin notebooks.

## Features

- **Batch Conversion**: Convert multiple HTML files at once
- **Flexible Output Options**: 
  - Separate PDF files for each HTML file
  - Single combined PDF with all content
- **Image Support**: Automatically handles local images in HTML files
- **Customizable File Patterns**: Specify which HTML files to convert using glob patterns
- **Progress Tracking**: Real-time progress bar and status updates
- **Detailed Logging**: Comprehensive conversion results and error reporting
- **Cross-Platform**: Works on Windows (requires wkhtmltopdf)

## Requirements

### Python Dependencies
```bash
pip install pdfkit
```

### System Requirements
- **Windows**: wkhtmltopdf executable
- **Python 3.6+** with tkinter (usually included by default)

### wkhtmltopdf Installation
1. Download wkhtmltopdf from [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
2. Install it or extract the portable version
3. Note the path to `wkhtmltopdf.exe` for the application configuration

## Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install pdfkit
   ```
3. **Download wkhtmltopdf** (see System Requirements above)
4. **Run the application**:
   ```bash
   python html_to_pdf_converter.py
   ```

## Usage

### Step 0: Export your Joplin Notebook (Export -> Export HTML Directory)

### Step 1: Configure wkhtmltopdf
- Click "Browse" to locate your `wkhtmltopdf.exe` file
- Click "Test" to verify the installation works correctly

### Step 2: Select HTML Files
- Click "Browse" to choose a folder containing your Joplin HTML Export files
- Adjust the "File pattern" if needed (default: `*.html`)

### Step 3: Choose Conversion Options
- **Export Type**:
  - **Separate PDFs**: Creates individual PDF files for each HTML file
  - **Combined PDF**: Merges all HTML content into a single PDF
- **Include Images**: Toggle image support in the converted PDFs

### Step 4: Convert
- Click the large **"CONVERT HTML TO PDF"** button
- Monitor progress in the status area
- View detailed results in the conversion log

## File Structure

The application will create PDF files in the same directory as your HTML files:
- **Separate mode**: `filename.html` → `filename.pdf`
- **Combined mode**: Creates `[folder_name]_combined.pdf`

## Supported Formats

- **Input**: HTML files (.html, .htm)
- **Output**: PDF files (.pdf)
- **Images**: Local images (JPEG, PNG, GIF, etc.) with proper file paths

## Troubleshooting

### Common Issues

1. **"wkhtmltopdf not found"**
   - Ensure you've downloaded and configured the correct path to wkhtmltopdf.exe
   - Test the configuration using the "Test" button

2. **Images not appearing in PDF**
   - Check that image paths in your HTML are relative to the HTML file location
   - Enable "Include images" option in the application

3. **Conversion fails**
   - Verify HTML files are valid and properly formatted
   - Check the results log for specific error messages
   - Ensure adequate disk space in the output directory

4. **Character encoding issues**
   - Ensure your HTML files specify correct encoding (UTF-8 recommended)
   - The application automatically handles UTF-8 encoding

### Performance Tips

- For large numbers of files, consider using "Separate PDFs" mode
- The application processes files in sequence to avoid system overload
- Progress is shown in real-time for monitoring conversion status

## Technical Details

- Built with Python and Tkinter for the GUI
- Uses pdfkit as a wrapper for wkhtmltopdf
- Threaded conversion to keep the interface responsive
- Comprehensive error handling and logging

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all requirements are properly installed
3. Ensure your HTML files are valid and accessible

For additional help, please check the [wkhtmltopdf documentation](https://wkhtmltopdf.org/usage/wkhtmltopdf.txt) for advanced configuration options.

---

**Note**: This application requires the wkhtmltopdf engine, which is not included. You must download it separately from the official website.
```

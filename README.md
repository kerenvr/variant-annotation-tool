## Genetic Variant Annotation

### Description

The Genetic Variant Annotation tool processes GVF (Genome Variant Format) files to extract relevant information based on rs IDs. It is designed to facilitate the annotation of genetic variants by leveraging specific identifiers.

### Setup Instructions

1. **Create a Virtual Environment:**
   - Begin by setting up a virtual environment to isolate dependencies.
     ```
     python -m venv venv_name
     ```
     Replace `venv_name` with your preferred name for the virtual environment.

2. **Activate the Virtual Environment:**
   - Activate the virtual environment based on your operating system:
     - On Windows:
       ```
       venv_name\Scripts\activate
       ```
     - On macOS and Linux:
       ```
       source venv_name/bin/activate
       ```

3. **Install Dependencies:**
   - Install the necessary dependencies listed in the `requirements.txt` file.
     ```
     pip install -r requirements.txt
     ```
   - This step ensures all required libraries are available within the virtual environment.

### Usage

- Once the virtual environment is set up and dependencies are installed, the Genetic Variant Annotation tool can be executed to process GVF files.

### Notes

- Ensure that the input GVF file is correctly specified in the script.
- The randomized output file will be created in the same directory as specified in the script.

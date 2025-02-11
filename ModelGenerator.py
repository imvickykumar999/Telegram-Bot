import os

# Define file paths
directory = "extracted_content"
output_file = "Modelfile"

# Start writing the Modelfile content
with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write("FROM llama3.2:1b\n\n")
    outfile.write("# set the temperature to 1 [higher is more creative, lower is more coherent]\n")
    outfile.write("PARAMETER temperature 1\n\n")
    outfile.write("# set the system message\n")
    outfile.write("SYSTEM \"\"\"\n")
    
    # Iterate through markdown files and append content
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as infile:
                outfile.write(f"## {filename.replace('_', ' ').replace('.md', '')}\n\n")
                outfile.write(infile.read() + "\n\n")
    
    outfile.write("\"\"\"")

print(f"{output_file} has been created successfully.")

# ollama create blogforge -f ./Modelfile

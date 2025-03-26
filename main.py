import os
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # YAML Front Matter parseren
    if content.startswith('---'):
        _, front_matter, markdown_content = content.split('---', 2)
        metadata = yaml.safe_load(front_matter)
    else:
        metadata = {}
        markdown_content = content

    # Markdown converteren naar HTML
    html_content = markdown.markdown(markdown_content)
    
    return metadata, html_content

def save_html(output_path, content):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_directory(input_dir, output_dir, template):
    # Zorg ervoor dat de output directory bestaat
    os.makedirs(output_dir, exist_ok=True)
    
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.md'):
                input_file = os.path.join(root, file_name)
                
                # Markdown omzetten naar HTML
                metadata, html_content = parse_markdown(input_file)
                
                # Template renderen
                rendered_content = template.render(
                    title=metadata.get('title', 'Geen Titel'),
                    author=metadata.get('author', 'Onbekend'),
                    date=metadata.get('date', 'Onbekende Datum'),
                    content=html_content
                )
                
                # Bestandspad genereren in de output directory
                relative_path = os.path.relpath(input_file, input_dir)
                output_file = os.path.join(output_dir, os.path.splitext(relative_path)[0] + '.html')
                
                # Zorg ervoor dat de map bestaat waar het HTML bestand wordt opgeslagen
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                # HTML bestand opslaan
                save_html(output_file, rendered_content)
                print(f"Gegenereerd: {output_file}")

if __name__ == "__main__":
    # Jinja2 omgeving instellen
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('base.html')

    # Verwerk posts en pages mappen
    process_directory('posts', '_site/posts', template)
    process_directory('pages', '_site/pages', template)

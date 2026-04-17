import os
import sys
import json
import shutil
from jinja2 import Environment, FileSystemLoader
import markdown2
import frontmatter

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from scripts.generate_index import generate_search_index

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def scan_notes():
    notes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notes')
    categories = {}
    
    for root, dirs, files in os.walk(notes_dir):
        rel_path = os.path.relpath(root, notes_dir)
        if rel_path == '.':
            category_path = []
        else:
            category_path = rel_path.split(os.sep)
        
        for file in files:
            if file.endswith(('.md', '.html', '.pdf')):
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, notes_dir)
                file_info = {
                    'name': file,
                    'path': rel_file_path,
                    'type': file.split('.')[-1],
                    'mtime': os.path.getmtime(file_path)
                }
                
                if file.endswith('.md'):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        try:
                            post = frontmatter.loads(f.read())
                            file_info['title'] = post.get('title', file[:-3])
                            file_info['tags'] = post.get('tags', [])
                            file_info['summary'] = post.get('summary', '')
                        except:
                            file_info['title'] = file[:-3]
                            file_info['tags'] = []
                            file_info['summary'] = ''
                elif file.endswith('.html'):
                    file_info['title'] = file[:-5]
                    file_info['tags'] = []
                    file_info['summary'] = ''
                elif file.endswith('.pdf'):
                    file_info['title'] = file[:-4]
                    file_info['tags'] = []
                    file_info['summary'] = ''
                
                if not category_path:
                    if '__root__' not in categories:
                        categories['__root__'] = {'children': {}, 'files': []}
                    categories['__root__']['files'].append(file_info)
                else:
                    current = categories
                    for i, cat in enumerate(category_path):
                        if i == 0:
                            if cat not in current:
                                current[cat] = {'children': {}, 'files': []}
                            current = current[cat]
                        else:
                            if cat not in current['children']:
                                current['children'][cat] = {'children': {}, 'files': []}
                            current = current['children'][cat]
                    if 'files' not in current:
                        current['files'] = []
                    current['files'].append(file_info)
    
    return categories

def render_markdown(content):
    extras = ['fenced-code-blocks', 'tables', 'toc', 'metadata', 'code-friendly', 'footnotes']
    return markdown2.markdown(content, extras=extras)

def build_site():
    config = load_config()
    categories = scan_notes()
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    templates_dir = os.path.join(base_dir, 'templates')
    output_dir = os.path.join(base_dir, 'docs')
    static_dir = os.path.join(base_dir, 'static')
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, os.path.join(output_dir, 'static'))
    
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
    
    index_template = env.get_template('base.html')
    category_template = env.get_template('category.html')
    note_template = env.get_template('note.html')
    
    index_html = index_template.render(config=config, categories=categories)
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    def process_category(path, category_data):
        category_path = os.path.join(output_dir, *path)
        os.makedirs(category_path, exist_ok=True)
        
        # 计算相对路径前缀
        depth = len(path)
        relative_prefix = '../' * depth
        
        category_html = category_template.render(
            config=config,
            categories=categories,
            current_path=path,
            category_data=category_data,
            relative_prefix=relative_prefix
        )
        with open(os.path.join(category_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(category_html)
        
        for file_info in category_data['files']:
            file_output_path = os.path.join(output_dir, file_info['path'])
            os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
            
            if file_info['type'] == 'md':
                file_path = os.path.join(base_dir, 'notes', file_info['path'])
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                post = frontmatter.loads(content)
                # 如果没有frontmatter，使用整个内容
                if not post.content:
                    html_content = render_markdown(content)
                else:
                    html_content = render_markdown(post.content)
                
                # 计算笔记页面的相对路径前缀
                note_depth = len(file_info['path'].split(os.sep)) - 1
                note_relative_prefix = '../' * note_depth
                
                note_html = note_template.render(
                    config=config,
                    categories=categories,
                    file_info=file_info,
                    content=html_content,
                    relative_prefix=note_relative_prefix
                )
                with open(file_output_path.replace('.md', '.html'), 'w', encoding='utf-8') as f:
                    f.write(note_html)
            elif file_info['type'] == 'html':
                file_path = os.path.join(base_dir, 'notes', file_info['path'])
                shutil.copy(file_path, file_output_path)
            elif file_info['type'] == 'pdf':
                file_path = os.path.join(base_dir, 'notes', file_info['path'])
                shutil.copy(file_path, file_output_path)
        
        for cat_name, cat_data in category_data['children'].items():
            process_category(path + [cat_name], cat_data)
    
    for cat_name, cat_data in categories.items():
        process_category([cat_name], cat_data)
    
    generate_search_index()
    print('Site built successfully!')

if __name__ == '__main__':
    build_site()
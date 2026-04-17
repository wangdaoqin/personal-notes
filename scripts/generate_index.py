import os
import json
import frontmatter

def generate_search_index():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    notes_dir = os.path.join(base_dir, 'notes')
    output_dir = os.path.join(base_dir, 'docs')
    
    index = []
    
    for root, dirs, files in os.walk(notes_dir):
        for file in files:
            if file.endswith(('.md', '.html', '.pdf')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, notes_dir)
                category = os.path.dirname(rel_path).replace(os.sep, '/')
                
                item = {
                    'title': file.split('.')[0],
                    'path': rel_path,
                    'category': category,
                    'type': file.split('.')[-1],
                    'mtime': os.path.getmtime(file_path),
                    'content': ''
                }
                
                if file.endswith('.md'):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        try:
                            post = frontmatter.loads(f.read())
                            item['title'] = post.get('title', item['title'])
                            item['tags'] = post.get('tags', [])
                            item['content'] = post.content
                        except:
                            pass
                elif file.endswith('.html'):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        try:
                            content = f.read()
                            # 简单提取文本内容，去除HTML标签
                            import re
                            item['content'] = re.sub(r'<[^>]+>', '', content)
                        except:
                            pass
                
                index.append(item)
    
    index_path = os.path.join(output_dir, 'search_index.json')
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"Search index generated at: {index_path}")
    return index

if __name__ == '__main__':
    generate_search_index()
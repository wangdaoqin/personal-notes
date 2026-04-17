document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    let searchIndex = [];
    
    // 加载搜索索引
    fetch('/search_index.json')
        .then(response => response.json())
        .then(data => {
            searchIndex = data;
        })
        .catch(error => {
            console.error('Failed to load search index:', error);
        });
    
    // 搜索输入事件
    searchInput.addEventListener('input', function() {
        const query = this.value.trim().toLowerCase();
        
        if (query.length < 2) {
            searchResults.classList.remove('show');
            return;
        }
        
        // 搜索匹配
        const results = searchIndex.filter(item => {
            return (
                item.title.toLowerCase().includes(query) ||
                item.content.toLowerCase().includes(query) ||
                (item.tags && item.tags.some(tag => tag.toLowerCase().includes(query)))
            );
        });
        
        // 显示搜索结果
        displaySearchResults(results);
    });
    
    // 点击页面其他地方关闭搜索结果
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
            searchResults.classList.remove('show');
        }
    });
    
    // 显示搜索结果
    function displaySearchResults(results) {
        searchResults.innerHTML = '';
        
        if (results.length === 0) {
            searchResults.classList.remove('show');
            return;
        }
        
        const ul = document.createElement('ul');
        
        results.forEach(item => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            
            let path = item.path;
            if (item.type === 'md') {
                path = path.replace('.md', '.html');
            }
            
            a.href = '/' + path;
            a.textContent = item.title;
            
            const meta = document.createElement('div');
            meta.className = 'search-result-meta';
            meta.textContent = `${item.category || '未分类'} • ${item.type.toUpperCase()}`;
            
            li.appendChild(a);
            li.appendChild(meta);
            ul.appendChild(li);
        });
        
        searchResults.appendChild(ul);
        searchResults.classList.add('show');
    }
    
    // 添加搜索结果样式
    const style = document.createElement('style');
    style.textContent = `
        .search-result-meta {
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }
        body.dark-theme .search-result-meta {
            color: #aaa;
        }
    `;
    document.head.appendChild(style);
});
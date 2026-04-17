document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const darkThemeLink = document.getElementById('dark-theme');
    
    // 检查本地存储中的主题设置
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        darkThemeLink.disabled = false;
    }
    
    // 主题切换按钮点击事件
    themeToggle.addEventListener('click', function() {
        const isDark = document.body.classList.toggle('dark-theme');
        darkThemeLink.disabled = !isDark;
        
        // 保存主题设置到本地存储
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});
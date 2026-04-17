import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from scripts.build import build_site

class NotesEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_build = 0
        self.build_cooldown = 2  # 2秒冷却时间，避免频繁构建
    
    def on_any_event(self, event):
        # 忽略目录变化和隐藏文件
        if event.is_directory or os.path.basename(event.src_path).startswith('.'):
            return
        
        # 只处理指定类型的文件
        if not event.src_path.endswith(('.md', '.html', '.pdf')):
            return
        
        current_time = time.time()
        if current_time - self.last_build > self.build_cooldown:
            print(f"Detected change: {event.src_path}")
            print("Rebuilding site...")
            build_site()
            self.last_build = current_time

def start_watching():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    notes_dir = os.path.join(base_dir, 'notes')
    
    event_handler = NotesEventHandler()
    observer = Observer()
    observer.schedule(event_handler, notes_dir, recursive=True)
    
    print(f"Watching for changes in: {notes_dir}")
    print("Press Ctrl+C to stop.")
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == '__main__':
    start_watching()
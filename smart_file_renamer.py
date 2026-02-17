import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path

# 다국어 딕셔너리
LANGUAGES = {
    'KR': {
        'title': '파일 이름 일괄 변경기',
        'select_folder': '폴더 선택',
        'enter_prefix': '접두사 입력',
        'preview': '미리보기',
        'rename_all': '전체 변경',
        'language': '언어',
        'current_name': '현재 이름',
        'new_name': '새 이름',
        'select_language': '언어 선택',
        'no_folder_selected': '폴더를 선택해주세요.',
        'no_prefix': '접두사를 입력해주세요.',
        'preview_generated': '미리보기 생성 완료',
        'confirm_rename': '파일 이름을 변경하시겠습니까?',
        'rename_success': '파일 이름 변경이 완료되었습니다.',
        'rename_error': '파일 이름 변경 중 오류가 발생했습니다.',
        'no_files': '변경할 파일이 없습니다.'
    },
    'EN': {
        'title': 'Smart File Renamer',
        'select_folder': 'Select Folder',
        'enter_prefix': 'Enter Prefix',
        'preview': 'Preview',
        'rename_all': 'Rename All',
        'language': 'Language',
        'current_name': 'Current Name',
        'new_name': 'New Name',
        'select_language': 'Select Language',
        'no_folder_selected': 'Please select a folder.',
        'no_prefix': 'Please enter a prefix.',
        'preview_generated': 'Preview generated successfully',
        'confirm_rename': 'Do you want to rename the files?',
        'rename_success': 'Files renamed successfully.',
        'rename_error': 'An error occurred while renaming files.',
        'no_files': 'No files to rename.'
    },
    'JP': {
        'title': 'スマートファイル名変更',
        'select_folder': 'フォルダ選択',
        'enter_prefix': 'プレフィックス入力',
        'preview': 'プレビュー',
        'rename_all': '一括変更',
        'language': '言語',
        'current_name': '現在の名前',
        'new_name': '新しい名前',
        'select_language': '言語選択',
        'no_folder_selected': 'フォルダを選択してください。',
        'no_prefix': 'プレフィックスを入力してください。',
        'preview_generated': 'プレビューが生成されました',
        'confirm_rename': 'ファイル名を変更しますか？',
        'rename_success': 'ファイル名の変更が完了しました。',
        'rename_error': 'ファイル名変更中にエラーが発生しました。',
        'no_files': '変更するファイルがありません。'
    }
}


class SmartFileRenamer:
    def __init__(self, root):
        self.root = root
        self.current_language = 'KR'
        self.selected_folder = None
        self.preview_data = []  # [(current_name, new_name), ...]
        
        # 언어 딕셔너리 가져오기
        self.lang = LANGUAGES[self.current_language]
        
        # 윈도우 설정
        self.root.title(self.lang['title'])
        self.root.geometry('800x600')
        self.root.resizable(True, True)
        
        # UI 구성
        self.create_widgets()
        
    def get_text(self, key):
        """현재 언어에 맞는 텍스트 반환"""
        return LANGUAGES[self.current_language][key]
    
    def update_ui_text(self):
        """UI 텍스트를 현재 언어로 업데이트"""
        self.lang = LANGUAGES[self.current_language]
        self.root.title(self.lang['title'])
        self.select_folder_btn.config(text=self.lang['select_folder'])
        self.prefix_label.config(text=self.lang['enter_prefix'])
        self.preview_btn.config(text=self.lang['preview'])
        self.rename_all_btn.config(text=self.lang['rename_all'])
        self.language_label.config(text=self.lang['language'])
        
        # Treeview 컬럼 헤더 업데이트
        self.preview_tree.heading('#1', text=self.lang['current_name'])
        self.preview_tree.heading('#2', text=self.lang['new_name'])
        
    def create_widgets(self):
        # 상단 프레임 (언어 선택)
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        self.language_label = ttk.Label(top_frame, text=self.lang['language'])
        self.language_label.pack(side=tk.LEFT, padx=5)
        
        # 언어 선택 라디오 버튼
        language_frame = ttk.Frame(top_frame)
        language_frame.pack(side=tk.LEFT, padx=10)
        
        self.language_var = tk.StringVar(value=self.current_language)
        for lang_code, lang_name in [('KR', '한국어'), ('EN', 'English'), ('JP', '日本語')]:
            rb = ttk.Radiobutton(
                language_frame,
                text=lang_name,
                variable=self.language_var,
                value=lang_code,
                command=self.on_language_change
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # 폴더 선택 프레임
        folder_frame = ttk.Frame(self.root, padding="10")
        folder_frame.pack(fill=tk.X)
        
        self.select_folder_btn = ttk.Button(
            folder_frame,
            text=self.lang['select_folder'],
            command=self.select_folder
        )
        self.select_folder_btn.pack(side=tk.LEFT, padx=5)
        
        self.folder_label = ttk.Label(
            folder_frame,
            text="",
            foreground="gray"
        )
        self.folder_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # 접두사 입력 프레임
        prefix_frame = ttk.Frame(self.root, padding="10")
        prefix_frame.pack(fill=tk.X)
        
        self.prefix_label = ttk.Label(prefix_frame, text=self.lang['enter_prefix'])
        self.prefix_label.pack(side=tk.LEFT, padx=5)
        
        self.prefix_entry = ttk.Entry(prefix_frame, width=30)
        self.prefix_entry.pack(side=tk.LEFT, padx=5)
        
        # 버튼 프레임
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        self.preview_btn = ttk.Button(
            button_frame,
            text=self.lang['preview'],
            command=self.generate_preview
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.rename_all_btn = ttk.Button(
            button_frame,
            text=self.lang['rename_all'],
            command=self.rename_all_files,
            state=tk.DISABLED
        )
        self.rename_all_btn.pack(side=tk.LEFT, padx=5)
        
        # 미리보기 프레임
        preview_frame = ttk.Frame(self.root, padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview 생성
        self.preview_tree = ttk.Treeview(
            preview_frame,
            columns=('new_name',),
            show='tree headings',
            height=15
        )
        
        # 컬럼 설정
        self.preview_tree.heading('#0', text=self.lang['current_name'])
        self.preview_tree.heading('new_name', text=self.lang['new_name'])
        self.preview_tree.column('#0', width=350, anchor=tk.W)
        self.preview_tree.column('new_name', width=350, anchor=tk.W)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def on_language_change(self):
        """언어 변경 이벤트 핸들러"""
        self.current_language = self.language_var.get()
        self.update_ui_text()
        
    def select_folder(self):
        """폴더 선택"""
        folder = filedialog.askdirectory(title=self.lang['select_folder'])
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=folder, foreground="black")
            # 폴더 선택 시 미리보기 초기화
            self.clear_preview()
    
    def clear_preview(self):
        """미리보기 초기화"""
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        self.preview_data = []
        self.rename_all_btn.config(state=tk.DISABLED)
    
    def generate_preview(self):
        """미리보기 생성"""
        # 입력 검증
        if not self.selected_folder:
            messagebox.showwarning(
                self.lang['title'],
                self.lang['no_folder_selected']
            )
            return
        
        prefix = self.prefix_entry.get().strip()
        if not prefix:
            messagebox.showwarning(
                self.lang['title'],
                self.lang['no_prefix']
            )
            return
        
        # 기존 미리보기 초기화
        self.clear_preview()
        
        # 파일 목록 가져오기
        try:
            files = [f for f in os.listdir(self.selected_folder) 
                    if os.path.isfile(os.path.join(self.selected_folder, f))]
            
            if not files:
                messagebox.showinfo(
                    self.lang['title'],
                    self.lang['no_files']
                )
                return
            
            # 미리보기 데이터 생성
            self.preview_data = []
            for file in sorted(files):
                file_path = Path(file)
                new_name = f"{prefix}{file_path.stem}{file_path.suffix}"
                self.preview_data.append((file, new_name))
                self.preview_tree.insert('', tk.END, text=file, values=(new_name,))
            
            # Rename All 버튼 활성화
            self.rename_all_btn.config(state=tk.NORMAL)
            
            messagebox.showinfo(
                self.lang['title'],
                self.lang['preview_generated']
            )
            
        except Exception as e:
            messagebox.showerror(
                self.lang['title'],
                f"{self.lang['rename_error']}: {str(e)}"
            )
    
    def rename_all_files(self):
        """모든 파일 이름 변경"""
        if not self.preview_data:
            return
        
        # 확인 팝업
        result = messagebox.askyesno(
            self.lang['title'],
            self.lang['confirm_rename']
        )
        
        if not result:
            return
        
        # 파일 이름 변경 실행
        success_count = 0
        error_count = 0
        
        try:
            for current_name, new_name in self.preview_data:
                old_path = os.path.join(self.selected_folder, current_name)
                new_path = os.path.join(self.selected_folder, new_name)
                
                # 이름이 같은 경우 스킵
                if current_name == new_name:
                    continue
                
                try:
                    os.rename(old_path, new_path)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Error renaming {current_name}: {str(e)}")
            
            # 결과 메시지
            if error_count == 0:
                messagebox.showinfo(
                    self.lang['title'],
                    self.lang['rename_success']
                )
            else:
                messagebox.showwarning(
                    self.lang['title'],
                    f"{self.lang['rename_success']} ({success_count} files). {error_count} errors occurred."
                )
            
            # 미리보기 초기화
            self.clear_preview()
            self.prefix_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror(
                self.lang['title'],
                f"{self.lang['rename_error']}: {str(e)}"
            )


def main():
    root = tk.Tk()
    app = SmartFileRenamer(root)
    root.mainloop()


if __name__ == '__main__':
    main()

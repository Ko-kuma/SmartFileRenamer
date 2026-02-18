import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from typing import List, Tuple, Optional


# ============================================================================
# 다국어 지원
# ============================================================================

LANGUAGES = {
    'KR': {
        'title': 'Smart File Renamer v0.2',
        'select_folder': '폴더 선택',
        'folder_path': '선택된 폴더',
        'file_count': '파일 수',
        'rename_settings': '이름 변경 설정',
        'prefix': '접두사',
        'sequential_numbering': '순차 번호 추가',
        'start_number': '시작 번호',
        'digit_padding': '자릿수 패딩',
        'preview': '미리보기',
        'rename_all': '전체 변경',
        'current_name': '현재 이름',
        'new_name': '새 이름',
        'status': '상태',
        'no_folder_selected': '폴더를 선택해주세요.',
        'no_files': '변경할 파일이 없습니다.',
        'preview_generated': '미리보기 생성 완료',
        'confirm_rename': '파일 이름을 변경하시겠습니까?',
        'rename_success': '파일 이름 변경이 완료되었습니다.',
        'rename_error': '파일 이름 변경 중 오류가 발생했습니다.',
        'files_renamed': '개 파일이 변경되었습니다.',
        'waiting': '대기 중...',
        'folder_selected': '폴더가 선택되었습니다.',
        'warning_no_folder': '경고: 폴더를 선택해주세요.',
        'warning_no_files': '경고: 변경할 파일이 없습니다.',
        'warning_no_prefix': '경고: 접두사를 입력해주세요.',
        'preview_complete': '미리보기 생성 완료',
        'success_renamed': '성공:',
        'partial_success': '부분 성공:',
        'error': '오류:',
        'no_prefix_enter': '접두사를 입력해주세요.'
    },
    'EN': {
        'title': 'Smart File Renamer v0.2',
        'select_folder': 'Select Folder',
        'folder_path': 'Selected Folder',
        'file_count': 'File Count',
        'rename_settings': 'Rename Settings',
        'prefix': 'Prefix',
        'sequential_numbering': 'Add Sequential Numbering',
        'start_number': 'Start Number',
        'digit_padding': 'Digit Padding',
        'preview': 'Preview',
        'rename_all': 'Rename All',
        'current_name': 'Current Name',
        'new_name': 'New Name',
        'status': 'Status',
        'no_folder_selected': 'Please select a folder.',
        'no_files': 'No files to rename.',
        'preview_generated': 'Preview generated successfully',
        'confirm_rename': 'Do you want to rename the files?',
        'rename_success': 'Files renamed successfully.',
        'rename_error': 'An error occurred while renaming files.',
        'files_renamed': 'files renamed.',
        'waiting': 'Waiting...',
        'folder_selected': 'Folder selected.',
        'warning_no_folder': 'Warning: Please select a folder.',
        'warning_no_files': 'Warning: No files to rename.',
        'warning_no_prefix': 'Warning: Please enter a prefix.',
        'preview_complete': 'Preview generated',
        'success_renamed': 'Success:',
        'partial_success': 'Partial success:',
        'error': 'Error:',
        'no_prefix_enter': 'Please enter a prefix.'
    },
    'JP': {
        'title': 'Smart File Renamer v0.2',
        'select_folder': 'フォルダ選択',
        'folder_path': '選択されたフォルダ',
        'file_count': 'ファイル数',
        'rename_settings': '名前変更設定',
        'prefix': 'プレフィックス',
        'sequential_numbering': '連番追加',
        'start_number': '開始番号',
        'digit_padding': '桁数パディング',
        'preview': 'プレビュー',
        'rename_all': '一括変更',
        'current_name': '現在の名前',
        'new_name': '新しい名前',
        'status': '状態',
        'no_folder_selected': 'フォルダを選択してください。',
        'no_files': '変更するファイルがありません。',
        'preview_generated': 'プレビューが生成されました',
        'confirm_rename': 'ファイル名を変更しますか？',
        'rename_error': 'ファイル名変更中にエラーが発生しました。',
        'rename_success': 'ファイル名の変更が完了しました。',
        'files_renamed': '個のファイルが変更されました。',
        'waiting': '待機中...',
        'folder_selected': 'フォルダが選択されました。',
        'warning_no_folder': '警告: フォルダを選択してください。',
        'warning_no_files': '警告: 変更するファイルがありません。',
        'warning_no_prefix': '警告: プレフィックスを入力してください。',
        'preview_complete': 'プレビュー生成完了',
        'success_renamed': '成功:',
        'partial_success': '部分成功:',
        'error': 'エラー:',
        'no_prefix_enter': 'プレフィックスを入力してください。'
    }
}


# ============================================================================
# Rename Mode - 파일 이름 변경 로직
# ============================================================================

class RenameMode:
    """파일 이름 변경 모드 핵심 로직"""
    
    def __init__(self):
        self.selected_folder: Optional[str] = None
        self.files: List[str] = []
    
    def set_folder(self, folder_path: str):
        """작업할 폴더 설정"""
        self.selected_folder = folder_path
        self._scan_files()
    
    def _scan_files(self):
        """폴더 내 파일 스캔"""
        if not self.selected_folder:
            self.files = []
            return
        
        try:
            self.files = [
                f for f in os.listdir(self.selected_folder)
                if os.path.isfile(os.path.join(self.selected_folder, f))
            ]
            self.files.sort()
        except Exception:
            self.files = []
    
    def get_file_count(self) -> int:
        """파일 수 반환"""
        return len(self.files)
    
    def generate_new_names(
        self,
        prefix: str,
        use_sequential: bool = False,
        start_number: int = 1,
        digit_padding: int = 3
    ) -> List[Tuple[str, str]]:
        """
        새로운 파일명 생성
        
        Args:
            prefix: 접두사
            use_sequential: 순차 번호 사용 여부
            start_number: 시작 번호
            digit_padding: 자릿수 패딩
        
        Returns:
            [(현재이름, 새이름), ...] 리스트
        """
        if not self.files:
            return []
        
        preview_data = []
        used_names = set()  # 충돌 방지를 위한 사용된 이름 추적
        
        for idx, file in enumerate(self.files):
            file_path = Path(file)
            stem = file_path.stem
            suffix = file_path.suffix
            
            # 기본 새 이름 생성
            if use_sequential:
                number = start_number + idx
                padded_number = str(number).zfill(digit_padding)
                new_name = f"{prefix}{padded_number}{suffix}"
            else:
                new_name = f"{prefix}{stem}{suffix}"
            
            # 충돌 처리: 이미 사용된 이름이면 증분 번호 추가
            new_name = self._resolve_collision(new_name, used_names)
            used_names.add(new_name)
            
            preview_data.append((file, new_name))
        
        return preview_data
    
    def _resolve_collision(self, base_name: str, used_names: set) -> str:
        """
        파일명 충돌 해결
        file.txt → file(1).txt → file(2).txt 형식으로 자동 증분
        """
        if base_name not in used_names:
            return base_name
        
        # 확장자 분리
        path = Path(base_name)
        stem = path.stem
        suffix = path.suffix
        
        # 증분 번호 찾기
        counter = 1
        while True:
            new_name = f"{stem}({counter}){suffix}"
            if new_name not in used_names:
                return new_name
            counter += 1
    
    def rename_files(self, rename_list: List[Tuple[str, str]]) -> Tuple[int, int]:
        """
        파일 이름 변경 실행
        
        Args:
            rename_list: [(현재이름, 새이름), ...] 리스트
        
        Returns:
            (성공 수, 실패 수) 튜플
        """
        if not self.selected_folder:
            return (0, 0)
        
        success_count = 0
        error_count = 0
        
        for current_name, new_name in rename_list:
            # 이름이 같으면 스킵
            if current_name == new_name:
                continue
            
            try:
                old_path = os.path.join(self.selected_folder, current_name)
                new_path = os.path.join(self.selected_folder, new_name)
                
                # 실제 파일 존재 확인
                if not os.path.exists(old_path):
                    error_count += 1
                    continue
                
                os.rename(old_path, new_path)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"Error renaming {current_name}: {str(e)}")
        
        return (success_count, error_count)


# ============================================================================
# 메인 애플리케이션
# ============================================================================

class SmartFileRenamer:
    """Smart File Renamer 메인 애플리케이션"""
    
    def __init__(self, root):
        self.root = root
        self.current_language = 'KR'
        self.lang = LANGUAGES[self.current_language]
        
        # 모드 관리자 (향후 확장을 위해)
        self.rename_mode = RenameMode()
        
        # UI 상태
        self.preview_data: List[Tuple[str, str]] = []
        
        # 윈도우 설정
        self.root.title(self.lang['title'])
        self.root.geometry('900x700')
        self.root.resizable(True, True)
        
        # UI 구성
        self.create_widgets()
    
    def get_text(self, key: str) -> str:
        """현재 언어에 맞는 텍스트 반환"""
        return LANGUAGES[self.current_language][key]
    
    def update_ui_text(self):
        """UI 텍스트를 현재 언어로 업데이트"""
        self.lang = LANGUAGES[self.current_language]
        self.root.title(self.lang['title'])
        self._update_all_widgets_text()
    
    def _update_all_widgets_text(self):
        """모든 위젯 텍스트 업데이트"""
        self.select_folder_btn.config(text=self.lang['select_folder'])
        self.folder_path_label.config(text=self.lang['folder_path'])
        self.file_count_label.config(text=self.lang['file_count'])
        self.prefix_label.config(text=self.lang['prefix'])
        self.sequential_check.config(text=self.lang['sequential_numbering'])
        self.start_number_label.config(text=self.lang['start_number'])
        self.digit_padding_label.config(text=self.lang['digit_padding'])
        self.preview_btn.config(text=self.lang['preview'])
        self.rename_all_btn.config(text=self.lang['rename_all'])
        self.status_label.config(text=self.lang['status'])
        
        # Treeview 컬럼 헤더
        self.preview_tree.heading('#0', text=self.lang['current_name'])
        self.preview_tree.heading('new_name', text=self.lang['new_name'])
        
        # 상태 메시지 초기화
        self.status_value.config(text=self.lang['waiting'])
    
    def create_widgets(self):
        """UI 위젯 생성"""
        # 메인 컨테이너
        main_container = ttk.Frame(self.root, padding="15")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ====================================================================
        # 1. 언어 선택 섹션
        # ====================================================================
        language_frame = ttk.LabelFrame(main_container, text="", padding="10")
        language_frame.pack(fill=tk.X, pady=(0, 15))
        
        language_inner = ttk.Frame(language_frame)
        language_inner.pack()
        
        ttk.Label(language_inner, text="Language / 言語 / 언어:").pack(side=tk.LEFT, padx=5)
        
        self.language_var = tk.StringVar(value=self.current_language)
        for lang_code, lang_name in [('KR', '한국어'), ('EN', 'English'), ('JP', '日本語')]:
            rb = ttk.Radiobutton(
                language_inner,
                text=lang_name,
                variable=self.language_var,
                value=lang_code,
                command=self.on_language_change
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # ====================================================================
        # 2. 폴더 선택 섹션
        # ====================================================================
        self.folder_section = ttk.LabelFrame(main_container, text=self.lang['select_folder'], padding="10")
        self.folder_section.pack(fill=tk.X, pady=(0, 15))
        
        # 폴더 선택 버튼
        button_row = ttk.Frame(self.folder_section)
        button_row.pack(fill=tk.X, pady=(0, 10))
        
        self.select_folder_btn = ttk.Button(
            button_row,
            text=self.lang['select_folder'],
            command=self.select_folder
        )
        self.select_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # 폴더 경로 표시
        info_row = ttk.Frame(self.folder_section)
        info_row.pack(fill=tk.X)
        
        self.folder_path_label = ttk.Label(info_row, text=self.lang['folder_path'] + ":")
        self.folder_path_label.pack(side=tk.LEFT, padx=5)
        
        self.folder_path_value = ttk.Label(
            info_row,
            text="",
            foreground="gray",
            font=('TkDefaultFont', 9)
        )
        self.folder_path_value.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 파일 수 표시
        file_count_row = ttk.Frame(self.folder_section)
        file_count_row.pack(fill=tk.X, pady=(5, 0))
        
        self.file_count_label = ttk.Label(file_count_row, text=self.lang['file_count'] + ":")
        self.file_count_label.pack(side=tk.LEFT, padx=5)
        
        self.file_count_value = ttk.Label(
            file_count_row,
            text="0",
            foreground="blue",
            font=('TkDefaultFont', 9, 'bold')
        )
        self.file_count_value.pack(side=tk.LEFT, padx=5)
        
        # ====================================================================
        # 3. 이름 변경 설정 섹션
        # ====================================================================
        self.settings_section = ttk.LabelFrame(main_container, text=self.lang['rename_settings'], padding="10")
        self.settings_section.pack(fill=tk.X, pady=(0, 15))
        
        # 접두사 입력
        prefix_row = ttk.Frame(self.settings_section)
        prefix_row.pack(fill=tk.X, pady=(0, 10))
        
        self.prefix_label = ttk.Label(prefix_row, text=self.lang['prefix'] + ":")
        self.prefix_label.pack(side=tk.LEFT, padx=5)
        
        self.prefix_entry = ttk.Entry(prefix_row, width=30)
        self.prefix_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 순차 번호 체크박스
        sequential_row = ttk.Frame(self.settings_section)
        sequential_row.pack(fill=tk.X, pady=(0, 10))
        
        self.sequential_var = tk.BooleanVar(value=False)
        self.sequential_check = ttk.Checkbutton(
            sequential_row,
            text=self.lang['sequential_numbering'],
            variable=self.sequential_var,
            command=self.on_sequential_toggle
        )
        self.sequential_check.pack(side=tk.LEFT, padx=5)
        
        # 시작 번호 및 자릿수 패딩 (순차 번호 활성화 시에만 표시)
        number_row = ttk.Frame(self.settings_section)
        number_row.pack(fill=tk.X)
        
        self.start_number_label = ttk.Label(number_row, text=self.lang['start_number'] + ":")
        self.start_number_label.pack(side=tk.LEFT, padx=5)
        
        self.start_number_entry = ttk.Entry(number_row, width=10)
        self.start_number_entry.insert(0, "1")
        self.start_number_entry.pack(side=tk.LEFT, padx=5)
        
        self.digit_padding_label = ttk.Label(number_row, text=self.lang['digit_padding'] + ":")
        self.digit_padding_label.pack(side=tk.LEFT, padx=(15, 5))
        
        self.digit_padding_entry = ttk.Entry(number_row, width=10)
        self.digit_padding_entry.insert(0, "3")
        self.digit_padding_entry.pack(side=tk.LEFT, padx=5)
        
        # 초기 상태: 순차 번호 비활성화
        self._toggle_sequential_controls(False)
        
        # ====================================================================
        # 4. 액션 버튼 섹션
        # ====================================================================
        action_frame = ttk.Frame(main_container)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.preview_btn = ttk.Button(
            action_frame,
            text=self.lang['preview'],
            command=self.generate_preview
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.rename_all_btn = ttk.Button(
            action_frame,
            text=self.lang['rename_all'],
            command=self.rename_all_files,
            state=tk.DISABLED
        )
        self.rename_all_btn.pack(side=tk.LEFT, padx=5)
        
        # ====================================================================
        # 5. 미리보기 섹션
        # ====================================================================
        self.preview_section = ttk.LabelFrame(main_container, text=self.lang['preview'], padding="10")
        self.preview_section.pack(fill=tk.BOTH, expand=True)
        
        # Treeview 및 스크롤바
        tree_frame = ttk.Frame(self.preview_section)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview_tree = ttk.Treeview(
            tree_frame,
            columns=('new_name',),
            show='tree headings',
            height=12
        )
        
        self.preview_tree.heading('#0', text=self.lang['current_name'])
        self.preview_tree.heading('new_name', text=self.lang['new_name'])
        self.preview_tree.column('#0', width=400, anchor=tk.W)
        self.preview_tree.column('new_name', width=400, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ====================================================================
        # 6. 상태 표시 섹션
        # ====================================================================
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text=self.lang['status'] + ":")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.status_value = ttk.Label(
            status_frame,
            text=self.lang['waiting'],
            foreground="gray",
            font=('TkDefaultFont', 9)
        )
        self.status_value.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def _toggle_sequential_controls(self, enabled: bool):
        """순차 번호 관련 컨트롤 활성화/비활성화"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.start_number_label.config(state=state)
        self.start_number_entry.config(state=state)
        self.digit_padding_label.config(state=state)
        self.digit_padding_entry.config(state=state)
    
    def on_sequential_toggle(self):
        """순차 번호 체크박스 토글 이벤트"""
        enabled = self.sequential_var.get()
        self._toggle_sequential_controls(enabled)
    
    def on_language_change(self):
        """언어 변경 이벤트 핸들러"""
        self.current_language = self.language_var.get()
        self.update_ui_text()
    
    def select_folder(self):
        """폴더 선택"""
        folder = filedialog.askdirectory(title=self.get_text('select_folder'))
        if folder:
            self.rename_mode.set_folder(folder)
            self.folder_path_value.config(text=folder, foreground="black")
            self._update_file_count()
            self._update_status(self.get_text('folder_selected'))
            self.clear_preview()
    
    def _update_file_count(self):
        """파일 수 업데이트"""
        count = self.rename_mode.get_file_count()
        self.file_count_value.config(text=str(count))
    
    def _update_status(self, message: str):
        """상태 메시지 업데이트"""
        self.status_value.config(text=message, foreground="black")
    
    def clear_preview(self):
        """미리보기 초기화"""
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        self.preview_data = []
        self.rename_all_btn.config(state=tk.DISABLED)
    
    def generate_preview(self):
        """미리보기 생성"""
        # 입력 검증
        if not self.rename_mode.selected_folder:
            messagebox.showwarning(
                self.get_text('title'),
                self.get_text('no_folder_selected')
            )
            self._update_status(self.get_text('warning_no_folder'))
            return
        
        file_count = self.rename_mode.get_file_count()
        if file_count == 0:
            messagebox.showwarning(
                self.get_text('title'),
                self.get_text('no_files')
            )
            self._update_status(self.get_text('warning_no_files'))
            return
        
        prefix = self.prefix_entry.get().strip()
        if not prefix:
            messagebox.showwarning(
                self.get_text('title'),
                self.get_text('no_prefix_enter')
            )
            self._update_status(self.get_text('warning_no_prefix'))
            return
        
        # 순차 번호 설정 읽기
        use_sequential = self.sequential_var.get()
        start_number = 1
        digit_padding = 3
        
        if use_sequential:
            try:
                start_number = int(self.start_number_entry.get())
                if start_number < 0:
                    start_number = 1
            except ValueError:
                start_number = 1
            
            try:
                digit_padding = int(self.digit_padding_entry.get())
                if digit_padding < 1:
                    digit_padding = 3
            except ValueError:
                digit_padding = 3
        
        # 미리보기 생성
        try:
            self.clear_preview()
            self.preview_data = self.rename_mode.generate_new_names(
                prefix=prefix,
                use_sequential=use_sequential,
                start_number=start_number,
                digit_padding=digit_padding
            )
            
            # Treeview에 표시
            for current_name, new_name in self.preview_data:
                self.preview_tree.insert('', tk.END, text=current_name, values=(new_name,))
            
            # Rename All 버튼 활성화
            self.rename_all_btn.config(state=tk.NORMAL)
            
            status_msg = f"{self.get_text('preview_complete')}: {len(self.preview_data)} {self.get_text('file_count').lower()}"
            self._update_status(status_msg)
            
        except Exception as e:
            messagebox.showerror(
                self.get_text('title'),
                f"{self.get_text('rename_error')}: {str(e)}"
            )
            self._update_status(f"{self.get_text('error')} {str(e)}")
    
    def rename_all_files(self):
        """모든 파일 이름 변경"""
        if not self.preview_data:
            return
        
        # 확인 팝업
        result = messagebox.askyesno(
            self.get_text('title'),
            self.get_text('confirm_rename')
        )
        
        if not result:
            return
        
        # 파일 이름 변경 실행
        try:
            success_count, error_count = self.rename_mode.rename_files(self.preview_data)
            
            # 결과 메시지
            if error_count == 0:
                message = f"{self.get_text('rename_success')} ({success_count} {self.get_text('files_renamed')})"
                messagebox.showinfo(self.get_text('title'), message)
                self._update_status(f"{self.get_text('success_renamed')} {success_count} {self.get_text('files_renamed')}")
            else:
                message = f"{success_count} files renamed. {error_count} errors occurred."
                messagebox.showwarning(self.get_text('title'), message)
                self._update_status(f"{self.get_text('partial_success')} {success_count} renamed, {error_count} errors")
            
            # 미리보기 초기화 및 파일 수 업데이트
            self.clear_preview()
            self.rename_mode._scan_files()
            self._update_file_count()
            self.prefix_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror(
                self.get_text('title'),
                f"{self.get_text('rename_error')}: {str(e)}"
            )
            self._update_status(f"{self.get_text('error')} {str(e)}")


# ============================================================================
# 진입점
# ============================================================================

def main():
    """메인 함수"""
    root = tk.Tk()
    app = SmartFileRenamer(root)
    root.mainloop()


if __name__ == '__main__':
    main()

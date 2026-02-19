import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from typing import List, Tuple, Optional, Set


# ============================================================================
# 다국어 지원
# ============================================================================

LANGUAGES = {
    'KR': {
        'title': 'Smart File Renamer v0.3',
        'select_folder': '폴더 선택',
        'folder_path': '선택된 폴더',
        'file_count': '파일 수',
        'file_type_filter': '파일 타입 필터',
        'images': '이미지',
        'videos': '비디오',
        'documents': '문서',
        'others': '기타',
        'rename_settings': '이름 변경 설정',
        'prefix': '접두사',
        'sequential_numbering': '순차 번호 추가',
        'start_number': '시작 번호',
        'digit_padding': '자릿수 패딩',
        'preview': '미리보기',
        'select_all': '전체 선택',
        'deselect_all': '전체 해제',
        'rename_selected': '선택된 파일 변경',
        'current_name': '현재 이름',
        'new_name': '새 이름',
        'status': '상태',
        'no_folder_selected': '폴더를 선택해주세요.',
        'no_files': '변경할 파일이 없습니다.',
        'no_file_type_selected': '파일 타입을 하나 이상 선택해주세요.',
        'no_files_selected': '변경할 파일을 하나 이상 선택해주세요.',
        'preview_generated': '미리보기 생성 완료',
        'confirm_rename': '선택된 파일 이름을 변경하시겠습니까?',
        'rename_success': '파일 이름 변경이 완료되었습니다.',
        'rename_error': '파일 이름 변경 중 오류가 발생했습니다.',
        'files_renamed': '개 파일이 변경되었습니다.',
        'waiting': '대기 중...',
        'folder_selected': '폴더가 선택되었습니다.',
        'warning_no_folder': '경고: 폴더를 선택해주세요.',
        'warning_no_files': '경고: 변경할 파일이 없습니다.',
        'warning_no_file_type': '경고: 파일 타입을 선택해주세요.',
        'warning_no_prefix': '경고: 접두사를 입력해주세요.',
        'warning_no_selection': '경고: 변경할 파일을 선택해주세요.',
        'preview_complete': '미리보기 생성 완료',
        'success_renamed': '성공:',
        'partial_success': '부분 성공:',
        'error': '오류:',
        'no_prefix_enter': '접두사를 입력해주세요.'
    },
    'EN': {
        'title': 'Smart File Renamer v0.3',
        'select_folder': 'Select Folder',
        'folder_path': 'Selected Folder',
        'file_count': 'File Count',
        'file_type_filter': 'File Type Filter',
        'images': 'Images',
        'videos': 'Videos',
        'documents': 'Documents',
        'others': 'Others',
        'rename_settings': 'Rename Settings',
        'prefix': 'Prefix',
        'sequential_numbering': 'Add Sequential Numbering',
        'start_number': 'Start Number',
        'digit_padding': 'Digit Padding',
        'preview': 'Preview',
        'select_all': 'Select All',
        'deselect_all': 'Deselect All',
        'rename_selected': 'Rename Selected',
        'current_name': 'Current Name',
        'new_name': 'New Name',
        'status': 'Status',
        'no_folder_selected': 'Please select a folder.',
        'no_files': 'No files to rename.',
        'no_file_type_selected': 'Please select at least one file type.',
        'no_files_selected': 'Please select at least one file to rename.',
        'preview_generated': 'Preview generated successfully',
        'confirm_rename': 'Do you want to rename the selected files?',
        'rename_success': 'Files renamed successfully.',
        'rename_error': 'An error occurred while renaming files.',
        'files_renamed': 'files renamed.',
        'waiting': 'Waiting...',
        'folder_selected': 'Folder selected.',
        'warning_no_folder': 'Warning: Please select a folder.',
        'warning_no_files': 'Warning: No files to rename.',
        'warning_no_file_type': 'Warning: Please select a file type.',
        'warning_no_prefix': 'Warning: Please enter a prefix.',
        'warning_no_selection': 'Warning: Please select files to rename.',
        'preview_complete': 'Preview generated',
        'success_renamed': 'Success:',
        'partial_success': 'Partial success:',
        'error': 'Error:',
        'no_prefix_enter': 'Please enter a prefix.'
    },
    'JP': {
        'title': 'Smart File Renamer v0.3',
        'select_folder': 'フォルダ選択',
        'folder_path': '選択されたフォルダ',
        'file_count': 'ファイル数',
        'file_type_filter': 'ファイルタイプフィルター',
        'images': '画像',
        'videos': '動画',
        'documents': '文書',
        'others': 'その他',
        'rename_settings': '名前変更設定',
        'prefix': 'プレフィックス',
        'sequential_numbering': '連番追加',
        'start_number': '開始番号',
        'digit_padding': '桁数パディング',
        'preview': 'プレビュー',
        'select_all': 'すべて選択',
        'deselect_all': 'すべて解除',
        'rename_selected': '選択したファイルを変更',
        'current_name': '現在の名前',
        'new_name': '新しい名前',
        'status': '状態',
        'no_folder_selected': 'フォルダを選択してください。',
        'no_files': '変更するファイルがありません。',
        'no_file_type_selected': 'ファイルタイプを1つ以上選択してください。',
        'no_files_selected': '変更するファイルを1つ以上選択してください。',
        'preview_generated': 'プレビューが生成されました',
        'confirm_rename': '選択したファイル名を変更しますか？',
        'rename_error': 'ファイル名変更中にエラーが発生しました。',
        'rename_success': 'ファイル名の変更が完了しました。',
        'files_renamed': '個のファイルが変更されました。',
        'waiting': '待機中...',
        'folder_selected': 'フォルダが選択されました。',
        'warning_no_folder': '警告: フォルダを選択してください。',
        'warning_no_files': '警告: 変更するファイルがありません。',
        'warning_no_file_type': '警告: ファイルタイプを選択してください。',
        'warning_no_prefix': '警告: プレフィックスを入力してください。',
        'warning_no_selection': '警告: 変更するファイルを選択してください。',
        'preview_complete': 'プレビュー生成完了',
        'success_renamed': '成功:',
        'partial_success': '部分成功:',
        'error': 'エラー:',
        'no_prefix_enter': 'プレフィックスを入力してください。'
    }
}


# ============================================================================
# 파일 타입 분류 유틸리티
# ============================================================================

class FileTypeClassifier:
    """파일 타입 분류기"""
    
    # 이미지 확장자
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', 
                        '.webp', '.svg', '.ico', '.heic', '.heif', '.raw', '.cr2', 
                        '.nef', '.orf', '.sr2', '.psd', '.ai', '.eps'}
    
    # 비디오 확장자
    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
                        '.m4v', '.mpg', '.mpeg', '.3gp', '.ogv', '.ts', '.mts',
                        '.m2ts', '.vob', '.asf', '.rm', '.rmvb', '.divx', '.xvid'}
    
    # 문서 확장자
    DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                           '.txt', '.rtf', '.odt', '.ods', '.odp', '.csv', '.md',
                           '.html', '.htm', '.xml', '.json', '.yaml', '.yml', '.ini',
                           '.cfg', '.conf', '.log', '.tex', '.latex'}
    
    @classmethod
    def get_file_type(cls, filename: str) -> str:
        """
        파일의 타입을 반환
        
        Args:
            filename: 파일명
            
        Returns:
            'image', 'video', 'document', 'other' 중 하나
        """
        ext = Path(filename).suffix.lower()
        
        if ext in cls.IMAGE_EXTENSIONS:
            return 'image'
        elif ext in cls.VIDEO_EXTENSIONS:
            return 'video'
        elif ext in cls.DOCUMENT_EXTENSIONS:
            return 'document'
        else:
            return 'other'
    
    @classmethod
    def filter_files_by_type(cls, files: List[str], selected_types: Set[str]) -> List[str]:
        """
        선택된 타입의 파일만 필터링
        
        Args:
            files: 파일 리스트
            selected_types: 선택된 타입 집합 {'image', 'video', 'document', 'other'}
            
        Returns:
            필터링된 파일 리스트
        """
        if not selected_types:
            return []
        
        filtered = []
        for file in files:
            file_type = cls.get_file_type(file)
            if file_type in selected_types:
                filtered.append(file)
        
        return filtered


# ============================================================================
# Rename Mode - 파일 이름 변경 로직
# ============================================================================

class RenameMode:
    """파일 이름 변경 모드 핵심 로직"""
    
    def __init__(self):
        self.selected_folder: Optional[str] = None
        self.all_files: List[str] = []  # 모든 파일 (필터 전)
        self.filtered_files: List[str] = []  # 필터링된 파일
    
    def set_folder(self, folder_path: str):
        """작업할 폴더 설정"""
        self.selected_folder = folder_path
        self._scan_files()
    
    def _scan_files(self):
        """Step 1: 폴더 내 모든 파일 수집"""
        if not self.selected_folder:
            self.all_files = []
            self.filtered_files = []
            return
        
        try:
            self.all_files = [
                f for f in os.listdir(self.selected_folder)
                if os.path.isfile(os.path.join(self.selected_folder, f))
            ]
            self.all_files.sort()
            self.filtered_files = []
        except Exception:
            self.all_files = []
            self.filtered_files = []
    
    def apply_file_type_filter(self, selected_types: Set[str]):
        """Step 2: 파일 타입 필터 적용"""
        if not selected_types:
            self.filtered_files = []
            return
        
        self.filtered_files = FileTypeClassifier.filter_files_by_type(
            self.all_files, selected_types
        )
    
    def get_file_count(self) -> int:
        """필터링된 파일 수 반환"""
        return len(self.filtered_files)
    
    def generate_new_names(
        self,
        prefix: str,
        use_sequential: bool = False,
        start_number: int = 1,
        digit_padding: int = 3
    ) -> List[Tuple[str, str]]:
        """
        Step 3: 새로운 파일명 생성
        Step 4: 충돌 방지 처리
        
        Args:
            prefix: 접두사
            use_sequential: 순차 번호 사용 여부
            start_number: 시작 번호
            digit_padding: 자릿수 패딩
        
        Returns:
            [(현재이름, 새이름), ...] 리스트
        """
        if not self.filtered_files:
            return []
        
        preview_data = []
        used_names = set()  # 충돌 방지를 위한 사용된 이름 추적
        
        for idx, file in enumerate(self.filtered_files):
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
        Step 6: 파일 이름 변경 실행
        
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
        
        # 모드 관리자
        self.rename_mode = RenameMode()
        
        # UI 상태
        self.preview_data: List[Tuple[str, str]] = []
        self.file_checkboxes: dict = {}  # {item_id: BooleanVar}
        self.item_id_to_index: dict = {}  # {item_id: index} - preview_data 인덱스 매핑
        
        # 파일 타입 필터 변수
        self.image_var = tk.BooleanVar(value=False)
        self.video_var = tk.BooleanVar(value=False)
        self.document_var = tk.BooleanVar(value=False)
        self.other_var = tk.BooleanVar(value=False)
        
        # 윈도우 설정
        self.root.title(self.lang['title'])
        self.root.geometry('950x750')
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
        self.file_type_filter_label.config(text=self.lang['file_type_filter'])
        self.image_check.config(text=self.lang['images'])
        self.video_check.config(text=self.lang['videos'])
        self.document_check.config(text=self.lang['documents'])
        self.other_check.config(text=self.lang['others'])
        self.prefix_label.config(text=self.lang['prefix'])
        self.sequential_check.config(text=self.lang['sequential_numbering'])
        self.start_number_label.config(text=self.lang['start_number'])
        self.digit_padding_label.config(text=self.lang['digit_padding'])
        self.preview_btn.config(text=self.lang['preview'])
        self.select_all_btn.config(text=self.lang['select_all'])
        self.deselect_all_btn.config(text=self.lang['deselect_all'])
        self.rename_selected_btn.config(text=self.lang['rename_selected'])
        self.status_label.config(text=self.lang['status'])
        
        # Treeview 컬럼 헤더
        self.preview_tree.heading('selected', text='✓')
        self.preview_tree.heading('current_name', text=self.lang['current_name'])
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
        # 3. 파일 타입 필터 섹션
        # ====================================================================
        self.file_type_section = ttk.LabelFrame(main_container, text=self.lang['file_type_filter'], padding="10")
        self.file_type_section.pack(fill=tk.X, pady=(0, 15))
        
        filter_row = ttk.Frame(self.file_type_section)
        filter_row.pack(fill=tk.X)
        
        self.file_type_filter_label = ttk.Label(filter_row, text=self.lang['file_type_filter'] + ":")
        self.file_type_filter_label.pack(side=tk.LEFT, padx=5)
        
        self.image_check = ttk.Checkbutton(
            filter_row,
            text=self.lang['images'],
            variable=self.image_var,
            command=self.on_file_type_filter_change
        )
        self.image_check.pack(side=tk.LEFT, padx=10)
        
        self.video_check = ttk.Checkbutton(
            filter_row,
            text=self.lang['videos'],
            variable=self.video_var,
            command=self.on_file_type_filter_change
        )
        self.video_check.pack(side=tk.LEFT, padx=10)
        
        self.document_check = ttk.Checkbutton(
            filter_row,
            text=self.lang['documents'],
            variable=self.document_var,
            command=self.on_file_type_filter_change
        )
        self.document_check.pack(side=tk.LEFT, padx=10)
        
        self.other_check = ttk.Checkbutton(
            filter_row,
            text=self.lang['others'],
            variable=self.other_var,
            command=self.on_file_type_filter_change
        )
        self.other_check.pack(side=tk.LEFT, padx=10)
        
        # ====================================================================
        # 4. 이름 변경 설정 섹션
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
        # 5. 액션 버튼 섹션
        # ====================================================================
        action_frame = ttk.Frame(main_container)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.preview_btn = ttk.Button(
            action_frame,
            text=self.lang['preview'],
            command=self.generate_preview
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.rename_selected_btn = ttk.Button(
            action_frame,
            text=self.lang['rename_selected'],
            command=self.rename_selected_files,
            state=tk.DISABLED
        )
        self.rename_selected_btn.pack(side=tk.LEFT, padx=5)
        
        # ====================================================================
        # 6. 미리보기 섹션
        # ====================================================================
        self.preview_section = ttk.LabelFrame(main_container, text=self.lang['preview'], padding="10")
        self.preview_section.pack(fill=tk.BOTH, expand=True)
        
        # 선택 버튼 행
        select_buttons_row = ttk.Frame(self.preview_section)
        select_buttons_row.pack(fill=tk.X, pady=(0, 10))
        
        self.select_all_btn = ttk.Button(
            select_buttons_row,
            text=self.lang['select_all'],
            command=self.select_all_files
        )
        self.select_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.deselect_all_btn = ttk.Button(
            select_buttons_row,
            text=self.lang['deselect_all'],
            command=self.deselect_all_files
        )
        self.deselect_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview 및 스크롤바
        tree_frame = ttk.Frame(self.preview_section)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # 체크박스를 위한 컬럼 추가
        self.preview_tree = ttk.Treeview(
            tree_frame,
            columns=('selected', 'current_name', 'new_name'),
            show='headings',
            height=12
        )
        
        self.preview_tree.heading('selected', text='✓')
        self.preview_tree.heading('current_name', text=self.lang['current_name'])
        self.preview_tree.heading('new_name', text=self.lang['new_name'])
        self.preview_tree.column('selected', width=40, anchor=tk.CENTER)
        self.preview_tree.column('current_name', width=300, anchor=tk.W)
        self.preview_tree.column('new_name', width=300, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        self.preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 체크박스 클릭 이벤트 바인딩
        self.preview_tree.bind('<Button-1>', self.on_tree_click)
        
        # ====================================================================
        # 7. 상태 표시 섹션
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
    
    def on_file_type_filter_change(self):
        """파일 타입 필터 변경 이벤트 핸들러"""
        if self.rename_mode.selected_folder:
            self._update_file_count()
            self.clear_preview()
    
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
        """필터링된 파일 수 업데이트"""
        # 파일 타입 필터 적용
        selected_types = self._get_selected_file_types()
        self.rename_mode.apply_file_type_filter(selected_types)
        
        count = self.rename_mode.get_file_count()
        self.file_count_value.config(text=str(count))
    
    def _get_selected_file_types(self) -> Set[str]:
        """선택된 파일 타입 집합 반환"""
        selected = set()
        if self.image_var.get():
            selected.add('image')
        if self.video_var.get():
            selected.add('video')
        if self.document_var.get():
            selected.add('document')
        if self.other_var.get():
            selected.add('other')
        return selected
    
    def _update_status(self, message: str):
        """상태 메시지 업데이트"""
        self.status_value.config(text=message, foreground="black")
    
    def clear_preview(self):
        """미리보기 초기화"""
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        self.preview_data = []
        self.file_checkboxes.clear()
        self.item_id_to_index.clear()
        self.rename_selected_btn.config(state=tk.DISABLED)
    
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
        
        # 파일 타입 필터 검증
        selected_types = self._get_selected_file_types()
        if not selected_types:
            messagebox.showwarning(
                self.get_text('title'),
                self.get_text('no_file_type_selected')
            )
            self._update_status(self.get_text('warning_no_file_type'))
            return
        
        # 파일 타입 필터 적용
        self.rename_mode.apply_file_type_filter(selected_types)
        
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
            
            # Treeview에 표시 (체크박스 포함)
            self.item_id_to_index.clear()
            for idx, (current_name, new_name) in enumerate(self.preview_data):
                # 체크박스 변수 생성
                var = tk.BooleanVar(value=True)  # 기본값: 선택됨
                item_id = self.preview_tree.insert(
                    '', tk.END,
                    values=('☑', current_name, new_name)
                )
                self.file_checkboxes[item_id] = var
                self.item_id_to_index[item_id] = idx
            
            # Rename Selected 버튼 활성화
            self.rename_selected_btn.config(state=tk.NORMAL)
            
            status_msg = f"{self.get_text('preview_complete')}: {len(self.preview_data)} {self.get_text('file_count').lower()}"
            self._update_status(status_msg)
            
        except Exception as e:
            messagebox.showerror(
                self.get_text('title'),
                f"{self.get_text('rename_error')}: {str(e)}"
            )
            self._update_status(f"{self.get_text('error')} {str(e)}")
    
    def on_tree_click(self, event):
        """Treeview 클릭 이벤트 - 체크박스 토글"""
        item = self.preview_tree.identify_row(event.y)
        if not item:
            return
        
        region = self.preview_tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        # 첫 번째 컬럼('selected') 클릭인지 확인
        is_first_column = False
        
        # 방법 1: identify_column이 '#1'을 반환하는지 확인
        # identify_column은 x 좌표만 받습니다
        column = self.preview_tree.identify_column(event.x)
        if column == '#1':
            is_first_column = True
        else:
            # 방법 2: 첫 번째 컬럼의 실제 bbox 확인
            try:
                bbox = self.preview_tree.bbox(item, '#1')
                if bbox:
                    col_x, col_y, col_w, col_h = bbox
                    # 클릭한 x 좌표가 첫 번째 컬럼 범위 내인지 확인
                    if col_x <= event.x <= col_x + col_w:
                        is_first_column = True
            except:
                # 방법 3: 첫 번째 컬럼의 너비(40px)로 대략 확인
                # Treeview의 왼쪽 여백은 보통 0이지만, 스크롤바 등 고려 필요
                # 더 정확하게는 첫 번째 컬럼의 실제 너비를 가져옴
                try:
                    first_col_width = int(self.preview_tree.column('#1', 'width'))
                    if event.x <= first_col_width + 5:  # 여유값 5px
                        is_first_column = True
                except:
                    pass
        
        if is_first_column:
            var = self.file_checkboxes.get(item)
            if var:
                # 체크 상태 토글
                new_value = not var.get()
                var.set(new_value)
                self._update_checkbox_display(item)
                return 'break'  # 기본 선택 동작 방지
    
    def _update_checkbox_display(self, item_id):
        """체크박스 표시 업데이트"""
        var = self.file_checkboxes.get(item_id)
        if var:
            checkmark = '☑' if var.get() else '☐'
            current_values = list(self.preview_tree.item(item_id, 'values'))
            if len(current_values) >= 2:
                current_values[0] = checkmark
                self.preview_tree.item(item_id, values=tuple(current_values))
    
    def select_all_files(self):
        """모든 파일 선택"""
        for item_id, var in self.file_checkboxes.items():
            var.set(True)
            self._update_checkbox_display(item_id)
    
    def deselect_all_files(self):
        """모든 파일 선택 해제"""
        for item_id, var in self.file_checkboxes.items():
            var.set(False)
            self._update_checkbox_display(item_id)
    
    def rename_selected_files(self):
        """선택된 파일만 이름 변경"""
        if not self.preview_data:
            return
        
        # 선택된 파일만 필터링
        selected_files = []
        for item_id, var in self.file_checkboxes.items():
            if var and var.get():
                idx = self.item_id_to_index.get(item_id)
                if idx is not None and idx < len(self.preview_data):
                    current_name, new_name = self.preview_data[idx]
                    selected_files.append((current_name, new_name))
        
        if not selected_files:
            messagebox.showwarning(
                self.get_text('title'),
                self.get_text('no_files_selected')
            )
            self._update_status(self.get_text('warning_no_selection'))
            return
        
        # 확인 팝업
        result = messagebox.askyesno(
            self.get_text('title'),
            f"{self.get_text('confirm_rename')} ({len(selected_files)} {self.get_text('file_count').lower()})"
        )
        
        if not result:
            return
        
        # 파일 이름 변경 실행
        try:
            success_count, error_count = self.rename_mode.rename_files(selected_files)
            
            # 결과 메시지
            if error_count == 0:
                message = f"{self.get_text('rename_success')} ({success_count} {self.get_text('files_renamed')})"
                messagebox.showinfo(self.get_text('title'), message)
                self._update_status(f"{self.get_text('success_renamed')} {success_count} {self.get_text('files_renamed')}")
            else:
                message = f"{success_count} {self.get_text('files_renamed')} {error_count} errors occurred."
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

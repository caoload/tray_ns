import ctypes, sys, time, re, os, asyncio, pyperclip, subprocess
from ctypes import wintypes, c_long
from ctypes import wintypes, WINFUNCTYPE, c_uint, c_int, Structure, POINTER
from ctypes import WINFUNCTYPE, POINTER, wintypes
from ctypes import wintypes
from sortedcontainers import SortedDict  # BST tối ưu tra cứu thông điệp
import threading, win32clipboard, win32con
from sortedcontainers import SortedDict
from ctypes.wintypes import WORD, DWORD, BOOL, HHOOK, MSG, LPWSTR, WCHAR, WPARAM, LPARAM, LONG, HMODULE, LPCWSTR, HINSTANCE, HWND
from ctypes import c_short, c_char, c_uint8, c_int32, c_int, c_uint, c_uint32, c_long, Structure, CFUNCTYPE, POINTER
import pyperclip, inspect, textwrap
import asyncio, threading, subprocess, concurrent
from markdownify import markdownify

from line_remove import LineFilter, text_to_list

# bạn hướng dẫn về "handle   left click double click speed" trong khoảng time <0.8 sẽ thế nào bạn hướng dẫn nhé. 


# Ở đầu file:
IS_ADMIN = "--elevated" in sys.argv
SHOW_CMD_AFTER_ADMIN = None
# if IS_ADMIN and SHOW_CMD_AFTER_ADMIN is None:
#     response = ctypes.windll.user32.MessageBoxW(
#         None, "Bạn muốn chạy lệnh Python với CMD hay ẩn CMD?\nYES = CMD | NO = ẩn",
#         "Chọn hiển thị CMD", 0x04 | 0x40)
#     SHOW_CMD_AFTER_ADMIN = (response == 6)




BASEDIR, current_file = os.path.dirname(f"{__file__}"), rf"{__file__}"
# file_input_dir = fr"{basedir}/____.txt"
ICONHEART = fr"{BASEDIR}/heart_icon_user.ico"
ICONHEART_ADM = fr"{BASEDIR}/heart_icon_adm.ico"
PYTHON_W = sys.executable.replace("python.exe", "pythonw.exe")
PYTHON = sys.executable.replace("pythonw.exe", "python.exe")

USER_FOLDER = os.environ.get('USERPROFILE')
VSCODE_PATH = os.path.join(os.environ.get('USERPROFILE'), "AppData", "Local", "Programs", "Microsoft VS Code", "Code.exe")

SET_TEMP_PATH = fr"d:\______PY_PROJECTS\_TRAY__ICON\Tools_SHMG"



# Khởi tạo logger
from daudat import get_logger
import logging
logger = get_logger( name=__name__, level=logging.DEBUG)
# Tải thư viện gốc của Windows, # Utility for creating menu
windll = ctypes.LibraryLoader(ctypes.WinDLL)
user32 = ctypes.WinDLL('user32', use_last_error = True)

shell32 = ctypes.WinDLL('shell32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

# Định nghĩa các kiểu và hàm cơ bản

is_64bit = sys.maxsize > 2**32
LRESULT = LPARAM = ctypes.c_int64 if is_64bit else ctypes.c_long
WPARAM = ctypes.c_uint64 if is_64bit else ctypes.c_uint

HCURSOR = ctypes.c_void_p
HICON = ctypes.c_void_p
HBRUSH = ctypes.c_void_p
HGDIOBJ = ctypes.c_void_p
WM_QUIT = 0x0012
# Hủy cửa sổ
DestroyWindow = windll.user32.DestroyWindow
DestroyWindow.argtypes = (wintypes.HWND,)
DestroyWindow.restype = wintypes.BOOL

# user32.DefWindowProcW.argtypes = [wintypes.HWND, c_uint, WPARAM, LPARAM]																																			# Định nghĩa các kiểu tham số của hàm DefWindowProcW
# user32.DefWindowProcW.restype = LRESULT																																			# Định nghĩa kiểu trả về của hàm DefWindowProcW

#module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "E:\SHMG_Library"))
module_shmg = r"D:\SHMG_Library\__Lib_Include"
if module_shmg not in sys.path: sys.path.append(module_shmg)
import Constants_w_api as hm           # import Constants_w_api


# Kiểu callback cho WNDPROC

TPM_VCENTERALIGN = 0x0010
# Thêm các hằng số message cần thiết
WM_NULL = 0x0000
WM_COMMAND = 0x0111
WM_INITMENUPOPUP = 0x0117
WM_MENUSELECT = 0x011F
WM_ENTERMENULOOP = 0x0211
WM_EXITMENULOOP = 0x0212
WM_CONTEXTMENU = 0x007B



# WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

WM_TASKBARCREATED = user32.RegisterWindowMessageW("TaskbarCreated")

WM_NULL = 0
WS_EX_LAYERED = 0x00080000
WS_OVERLAPPED = 0x00000000
WS_CAPTION = 0x00C00000
WS_MAXIMIZEBOX = 0x00010000
WS_MINIMIZEBOX = 0x00020000
WS_THICKFRAME = 0x00040000
WS_SYSMENU = 0x00080000
SW_RESTORE = 9


# Constants for tray icon
NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002
WM_TRAYICON = 0x0400  # Custom Windows message for tray icon
NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004
TPM_LEFTALIGN = 0x0000
TPM_RETURNCMD = 0x0100
MF_STRING = 0x0000
MF_POPUP = 0x0010
WM_USER = 0x0400



S_DWEXSTYLE = wintypes.DWORD(WS_SYSMENU | 0x00000008 | 0x00000080)
S_DWSTYLE = (WS_EX_LAYERED | WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU |
                       WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX)

# Định nghĩa TrackMouseEvent
class TRACKMOUSEEVENT(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("hwndTrack", wintypes.HWND),
        ("dwHoverTime", wintypes.DWORD),
    ]

# Hàm đăng ký theo dõi chuột bằng TrackMouseEvent
def enable_mouse_tracking(hwnd, flags):
    tme = TRACKMOUSEEVENT()
    tme.cbSize = ctypes.sizeof(TRACKMOUSEEVENT)
    tme.dwFlags = flags
    tme.hwndTrack = hwnd
    tme.dwHoverTime = 100  # 100ms để nhận WM_MOUSEHOVER
    result = ctypes.windll.user32.TrackMouseEvent(ctypes.byref(tme))
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())


# Định nghĩa các kiểu cơ bản từ ctypes
# WndProcType = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, ctypes.c_int64)

from ctypes import WINFUNCTYPE, c_int, c_void_p, c_uint
# WNDPROC = WINFUNCTYPE(c_long, c_void_p, c_int, c_void_p, c_void_p)
WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, ctypes.c_int64)



# WNDCLASS structure
class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ('style',             ctypes.c_uint),
        ('lpfnWndProc',       WNDPROC),  # Sửa thành WndProcType
        ('cbClsExtra',        ctypes.c_int),
        ('cbWndExtra',        ctypes.c_int),
        ('hInstance',         ctypes.c_void_p),
        ('hIcon',             ctypes.c_void_p),
        ('hCursor',           ctypes.c_void_p),
        ('hbrBackground',     ctypes.c_void_p),
        ('lpszMenuName',      ctypes.c_wchar_p),
        ('lpszClassName',     ctypes.c_wchar_p),
    ]

TPM_NONOTIFY = 0x0080
TPM_BOTTOMALIGN = 0x0020
TPM_RIGHTALIGN = 0x0080
TPM_VERTICAL = 0x0040
WM_DESTROY = 0x0002
WM_LBUTTONDOWN = 0x0201
WS_OVERLAPPEDWINDOW = (WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU |
                       WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX)

CW_USEDEFAULT = 0x80000000  # Giá trị: -2147483648 nếu là số signed (có dấu)
SW_HIDE = 0

RGB = wintypes.RGB
def RGB(r, g, b): return r | (g << 8) | (b << 16)



class WindowsPathConverter:
    def __init__(self):
        # Khai báo các hàm Windows API
        # fsutil 8dot3name set 0
        self._GetLongPathNameW = ctypes.windll.kernel32.GetLongPathNameW
        self._GetLongPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        self._GetLongPathNameW.restype = wintypes.DWORD

        self._GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
        self._GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        self._GetShortPathNameW.restype = wintypes.DWORD

    def get_long_path_name(self, short_path, buffer_size=256):
        """
        :param buffer_size: Kích thước buffer (mặc định 256) # Có thể điều chỉnh kích thước nếu cần
        """
        output_buffer = ctypes.create_unicode_buffer(buffer_size)
        result = self._GetLongPathNameW(short_path, output_buffer, buffer_size)

        if result == 0: raise ctypes.WinError()
        return output_buffer.value

    def get_short_path_name(self, long_path, buffer_size=256):
        """
        :param buffer_size: Kích thước buffer (mặc định 256)  # Có thể điều chỉnh kích thước nếu cần
        """
        output_buffer = ctypes.create_unicode_buffer(buffer_size)
        result = self._GetShortPathNameW(long_path, output_buffer, buffer_size)
        if result == 0:
            error_code = ctypes.GetLastError()
            raise ctypes.WinError(error_code)
        return output_buffer.value



def get_clipboard_file_paths(get_full_path=True, remove_file_type=False):
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
            paths = win32clipboard.GetClipboardData(win32con.CF_HDROP)
            if len(paths) == 1:
                if get_full_path: return paths[0]  # Return single full path
                else:
                    file_name = os.path.basename(paths[0])
                    if remove_file_type: return os.path.splitext(file_name)[0]
                    else: return file_name  # Return single filename
            else:  # len(paths) > 1
                result = []
                for path in paths:
                    if get_full_path: result.append(path)
                    else:
                        file_name = os.path.basename(path)
                        if remove_file_type: result.append(os.path.splitext(file_name)[0])
                        else: result.append(file_name)
                return '\n'.join(result)
    finally:
        win32clipboard.CloseClipboard()
    return None

def show_auto_close_messagebox(mess="Test auto close box", on_close_callback=None, callback_args=None, width=400, height=200, max_line_length=50, autoclose_time=1.5):
    """Hiển thị hộp thoại thông báo ở giữa màn hình, tự động xuống dòng và tự động đóng sau 1.5 giây."""

    auto_closed = [False]

    # Định dạng lại nội dung để tự động xuống dòng
    formatted_message = "\n".join(textwrap.wrap(mess, max_line_length))

    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    def center_window(hwnd):
        """Đặt hộp thoại vào giữa màn hình"""
        # Lấy kích thước màn hình
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)  # SM_CXSCREEN
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)  # SM_CYSCREEN

        # Tính toán vị trí để căn giữa
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        # Di chuyển cửa sổ đến vị trí giữa màn hình và đặt kích thước
        ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height, True)

    def find_and_center_messagebox():
        """Tìm và căn giữa hộp thoại"""
        hwnd = ctypes.windll.user32.FindWindowW("#32770", mess)
        if hwnd:
            center_window(hwnd)

    def close_messagebox():
        """Tìm và đóng hộp thoại"""
        hwnd = ctypes.windll.user32.FindWindowW("#32770", mess)
        if hwnd:
            auto_closed[0] = True
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE

    # Thiết lập timer để điều chỉnh vị trí và kích thước hộp thoại
    center_timer = threading.Timer(0.05, find_and_center_messagebox)
    center_timer.start()

    # Thiết lập timer để tự động đóng hộp thoại
    close_timer = threading.Timer(autoclose_time, close_messagebox)
    close_timer.start()

    # Hiển thị hộp thoại với nội dung đã được định dạng
    response = ctypes.windll.user32.MessageBoxW(
        None,
        formatted_message,
        mess,
        hm.MB_OK | hm.MB_SYSTEMMODAL | hm.MB_TOPMOST
    )

    # Hủy các timer
    center_timer.cancel()
    close_timer.cancel()

    # Xử lý callback n ếu có
    if on_close_callback:
        status = "AUTO_CLOSED" if auto_closed[0] else "CLICKED_OK"
        if callback_args:
            on_close_callback(status, *callback_args)
        else:
            on_close_callback(status)

def handle_close(status, path=None):
    """Xử lý sự kiện đóng hộp thoại."""
    if status == "CLICKED_OK":
        print(f"Người dùng đã click OK")
    elif status == "AUTO_CLOSED":
        print("Cửa sổ đã tự động đóng sau 1.5 giây")







# show_auto_close_messagebox("RUN WITH NO ADM")  # no callback
# exit(f'++++++++++++++++++++++++++++++++++')

class clipboard_shmg:
    def __init__(self, align=None):
        self.align = align or []

    # ----------- 📋 Clipboard File Path -----------
    @staticmethod
    def read_get_file_paths(get_full_path=True, remove_file_type=False):
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
                paths = win32clipboard.GetClipboardData(win32con.CF_HDROP)
                if len(paths) == 1:
                    if get_full_path:
                        return paths[0]
                    else:
                        file_name = os.path.basename(paths[0])
                        return os.path.splitext(file_name)[0] if remove_file_type else file_name
                else:
                    result = []
                    for path in paths:
                        if get_full_path:
                            result.append(path)
                        else:
                            file_name = os.path.basename(path)
                            result.append(os.path.splitext(file_name)[0] if remove_file_type else file_name)
                    return '\n'.join(result)
        finally:
            win32clipboard.CloseClipboard()
        return None

    @staticmethod
    def get_file_paths(get_full_path=True, remove_file_type=False):
        pyperclip.copy(cb.read_get_file_paths(get_full_path, remove_file_type))

    def html_2_markdown(data):
        # pip install markdownify
        # clip = pyperclip.paste()
        from markdownify import markdownify
        markdown = markdownify(data, heading_style="ATX")
        pyperclip.copy(markdown)
        # let m = $x('//*[@id="root"]/div/div/div[2]')[0];copy(m.outerHTML);
        # let m = $x('//html/body/div[1]/div/div[1]/div[2]')[0];copy(m.outerHTML);

    # ----------- 🌐 Clipboard HTML -----------
    @staticmethod
    def get_html(getdata=0):
        # show_auto_close_messagebox(f"get_html -> {getdata}")  # no callback
        win32clipboard.OpenClipboard()
        try:
            cf_html = win32clipboard.RegisterClipboardFormat("HTML Format")
            if win32clipboard.IsClipboardFormatAvailable(cf_html):
                html_data = win32clipboard.GetClipboardData(cf_html)
                if isinstance(html_data, bytes):
                    try:
                        html_data = html_data.decode('utf-8')
                    except UnicodeDecodeError:
                        html_data = html_data.decode('latin-1')
                # show_auto_close_messagebox(f"_convert_html_2_markdown -> {len(html_data)}")  # no callback
                if getdata:
                    # show_auto_close_messagebox(f"_convert_html_2_markdown -> {html_data}")  # no callback
                    return html_data
                return clipboard_shmg._extract_html_fragment(html_data)
            return None
        finally:
            win32clipboard.CloseClipboard()

    @staticmethod
    def _convert_html_2_markdown():
        datacheck = clipboard_shmg.get_html(getdata=1)
        print(f"_convert_html_2_markdown -> {type(datacheck)} -> len -> {len(datacheck)} -> len -> {datacheck}", flush=True)
        if re.search(r"\bStartFragment\b\:\d+", datacheck, re.I | re.M) and re.search(r"\bEndFragment\b\:\d+", datacheck, re.I | re.M):
            show_auto_close_messagebox("data converted -> ")  # no callback
            clipboard_shmg.html_2_markdown(datacheck)

    @staticmethod
    def _extract_html_fragment(data):
        """Ưu tiên lấy fragment HTML từ dữ liệu clipboard"""
        start = re.search(r'StartFragment:(\d+)', data)
        end = re.search(r'EndFragment:(\d+)', data)
        if start and end:
            return data[int(start.group(1)):int(end.group(1))]

        start = re.search(r'StartHTML:(\d+)', data)
        end = re.search(r'EndHTML:(\d+)', data)
        if start and end:
            return data[int(start.group(1)):int(end.group(1))]

        return data

    # ----------- 📄 Clipboard Table -> Markdown -----------
    def clipboard_table_to_markdown(self):
        raw_text = pyperclip.paste()
        headers, data = self.parse_raw_text(raw_text)
        markdown = self.create_table(headers, data)
        pyperclip.copy(markdown)
        return markdown

    @staticmethod
    def parse_raw_text(raw_text):
        lines = raw_text.strip().splitlines()
        if not lines: raise ValueError("Empty input text")
        headers = lines[0].split("\t")
        expected_cols = len(headers)
        data = []
        for line in lines[1:]:
            cols = line.split("\t")
            if len(cols) < expected_cols: cols += [""] * (expected_cols - len(cols))
            data.append(cols)
        return headers, data

    def create_table(self, headers, data):
        if not self.align: self.align = ['left'] * len(headers)
        for row in data:
            if len(row) < len(headers): row += [""] * (len(headers) - len(row))
        col_widths = [max(len(str(headers[i])), max(len(str(row[i])) for row in data)) for i in range(len(headers))]
        header_cells = [f" {headers[i]:<{col_widths[i]}} " for i in range(len(headers))]
        markdown = "|" + "|".join(header_cells) + "|\n"
        align_chars = {'left': ':--', 'center': ':-:', 'right': '--:'}
        separator = [f"{align_chars[self.align[i]]:<{col_widths[i]+2}}" for i in range(len(headers))]
        markdown += "|" + "|".join(separator) + "|\n"
        for row in data:
            cells = [f" {row[i]:<{col_widths[i]}} " for i in range(len(headers))]
            markdown += "|" + "|".join(cells) + "|\n"
        print(f"> > > {markdown} < < < ", flush=True)
        return markdown

    @staticmethod
    def convert_html_to_markdown(htmldata):
        # print(f"> > > {htmldata} < < < ", flush=True)
        # return pyperclip.copy(htmldata)

        try:
            markdown = markdownify(htmldata, heading_style="ATX")
            print(f"> > > {markdown} < < < ", flush=True)
            # markdown = re.sub(pattern=r"```[\n]\s*(?=(?:(python|cmd|powershell|c|json|php|bash)\b\s+(?:Copy code)?))", repl="```\1", string=markdown, count=0, flags=re.I | re.M)
            markdown = re.sub(pattern=r"```\n\s*(?=(?:python|cmd|powershell|r|c|json|php|bash|css|javascript|asm|mermaid)\s*$)", repl="```", string=markdown, count=0, flags=re.I | re.M)
            markdown = re.sub(pattern=r"(?![\r\n])\s+(?=```)", repl="", string=markdown, count=0, flags=re.I | re.M)
            print(f"> > > {markdown} < < < ", flush=True)
            
            pyperclip.copy(markdown)
        except Exception as e:
            logger.error(f"❌ error from convert_html_to_markdown {e}", exc_info=e)



    def html_2_markdown(self):
        # pip install markdownify
        clip = pyperclip.paste()
        from markdownify import markdownify
        markdown = markdownify(clip, heading_style="ATX")
        pyperclip.copy(markdown)
        # let m = $x('//*[@id="root"]/div/div/div[2]')[0];copy(m.outerHTML);
        # let m = $x('//html/body/div[1]/div/div[1]/div[2]')[0];copy(m.outerHTML);

    @staticmethod
    def html_to_markd():
        cliphtml= cb.get_clipboard_html()
        if cliphtml:
            cb.convert_html_to_markdown(cliphtml)
            show_auto_close_messagebox("not match html to convert", autoclose_time=0.8)

    @staticmethod
    def extract_html_from_clipboard_data(data):
        """
        Trích xuất nội dung HTML từ dữ liệu clipboard, ưu tiên sử dụng Fragment
        """
        # Ưu tiên tìm kiếm StartFragment và EndFragment trước
        start = re.search(r'StartFragment:(\d+)', data)
        end = re.search(r'EndFragment:(\d+)', data)

        if start and end:
            start_index = int(start.group(1))
            end_index = int(end.group(1))
            return data[start_index:end_index]

        # Nếu không tìm thấy Fragment, thử dùng HTML đầy đủ
        start = re.search(r'StartHTML:(\d+)', data)
        end = re.search(r'EndHTML:(\d+)', data)

        if start and end:
            start_index = int(start.group(1))
            end_index = int(end.group(1))
            return data[start_index:end_index]

        # Nếu không thể phân tích theo cả hai cách, trả về toàn bộ dữ liệu
        return data

    @staticmethod
    def get_clipboard_html():
        win32clipboard.OpenClipboard()
        try:
            # Đăng ký định dạng HTML
            cf_html = win32clipboard.RegisterClipboardFormat("HTML Format")
            if win32clipboard.IsClipboardFormatAvailable(cf_html):
                html_data = win32clipboard.GetClipboardData(cf_html)
                # Chuyển đổi bytes thành string
                if isinstance(html_data, bytes):
                    try:
                        html_data = html_data.decode('utf-8')
                    except UnicodeDecodeError:
                        html_data = html_data.decode('latin-1')
                # print(f"> > > {html_data} < < < ", flush=True)
                # Trích xuất nội dung HTML ưu tiên Fragment
                html_content = cb.extract_html_from_clipboard_data(html_data)
                return html_content
            else:
                return None
        finally:
            win32clipboard.CloseClipboard()

cb = clipboard_shmg()
line_filter  = LineFilter()


def remove_line_duplicate():
    raw_text = pyperclip.paste()
    raw_text = text_to_list(raw_text, remove_duplicates=True, keep_empty='none')
    # print(f"> > > {raw_text} < < < ", flush=True)
    cleaned_lines = [line.rstrip('\r') for line in raw_text]
    result = '\n'.join(cleaned_lines)
    # line_filter.set_keep_empty('none').set_keep_whitespace(False).set_ignore_case(False)
    pyperclip.copy(result)


def restart_with_admin_rights():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
        else:
            python_exe = sys.executable
            script_path = os.path.abspath(sys.argv[0])
            params = ' '.join(f'"{arg}"' for arg in sys.argv[1:])
            script_dir = os.path.dirname(script_path)

            # 👉 Hỏi người dùng có muốn hiện CMD không
            response = ctypes.windll.user32.MessageBoxW(
                None, "Bạn muốn chạy script với cửa sổ CMD (hiện) hay ẩn hoàn toàn?",
                "Chọn kiểu hiển thị CMD", 0x04 | 0x40 )      # MB_YESNO | MB_ICONQUESTION 
            show_cmd = (response == 6)  # YES = hiện CMD

            nShowCmd = 1 if show_cmd else 0  # 👈 chính là chỗ này

            command = f'/k cd /d "{script_dir}" && "{python_exe}" "{script_path}" {params} --elevated'

            ctypes.windll.shell32.ShellExecuteW( None, "runas", "cmd.exe", command, None,
                nShowCmd  # 👈 dùng biến này để điều khiển hiển thị
            )
            sys.exit()
            return False
    except Exception as e:
        print(f"Lỗi khi khởi động lại với quyền admin: {e}")
        return False







# 1. Decorator toàn cục: `@register_message`
def register_message(msg):
    """
    Decorator để đăng ký thông điệp cho các handler.
    """
    def decorator(func):
        func._message = msg  # Đánh dấu hàm với thông điệp
        return func
    return decorator
# 2. Lớp cơ bản (BaseHandler)
class BaseHandler:
    """
    Lớp cơ sở cho handler, quản lý ánh xạ thông điệp (message map).
    """
    def __init__(self):
        self.handlers = SortedDict()  # Sử dụng SortedDict để tối ưu tra cứu thông điệp

        # Tự động quét và đăng ký các phương thức với `@register_message`
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "_message"):  # Tìm các hàm có _message
                self.bind(attr._message, attr)

    def bind(self, msg, func):
        """Ràng buộc thông điệp với hàm xử lý."""
        self.handlers[msg] = func

    def handle_event(self, hwnd, msg, wparam, lparam):
        """Xử lý thông điệp nếu đã đăng ký, trả về None nếu không tìm thấy handler."""
        if msg in self.handlers:
            return self.handlers[msg](hwnd,msg,wparam,lparam)
        return None

# 3. Các lớp xử lý cụ thể, # MouseHandler dùng để xử lý sự kiện chuột
class MouseHandler(BaseHandler):
    """Xử lý các sự kiện liên quan đến chuột."""
    def __init__(self):
        super().__init__()
        self.state = {"mouse_down": False, "mouse_position": (0, 0)}

    @register_message(0x0201)  # WM_LBUTTONDOWN
    def on_left_button_down(self, hwnd, msg, wparam, lparam):
        x = ctypes.c_short(lparam & 0xFFFF).value
        y = ctypes.c_short((lparam >> 16) & 0xFFFF).value
        self.state["mouse_down"] = True
        self.state["mouse_position"] = (x, y)
        print(f"Left Mouse Button Down at ({x}, {y})!")

    @register_message(0x0202)  # WM_LBUTTONUP
    def on_left_button_up(self, hwnd, msg, wparam, lparam):
        self.state["mouse_down"] = False
        print("Left Mouse Button Released!")

    @register_message(0x0200)  # WM_MOUSEMOVE
    def on_mouse_move(self, hwnd, msg, wparam, lparam):
        x = ctypes.c_short(lparam & 0xFFFF).value
        y = ctypes.c_short((lparam >> 16) & 0xFFFF).value
        self.state["mouse_position"] = (x, y)
        print(f"Mouse moved to ({x}, {y})")

# WindowStateHandler để xử lý trạng thái cửa sổ
class WindowStateHandler(BaseHandler):
    """Xử lý các sự kiện trạng thái cửa sổ."""
    def __init__(self):
        super().__init__()

    @register_message(0x0007)  # WM_SETFOCUS
    def on_set_focus(self, hwnd, msg, wparam, lparam):
        print("Window received focus.")

    @register_message(0x0008)  # WM_KILLFOCUS
    def on_kill_focus(self, hwnd, msg, wparam, lparam):
        print("Window lost focus.")

    @register_message(0x0002)  # WM_DESTROY
    def on_destroy(self, hwnd, msg, wparam, lparam):
        print("Window is being destroyed.")
        ctypes.windll.user32.PostQuitMessage(0)

# 4. CompositeHandler để kết hợp các handler
class CompositeHandler:
    """
    Kết hợp các handler con và định tuyến thông điệp đến handler phù hợp.
    """
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def handle_event(self, hwnd, msg, wparam, lparam):
        for handler in self.handlers:
            result = handler.handle_event(hwnd, msg, wparam, lparam)
            if result is not None:
                return result
        return ctypes.windll.user32.DefWindowProcW( hwnd, msg, wintypes.WPARAM(wparam), wintypes.LPARAM(lparam) )

# 5. Quản lý cửa sổ
class WindowManager:
    """
    Quản lý ánh xạ các cửa sổ (HWND) tương ứng với handler.
    """
    def __init__(self):
        self.window_handlers = {}

    def register_window(self, hwnd, handler):
        self.window_handlers[hwnd] = handler

    def unregister_window(self, hwnd):
        if hwnd in self.window_handlers:
            del self.window_handlers[hwnd]

    def handle_event(self, hwnd, msg, wparam, lparam):
        handler = self.window_handlers.get(hwnd)
        if handler:
            return handler.handle_event(hwnd, msg, wparam, lparam)
        return ctypes.windll.user32.DefWindowProcW( hwnd, msg, wintypes.WPARAM(wparam), wintypes.LPARAM(lparam) )

# 6. WindowClass để quản lý cửa sổ
class WindowClass:
    """Quản lý việc đăng ký và tạo cửa sổ."""
    def __init__(self, class_name, hInstance=None, wnd_proc=None,
                 style=0, hIcon=None, hCursor=None, hbrBackground=None):
        self.class_name = class_name
        self.hInstance = hInstance or ctypes.windll.kernel32.GetModuleHandleW(None)
        self.wnd_proc = wnd_proc
        self.style = style

        # Biểu tượng và con trỏ mặc định
        self.hIcon = hIcon or ctypes.windll.user32.LoadIconW(0, 32512)  # IDI_APPLICATION
        self.hCursor = hCursor or ctypes.windll.user32.LoadCursorW(0, 32512)  # IDC_ARROW
        self.hbrBackground = hbrBackground or ctypes.cast(6, wintypes.HBRUSH)  # COLOR_WINDOW + 1

        # Đăng ký lớp cửa sổ
        self._register_window_class()
    def _register_window_class(self):
        """Đăng ký lớp cửa sổ nếu chưa tồn tại."""
        self.wnd_proc_callback = WNDPROC(self.wnd_proc)
        wc = WNDCLASS()
        wc.style = self.style
        wc.lpfnWndProc = self.wnd_proc_callback
        wc.cbClsExtra = 0
        wc.cbWndExtra = 0
        wc.hInstance = self.hInstance
        wc.hIcon = self.hIcon
        wc.hCursor = self.hCursor
        wc.hbrBackground = self.hbrBackground
        wc.lpszMenuName = None
        wc.lpszClassName = self.class_name

        if not ctypes.windll.user32.GetClassInfoW(self.hInstance, self.class_name, ctypes.byref(wc)):
            print(f"Đăng ký lớp cửa sổ: {self.class_name}")
            if not ctypes.windll.user32.RegisterClassW(ctypes.byref(wc)):
                raise ctypes.WinError(ctypes.get_last_error())
        else:
            print(f"Lớp {self.class_name} đã tồn tại, bỏ qua việc đăng ký.")

    def create_window(self, title, x=100, y=100, width=300, height=200,
                      style=0x10CF0000, exstyle=0, parent=None, menu=None):
        """Tạo cửa sổ."""
        hwnd = ctypes.windll.user32.CreateWindowExW(
            exstyle,
            self.class_name,
            title,
            style,
            x, y, width, height,
            parent,
            menu,
            self.hInstance,
            None
        )
        if not hwnd:
            raise ctypes.WinError(ctypes.get_last_error())
        return hwnd

LWA_ALPHA = 0x00000002

# Structures for tray icon
class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hwnd", wintypes.HWND),
        ("uID", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("uCallbackMessage", wintypes.UINT),
        ("hIcon", wintypes.HICON),
        ("szTip", ctypes.c_char * 128),
        ("dwState", wintypes.DWORD),
        ("dwStateMask", wintypes.DWORD),
        ("szInfo", ctypes.c_char * 256),
        ("uTimeoutOrVersion", wintypes.UINT),
        ("szInfoTitle", ctypes.c_char * 64),
        ("dwInfoFlags", wintypes.DWORD),
        ("guidItem", ctypes.c_char * 16),
    ]




# Tải thư viện user32.dll và kernel32.dll
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Định nghĩa kiểu trả về và tham số cho các hàm Windows API
user32.SetWindowsHookExW.argtypes = [ctypes.c_int, ctypes.c_void_p, wintypes.HINSTANCE,  wintypes.DWORD]
user32.SetWindowsHookExW.restype = wintypes.HHOOK

user32.CallNextHookEx.argtypes = [ wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
user32.CallNextHookEx.restype = wintypes.LPARAM

user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
user32.UnhookWindowsHookEx.restype = wintypes.BOOL

user32.GetMessageW.argtypes = [ ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT ]
user32.GetMessageW.restype = wintypes.BOOL

user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
user32.TranslateMessage.restype = wintypes.BOOL

user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]
user32.DispatchMessageW.restype = wintypes.LPARAM

user32.MapVirtualKeyW.argtypes = [wintypes.UINT, wintypes.UINT]
user32.MapVirtualKeyW.restype = wintypes.UINT

user32.GetKeyNameTextW.argtypes = [wintypes.LONG, wintypes.LPWSTR, ctypes.c_int]
user32.GetKeyNameTextW.restype = ctypes.c_int

kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
kernel32.GetModuleHandleW.restype = wintypes.HMODULE

# Định nghĩa cấu trúc KBDLLHOOKSTRUCT
class KBDLLHOOKSTRUCT(ctypes.Structure): _fields_ = [ ("vkCode", wintypes.DWORD), ("scanCode", wintypes.DWORD), ("flags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)) ]

# Định nghĩa callback function
HOOKPROC = ctypes.WINFUNCTYPE( wintypes.LPARAM, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM )




class TooltipWindow:
    def __init__(self):
        # Khởi tạo...
        self._visible = False
        self._hide_timer = None

    def is_visible(self):
        return self._visible        # """Kiểm tra xem tooltip có đang hiển thị không"""

    def update(self, text, x, y, style="info"):
        """Cập nhật nội dung và vị trí của tooltip đang hiển thị"""
        if self._hide_timer: self._hide_timer.cancel(); self._hide_timer = None                    # Hủy timer hiện tại nếu có
            
        # (Giả sử đã có phương thức _set_text và _set_style) # Cập nhật nội dung
        self._set_text(text)
        self._set_style(style)

        # Di chuyển tooltip
        user32.SetWindowPos(
            self.hwnd, None,  # hWndInsertAfter
            x, y,  0, 0,  # cx, cy (không thay đổi kích thước)
            0x0001 | 0x0004 )   # SWP_NOSIZE | SWP_NOZORDER

    def show(self, text, x, y, duration=2.0, style="info"):
        """Hiển thị tooltip"""
        # Hiển thị tooltip...
        self._visible = True

        # Đặt timer để ẩn
        if self._hide_timer: self._hide_timer.cancel()
        self._hide_timer = threading.Timer(duration, self.hide)
        self._hide_timer.daemon = True
        self._hide_timer.start()

    def hide(self):
        """Ẩn tooltip"""
        self._visible = False
        if self._hide_timer: self._hide_timer.cancel(); self._hide_timer = None

class CustomTooltip:
    def __init__(self, parent_hwnd, width, height, bg_color=0xF0F0F0):
        """
        Tạo Tooltip tùy chỉnh sử dụng cửa sổ và GDI.
        :param parent_hwnd: HWND của cửa sổ cha.
        :param width: Chiều rộng của tooltip (px).
        :param height: Chiều cao của tooltip (px).
        :param bg_color: Màu nền (RGB).
        """
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.parent_hwnd = parent_hwnd  # Lưu lại parent_hwnd
        logger.debug(f"CustomTooltip initialized with width={width}, height={height}, bg_color={bg_color}")

        # Tạo tooltip window
        self.hwnd = ctypes.windll.user32.CreateWindowExW(
            0x00000080,  # WS_EX_TOOLWINDOW - Cửa sổ không xuất hiện trong thanh taskbar
            "STATIC",    # Lớp cửa sổ (DEFAULT)
            None,
            0x80000000 | 0x40000000,  # WS_POPUP | WS_VISIBLE
            0, 0, width, height,      # Vị trí và kích thước (sẽ chỉnh sau)
            parent_hwnd,
            None,
            None,
            None
        )

        if not self.hwnd:
            error = ctypes.get_last_error()
            logger.error(f"Không thể tạo tooltip window. Mã lỗi: {error}")
            raise ctypes.WinError(error)

        # Thiết lập nền tooltip
        hBrush = ctypes.windll.gdi32.CreateSolidBrush(self.bg_color)
        ctypes.windll.user32.SetClassLongPtrW(self.hwnd, -10, hBrush)  # -10: GCLP_HBRBACKGROUND

        self.hdc = None  # Graphics context (sẽ được sử dụng cho GDI sau)

    def show(self, text, x, y):
        """
        Hiển thị Custom Tooltip với nội dung và vị trí thiết lập.
        :param text: Văn bản hiển thị trên tooltip.
        :param x: Tọa độ x (cạnh trên-trái).
        :param y: Tọa độ y (cạnh trên-trái).
        """
        logger.debug(f"CustomTooltip.show called with text='{text}', x={x}, y={y}")
        # Đặt vị trí tooltip
        ctypes.windll.user32.SetWindowPos(
            self.hwnd,
            None,
            x,
            y,
            self.width,
            self.height,
            0x0040  # SWP_NOZORDER (không thay đổi thứ tự lớp)
        )

        # Lấy device context (hDC) để vẽ
        self.hdc = ctypes.windll.user32.GetDC(self.hwnd)
        if not self.hdc:
            error = ctypes.get_last_error()
            logger.error(f"Không thể lấy HDC. Mã lỗi: {error}")
            return  # Hoặc raise exception nếu cần thiết

        self._draw_text(text)

        # Hiển thị tooltip
        ctypes.windll.user32.ShowWindow(self.hwnd, 5)  # SW_SHOW

    def _draw_text(self, text):
        """
        Vẽ văn bản lên tooltip bằng GDI.
        :param text: Văn bản cần hiển thị.
        """
        logger.debug(f"CustomTooltip._draw_text called with text='{text}'")

        # Chọn font
        hFont = ctypes.windll.gdi32.CreateFontW(
            24, 0, 0, 0, 700, 0, 0, 0, 0, 0, 0, 0, 0, "Segoe UI"
        )
        if not hFont:
            error = ctypes.get_last_error()
            logger.error(f"Không thể tạo font. Mã lỗi: {error}")
            return

        ctypes.windll.gdi32.SelectObject(self.hdc, hFont)

        # Đặt màu
        ctypes.windll.gdi32.SetTextColor(self.hdc, 0x000000)  # Màu chữ đen (RGB)
        ctypes.windll.gdi32.SetBkMode(self.hdc, 1)            # TRANSPARENT

        # Vẽ văn bản
        rect = wintypes.RECT(10, 10, self.width - 10, self.height - 10)
        ctypes.windll.user32.DrawTextW(
            self.hdc,
            text,
            len(text),
            ctypes.byref(rect),
            0x00000000  # DT_LEFT (căn trái)
        )

        # Dọn dẹp
        ctypes.windll.gdi32.DeleteObject(hFont)

    def hide(self):
        """
        Ẩn tooltip.
        """
        logger.debug("CustomTooltip.hide called")
        ctypes.windll.user32.ShowWindow(self.hwnd, 0)  # SW_HIDE

    def destroy(self):
        """
        Giải phóng tài nguyên và hủy cửa sổ tooltip.
        """
        logger.debug("CustomTooltip.destroy called")
        if self.hdc:
            ctypes.windll.user32.ReleaseDC(self.hwnd, self.hdc)
        ctypes.windll.user32.DestroyWindow(self.hwnd)





class EnhancedTooltip(CustomTooltip):
    """Tooltip nâng cao với nhiều tùy chọn hiển thị"""
    def __init__(self, parent_hwnd, width=300, height=80, bg_color=0xF0F0F0):
        super().__init__(parent_hwnd, width, height, bg_color)
        self.animation_thread = None
        self.stop_animation = False
        logger.debug("EnhancedTooltip initialized")

    def show_with_fade(self, text, x, y, duration=1.5):
        """Hiển thị tooltip với hiệu ứng fade in/out"""
        logger.debug(f"EnhancedTooltip.show_with_fade called with text='{text}', x={x}, y={y}, duration={duration}")

        # Dừng animation hiện tại nếu có
        self.stop_animation_if_running()

        # Khởi động thread mới cho animation
        self.stop_animation = False
        self.animation_thread = threading.Thread(
            target=self._animate_fade,
            args=(text, x, y, duration),
            daemon=True
        )
        self.animation_thread.start()

    def _animate_fade(self, text, x, y, duration):
        """Thực hiện animation fade in/out"""
        logger.debug(f"EnhancedTooltip._animate_fade called with text='{text}', x={x}, y={y}, duration={duration}")
        try:
            # Fade in
            self.show(text, x, y)
            time.sleep(duration)

            # Fade out (nếu chưa bị dừng)
            if not self.stop_animation:
                self.hide()
        except Exception as e:
            logger.error(f"Lỗi trong animation tooltip: {e}", exc_info=True)

    def show_with_style(self, text, x, y, style="info", duration=1.5):
        """Hiển thị tooltip với các kiểu khác nhau"""
        logger.debug(f"EnhancedTooltip.show_with_style called with text='{text}', x={x}, y={y}, style='{style}', duration={duration}")

        # Xác định màu sắc và biểu tượng dựa trên kiểu
        icon = "ℹ️"  # Mặc định: info
        if style == "success":
            icon = "✅"
            self.bg_color = RGB(230, 255, 230)  # Màu xanh lá nhạt
        elif style == "warning":
            icon = "⚠️"
            self.bg_color = RGB(255, 255, 220)  # Màu vàng nhạt
        elif style == "error":
            icon = "❌"
            self.bg_color = RGB(255, 230, 230)  # Màu đỏ nhạt

        # Tạo văn bản có biểu tượng
        styled_text = f"{icon} {text}"

        # Hiển thị với hiệu ứng fade
        self.show_with_fade(styled_text, x, y, duration)

    def stop_animation_if_running(self):
        """Dừng animation hiện tại nếu đang chạy"""
        logger.debug("EnhancedTooltip.stop_animation_if_running called")
        if self.animation_thread and self.animation_thread.is_alive():
            self.stop_animation = True
            self.hide()
            self.animation_thread.join(0.5)  # Chờ tối đa 0.5 giây

    def destroy(self):
        """Giải phóng tài nguyên và hủy cửa sổ tooltip"""
        logger.debug("EnhancedTooltip.destroy called")
        self.stop_animation_if_running()
        super().destroy()

    def set_hotkey_handler(self, handler_function):
        """Đặt hàm xử lý cho sự kiện phím tắt

        Args:
            handler_function: Hàm xử lý nhận tham số combo_name
        """
        self._hotkey_handler = handler_function
        logger.info(f"Đã đăng ký handler cho phím tắt: {handler_function.__qualname__ if hasattr(handler_function, '__qualname__') else handler_function}")

    def init_hook(self):
        logger.debug("init_hook: Bắt đầu")
        if self.is_hook_active: logger.warning("init_hook: Hook bàn phím đã được kích hoạt!");  return True

        # Định nghĩa callback function
        self.HOOKPROC = ctypes.WINFUNCTYPE( wintypes.LPARAM, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM )

        # Tạo instance của keyboard_hook
        self.keyboard_hook_instance = self.HOOKPROC(self.keyboard_callback)

        # Lấy handle của module hiện tại (None = module hiện tại của process)
        module_handle = kernel32.GetModuleHandleW(None)

        # Thiết lập hook sử dụng SetWindowsHookExW (phiên bản Unicode)
        self.hook_id = user32.SetWindowsHookExW(
            13,                         # WH_KEYBOARD_LL: low-level keyboard
            self.keyboard_hook_instance,  # hàm callback
            module_handle,              # instance của module hiện tại
            0                           # hook cho tất cả thread
        )

        if not self.hook_id:
            error_code = ctypes.get_last_error()
            logger.error(f"init_hook: Không thể thiết lập keyboard hook. Lỗi: {error_code}")
            logger.debug(f"init_hook: self.is_hook_active trước khi return False: {self.is_hook_active}")  # Thêm dòng này
            return False

        # Giữ tham chiếu global để tránh garbage collection
        self._keyboard_hook_ref = self.keyboard_hook_instance
        self.is_hook_active = True
        logger.info("init_hook: ✅ Đã kích hoạt keyboard hook thành công")
        logger.debug(f"init_hook: self.is_hook_active trước khi return True: {self.is_hook_active}")  # Thêm dòng này
        return True

    def setup_hotkeys(self, combinations, descriptions=None):
        """Thiết lập các tổ hợp phím cần theo dõi Args: combinations: dict - Từ điển với khóa là tên tổ hợp, giá trị là dict Virtual-Key codes
            descriptions: dict - Từ điển với khóa là tên tổ hợp, giá trị là mô tả chức năng """
        self.hotkey_combinations = combinations

        # Khởi tạo mô tả chức năng
        if descriptions: self.hotkey_descriptions = descriptions
        else: self.hotkey_descriptions = {name: f"Kích hoạt {name}" for name in combinations.keys()} # Tạo mô tả mặc định nếu không được cung cấp

        # Khởi tạo key_state với tất cả các phím cần theo dõi
        for combo_keys in combinations.values():
            for key in combo_keys:
                self.key_state[key] = False

        logger.info(f"Đã thiết lập {len(combinations)} tổ hợp phím: {', '.join(combinations.keys())}")  # Thêm log

    def disable_hook(self):
        logger.debug("disable_hook: Bắt đầu")
        if not self.is_hook_active:
            logger.warning("disable_hook: Hook bàn phím chưa được kích hoạt!")
            return True

        if self.hook_id:
            result = user32.UnhookWindowsHookEx(self.hook_id)
            if result:
                self.hook_id = None
                self._keyboard_hook_ref = None
                self.is_hook_active = False
                logger.info("disable_hook: ✅ Đã hủy keyboard hook thành công")
                logger.debug(f"disable_hook: self.is_hook_active trước khi return True: {self.is_hook_active}")  # Thêm dòng này
                return True
            else:
                error_code = ctypes.get_last_error()
                logger.error(f"disable_hook: Không thể hủy keyboard hook. Lỗi: {error_code}")
                logger.debug(f"disable_hook: self.is_hook_active trước khi return False: {self.is_hook_active}")  # Thêm dòng này
                return False
        logger.debug(f"disable_hook: self.is_hook_active trước khi return True (hook_id là None): {self.is_hook_active}")  # Thêm dòng này
        return True

    def toggle_key_status_display(self):
        """Bật/tắt hiển thị trạng thái phím"""
        self.show_key_status = not self.show_key_status

        # Khởi tạo status_tooltip nếu chưa có và cần hiển thị
        if self.show_key_status and not self.status_tooltip:
            self.status_tooltip = EnhancedTooltip(
                self.hwnd,
                width=200,
                height=60,
                bg_color=RGB(230, 230, 250)  # Màu nhạt để phân biệt
            )

        # Ẩn tooltip nếu tắt hiển thị
        if not self.show_key_status and self.status_tooltip:
            self.status_tooltip.hide()


    def keyboard_callback(self, nCode, wParam, lParam):
        """Callback function xử lý sự kiện bàn phím"""
        if nCode == 0:  # HC_ACTION
            kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk_code = kb.vkCode

            # Chỉ xử lý các phím được theo dõi
            if vk_code in self.key_state or any(vk_code in combo for combo in self.hotkey_combinations.values()):
                # Cập nhật trạng thái phím
                if wParam == 0x0100 or wParam == 0x0104:  # WM_KEYDOWN or WM_SYSKEYDOWN
                    if vk_code not in self.key_state:
                        self.key_state[vk_code] = False
                    self.key_state[vk_code] = True

                    # Chỉ kiểm tra tổ hợp phím khi có phím mới được nhấn
                    current_time = time.time()
                    if current_time - self.last_hotkey_time >= self.hotkey_cooldown:
                        # Tìm tổ hợp phím đang được nhấn
                        for combo_name, combo_keys in self.hotkey_combinations.items():
                            if all(self.key_state.get(k, False) for k in combo_keys):
                                logger.info(f"⌨️ Phát hiện tổ hợp phím: {combo_name}")
                                self.last_hotkey_time = current_time

                                # Xử lý trong thread riêng để tránh block callback
                                threading.Thread(
                                    target=self._process_hotkey,
                                    args=(combo_name,),
                                    daemon=True
                                ).start()
                                break  # Chỉ xử lý tổ hợp phím đầu tiên tìm thấy

                elif wParam == 0x0101 or wParam == 0x0105:  # WM_KEYUP or WM_SYSKEYUP
                    if vk_code in self.key_state:
                        self.key_state[vk_code] = False

        # Chuyển tiếp thông điệp cho hook tiếp theo
        return user32.CallNextHookEx(None, nCode, wParam, lParam)


    def _process_hotkey(self, combo_name):
        """Xử lý tổ hợp phím trong thread riêng"""
        try:
            # Hiển thị tooltip
            self.show_hotkey_tooltip(combo_name)

            # Gọi handler đã đăng ký nếu có
            if hasattr(self, '_hotkey_handler'):
                logger.debug(f"Gọi handler đã đăng ký cho phím tắt: {combo_name}")
                self._hotkey_handler(combo_name)
            else:
                # Fallback, gọi handle_hotkey nếu chưa đăng ký handler
                logger.debug(f"Không có handler đăng ký, fallback cho phím tắt: {combo_name}")
                self.handle_hotkey(combo_name)

        except Exception as e:
            logger.error(f"Lỗi khi xử lý tổ hợp phím {combo_name}: {e}", exc_info=True)

    def show_hotkey_tooltip(self, combo_name):
        """Hiển thị tooltip với thông tin về phím tắt được kích hoạt"""
        if self.tooltip:
            # Lấy mô tả nếu có, nếu không sử dụng tên phím tắt
            description = self.hotkey_descriptions.get(combo_name, f"Kích hoạt {combo_name}")

            # Lấy vị trí chuột hiện tại để hiển thị tooltip gần đó
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))

            # Hiển thị tooltip với thông báo và vị trí
            tooltip_text = f"{combo_name}\n{description}"

            # Xác định kiểu tooltip dựa trên phím tắt
            style = "info"
            if "Ctrl+Shift+T" in combo_name:
                style = "success"
            elif "Ctrl+Shift+Space" in combo_name:
                style = "warning"

            # Gọi phương thức hiển thị tooltip với kiểu tương ứng
            if hasattr(self.tooltip, 'show_with_style'):
                # Sử dụng EnhancedTooltip (đã có tự động ẩn)
                self.tooltip.show_with_style(
                    tooltip_text,
                    pt.x + 15,
                    pt.y + 15,
                    style=style,
                    duration=1.5  # Thời gian hiển thị cố định
                )
            else:
                # Sử dụng CustomTooltip tiêu chuẩn với timer để ẩn
                self.tooltip.show(tooltip_text, pt.x + 15, pt.y + 15)

                # Tạo timer để ẩn tooltip sau 1.5 giây
                timer = threading.Timer(1.5, self.tooltip.hide)
                timer.daemon = True  # Đảm bảo thread sẽ kết thúc khi chương trình chính kết thúc
                timer.start()

                # Lưu tham chiếu đến timer để có thể hủy nếu cần
                if not hasattr(self, '_tooltip_timers'):
                    self._tooltip_timers = []
                self._tooltip_timers.append(timer)

    def show_tooltip(self, text, duration=2.0, style="info"):
        """Hiển thị tooltip với văn bản và kiểu cho trước"""
        try:
            # Lấy vị trí chuột
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))

            if not hasattr(self, 'tooltip'):        # Tạo tooltip nếu chưa có
                self.tooltip = TooltipWindow()

            self.tooltip.show(text, pt.x + 15, pt.y + 15, duration, style)      # Hiển thị tooltip
        except Exception as e:
            logger.error(f"Lỗi khi hiển thị tooltip: {e}", exc_info=True)

    def _show_tooltip_with_auto_hide(self, text, x, y, duration=1.5):
        """Hiển thị tooltip và tự động ẩn sau một khoảng thời gian"""
        def _hide_after_delay():
            try:
                time.sleep(duration)
                self.tooltip.hide()
            except Exception as e:
                logger.error(f"Lỗi khi ẩn tooltip: {e}", exc_info=True)

        try:
            self.tooltip.show(text, x, y)

            # Tạo thread để ẩn tooltip sau khoảng thời gian
            hide_thread = threading.Thread(target=_hide_after_delay, daemon=True)
            hide_thread.start()

            # Lưu tham chiếu đến thread để có thể quản lý nếu cần
            if not hasattr(self, '_tooltip_threads'):
                self._tooltip_threads = []
            self._tooltip_threads.append(hide_thread)
        except Exception as e:
            logger.error(f"Lỗi khi hiển thị tooltip: {e}", exc_info=True)

    def handle_hotkey(self, combo_name):
        """Xử lý khi phát hiện tổ hợp phím
        Args:
            combo_name: str - Tên của tổ hợp phím được nhấn
        """
        # Phương thức này sẽ được ghi đè trong lớp con hoặc gán callback function
        logger.info(f"Đã phát hiện tổ hợp phím: {combo_name}")
        # if "Ctrl+Shift+Space" in combo_name: self.run_async_in_thread(self.async_restart_exploder())

        # Thực hiện hành động tương ứng tại đây



class KeyboardHookHandler(BaseHandler):
    """Handler quản lý keyboard hook để bắt phím tắt toàn cục"""

    def __init__(self, tooltip=None):  # Chấp nhận tooltip trong __init__
        super().__init__()
        self.hook_id = None
        self._keyboard_hook_ref = None
        self.hotkey_combinations = {}
        self.key_state = {}
        self.is_hook_active = False
        self.last_hotkey_time = 0
        self.hotkey_cooldown = 0.5  # Thời gian chờ giữa các lần kích hoạt (giây)
        self.status_tooltip = None  # Tooltip hiển thị trạng thái phím
        self.show_key_status = False  # Có hiển thị trạng thái phím không
        self.tooltip = None  # Sẽ được gán từ TrayIconHandler
        self.hotkey_descriptions = {}  # Cần thêm vào để tránh AttributeError
        logger.debug("KeyboardHookHandler initialized")  # Thêm log khi khởi tạo


    def set_hotkey_handler(self, handler_function):
        """Đặt hàm xử lý cho sự kiện phím tắt

        Args:
            handler_function: Hàm xử lý nhận tham số combo_name
        """
        self._hotkey_handler = handler_function
        logger.info(f"Đã đăng ký handler cho phím tắt: {handler_function.__qualname__ if hasattr(handler_function, '__qualname__') else handler_function}")

    def init_hook(self):
        logger.debug("init_hook: Bắt đầu")
        if self.is_hook_active:
            logger.warning("init_hook: Hook bàn phím đã được kích hoạt!")
            return True

        # Định nghĩa callback function
        self.HOOKPROC = ctypes.WINFUNCTYPE( wintypes.LPARAM, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM )

        # Tạo instance của keyboard_hook
        self.keyboard_hook_instance = self.HOOKPROC(self.keyboard_callback)

        # Lấy handle của module hiện tại (None = module hiện tại của process)
        module_handle = kernel32.GetModuleHandleW(None)

        # Thiết lập hook sử dụng SetWindowsHookExW (phiên bản Unicode)
        self.hook_id = user32.SetWindowsHookExW(
            13,                         # WH_KEYBOARD_LL: low-level keyboard
            self.keyboard_hook_instance,  # hàm callback
            module_handle,              # instance của module hiện tại
            0                           # hook cho tất cả thread
        )


        if not self.hook_id:
            error_code = ctypes.get_last_error()
            logger.error(f"init_hook: Không thể thiết lập keyboard hook. Lỗi: {error_code}")
            logger.debug(f"init_hook: self.is_hook_active trước khi return False: {self.is_hook_active}")  # Thêm dòng này
            return False

        # Giữ tham chiếu global để tránh garbage collection
        self._keyboard_hook_ref = self.keyboard_hook_instance
        self.is_hook_active = True
        logger.info("init_hook: ✅ Đã kích hoạt keyboard hook thành công")
        logger.debug(f"init_hook: self.is_hook_active trước khi return True: {self.is_hook_active}")  # Thêm dòng này
        return True

    def setup_hotkeys(self, combinations, descriptions=None):
        """Thiết lập các tổ hợp phím cần theo dõi

        Args:
            combinations: dict - Từ điển với khóa là tên tổ hợp, giá trị là dict Virtual-Key codes
            descriptions: dict - Từ điển với khóa là tên tổ hợp, giá trị là mô tả chức năng
        """
        self.hotkey_combinations = combinations

        # Khởi tạo mô tả chức năng
        if descriptions:
            self.hotkey_descriptions = descriptions
        else:
            # Tạo mô tả mặc định nếu không được cung cấp
            self.hotkey_descriptions = {name: f"Kích hoạt {name}" for name in combinations.keys()}

        # Khởi tạo key_state với tất cả các phím cần theo dõi
        for combo_keys in combinations.values():
            for key in combo_keys:
                self.key_state[key] = False

        logger.info(f"Đã thiết lập {len(combinations)} tổ hợp phím: {', '.join(combinations.keys())}")  # Thêm log

    def disable_hook(self):
        logger.debug("disable_hook: Bắt đầu")
        if not self.is_hook_active:
            logger.warning("disable_hook: Hook bàn phím chưa được kích hoạt!")
            return True

        if self.hook_id:
            result = user32.UnhookWindowsHookEx(self.hook_id)
            if result:
                self.hook_id = None
                self._keyboard_hook_ref = None
                self.is_hook_active = False
                logger.info("disable_hook: ✅ Đã hủy keyboard hook thành công")
                logger.debug(f"disable_hook: self.is_hook_active trước khi return True: {self.is_hook_active}")  # Thêm dòng này
                return True
            else:
                error_code = ctypes.get_last_error()
                logger.error(f"disable_hook: Không thể hủy keyboard hook. Lỗi: {error_code}")
                logger.debug(f"disable_hook: self.is_hook_active trước khi return False: {self.is_hook_active}")  # Thêm dòng này
                return False
        logger.debug(f"disable_hook: self.is_hook_active trước khi return True (hook_id là None): {self.is_hook_active}")  # Thêm dòng này
        return True

    def toggle_key_status_display(self):
        """Bật/tắt hiển thị trạng thái phím"""
        self.show_key_status = not self.show_key_status

        # Khởi tạo status_tooltip nếu chưa có và cần hiển thị
        if self.show_key_status and not self.status_tooltip:
            self.status_tooltip = EnhancedTooltip(
                self.hwnd,
                width=200,
                height=60,
                bg_color=RGB(230, 230, 250)  # Màu nhạt để phân biệt
            )

        # Ẩn tooltip nếu tắt hiển thị
        if not self.show_key_status and self.status_tooltip:
            self.status_tooltip.hide()

    def keyboard_callback(self, nCode, wParam, lParam):
        """Callback function xử lý sự kiện bàn phím"""
        if nCode == 0:  # HC_ACTION
            kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk_code = kb.vkCode

            # Chỉ xử lý các phím được theo dõi
            if vk_code in self.key_state or any(vk_code in combo for combo in self.hotkey_combinations.values()):
                # Cập nhật trạng thái phím
                if wParam == 0x0100 or wParam == 0x0104:  # WM_KEYDOWN or WM_SYSKEYDOWN
                    if vk_code not in self.key_state:
                        self.key_state[vk_code] = False
                    self.key_state[vk_code] = True

                    # Chỉ kiểm tra tổ hợp phím khi có phím mới được nhấn
                    current_time = time.time()
                    if current_time - self.last_hotkey_time >= self.hotkey_cooldown:
                        # Tìm tổ hợp phím đang được nhấn
                        for combo_name, combo_keys in self.hotkey_combinations.items():
                            if all(self.key_state.get(k, False) for k in combo_keys):
                                logger.info(f"⌨️ Phát hiện tổ hợp phím: {combo_name}")
                                self.last_hotkey_time = current_time

                                # Xử lý trong thread riêng để tránh block callback
                                threading.Thread(
                                    target=self._process_hotkey,
                                    args=(combo_name,),
                                    daemon=True
                                ).start()
                                break  # Chỉ xử lý tổ hợp phím đầu tiên tìm thấy

                elif wParam == 0x0101 or wParam == 0x0105:  # WM_KEYUP or WM_SYSKEYUP
                    if vk_code in self.key_state:
                        self.key_state[vk_code] = False

        # Chuyển tiếp thông điệp cho hook tiếp theo
        return user32.CallNextHookEx(None, nCode, wParam, lParam)


    def _process_hotkey(self, combo_name):
        """Xử lý tổ hợp phím trong thread riêng"""
        try:
            # Hiển thị tooltip
            self.show_hotkey_tooltip(combo_name)

            # Gọi handler đã đăng ký nếu có
            if hasattr(self, '_hotkey_handler'):
                logger.debug(f"Gọi handler đã đăng ký cho phím tắt: {combo_name}")
                self._hotkey_handler(combo_name)
            else:
                # Fallback, gọi handle_hotkey nếu chưa đăng ký handler
                logger.debug(f"Không có handler đăng ký, fallback cho phím tắt: {combo_name}")
                self.handle_hotkey(combo_name)

        except Exception as e:
            logger.error(f"Lỗi khi xử lý tổ hợp phím {combo_name}: {e}", exc_info=True)

    def show_hotkey_tooltip(self, combo_name):
        """Hiển thị tooltip với thông tin về phím tắt được kích hoạt"""
        if self.tooltip:
            # Lấy mô tả nếu có, nếu không sử dụng tên phím tắt
            description = self.hotkey_descriptions.get(combo_name, f"Kích hoạt {combo_name}")

            # Lấy vị trí chuột hiện tại để hiển thị tooltip gần đó
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))

            # Hiển thị tooltip với thông báo và vị trí
            tooltip_text = f"{combo_name}\n{description}"

            # Xác định kiểu tooltip dựa trên phím tắt
            style = "info"
            if "Ctrl+Shift+T" in combo_name:
                style = "success"
            elif "Ctrl+Shift+Space" in combo_name:
                style = "warning"

            # Gọi phương thức hiển thị tooltip với kiểu tương ứng
            if hasattr(self.tooltip, 'show_with_style'):
                # Sử dụng EnhancedTooltip (đã có tự động ẩn)
                self.tooltip.show_with_style(
                    tooltip_text,
                    pt.x + 15,
                    pt.y + 15,
                    style=style,
                    duration=1.5  # Thời gian hiển thị cố định
                )
            else:
                # Sử dụng CustomTooltip tiêu chuẩn với timer để ẩn
                self.tooltip.show(tooltip_text, pt.x + 15, pt.y + 15)

                # Tạo timer để ẩn tooltip sau 1.5 giây
                timer = threading.Timer(1.5, self.tooltip.hide)
                timer.daemon = True  # Đảm bảo thread sẽ kết thúc khi chương trình chính kết thúc
                timer.start()

                # Lưu tham chiếu đến timer để có thể hủy nếu cần
                if not hasattr(self, '_tooltip_timers'):
                    self._tooltip_timers = []
                self._tooltip_timers.append(timer)

    def show_tooltip(self, text, duration=2.0, style="info"):
        """Hiển thị tooltip với văn bản và kiểu cho trước"""
        try:
            # Lấy vị trí chuột
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))

            if not hasattr(self, 'tooltip'):        # Tạo tooltip nếu chưa có
                self.tooltip = TooltipWindow()

            self.tooltip.show(text, pt.x + 15, pt.y + 15, duration, style)      # Hiển thị tooltip
        except Exception as e:
            logger.error(f"Lỗi khi hiển thị tooltip: {e}", exc_info=True)

    def _show_tooltip_with_auto_hide(self, text, x, y, duration=1.5):
        """Hiển thị tooltip và tự động ẩn sau một khoảng thời gian"""
        def _hide_after_delay():
            try:
                time.sleep(duration)
                self.tooltip.hide()
            except Exception as e:
                logger.error(f"Lỗi khi ẩn tooltip: {e}", exc_info=True)

        try:
            self.tooltip.show(text, x, y)

            # Tạo thread để ẩn tooltip sau khoảng thời gian
            hide_thread = threading.Thread(target=_hide_after_delay, daemon=True)
            hide_thread.start()

            # Lưu tham chiếu đến thread để có thể quản lý nếu cần
            if not hasattr(self, '_tooltip_threads'):
                self._tooltip_threads = []
            self._tooltip_threads.append(hide_thread)
        except Exception as e:
            logger.error(f"Lỗi khi hiển thị tooltip: {e}", exc_info=True)

    def handle_hotkey(self, combo_name):
        """Xử lý khi phát hiện tổ hợp phím
        Args:
            combo_name: str - Tên của tổ hợp phím được nhấn
        """
        # Phương thức này sẽ được ghi đè trong lớp con hoặc gán callback function
        logger.info(f"Đã phát hiện tổ hợp phím: {combo_name}")
        # if "Ctrl+Shift+Space" in combo_name: self.run_async_in_thread(self.async_restart_exploder())

        # Thực hiện hành động tương ứng tại đây



class TrayIconHandler(BaseHandler):
    """Handler quản lý các sự kiện từ Tray Icon"""
    def __init__(self, icon_path, tooltip="Tray App"):
        super().__init__()
        self.last_click_time = 0
        self.double_click_threshold = 0.8  # giây

        self.hwnd = None

        self.is_hovered = False
        self.is_clicked = False
        self.is_active = False
        self._tracking_mouse = False

        self.menu_active = False
        self.icon_path = icon_path
        self.tooltip = tooltip
        self.nid = None
        self._last_opaque_state = None

        self.wnd_proc_callback = WNDPROC(self.tray_wnd_proc)  # Callback for handling window messages

        # Tạo window trước
        self.create_hidden_window()
        # Sau đó mới khởi tạo tooltip với hwnd đúng
        self.custom_tooltip = EnhancedTooltip(self.hwnd, width=300, height=80, bg_color=RGB(240, 240, 240))

        self.icon_handle = user32.LoadImageW( None, ICONHEART, 1, 0, 0, 0x00000010 | 0x00000040)                                     # LR_LOADFROMFILE | LR_DEFAULTSIZE
        if IS_ADMIN: self.icon_handle = user32.LoadImageW( None, ICONHEART_ADM, 1, 0, 0, 0x00000010 | 0x00000040)


        self.register_tray_icon()

        # Khởi tạo keyboard handler với tooltip
        self.keyboard_hook = KeyboardHookHandler()
        self.keyboard_hook.tooltip = self.custom_tooltip

        # Thiết lập phím tắt
        self.setup_keyboard_hooks()

        self._threads = []
        self._thread_stop_event = threading.Event()

        self.menu_actions = {}  # Ánh xạ ID với action
        self.menu_structure = self._create_menu_structure()  # Tạo cấu trúc menu

        logger.debug("TrayIconHandler initialized")  # Thêm log khi khởi tạo

    def setup_keyboard_hooks(self, config=None):
        # Định nghĩa cả phím trái và phím phải
        VK_LCONTROL = 0xA2  # Left Control
        VK_RCONTROL = 0xA3  # Right Control
        VK_LSHIFT = 0xA0    # Left Shift
        VK_RSHIFT = 0xA1    # Right Shift
        VK_SPACE = 0x20     # Space
        VK_T = 0x54         # T
        VK_RETURN = 0x0D    # Enter

        # Định nghĩa các tổ hợp phím với cả phím trái và phải
        default_hotkeys = {
            "Ctrl+Shift+T": {VK_LCONTROL: True, VK_LSHIFT: True, VK_T: True},
            "RCtrl+RShift+T": {VK_RCONTROL: True, VK_RSHIFT: True, VK_T: True},
            "Ctrl+Shift+Space": {VK_LCONTROL: True, VK_LSHIFT: True, VK_SPACE: True},
            "RCtrl+RShift+Space": {VK_RCONTROL: True, VK_RSHIFT: True, VK_SPACE: True},
            "Ctrl+Enter": {VK_LCONTROL: True, VK_RETURN: True},
            "RCtrl+Enter": {VK_RCONTROL: True, VK_RETURN: True}
        }


        # Định nghĩa mô tả cho mỗi phím tắt để hiển thị trong tooltip
        default_descriptions = {
            "Ctrl+Shift+T": "Hiển thị/ẩn cửa sổ ứng dụng",
            "Ctrl+Shift+Space": "Khởi động lại Windows Explorer",
            "Ctrl+Enter": "Hiển thị menu tray icon"
        }

            # Sử dụng cấu hình từ bên ngoài nếu có
        if config and 'hotkeys' in config: hotkey_combinations = config['hotkeys']
        else: hotkey_combinations = default_hotkeys

        if config and 'descriptions' in config: hotkey_descriptions = config['descriptions']
        else: hotkey_descriptions = default_descriptions

        # Thiết lập và kích hoạt hook với mô tả
        self.keyboard_hook.setup_hotkeys(hotkey_combinations, hotkey_descriptions)

        # Đăng ký callback thay vì ghi đè phương thức
        self.keyboard_hook.set_hotkey_handler(self.handle_hotkey)

        # Kích hoạt hook
        self.enable_keyboard_hook()

        logger.info(f"Đã thiết lập {len(hotkey_combinations)} phím tắt: {', '.join(hotkey_combinations.keys())}")

    def enable_keyboard_hook(self):
        """Bật chức năng lắng nghe phím tắt"""
        result = self.keyboard_hook.init_hook()
        if result:
            logger.info("Đã kích hoạt chức năng lắng nghe phím tắt")
        else:
            logger.error("Không thể kích hoạt chức năng lắng nghe phím tắt")
        logger.debug("enable_keyboard_hook called")

    def disable_keyboard_hook(self):
        """Tắt chức năng lắng nghe phím tắt"""
        result = self.keyboard_hook.disable_hook()
        if result:
            logger.info("Đã tắt chức năng lắng nghe phím tắt")
        else:
            logger.error("Không thể tắt chức năng lắng nghe phím tắt")
        logger.debug("disable_keyboard_hook called")

    def handle_hotkey(self, combo_name):
        """Xử lý khi phát hiện tổ hợp phím Args: combo_name: str - Tên của tổ hợp phím được nhấn """
        
        logger.info(f"TrayIconHandler xử lý tổ hợp phím: {combo_name}")

        # Xử lý các tổ hợp phím
        if combo_name == "Ctrl+Shift+T":
            logger.info("Kích hoạt chức năng cho Ctrl+Shift+T")
            # Gọi hàm xử lý tương ứng
            threading.Thread(target=self.handle_ctrl_shift_t, daemon=True).start()

        elif combo_name == "Ctrl+Shift+Space":
            logger.info("Kích hoạt chức năng cho Ctrl+Shift+Space")
            # Gọi hàm xử lý tương ứng
            threading.Thread(target=self.handle_ctrl_shift_space, daemon=True).start()

        elif combo_name == "Ctrl+Enter":
            logger.info("Kích hoạt chức năng cho Ctrl+Enter")
            # Gọi hàm xử lý tương ứng
            threading.Thread(target=self.handle_ctrl_enter, daemon=True).start()

    def handle_ctrl_shift_t(self):
        """Xử lý khi nhấn Ctrl+Shift+T"""
        # Ví dụ: Hiển thị cửa sổ ứng dụng
        logger.info("Xử lý Ctrl+Shift+T")
        if not user32.IsWindowVisible(self.hwnd):
            user32.ShowWindow(self.hwnd, 5)  # SW_SHOW
            user32.SetForegroundWindow(self.hwnd)
        else:
            user32.ShowWindow(self.hwnd, 0)  # SW_HIDE

    def handle_ctrl_shift_space(self):
        logger.info("Xử lý Ctrl+Shift+Space")

        # Định nghĩa callback để xử lý kết quả
        def on_complete(result=None, error=None):
            if error: logger.error(f"Khởi động lại Explorer thất bại: {error}")
            else: logger.info(f"Khởi động lại Explorer thành công: {result}")

        # Gọi với callback thay vì cố gắng lấy future
        self.run_async_in_thread(
            self.async_restart_exploder(),
            name="RestartExplorerThread",
            callback=on_complete
        )

    def handle_ctrl_enter(self):
        """Xử lý khi nhấn Ctrl+Enter"""
        # Ví dụ: Hiển thị menu
        logger.info("Xử lý Ctrl+Enter")
        self.show_tray_menu()

    def show_registered_hotkeys(self):
        """Hiển thị danh sách phím tắt đã đăng ký"""
        message = "Danh sách phím tắt đã đăng ký:\n\n"
        for combo_name in self.keyboard_hook.hotkey_combinations:
            message += f"- {combo_name}\n"

        # Hiển thị thông báo
        threading.Thread(target=lambda: show_auto_close_messagebox(message, autoclose_time=3000), daemon=True).start()
        logger.debug("show_registered_hotkeys called")

    def toggle_keyboard_hook(self):
        logger.debug(f"toggle_keyboard_hook: Bắt đầu, self.keyboard_hook.is_hook_active = {self.keyboard_hook.is_hook_active}")  # Thêm dòng này
        if self.keyboard_hook.is_hook_active:
            self.disable_keyboard_hook()
        else:
            self.enable_keyboard_hook()
        logger.debug(f"toggle_keyboard_hook: Kết thúc, self.keyboard_hook.is_hook_active = {self.keyboard_hook.is_hook_active}")  # Thêm dòng này

    def create_hidden_window(self):
        """Tạo cửa sổ chính"""
        try:
            logger.debug("create_hidden_window: Bắt đầu")

            # 1. Khởi tạo WNDCLASS
            logger.debug("create_hidden_window: Khởi tạo WNDCLASS")
            wnd_class = WNDCLASS()
            wnd_class.lpfnWndProc = self.wnd_proc_callback
            wnd_class.lpszClassName = "TrayIconPythonWindow"
            wnd_class.hInstance = kernel32.GetModuleHandleW(None)

            # 2. Lấy hInstance và ép kiểu
            logger.debug("create_hidden_window: Lấy hInstance và ép kiểu")
            hInstance = kernel32.GetModuleHandleW(None)
            hInstance_typed = ctypes.wintypes.HINSTANCE(hInstance)
            logger.debug(f"create_hidden_window: hInstance = {hInstance}, hInstance_typed = {hInstance_typed}")

            # 3. Tạo background brush
            logger.debug("create_hidden_window: Tạo background brush")
            self.hBrushBackground = gdi32.CreateSolidBrush(RGB(0x2E, 0x34, 0x40))
            wnd_class.hbrBackground = self.hBrushBackground

            # 4. Chuẩn bị tên class cho GetClassInfoW
            logger.debug("create_hidden_window: Chuẩn bị tên class cho GetClassInfoW")
            class_name_ptr = ctypes.c_wchar * (len("TrayIconPythonWindow") + 1)
            class_name_buffer = class_name_ptr(*"TrayIconPythonWindow", '\0')
            lpClassName = ctypes.cast(class_name_buffer, ctypes.c_wchar_p)
            logger.debug(f"create_hidden_window: lpClassName = {lpClassName}")

            # 5. Kiểm tra class đã đăng ký chưa
            logger.debug("create_hidden_window: Kiểm tra class đã đăng ký chưa")
            if user32.GetClassInfoW(hInstance_typed, lpClassName, ctypes.byref(wnd_class)):
                logger.warning("create_hidden_window: Lớp cửa sổ đã tồn tại, không cần đăng ký lại.")
            else:
                logger.debug("create_hidden_window: Đăng ký class")
                class_atom = user32.RegisterClassW(ctypes.byref(wnd_class))
                if class_atom == 0:
                    error = ctypes.get_last_error()
                    logger.error(f"create_hidden_window: Không thể đăng ký lớp cửa sổ. Mã lỗi: {error}", exc_info=True)
                    gdi32.DeleteObject(self.hBrushBackground)           # Giải phóng brush nếu đăng ký thất bại
                    raise ctypes.WinError(error)
                logger.debug(f"create_hidden_window: class_atom = {class_atom}")

            # 6. Tạo cửa sổ
            logger.debug("create_hidden_window: Tạo cửa sổ")
            self.hwnd = user32.CreateWindowExW(
                S_DWEXSTYLE, wnd_class.lpszClassName, "Tray Tools SHMG",
                S_DWSTYLE, 2300, 1000, 400, 777, None, None, None, None
            )
            if not self.hwnd:
                error = ctypes.get_last_error()
                logger.error("create_hidden_window: Không thể tạo cửa sổ", exc_info=True)
                gdi32.DeleteObject(self.hBrushBackground)           # Giải phóng brush nếu đăng ký thất bại
                raise ctypes.WinError(error)
            logger.debug(f"create_hidden_window: hwnd = {self.hwnd}")

            # 7. Cập nhật thuộc tính cửa sổ

            user32.SetPropA(self.hwnd, b"hBrushBackground", self.hBrushBackground)          # Lưu trữ tham chiếu đến brush trong window extra bytes để giải phóng sau này

            logger.debug("create_hidden_window: Cập nhật thuộc tính cửa sổ")
            user32.SetWindowLongPtrA(self.hwnd, -20, user32.GetWindowLongPtrA(self.hwnd, -20) | WS_EX_LAYERED)

            logger.info(f"create_hidden_window: Cửa sổ được tạo thành công hwnd = {self.hwnd}")

        except Exception as e:
            logger.error(f"Lỗi trong create_hidden_window: {e}", exc_info=True)
            # Đảm bảo giải phóng tài nguyên nếu có lỗi
            if hasattr(self, 'hBrushBackground') and self.hBrushBackground:
                gdi32.DeleteObject(self.hBrushBackground)
                self.hBrushBackground = None
            raise
        logger.debug("create_hidden_window: Kết thúc")

    def run_async_in_thread(self, coroutine, timeout=None, name=None, callback=None):
        """
        Chạy coroutine trong một thread riêng
        Args:
            coroutine: Coroutine cần chạy
            timeout: Thời gian chờ tối đa (giây)
            name: Tên thread
            callback: Hàm callback nhận kết quả/lỗi
        Returns:
            thread: Thread đã được khởi động
        """
        loop = asyncio.new_event_loop()         # Tạo event loop mới
        def run_async():            # Định nghĩa hàm chạy trong thread
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(coroutine)                 # Chạy coroutine và lấy kết quả
                if callback: callback(result=result, error=None)        # Gọi callback với kết quả nếu có
            except Exception as e:
                logger.error(f"Lỗi chạy coroutine: {e}", exc_info=e)
                if callback: callback(result=None, error=e)     # Gọi callback với lỗi nếu có
            finally:
                loop.close()
        # Tạo và khởi động thread
        thread = threading.Thread(target=run_async, name=name, daemon=True)
        thread.start()
        # Chỉ trả về thread
        return thread

    def sycn_restart_exploder(self):
        subprocess.run(["taskkill", "/F", "/IM", "explorer.exe"], shell=True)
        subprocess.Popen(["explorer.exe"])
        logger.debug("sycn_restart_exploder called")

    async def async_restart_exploder(self):
        logger.info("Đang khởi động lại Explorer...")
        proc = await asyncio.create_subprocess_shell( "taskkill /F /IM explorer.exe" )
        await proc.wait()
        await asyncio.create_subprocess_shell("explorer.exe")
        logger.info("Explorer đã khởi động lại!")
        logger.debug("async_restart_exploder called")

    def update_window_attributes(self):
        """Cập nhật thuộc tính cửa sổ (trong suốt hoặc không)"""
        try:
            # logger.info(f"\u2705 update_window_attributes called")
            # Kiểm tra xem cửa sổ có tồn tại không
            if not self.hwnd or not user32.IsWindow(self.hwnd): return logger.error("Cửa sổ không tồn tại khi cố gắng cập nhật thuộc tính")

            # Độ trong suốt dựa trên trạng thái
            alpha = 200  # Mặc định là không trong suốt
            if self.is_hovered: alpha = 255  # Hơi trong suốt khi hover
            if self.is_clicked: alpha = 150  # Nhiều trong suốt hơn khi click

            user32.SetLayeredWindowAttributes(self.hwnd, 0, alpha, LWA_ALPHA)  # LWA_ALPHA = 0x02        # Cập nhật độ trong suốt

            # Cập nhật vị trí cửa sổ nếu cần
            if self.is_hovered or self.is_clicked:
                pt = wintypes.POINT()       # Lấy vị trí chuột
                user32.GetCursorPos(ctypes.byref(pt))
                # user32.SetWindowPos(self.hwnd, None, pt.x, pt.y, 0, 0, 0x0001 | 0x0004)  # SWP_NOSIZE | SWP_NOZORDER      # Đặt cửa sổ ở vị trí chuột
        except Exception as e: logger.error(f"Lỗi khi cập nhật thuộc tính cửa sổ: {e}", exc_info=e)

    def _handle_wm_setfocus(self, hwnd, msg, wparam, lparam):
        """Xử lý thông điệp WM_SETFOCUS"""
        self.is_active = True
        self.update_window_attributes()
        logger.debug("_handle_wm_setfocus called")
        return 0

    def _create_menu_structure(self):
        """Tạo và trả về cấu trúc menu"""
        return {
            'main': {
                'items': [
                    {'id': 1, 'text': "Restart Explorer", 'action': lambda: self.run_async_in_thread(self.async_restart_exploder())},
                    {'id': 2, 'text': "table_2_md_rawtext", 'action': lambda: cb.clipboard_table_to_markdown()},
                    {'id': 3, 'text': "Html_To_Markd", 'action': lambda: cb.html_to_markd()},
                    {'id': 4, 'text': "Dup_line_remove", 'action': lambda: remove_line_duplicate()},
                    {'id': 5, 'text': "Focus Window", 'action': self.focus_window},
                    {'id': 0, 'text': "Clip_boardpath", 'submenu': 'clip_path'},
                    {'id': 0, 'text': "ToolSHMG", 'submenu': 'Tool_NS'},
                    {'id': 0, 'text': "HotKey", 'submenu': 'HotKeyManager'},
                    {'id': 6, 'text': "Open CMD with Path", 'action': lambda: self.open_cmd_at_path(pyperclip.paste())},
                    {'id': 7, 'text': "Run Python File", 'action': lambda: self.run_pyfile()},
                    {'id': 8, 'text': "Edit This SHMG", 'action': lambda: subprocess.Popen([fr"{VSCODE_PATH}", __file__])},
                    {'id': 9, 'text': "Run with Admin", 'action': lambda: restart_with_admin_rights()},
                    {'id': 10, 'text': "Exit", 'action': self.exit_app},
                ]
            },
            'clip_path': {
                'items': [
                    {'id': 101, 'text': "Filename", 'action': lambda: cb.get_file_paths(get_full_path=False)},
                    {'id': 102, 'text': "Full File Path", 'action': lambda: cb.get_file_paths(get_full_path=True)},
                ]
            },
            'Tool_NS': {
                'items': [
                    {'id': 201, 'text': "Voice Record", 'action': lambda: self.run_tool("voi_shmg.py")},
                    {'id': 202, 'text': "Image Crop", 'action': lambda: self.run_tool("25_2_Crop.py")},
                    {'id': 203, 'text': "R2_Cloudflare", 'action': lambda: self.run_tool("R2___cloudflare.py", run_as_admin=False)},
                ]
            },
            'HotKeyManager': {
                'items': [
                    {'id': 301, 'text': "✓ Bật phím tắt" if self.keyboard_hook.is_hook_active else "Bật phím tắt",
                     'action': lambda: self.toggle_keyboard_hook()},
                    {'id': 302, 'text': "✓ Hiển thị trạng thái phím" if self.keyboard_hook.show_key_status else "Hiển thị trạng thái phím",
                     'action': lambda: self.toggle_key_status_display()},
                    {'id': 303, 'text': "Danh sách phím tắt đã đăng ký",
                     'action': lambda: self.show_registered_hotkeys()},
                ]
            }
        }

    def _update_menu_actions(self):
        """Cập nhật ánh xạ ID với action từ cấu trúc menu"""
        self.menu_actions.clear()
        def process_menu(menu_data):            # Hàm đệ quy để duyệt qua tất cả menu item
            for item in menu_data['items']:
                if 'action' in item and item['action']:
                    self.menu_actions[item['id']] = item['action']

        for menu_name, menu_data in self.menu_structure.items():        # Duyệt qua tất cả menu
            process_menu(menu_data)

    def update_menu_item(self, item_id, properties):
        """Cập nhật thuộc tính của menu item
        Args:
            item_id (int): ID của menu item
            properties (dict): Các thuộc tính cần cập nhật
        """
        def update_item_in_menu(menu_data):     # Hàm đệ quy để tìm và cập nhật menu item
            for item in menu_data['items']:
                if item['id'] == item_id:
                    item.update(properties)
                    return True
            return False

        # Duyệt qua tất cả menu
        for menu_name, menu_data in self.menu_structure.items():
            if update_item_in_menu(menu_data):
                return True

        return False

    def _create_menu_handles(self):
        """Tạo menu handles từ cấu trúc menu
        Returns:
            dict: Dictionary chứa menu handles, hoặc None nếu lỗi
        """
        try:
            menu_handles = {}
            for menu_name in self.menu_structure:
                menu_handles[menu_name] = user32.CreatePopupMenu()
                if not menu_handles[menu_name]:
                    logger.error(f"Không thể tạo menu {menu_name}")
                    for handle in menu_handles.values():
                        user32.DestroyMenu(handle)
                    return None
            return menu_handles
        except Exception as e:
            logger.error(f"Lỗi khi tạo menu handles: {e}", exc_info=True)
            return None

    def _build_menu(self, menu_handles):
        """Xây dựng menu từ cấu trúc menu và handles
        Args:
            menu_handles (dict): Dictionary chứa menu handles
        """
        try:
            # Xây dựng menu
            for menu_name, menu_data in self.menu_structure.items():
                for item in menu_data['items']:
                    if 'submenu' in item:  # Đây là submenu
                        user32.AppendMenuW(menu_handles[menu_name], MF_POPUP,
                                          menu_handles[item['submenu']], item['text'])
                    else:  # Đây là item thông thường
                        user32.AppendMenuW(menu_handles[menu_name], MF_STRING,
                                          item['id'], item['text'])
        except Exception as e:
            logger.error(f"Lỗi khi xây dựng menu: {e}", exc_info=True)
            raise

    def _show_popup_menu(self, main_menu_handle):
        """Hiển thị menu popup và trả về ID của mục được chọn
        Args:
            main_menu_handle: Handle của menu chính
        Returns:
            int: ID của mục được chọn, hoặc 0 nếu không có mục nào được chọn
        """
        try:
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            user32.SetForegroundWindow(self.hwnd)

            command_id = user32.TrackPopupMenu(
                main_menu_handle,
                TPM_LEFTALIGN | TPM_VCENTERALIGN | TPM_RETURNCMD | TPM_NONOTIFY,
                pt.x, pt.y, 0, self.hwnd, None
            )

            user32.PostMessageW(self.hwnd, 0, 0, 0)
            return command_id
        except Exception as e:
            logger.error(f"Lỗi khi hiển thị menu: {e}", exc_info=True)
            return 0

    def _execute_menu_action(self, command_id):
        """Thực thi hành động tương ứng với ID menu
        Args:
            command_id (int): ID của menu item được chọn
        """
        if command_id in self.menu_actions: threading.Thread(target=self.menu_actions[command_id], daemon=True).start()

    def _cleanup_menu_handles(self, menu_handles):
        """Dọn dẹp menu handles
        Args:
            menu_handles (dict): Dictionary chứa menu handles
        """
        try:
            for handle in menu_handles.values(): user32.DestroyMenu(handle)
        except Exception as e: logger.error(f"Lỗi khi dọn dẹp menu handles: {e}", exc_info=True)

    def show_tray_menu(self):
        """Hiển thị menu tray"""
        try:
            self._update_menu_actions()     # Cập nhật ánh xạ ID với action từ cấu trúc menu

            menu_handles = self._create_menu_handles()      # Tạo menu handles
            if not menu_handles: return

            self._build_menu(menu_handles)      # Xây dựng menu

            command_id = self._show_popup_menu(menu_handles['main'])        # Hiển thị menu và nhận ID của mục được chọn

            self._execute_menu_action(command_id)        # Thực thi hành động tương ứng

            self._cleanup_menu_handles(menu_handles)        # Dọn dẹp menu handles

        except Exception as e:
            logger.error(f"Lỗi trong show_tray_menu: {e}", exc_info=True)

    # def run_tool(self, script_name, run_as_admin=False):
        # logger.warning(f"⚠️ Test run_tool ⚠️ ⚠️ {PYTHON_W}")
        # logger.warning(f"⚠️ Test run_tool ⚠️ ⚠️ {BASEDIR}")
        # logger.warning(f"⚠️ Test run_tool ⚠️ ⚠️ {script_name}")
        # try:
        #     mlp = subprocess.Popen([PYTHON_W, fr"{BASEDIR}/Tools_SHMG/{script_name}"], creationflags=subprocess.CREATE_NO_WINDOW)
        # except Exception as e:
        #     logger.error(f"❌ error from {e}", exc_info=e)
        # logger.debug(f"run_tool called{mlp}")


    def run_tool(self, script_name, run_as_admin=False):
        script_path = fr"{SET_TEMP_PATH}\{script_name}"

        def create_temp_batch_file(script_path):
            batch_content = f'@echo off\n"{PYTHON_W}" "{script_path}"'
            batch_path = fr"{SET_TEMP_PATH}\temp_runner.bat"
            with open(batch_path, "w", encoding='utf-8') as batch_file:
                batch_file.write(batch_content)
            return batch_path

        def create_temp_vbs_file(batch_path):
            vbs_content = f"""Set WshShell = CreateObject("WScript.Shell")
                            WshShell.Run chr(34) & "{batch_path}" & chr(34), 0
                            Set WshShell = Nothing"""
            vbs_path = fr"{SET_TEMP_PATH}\temp_runner.vbs"
            with open(vbs_path, "w", encoding='utf-8') as vbs_file:
                vbs_file.write(vbs_content)
            return vbs_path

        def run_as_user(script_path):
            try:
                batch_path = create_temp_batch_file(script_path)
                vbs_path = create_temp_vbs_file(batch_path)

                subprocess.Popen(
                    ['explorer.exe', vbs_path],
                    shell=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                )
            except Exception as e:
                logger.error(f"❌ Error running as user: {e}", exc_info=True)

        try:
            if run_as_admin:
                with open("output.log", "w") as out, open("error.log", "w") as err:
                    mlp = subprocess.Popen([PYTHON_W, script_path],
                                        creationflags=subprocess.CREATE_NO_WINDOW,
                                        stdout=out, stderr=err)
                    mlp.wait()
            else:
                run_as_user(script_path)

        except Exception as e:
            logger.error(f"❌ error from {e}", exc_info=e)








    def run_pyfile(self):
        """Chạy file Python từ clipboard hoặc đường dẫn"""
        try:
            # Lấy đường dẫn file từ clipboard
            path_copy = get_clipboard_file_paths()
            runfile = path_copy if path_copy is not None else pyperclip.paste()
            runfile = runfile.strip().strip('"\'')

            # Kiểm tra nếu là file .exe
            if runfile.lower().endswith('.exe') and len(runfile) > 4:
                logger.warning(f"⚠️ Phát hiện file .exe: {runfile}")
                admin_privileges = "YES" if ctypes.windll.shell32.IsUserAnAdmin() else "NO"
                # Chạy file .exe trong cmd mới
                subprocess.Popen(
                    f'start cmd /K "echo Admin privileges: {admin_privileges} && "{runfile}""',
                    shell=True
                )
                return

            # Kiểm tra tồn tại của Python interpreter và file script
            if not os.path.exists(PYTHON):
                logger.error(f"Python interpreter không tìm thấy: {PYTHON}")
                show_auto_close_messagebox(f"Python interpreter không tìm thấy: {PYTHON}")
                return

            if not os.path.exists(runfile):
                logger.error(f"Script không tìm thấy: {runfile}")
                show_auto_close_messagebox(f"Script không tìm thấy: {runfile}")
                return

            # Xây dựng lệnh chạy dựa trên quyền admin
            if ctypes.windll.shell32.IsUserAnAdmin():
                run_cmdline = fr'start cmd /K "net session >nul 2>&1 && (echo Admin privileges: YES && "{PYTHON}" "{runfile}") || (echo Admin privileges: NO)"'
                logger.info(f"Chạy với quyền Admin: {run_cmdline}")
            else:
                run_cmdline = fr'start cmd /K "echo Admin privileges: NO && "{PYTHON}" "{runfile}""'
                logger.info(f"Chạy không có quyền Admin: {run_cmdline}")


            threading.Thread(                                           # Chạy lệnh trong thread riêng để không block UI
                target=lambda: subprocess.Popen(run_cmdline, shell=True),
                daemon=True
            ).start()

        except Exception as e:
            logger.error(f"❌ Lỗi khi chạy file Python: {e}", exc_info=e)
            show_auto_close_messagebox(f"Lỗi khi chạy file: {str(e)}")

    def _handle_wm_killfocus(self, hwnd, msg, wparam, lparam):
        """Xử lý thông điệp WM_KILLFOCUS"""
        self.is_active = False
        self.is_hovered = False
        self.is_clicked = False
        self.update_window_attributes()
        logger.debug("_handle_wm_killfocus called")
        return 0

    def on_tray_left_click(self):
        now = time.time()
        if now - self.last_click_time < self.double_click_threshold:
            self.on_double_click()
        else:
            self.on_single_click()
        self.last_click_time = now

    def on_single_click(self):
        print("🖱️ Click thường (single click)")
        """
        self.is_clicked = False
        self.update_window_attributes()
        if user32.IsWindowVisible(self.hwnd): user32.ShowWindow(self.hwnd, 0)                   # Ẩn cửa sổ, # Kiểm tra nếu cửa sổ đang ẩn thì hiển thị, nếu đang hiện thì ẩn đi
        else:
            user32.ShowWindow(self.hwnd, SW_RESTORE)  # Hiện cửa sổ
            user32.SetForegroundWindow(self.hwnd)  # Đưa cửa sổ lên trước
        """

    def on_double_click(self):
        print("🖱️🖱️ Double click rồi đó tình yêu!")
        cb.html_to_markd()

    def _handle_wm_trayicon(self, hwnd, msg, wparam, lparam):
        """Xử lý thông điệp WM_TRAYICON"""
        event = lparam & 0xFFFFFFFF
        if event == hm.WM_RBUTTONUP:
            self.show_tray_menu()

        elif event == hm.WM_LBUTTONUP:
            # logger.debug("WM_LBUTTONUP trên tray icon")
            self.on_tray_left_click()

            """
            self.is_clicked = False
            self.update_window_attributes()
            if user32.IsWindowVisible(self.hwnd): user32.ShowWindow(self.hwnd, 0)                   # Ẩn cửa sổ, # Kiểm tra nếu cửa sổ đang ẩn thì hiển thị, nếu đang hiện thì ẩn đi
            else:
                user32.ShowWindow(self.hwnd, SW_RESTORE)  # Hiện cửa sổ
                user32.SetForegroundWindow(self.hwnd)  # Đưa cửa sổ lên trước
            """

        # Xử lý các sự kiện chuột giữa (nếu cần)
        elif event == hm.WM_MBUTTONUP:
            # logger.debug("WM_MBUTTONUP trên tray icon")
            self.handle_middle_click()       # Thực hiện hành động đặc biệt khi nhấn chuột giữa
            return 0

        elif event == hm.WM_LBUTTONDOWN:
            # logger.debug("WM_LBUTTONDOWN trên tray icon")
            self.is_clicked = True
            self.update_window_attributes()
        return 0


    def toggle_window_visibility(self):
        """Chuyển đổi trạng thái hiển thị của cửa sổ"""
        if user32.IsWindowVisible(self.hwnd):
            # Ẩn cửa sổ nếu đang hiển thị
            user32.ShowWindow(self.hwnd, 0)  # SW_HIDE
            logger.debug("Ẩn cửa sổ")
        else:
            # Hiện cửa sổ nếu đang ẩn
            user32.ShowWindow(self.hwnd, SW_RESTORE)
            user32.SetForegroundWindow(self.hwnd)
            logger.debug("Hiện cửa sổ và đưa lên trước")

    def handle_middle_click(self):
        """Xử lý khi nhấn chuột giữa vào tray icon"""
        # Ví dụ: Hiển thị thông tin phiên bản hoặc thực hiện hành động đặc biệt
        logger.info("Xử lý sự kiện chuột giữa")

        # Ví dụ: Hiển thị thông tin phiên bản
        if hasattr(self, 'custom_tooltip'):
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))

            version_info = "Tray Tools SHMG\nPhiên bản: 1.0.0"
            self.custom_tooltip.show_with_style(
                version_info,
                pt.x + 15,
                pt.y + 15,
                style="info",
                duration=2.0
            )

    @register_message(WM_TRAYICON)
    def tray_wnd_proc(self, hwnd, msg, wparam, lparam):
        """Xử lý tất cả thông điệp gửi đến cửa sổ, được gọi bởi wnd_proc

        Args:
            hwnd (int): Handle của cửa sổ nhận thông điệp
            msg (int): Mã thông điệp Windows
            wparam (int): Tham số word, ý nghĩa phụ thuộc vào loại thông điệp
            lparam (int): Tham số long, ý nghĩa phụ thuộc vào loại thông điệp

        Returns:
            int: Kết quả xử lý thông điệp, 0 nếu thông điệp được xử lý thành công
        """
        try:
            if msg == hm.WM_SETFOCUS:
                return self._handle_wm_setfocus(hwnd, msg, wparam, lparam)
            elif msg == hm.WM_KILLFOCUS:
                return self._handle_wm_killfocus(hwnd, msg, wparam, lparam)
            elif msg == WM_USER + 20:
                return self._handle_wm_trayicon(hwnd, msg, wparam, lparam)
            elif msg == hm.WM_MOUSEMOVE:
                return self._handle_wm_mousemove(hwnd, msg, wparam, lparam)
            elif msg == hm.WM_MOUSELEAVE:
                return self._handle_wm_mouseleave(hwnd, msg, wparam, lparam)
            elif msg == hm.WM_DESTROY:
                self.cleanup()
                user32.PostQuitMessage(0)
                return 0
            elif msg == hm.WM_CLOSE:
                logger.info("Cửa sổ đang được đóng - chỉ ẩn đi")
                user32.ShowWindow(self.hwnd, 0)  # SW_HIDE
                return 0
            elif msg == WM_TASKBARCREATED:
                logger.info("Explorer khởi động lại - Đăng ký lại tray icon")
                self.register_tray_icon()
                return 0
            else:
                return user32.DefWindowProcW(hwnd, msg, wintypes.WPARAM(wparam), wintypes.LPARAM(lparam))
        except Exception as e:
            logger.error(f"Lỗi nghiêm trọng trong tray_wnd_proc: {e}", exc_info=True)
            # Không thoát ứng dụng, chỉ ghi log và tiếp tục
            return user32.DefWindowProcW(hwnd, msg, wintypes.WPARAM(wparam), wintypes.LPARAM(lparam))

    def _handle_wm_mousemove(self, hwnd, msg, wparam, lparam):
        """Xử lý thông điệp WM_MOUSEMOVE"""
        try:
            # Bắt đầu theo dõi sự kiện chuột rời nếu chưa theo dõi
            if not self._tracking_mouse:
                trackmouseevent = TRACKMOUSEEVENT()
                trackmouseevent.cbSize = ctypes.sizeof(TRACKMOUSEEVENT)
                trackmouseevent.dwFlags = hm.TME_LEAVE
                trackmouseevent.hwndTrack = hwnd
                if user32.TrackMouseEvent(ctypes.byref(trackmouseevent)):
                    self._tracking_mouse = True
                    logger.debug("Bắt đầu theo dõi sự kiện chuột rời")
                else:
                    logger.warning("Không thể bắt đầu theo dõi sự kiện chuột rời")

            # Lấy tọa độ chuột trong client area
            client_x = ctypes.c_short(lparam & 0xFFFF).value
            client_y = ctypes.c_short(lparam >> 16).value

            # Lấy kích thước client area
            rect = wintypes.RECT()
            user32.GetClientRect(hwnd, ctypes.byref(rect))

            # Kiểm tra xem chuột có trong client area không
            if 0 <= client_x < rect.right and 0 <= client_y < rect.bottom:
                # Chuột đang ở trong client area
                if not self.is_hovered:
                    logger.debug("Chuột di vào khu vực cửa sổ")
                    self.is_hovered = True
                    self.update_window_attributes()
            else:
                # Chuột đã rời khỏi client area
                # Lưu ý: Thông thường sự kiện này sẽ được xử lý bởi WM_MOUSELEAVE
                # Nhưng chúng ta vẫn xử lý ở đây để đảm bảo
                if self.is_hovered:
                    logger.debug("Chuột đã rời khỏi khu vực cửa sổ (phát hiện bởi WM_MOUSEMOVE)")
                    self.is_hovered = False
                    self.update_window_attributes()
            return 0
        except Exception as e:
            logger.error(f"Lỗi trong _handle_wm_mousemove: {e}", exc_info=True)
            return 0

    def _handle_wm_mouseleave(self, hwnd, msg, wparam, lparam):
        """Xử lý thông điệp WM_MOUSELEAVE"""
        logger.debug(" ℹ️ ℹ️ WM_MOUSELEAVE nhận được")
        self._tracking_mouse = False
        if self.is_hovered:
            self.is_hovered = False
            self.update_window_attributes()
        return 0

    def _handle_tray_left_down(self):
        """Xử lý nhấn giữ chuột trái vào tray icon"""
        try:
            self.is_clicked = True
            self.update_window_attributes()
            return 0
        except Exception as e:
            logger.error(f"Error in _handle_tray_left_down: {e}")
            return 0
        logger.debug("_handle_tray_left_down called")

    async def focus_window_async(self):
        logger.info("Đang focus vào cửa sổ")
        await asyncio.sleep(1)
        logger.info("Cửa sổ đã được focus!")
        logger.debug("focus_window_async called")

    async def focus_window(self):
        logger.info("Đang focus vào cửa sổ")
        await self.focus_window_async()
        logger.info("Cửa sổ đã được focus!")
        logger.debug("focus_window called (async)")

    def focus_window(self):
        logger.info("Đang focus vào cửa sổ")
        threading.Thread(target=lambda: asyncio.run(self.focus_window_async()), daemon=True).start()
        logger.info("Cửa sổ đã được focus!")
        logger.debug("focus_window called (thread)")

    def register_tray_icon(self):
        """Đăng ký lại icon trên khay hệ thống"""
        try:
            # self.WM_TRAYICON = WM_USER + 20
            self.nid = NOTIFYICONDATA()
            self.nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
            self.nid.hwnd = self.hwnd  # Cửa sổ liên kết
            self.nid.uID = 1  # ID của biểu tượng
            self.nid.uFlags = 0x3  # NIF_MESSAGE | NIF_ICON
            self.nid.uCallbackMessage = WM_USER + 20
            self.nid.hIcon = self.icon_handle  # Đã được khởi tạo trước đó
            self.nid.szTip = b"My System Tray Icon"

            result = shell32.Shell_NotifyIconA(NIM_ADD, ctypes.byref(self.nid))
            if not result:
                error = ctypes.get_last_error()
                logger.error(f"Không thể đăng ký lại tray icon. Mã lỗi: {error}", exc_info=True)
                raise ctypes.WinError()

            logger.info("Đã đăng ký lại tray icon thành công.")
        except Exception as e: logger.error(f"Lỗi khi đăng ký lại tray icon: {e}", exc_info=True)
        logger.debug("register_tray_icon called")

    def _load_icon(self, icon_path):
        """Tải biểu tượng từ file hoặc sử dụng biểu tượng mặc định"""
        if icon_path:
            return user32.LoadImageW(None, icon_path, 1, 0, 0, 0x10)  # LR_LOADFROMFILE
        return user32.LoadIconW(0, 32512)  # IDI_APPLICATION
        logger.debug("_load_icon called")

    def cleanup(self):
        """Dọn dẹp tài nguyên trước khi thoát ứng dụng"""
        # Hủy các tooltip
        for tooltip_name in ['custom_tooltip', 'status_tooltip']:
            if hasattr(self, tooltip_name):
                try:
                    getattr(self, tooltip_name).destroy()
                    logger.info(f"✅ Đã hủy {tooltip_name}")
                except Exception as e:
                    logger.error(f"Lỗi khi hủy {tooltip_name}: {e}")

        # Hủy đăng ký hook bàn phím
        try:
            self.disable_keyboard_hook()
            logger.info("✅ Đã hủy keyboard hook")
        except Exception as e:
            logger.error(f"Lỗi khi hủy keyboard hook: {e}")

        # Hủy tray icon
        try:
            self.remove_tray_icon()
            logger.info("✅ Đã hủy tray icon")
        except Exception as e:
            logger.error(f"Lỗi khi hủy tray icon: {e}")

        # Hủy đăng ký các phím tắt
        try:
            for hotkey_id in [1, 2]:  # Liệt kê tất cả ID phím tắt đã đăng ký
                user32.UnregisterHotKey(self.hwnd, hotkey_id)
            logger.info("✅ Đã hủy đăng ký các phím tắt")
        except Exception as e:
            logger.error(f"Lỗi khi hủy đăng ký phím tắt: {e}")

    def remove_tray_icon(self):
        try:
            if hasattr(self, 'nid') and self.nid:
                result = shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(self.nid))
                if result:
                    logger.info("✅ Đã xóa icon khỏi khay hệ thống thành công.")
                    self.nid = None
                else:
                    error = ctypes.get_last_error()
                    logger.error(f"❌ Không thể xóa tray icon. Mã lỗi: {error}")
            else:
                logger.warning("⚠️ Không có tray icon để xóa.")
        except Exception as e:
            logger.error(f"Lỗi khi xóa tray icon: {e}", exc_info=True)
        logger.debug("remove_tray_icon called")

    def exit_app(self):
        """Dừng ứng dụng"""
        logger.warning("Đang dọn dẹp tray icon và cửa sổ.")
        try:
            # Ghi log trước khi thực hiện các thao tác dọn dẹp
            logger.info("Bắt đầu quá trình dọn dẹp tài nguyên...")

            # Dọn dẹp các thread
            self.cleanup_threads()

            # Dọn dẹp tray icon và các tài nguyên khác
            self.remove_tray_icon()
            self.cleanup()

            # Hủy cửa sổ
            if self.hwnd:
                logger.info("Đang hủy cửa sổ...")
                user32.SendMessageW(self.hwnd, WM_DESTROY, 0, 0)
                user32.DestroyWindow(self.hwnd)
                logger.info("Cửa sổ đã bị phá hủy.")

            logger.info("Tất cả tài nguyên đã được dọn dẹp. Thoát ứng dụng.")

            # Thoát ứng dụng
            sys.exit(0)
        except Exception as e:
            logger.error(f"Lỗi khi thoát ứng dụng: {e}")
            # Trong trường hợp lỗi nghiêm trọng, buộc thoát
            os._exit(1)

    def cleanup_threads(self):
        """Dừng tất cả các luồng nền đang chạy"""
        if hasattr(self, '_threads') and self._threads: 
            self._thread_stop_event.set()       # Đặt sự kiện dừng để thông báo cho tất cả thread
            for thread in self._threads.copy():         # Tạo bản sao danh sách thread để tránh lỗi khi thread tự xóa khỏi danh sách
                if thread.is_alive():
                    logger.info(f"Đang chờ luồng {thread.name} dừng...")
                    thread.join(timeout=1)  # Chờ tối đa 1 giây
                    if thread.is_alive():  # Nếu vẫn không dừng, log cảnh báo
                        logger.warning(f"Luồng {thread.name} không thể dừng trong thời gian chờ!")
            self._threads.clear()
            self._thread_stop_event.clear()
            logger.info("Tất cả luồng nền đã được xử lý.")
        logger.debug("cleanup_threads called")

    def create_managed_thread(self, target, args=(), kwargs=None, daemon=True, name=None):
        """Tạo và quản lý thread

        Args:
            target: Hàm mục tiêu của thread
            args: Tham số vị trí cho hàm mục tiêu
            kwargs: Tham số từ khóa cho hàm mục tiêu
            daemon: Có đặt thread là daemon không
            name: Tên của thread

        Returns:
            thread: Thread đã được tạo
        """
        if kwargs is None:
            kwargs = {}

        # Bọc hàm mục tiêu để kiểm tra sự kiện dừng
        def wrapped_target(*args, **kwargs):
            try:
                # Truyền sự kiện dừng vào kwargs nếu hàm mục tiêu chấp nhận nó
                if 'stop_event' in inspect.signature(target).parameters:
                    kwargs['stop_event'] = self._thread_stop_event
                return target(*args, **kwargs)
            except Exception as e:
                logger.error(f"Lỗi trong thread {threading.current_thread().name}: {e}", exc_info=True)
            finally:
                # Xóa thread khỏi danh sách khi kết thúc
                with threading.Lock():
                    if threading.current_thread() in self._threads:
                        self._threads.remove(threading.current_thread())

        # Tạo thread mới
        thread = threading.Thread(
            target=wrapped_target,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
            name=name
        )

        # Thêm vào danh sách quản lý
        self._threads.append(thread)

        return thread


        

    def open_cmd_at_path(self, path):
        # logger.warning("⚠️ Test open_cmd_at_path")
        try:
            pathopen = fr"{path}"       # Normalize path
            subprocess.Popen(f'start cmd /K "cd /d {pathopen} && net session >nul 2>&1 && (echo Admin privileges: YES) || (echo Admin privileges: NO)"', shell=True)        # Open CMD at specified path
        except Exception as e:
            logger.error(f"❌ error from open_cmd_at_path", exc_info=e)
        logger.debug("open_cmd_at_path called")

    async def async_subprocess_run(self, *cmd):
        print(f">>>>>>> {cmd}", flush=True)
        process = await asyncio.create_subprocess_exec(*cmd, shell=False)
        await process.communicate()
        logger.debug("async_subprocess_run called")

    async def async_subprocess_run_shell_await(self, *cmd):
        print(f"{cmd}", flush=True)
        logger.debug("async_subprocess_run_shell_await called")

    # Sửa trong phương thức on_destroy
    def on_destroy(self):
        """Xóa tray icon và gửi thông báo WM_QUIT"""
        logger.info("Bắt đầu xử lý on_destroy.")
        if hasattr(self, 'nid') and self.nid:
            result = shell32.Shell_NotifyIconA(NIM_DELETE, ctypes.byref(self.nid))
            if result:
                logger.info("Tray icon đã được xóa thành công.")
            else:
                logger.warning("Xóa tray icon thất bại.")
        else:
            logger.warning("Không tìm thấy tray icon trong on_destroy.")

        user32.PostQuitMessage(0)
        logger.info("Đã gửi WM_QUIT từ on_destroy.")
        return 0  # Trả về 0 để xử lý thông điệp
        logger.debug("on_destroy called")

    def remove_tray_icon(self):
        try:
            if hasattr(self, 'nid') and self.nid:
                result = shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(self.nid))
                if result:
                    logger.info("✅ Đã xóa icon khỏi khay hệ thống thành công.")
                    self.nid = None
                else:
                    error = ctypes.get_last_error()
                    logger.error(f"❌ Không thể xóa tray icon. Mã lỗi: {error}")
            else:
                logger.warning("⚠️ Không có tray icon để xóa.")
        except Exception as e:
            logger.error(f"Lỗi khi xóa tray icon: {e}", exc_info=True)
        logger.debug("remove_tray_icon called")





if __name__ == "__main__":
    # Instantiate handlers
    mouse_handler = MouseHandler()
    state_handler = WindowStateHandler()
    tray_icon_handler = TrayIconHandler(icon_path="your-icon-path.ico", tooltip="Tray App")

    # Kết hợp tất cả handler
    composite_handler = CompositeHandler()
    composite_handler.add_handler(mouse_handler)
    composite_handler.add_handler(state_handler)
    composite_handler.add_handler(tray_icon_handler)

    # Window manager để quản lý thông điệp/handler
    window_manager = WindowManager()
    window_manager.register_window(tray_icon_handler.hwnd, composite_handler)

    # Event loop cho ứng dụng
    msg = wintypes.MSG()
    while True:
        result = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)

        if result <= 0: break         # 0 = WM_QUIT, -1 = error

        # Quan trọng: xử lý menu đặc biệt
        if not (user32.IsDialogMessageW(None, ctypes.byref(msg)) or
               user32.TranslateAcceleratorW(None, None, ctypes.byref(msg))):
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    logger.debug("Main loop exited")














        #     # Cập nhật thuộc tính cửa sổ
        #     user32.SetWindowLongPtrA(self.hwnd, -20, user32.GetWindowLongPtrA(self.hwnd, -20) | WS_EX_LAYERED)
        #     # self.update_window_attributes()

        #     # self.restart_with_admin_rights()

        #     # Thêm hai dòng này để hiển thị cửa sổ lên màn hình
        #     # user32.ShowWindow(self.hwnd, SW_RESTORE)
        #     # user32.UpdateWindow(self.hwnd)

        #     logger.info(f"Cửa sổ được tạo thành công hwnd = {self.hwnd}")
        # except Exception as e:
        #     logger.error(f"Lỗi trong create_window: {e}", exc_info=e)
        #     raise
        # logger.debug("create_hidden_window called")







        # try:
        #     should_be_opaque = self.is_active or self.is_hovered or self.is_clicked
        #     if self._last_opaque_state != should_be_opaque:
        #         if should_be_opaque:
        #             logger.debug(" 🕑  Đặt cửa sổ thành không trong suốt")
        #             user32.SetLayeredWindowAttributes(self.hwnd, RGB(255, 255, 0), 255, LWA_ALPHA)
        #         else:
        #             # logger.debug(" 🔵  Đặt cửa sổ thành trong suốt")
        #             user32.SetLayeredWindowAttributes(self.hwnd, 0, 102, LWA_ALPHA)  # Trong suốt 40%
        #         self._last_opaque_state = should_be_opaque
        # except Exception as e:
        #     logger.error(f"Lỗi trong update_window_attributes: {e}", exc_info=True)
        # logger.debug("update_window_attributes called")






    # """
    #     xử lý all phím
    # def keyboard_callback(self, nCode, wParam, lParam):    # Callback function xử lý sự kiện bàn phím

    #     logger.debug(f"keyboard_callback: Bắt đầu, nCode={nCode}, wParam={wParam}, lParam={lParam}")  # Thêm log

    #     if nCode == 0:  # HC_ACTION
    #         kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
    #         vk_code = kb.vkCode
    #         logger.debug(f"keyboard_callback: vkCode={vk_code}")  # Thêm log

    #         # Cập nhật trạng thái phím
    #         if wParam == 0x0100 or wParam == 0x0104:  # WM_KEYDOWN or WM_SYSKEYDOWN
    #             # Nếu phím là một trong những phím cần theo dõi
    #             if vk_code in self.key_state or any(vk_code in combo for combo in self.hotkey_combinations.values()):
    #                 if vk_code not in self.key_state:
    #                     self.key_state[vk_code] = False
    #                 self.key_state[vk_code] = True
    #                 logger.debug(f"keyboard_callback: Key {vk_code} pressed, key_state: {self.key_state}")  # Thêm log

    #                 # Kiểm tra các tổ hợp phím
    #                 current_time = time.time()
    #                 for combo_name, combo_keys in self.hotkey_combinations.items():
    #                     if all(self.key_state.get(k, False) for k in combo_keys):
    #                         # Kiểm tra thời gian giữa các lần kích hoạt để tránh trigger nhiều lần
    #                         if current_time - self.last_hotkey_time >= self.hotkey_cooldown:
    #                             logger.info(f"keyboard_callback: ⌨️ Phát hiện tổ hợp phím: {combo_name}")
    #                             self.last_hotkey_time = current_time

    #                             # Hiển thị tooltip nếu đã được khởi tạo
    #                             self.show_hotkey_tooltip(combo_name)

    #                             # Gọi phương thức xử lý tương ứng
    #                             self.handle_hotkey(combo_name)

    #         elif wParam == 0x0101 or wParam == 0x0105:  # WM_KEYUP or WM_SYSKEYUP
    #             if vk_code in self.key_state:
    #                 self.key_state[vk_code] = False
    #             logger.debug(f"keyboard_callback: Key {vk_code} released, key_state: {self.key_state}")  # Thêm log

    #     # Chuyển tiếp thông điệp cho hook tiếp theo
    #     result = user32.CallNextHookEx(None, nCode, wParam, lParam)
    #     logger.debug(f"keyboard_callback: Kết thúc, result={result}")  # Thêm log
    #     return result
    #     """



    # def on_tray_left_click(self):
    #     """Xử lý khi click chuột trái vào tray icon"""
    #     if user32.IsWindowVisible(self.hwnd): user32.ShowWindow(self.hwnd, 0)             # Ẩn cửa sổ , # Kiểm tra nếu cửa sổ đang ẩn thì hiển thị, nếu đang hiện thì ẩn đi
    #     else:
    #         user32.ShowWindow(self.hwnd, SW_RESTORE)  # Hiện cửa sổ
    #         user32.SetForegroundWindow(self.hwnd)  # Đưa cửa sổ lên trước
    #     logger.info(f"\u2705 Tray Icon left clicked!")
    #     self.update_window_attributes()
    #     logger.debug("on_tray_left_click called")





    # """
    #     xử lý all phím
    # def keyboard_callback(self, nCode, wParam, lParam):    # Callback function xử lý sự kiện bàn phím

    #     logger.debug(f"keyboard_callback: Bắt đầu, nCode={nCode}, wParam={wParam}, lParam={lParam}")  # Thêm log

    #     if nCode == 0:  # HC_ACTION
    #         kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
    #         vk_code = kb.vkCode
    #         logger.debug(f"keyboard_callback: vkCode={vk_code}")  # Thêm log

    #         # Cập nhật trạng thái phím
    #         if wParam == 0x0100 or wParam == 0x0104:  # WM_KEYDOWN or WM_SYSKEYDOWN
    #             # Nếu phím là một trong những phím cần theo dõi
    #             if vk_code in self.key_state or any(vk_code in combo for combo in self.hotkey_combinations.values()):
    #                 if vk_code not in self.key_state:
    #                     self.key_state[vk_code] = False
    #                 self.key_state[vk_code] = True
    #                 logger.debug(f"keyboard_callback: Key {vk_code} pressed, key_state: {self.key_state}")  # Thêm log

    #                 # Kiểm tra các tổ hợp phím
    #                 current_time = time.time()
    #                 for combo_name, combo_keys in self.hotkey_combinations.items():
    #                     if all(self.key_state.get(k, False) for k in combo_keys):
    #                         # Kiểm tra thời gian giữa các lần kích hoạt để tránh trigger nhiều lần
    #                         if current_time - self.last_hotkey_time >= self.hotkey_cooldown:
    #                             logger.info(f"keyboard_callback: ⌨️ Phát hiện tổ hợp phím: {combo_name}")
    #                             self.last_hotkey_time = current_time

    #                             # Hiển thị tooltip nếu đã được khởi tạo
    #                             self.show_hotkey_tooltip(combo_name)

    #                             # Gọi phương thức xử lý tương ứng
    #                             self.handle_hotkey(combo_name)

    #         elif wParam == 0x0101 or wParam == 0x0105:  # WM_KEYUP or WM_SYSKEYUP
    #             if vk_code in self.key_state:
    #                 self.key_state[vk_code] = False
    #             logger.debug(f"keyboard_callback: Key {vk_code} released, key_state: {self.key_state}")  # Thêm log

    #     # Chuyển tiếp thông điệp cho hook tiếp theo
    #     result = user32.CallNextHookEx(None, nCode, wParam, lParam)
    #     logger.debug(f"keyboard_callback: Kết thúc, result={result}")  # Thêm log
    #     return result
    #     """






# def restart_with_admin_rights():
#     """
#     Kiểm tra xem chương trình đã chạy với quyền admin chưa.
#     Nếu chưa, khởi động lại với quyền admin và thoát chương trình hiện tại.
#     Trả về True nếu đang chạy với quyền admin, False nếu đã khởi động lại.
#     """
#     try:
#         if ctypes.windll.shell32.IsUserAnAdmin():
#             # Đã có quyền admin
#             return True
#         else:
#             # Chưa có quyền admin, khởi động lại

#             python_exe = sys.executable
#             script_path = os.path.abspath(sys.argv[0])
#             params = ' '.join(f'"{arg}"' for arg in sys.argv[1:])
#             script_dir = os.path.dirname(script_path)

#             # Chuyển ổ đĩa và thư mục trước khi chạy script
#             # command = f'/k cd /d "{script_dir}" && "{python_exe}" "{script_path}" {params}'
#             command = f'/k cd /d "{script_dir}" && "{python_exe}" "{script_path}" {params} --elevated'


#             # Sử dụng ShellExecuteW để chạy với quyền admin
#             ctypes.windll.shell32.ShellExecuteW(
#                 None,                   # Không có parent window
#                 "runas",                # Chạy với quyền admin
#                 "cmd.exe",         # Đường dẫn đến interpreter Python
#                 command, # Script và tham số
#                 None,                   # Thư mục mặc định (None = thư mục hiện tại)
#                 1                       # Hiển thị cửa sổ bình thường
#             )
#             # Thoát chương trình hiện tại
#             sys.exit()
#             return False
#     except Exception as e:
#         print(f"Lỗi khi khởi động lại với quyền admin: {e}")
#         return False

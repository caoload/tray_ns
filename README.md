### 1. **Quản lý tray icon và cửa sổ**

* `create_hidden_window()`: Tạo cửa sổ ẩn để tương tác với tray icon.
* `register_tray_icon()`: Đăng ký tray icon vào thanh tác vụ.
* `remove_tray_icon()`: Xóa tray icon khi thoát ứng dụng.
* `cleanup()`: Dọn dẹp khi thoát ứng dụng.

### 2. **Xử lý các sự kiện từ tray icon**

* Click chuột (`on_single_click()`, `on_double_click()`, `handle_middle_click()`).
* Hiển thị menu tray (`show_tray_menu()`).
* Cập nhật trạng thái cửa sổ và tray icon (`update_window_attributes()`).

### 3. **Quản lý menu tray**

* `_create_menu_structure()`: Tạo cấu trúc menu.
* `_update_menu_actions()`: Ánh xạ menu với hành động.
* `_build_menu()`, `_create_menu_handles()`, `_show_popup_menu()`, `_execute_menu_action()`: Hiển thị và xử lý menu.

### 4. **Quản lý phím tắt (hotkeys)**

* `setup_keyboard_hooks()`: Thiết lập các phím tắt và mô tả.
* `enable_keyboard_hook()`, `disable_keyboard_hook()`, `toggle_keyboard_hook()`: Điều khiển kích hoạt phím tắt.
* `handle_hotkey()`: Callback xử lý các phím tắt.

### 5. **Xử lý các tác vụ liên quan**

* Chạy các tác vụ đặc biệt (`async_restart_exploder()`, `run_tool()`, `run_pyfile()`).
* Hiển thị thông báo tooltip từ tray (`EnhancedTooltip`).

[Khởi tạo TrayIconHandler]
        │
        ├───► tạo cửa sổ ẩn (create_hidden_window)
        ├───► đăng ký tray icon (register_tray_icon)
        ├───► tạo EnhancedTooltip (với hwnd cửa sổ)
        ├───► thiết lập KeyboardHookManager
        │            │
        │            └──► setup_hotkeys (Ctrl+Shift+T, Ctrl+Shift+Space, Ctrl+Enter...)
        │                 │
        │                 └──► callback handle_hotkey() ────► xử lý phím tắt
        │                                                   ├──► hiển thị/ẩn cửa sổ
        │                                                   ├──► restart explorer
        │                                                   └──► hiển thị menu tray
        └──► hiển thị menu tray (chuột phải vào tray icon)
             ├──► xây dựng menu
             ├──► hiển thị menu popup
             └──► thực thi hành động được chọn


TrayIconHandler
                  │    │    │
                  │    │    └─── EnhancedTooltip (thông báo)
                  │    └─── TrayMenuManager (menu tray)
                  │
        KeyboardHookManager
                  │
    phát hiện hotkey ──► callback handle_hotkey()
                               │
                 ┌─────────────┴───────────────┐
        EnhancedTooltip                      chạy tác vụ
   (hiển thị nhanh tooltip)        (thông qua run_async_in_thread)
                               ┌───────────┴───────────┐
                       restart_explorer          mở menu tray



* Tái sử dụng duy nhất một instance **`EnhancedTooltip`**.
* Đưa quản lý menu tray vào một class con (**`TrayMenuManager`**) để tách biệt rõ ràng.
* Dùng **`TooltipManager`** để điều phối tooltip một cách tuần tự thay vì mỗi lần đều trực tiếp gọi `EnhancedTooltip`.


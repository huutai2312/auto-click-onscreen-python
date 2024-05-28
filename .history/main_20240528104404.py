import cv2
import numpy as np
from PIL import ImageGrab
from pywinauto import Application
from pywinauto import Desktop

# Liệt kê tất cả các cửa sổ đang mở
windows = Desktop(backend="uia").windows()
for window in windows:
    print(window.window_text())

# Hàm để click vào vị trí trong cửa sổ Nox
def click_nox(x, y):
    # Khởi động ứng dụng Nox
    app = Application(backend="uia").connect(title_re=".*Nox.*")
    window = app.top_window()

    # Click vào vị trí (x, y) trong cửa sổ Nox
    window.click_input(coords=(x, y))

# Đọc ảnh mẫu mà bạn muốn phát hiện
template = cv2.imread('img/yescoin_trang/1.png', 0)
w, h = template.shape[::-1]

# Lấy screenshot màn hình bằng Pillow
screenshot = ImageGrab.grab()
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Chuyển đổi screenshot sang ảnh xám
img_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# Sử dụng phương pháp matchTemplate để tìm ảnh mẫu
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)

for pt in zip(*loc[::-1]):
    # Vẽ hình chữ nhật để xác nhận vị trí phát hiện được (tùy chọn)
    cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    # Thực hiện click chuột tại vị trí phát hiện được trong cửa sổ Nox
    click_nox(pt[0] + w // 2, pt[1] + h // 2)

# Hiển thị ảnh đã xử lý (tùy chọn)
cv2.imshow('Detected', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()

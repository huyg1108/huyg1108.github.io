from PIL import Image, ImageOps
import os
from pathlib import Path

def resize_images(directory, max_side=1000):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Kiểm tra file có phải ảnh không
        if os.path.isfile(file_path) and Path(filename).suffix.lower() in image_extensions:
            try:
                # Mở ảnh
                img = Image.open(file_path)
                # Chuẩn hóa orientation theo EXIF để tránh ảnh bị xoay sai khi lưu
                img = ImageOps.exif_transpose(img)
                width, height = img.size
                
                # Tính toán kích thước mới
                if width > max_side or height > max_side:
                    if width > height:
                        new_width = max_side
                        new_height = int((max_side / width) * height)
                    else:
                        new_height = max_side
                        new_width = int((max_side / height) * width)
                    
                    # Resize ảnh (sử dụng LANCZOS để chất lượng tốt)
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Lưu ảnh (ghi đè file gốc)
                    img_resized.save(file_path, quality=95, optimize=True)
                    print(f"✓ {filename}: {width}x{height} → {new_width}x{new_height}")
                else:
                    print(f"- {filename}: {width}x{height} (không cần resize)")
                    
            except Exception as e:
                print(f"✗ {filename}: Lỗi - {str(e)}")

if __name__ == "__main__":
    # Lấy thư mục hiện tại (nơi script này nằm)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    resize_images(current_dir)
    print("Hoàn tất!")

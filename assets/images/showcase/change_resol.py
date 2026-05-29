# from PIL import Image, ImageOps
# import os
# from pathlib import Path

# def resize_images(directory, max_side=1000):
#     image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
#     for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)
        
#         # Kiểm tra file có phải ảnh không
#         if os.path.isfile(file_path) and Path(filename).suffix.lower() in image_extensions:
#             try:
#                 # Mở ảnh
#                 img = Image.open(file_path)
#                 # Chuẩn hóa orientation theo EXIF để tránh ảnh bị xoay sai khi lưu
#                 img = ImageOps.exif_transpose(img)
#                 width, height = img.size
                
#                 # Tính toán kích thước mới
#                 if width > max_side or height > max_side:
#                     if width > height:
#                         new_width = max_side
#                         new_height = int((max_side / width) * height)
#                     else:
#                         new_height = max_side
#                         new_width = int((max_side / height) * width)
                    
#                     # Resize ảnh (sử dụng LANCZOS để chất lượng tốt)
#                     img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
#                     # Lưu ảnh (ghi đè file gốc)
#                     img_resized.save(file_path, quality=95, optimize=True)
#                     print(f"✓ {filename}: {width}x{height} → {new_width}x{new_height}")
#                 else:
#                     print(f"- {filename}: {width}x{height} (không cần resize)")
                    
#             except Exception as e:
#                 print(f"✗ {filename}: Lỗi - {str(e)}")

# if __name__ == "__main__":
#     # Lấy thư mục hiện tại (nơi script này nằm)
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     resize_images(current_dir)
#     print("Hoàn tất!")


from PIL import Image, ImageOps
import os
from pathlib import Path


def convert_all_to_webp(directory, quality=85, replace=True, lossless=False):
	"""Convert all images in directory to .webp.

	directory: path to scan (non-recursive)
	quality: 0-100 (ignored if lossless=True)
	replace: if True, delete original file after successful conversion
	lossless: use lossless webp
	"""
	image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.avif'}

	for filename in os.listdir(directory):
		src_path = os.path.join(directory, filename)
		if not os.path.isfile(src_path):
			continue

		suffix = Path(filename).suffix.lower()
		if suffix == '.webp':
			print(f"- {filename}: đã là webp, bỏ qua")
			continue
		if suffix not in image_extensions:
			continue

		try:
			img = Image.open(src_path)
			img = ImageOps.exif_transpose(img)

			# Convert mode if needed (webp doesn't support palette/CMYK well)
			if img.mode in ('P', 'RGBA', 'LA'):
				img = img.convert('RGBA')
			else:
				img = img.convert('RGB')

			dest_path = os.path.splitext(src_path)[0] + '.webp'
			save_kwargs = {'quality': quality}
			if lossless:
				save_kwargs = {'lossless': True}

			img.save(dest_path, 'WEBP', **save_kwargs)
			print(f"✓ {filename} → {os.path.basename(dest_path)}")

			if replace:
				try:
					os.remove(src_path)
				except Exception:
					pass

		except Exception as e:
			print(f"✗ {filename}: Lỗi - {e}")


if __name__ == '__main__':
	current_dir = os.path.dirname(os.path.abspath(__file__))
	# Chuyển tất cả ảnh trong thư mục này sang .webp và xóa file gốc
	convert_all_to_webp(current_dir, quality=85, replace=True, lossless=False)
	print('Hoàn tất!')



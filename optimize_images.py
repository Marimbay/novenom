from PIL import Image
import os

def optimize_image(input_path, output_path, max_size=(800, 800), quality=85):
    """Optimize an image for web use."""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if larger than max_size
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            print(f"Optimized {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error optimizing {input_path}: {str(e)}")

def main():
    # Create optimized directory if it doesn't exist
    os.makedirs('static/optimized', exist_ok=True)
    
    # Optimize logo and banner
    optimize_image('static/logo.png', 'static/optimized/logo.jpg')
    optimize_image('static/banner.png', 'static/optimized/banner.jpg')
    
    print("Image optimization complete!")

if __name__ == '__main__':
    main() 
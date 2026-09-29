import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

frames_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frames"))
files = [os.path.join(frames_dir, f) for f in sorted(os.listdir(frames_dir)) if f.endswith('.png')]

def opt_file(path):
    try:
        im = Image.open(path)
        im_p = im.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)
        tmp_path = path + '.tmp'
        im_p.save(tmp_path, 'PNG', optimize=True)
        os.replace(tmp_path, path)
    except Exception as e:
        print(f"Error optimizing {path}: {e}")

if __name__ == '__main__':
    print(f"Optimizing {len(files)} war frames for repository storage...")
    with ThreadPoolExecutor(max_workers=16) as executor:
        list(executor.map(opt_file, files))
    print("Optimization complete!")

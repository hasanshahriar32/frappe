import json
import glob
import os
import shutil

def sync():
    dist_css = "/home/frappe/frappe-bench/apps/frappe/frappe/public/dist/css"
    dist_js = "/home/frappe/frappe-bench/apps/frappe/frappe/public/dist/js"
    sites_assets_dist = "/home/frappe/frappe-bench/sites/assets/frappe/dist"
    sites_assets_img = "/home/frappe/frappe-bench/sites/assets/frappe/images"
    src_img = "/home/frappe/frappe-bench/apps/frappe/frappe/public/images"

    for p in ["/home/frappe/frappe-bench/assets/assets.json", "/home/frappe/frappe-bench/sites/assets/assets.json"]:
        if not os.path.exists(p):
            continue
        try:
            with open(p, "r") as f:
                d = json.load(f)

            for fpath in glob.glob(os.path.join(dist_css, "*.css")):
                if "map" in fpath:
                    continue
                bn = os.path.basename(fpath)
                parts = bn.split(".")
                if len(parts) >= 3 and parts[-1] == "css":
                    k = ".".join(parts[:-2] + ["css"])
                    d[k] = f"/assets/frappe/dist/css/{bn}"

            for fpath in glob.glob(os.path.join(dist_js, "*.js")):
                if "map" in fpath:
                    continue
                bn = os.path.basename(fpath)
                parts = bn.split(".")
                if len(parts) >= 3 and parts[-1] == "js":
                    k = ".".join(parts[:-2] + ["js"])
                    d[k] = f"/assets/frappe/dist/js/{bn}"

            with open(p, "w") as f:
                json.dump(d, f, indent=4)
            print(f"Successfully updated {p}")
        except Exception as e:
            print(f"Error updating {p}: {e}")

    if os.path.exists(sites_assets_dist):
        try:
            shutil.copytree("/home/frappe/frappe-bench/apps/frappe/frappe/public/dist", sites_assets_dist, dirs_exist_ok=True)
            print("Copied dist assets to sites/assets/frappe/dist")
        except Exception as e:
            print(f"Error copying dist: {e}")

    if os.path.exists(sites_assets_img) and os.path.exists(src_img):
        try:
            shutil.copytree(src_img, sites_assets_img, dirs_exist_ok=True)
            print("Copied images to sites/assets/frappe/images")
        except Exception as e:
            print(f"Error copying images: {e}")

if __name__ == "__main__":
    sync()

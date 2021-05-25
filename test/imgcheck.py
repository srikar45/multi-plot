import io, os
from PIL import Image, ImageChops, ImageStat


def imgcheck(ref_file, img2, show_diff=False, generate_ref_files=False):

    def imgdiff(img1, img2, diff_file=None, show_diff=False):

        img1 = Image.open(io.BytesIO(img1))
        img2 = Image.open(io.BytesIO(img2))

        # See https://stackoverflow.com/q/15721484 for motivation
        #  for .convert('RGB')
        imgd = ImageChops.difference(img1, img2).convert('RGB')
        stat = ImageStat.Stat(imgd)

        diff = True
        if stat.sum[0] == 0.0 and stat.sum[1] == 0.0 and stat.sum[2] == 0.0:
            diff = False

        if diff and diff_file is not None:
            imgd.save(diff_file)

        if show_diff:
            imgd.show()

        return diff


    if not os.path.exists(ref_file) or generate_ref_files:

        if not os.path.exists(ref_file):
            print('Reference file does not exist. Writing ' + ref_file)
        else:
            print('Generating reference file.')

        img2 = Image.open(io.BytesIO(img2))
        img2.save(ref_file)

        return False

    with open(ref_file, 'rb') as f:
        img1 = f.read()

    img2x = Image.open(io.BytesIO(img2))
    img2x.save(ref_file.replace(".ref.",".now."))

    diff_file = ref_file.replace(".ref.",".dif.")

    diff = imgdiff(img1, img2, diff_file=diff_file, show_diff=show_diff)
    
    if diff == False:
        print("imgcheck(): \033[32mPASS\033[0m: Images are identical.")
    else:
        print("imgcheck(): \033[0;31mFAIL\033[0m: Images differ. See diff image: " + diff_file)

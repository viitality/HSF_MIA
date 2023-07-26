import sqlite3
import cv2
import argparse
import numpy as np

## TO COMPRESS IMAGE #####
def compress_image(image, quality=95):
    _, img_encoded = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return np.array(img_encoded)


##### TO GET THE SAME SHAPE FOR BOTH IMAGES #####
def redimension(image1, image2):
    first_image = cv2.imread(image1)
    second_image = cv2.imread(image2)

    second_image_resize = cv2.resize(second_image, (first_image.shape[1], first_image.shape[0]))
    print(first_image.shape)
    print(second_image_resize.shape)

    return first_image, second_image_resize


##### CONVERT IMAGE TO BINARY ########
def image_to_blob(image):
    return sqlite3.Binary(image)

##### SAVE DATA IN DATABASE #######
def save_to_database(image1, image2):
    conn = sqlite3.connect('biopsie_renale.db')
    temp = conn.cursor()

    temp.execute("""CREATE TABLE IF NOT EXISTS Images(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Image_PAS MEDIUMBLOB,
        Image_IF MEDIUMBLOB
    )""")

    image_pas = image_to_blob(compress_image(image1))
    image_if = image_to_blob(compress_image(image2))

    temp.execute("""INSERT INTO Images (Image_PAS, Image_IF) VALUES (?, ?)""", (image_pas, image_if))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize and save images to a database.")
    parser.add_argument("image1", help="Path to the first image")
    parser.add_argument("image2", help="Path to the second image")
    args = parser.parse_args()

    image1_resize, image2_resize = redimension(args.image1, args.image2)
    save_to_database(image1_resize, image2_resize)








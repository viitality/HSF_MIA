import cv2
import numpy as np 

# INPUT 
immunofluorescence_path = "52RG_FLUO.png"
coloration_standard_path = "52RG_PAS.png"


immunofluorescence_image = cv2.imread(immunofluorescence_path)
coloration_standard_image = cv2.imread(coloration_standard_path)

# Resize to get the same shape
immunofluorescence_image_resized = cv2.resize(immunofluorescence_image, (coloration_standard_image.shape[1], coloration_standard_image.shape[0]))

# alignement 
opacity = 0.7  # adjust (between 0 and 1)
composite_image = cv2.addWeighted(coloration_standard_image, 1 - opacity, immunofluorescence_image_resized, opacity, 0)

composite_image_path = "image_composite.png"
cv2.imwrite(composite_image_path, composite_image)


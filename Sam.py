import os
import json
import numpy as np
import sys
import cv2
import torch
import torchvision
# pip install 'git+https://github.com/facebookresearch/segment-anything.git' # type: ignore
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor


class SamGenerator:
    def __init__(self):
        sys.path.append("")
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"

        self.model_path = 'sam_vit_h_4b8939.pth'
        self.sam_checkpoint = "sam_vit_h_4b8939.pth"

        self.model_type = "vit_h"

        self.sam = sam_model_registry[self.model_type](checkpoint=self.sam_checkpoint)
        self.sam.to(device=self.device)
        self.mask_generator = SamAutomaticMaskGenerator(
            model=self.sam,
            points_per_side=16,
            pred_iou_thresh=0.86,
            stability_score_thresh=0.92,
            crop_n_layers=1,
            crop_n_points_downscale_factor=2,
            min_mask_region_area=100,  # Requires open-cv to run post-processing
        )

    def get_avg_color_per_mask(self, original_img, masks):
        avg_colors = []
        for mask in masks:
            # Ensure the mask is binary
            binary_mask = mask.astype(bool)

            # Extract the regions of the original image corresponding to the mask
            masked_img = original_img * np.expand_dims(binary_mask, axis=-1)

            # Compute the average color within the masked region
            avg_color = np.mean(masked_img[binary_mask], axis=0)
            avg_colors.append(avg_color)
        return avg_colors

    def generate(self, file_path):
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        masks = self.mask_generator.generate(image)
        return self.get_segment_info(image, masks)

    def get_segment_info(self, img, anns):
        """
        Compute information about each segment of the original image.

        Parameters:
            original_img (np.array): The original image, with shape (H, W, C).
            masks (list): A list of binary masks, each with shape (H, W).

        Returns:
            str: A JSON string containing information about each segment.
        """
        # anns = self.mask_generator.generate(img)
        sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)

        masks = [ann['segmentation'] for ann in sorted_anns]
        cords = [ann['point_coords'] for ann in sorted_anns]
        avg_colors = self.get_avg_color_per_mask(img, masks)

        segment_info = []
        for i, (mask, color) in enumerate(zip(masks, avg_colors)):
            area = np.sum(mask)  # Sum of all pixels in the mask gives the area
            segment_info.append({
                'segment': {
                    'idx': i,
                    'pixel_area': int(area),
                    'avg_color': color.tolist(),
                    'cords': cords[i]
                }
            })

            with open("test.txt", "w") as outfile:
                json.dump(segment_info, outfile)
            # string = json.dumps(segment_info, indent=2, separators=(',', ':'))'


if __name__ == "__main__":
    sam = SamGenerator()
    print(sam.generate('agcar_fly-1920x1080p30-0000-0899/agcar_fly-1920x1080p30.0000.png'))

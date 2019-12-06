import numpy as np
import cv2 as cv

def runGrabCut(image, boxes, indices):
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgbModel = np.zeros((1, 65), np.float64)

    # ensure at least one detection exists
    if len(indices) == 1:
        # loop over the indices we are keeping
        for i in indices.flatten():
            # extract the bounding box coordinates
            rect = (boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3])
            print(rect)

            # apply GrabCut
            cv.grabCut(image, mask, rect, bgdModel, fgbModel, 5, cv.GC_INIT_WITH_RECT)

            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            image = image * mask2[:, :, np.newaxis]

            return image

    else:
        print("not implemented")

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image")
    ap.add_argument("-y", "--yolo", required=True,
        help="base path to YOLO directory")
    ap.add_argument("-c", "--confidence", type=float, default=0.25,
        help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold", type=float, default=0.45,
        help="threshold when applying non-maxima suppression")
    args = vars(ap.parse_args())

    import yolo

    img, boxes, idxs = yolo.runYOLODetection(args)

    image = GrabCut(img, boxes, idxs)

    # show the output image
    #cv.namedWindow("Image", cv.WINDOW_NORMAL)
    #cv.resizeWindow("image", 1920, 1080)
    cv.imshow("Image", image)
    cv.imwrite("predictions.jpg", image)
    cv.waitKey(0)


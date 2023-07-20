from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import img_to_array
import imutils
import cv2 as cv
from test import solve
import copy
from PIL import Image


def find_puzzle(image, debug=False):
	gray = cv.cvtColor(src=image, code=cv.COLOR_BGR2GRAY)
	blurred = cv.GaussianBlur(src=gray, ksize=(7,7), sigmaX=3)

	thresh = cv.adaptiveThreshold(src=blurred, maxValue=255, 
			       adaptiveMethod=cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
				   thresholdType=cv.THRESH_BINARY, blockSize=11, C=2)
	thresh = cv.bitwise_not(src=thresh)  # Contours become white

	contours = cv.findContours(image=thresh.copy(), mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(cnts=contours)
	contours = sorted(contours, key=cv.contourArea, reverse=True)

	puzzle_contour = None
	for contour in contours:
		perimeter = cv.arcLength(curve=contour, closed=True)
		estimate = cv.approxPolyDP(curve=contour, epsilon=0.02*perimeter, closed=True)

		if len(estimate) == 4:
			puzzle_contour = estimate
			break

	if puzzle_contour is None:
		raise Exception(("Could not find Sudoku puzzle outline. "
			"Try debugging your thresholding and contour steps."))

	puzzle = four_point_transform(image=image, pts=puzzle_contour.reshape(4, 2))
	warped = four_point_transform(image=gray,  pts=puzzle_contour.reshape(4, 2))
	
	if debug:
		cv.imshow("Puzzle Input", image)
		cv.waitKey(0)

		cv.imshow("Puzzle Gray", gray)
		cv.waitKey(0)

		cv.imshow("Puzzle Blurred", blurred)
		cv.waitKey(0)

		cv.imshow("Puzzle Thresh", thresh)
		cv.waitKey(0)

		output = image.copy()
		cv.drawContours(image=output, contours=[puzzle_contour], contourIdx=-1, color=(255, 0, 0), thickness=3)
		cv.imshow("Puzzle Outline", output)
		cv.waitKey(0)

		cv.imshow("Puzzle Transform", puzzle)
		cv.waitKey(0)

		cv.imshow("Puzzle Warped", warped)
		cv.waitKey(0)
	return (puzzle, warped)


def extract_digit(cell, debug=False):
	_, thresh = cv.threshold(src=cell, thresh=0, maxval=255, type= cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
	thresh = clear_border(thresh)

	contours = cv.findContours(image=thresh.copy(), mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(cnts=contours)

	# Empty cell
	if len(contours) == 0:
		return None

	# Get largest contour
	mask = np.zeros(thresh.shape, dtype="uint8")
	contour = max(contours, key=cv.contourArea)
	cv.drawContours(image=mask, contours=[contour], contourIdx=-1, color=255, thickness=-1)

	h, w = thresh.shape
	if cv.countNonZero(mask) / float(w * h) < 0.03:  # Likely just noise --> 0
		return None

	digit = cv.bitwise_and(src1=thresh, src2=thresh, mask=mask)  # Why not just mask

	if debug:
		cv.imshow("Cell Thresh", thresh)
		cv.waitKey(0)
		cv.imshow("Digit", digit)
		cv.waitKey(0)

	return digit


def visualize(image):
    puzzleImage, warped = find_puzzle(image, debug=False)
    board = np.zeros((9, 9), dtype="int")
    stepX = warped.shape[1] // 9
    stepY = warped.shape[0] // 9
    cellLocs = []
    model = load_model('models/digit_classifier2.h5', compile=False)
    for y in range(0, 9):
        row = []
        for x in range(0, 9):
            startX = x * stepX
            startY = y * stepY
            endX = (x + 1) * stepX
            endY = (y + 1) * stepY
            row.append((startX, startY, endX, endY))

            cell = warped[startY:endY, startX:endX]
            digit = extract_digit(cell, debug=False)
            if digit is not None:
                roi = cv.resize(digit, (28, 28))
                roi = roi.astype("float") / 255.0
                # roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                # classify the digit and update the Sudoku board with the
                # prediction
                predictions = model.predict(roi, verbose=0)
                pred = predictions.argmax(axis=1)[0]
                if pred == 8 and predictions[0][6] > 0.00002:  ## 6 is barely recognized
                    pred = 6
                board[y, x] = pred
        # add the row to our cell locations
        cellLocs.append(row)
	
    solution = solve(board)
    # loop over the cell locations and board
    for r, (cellRow, boardRow) in enumerate(zip(cellLocs, solution)):
        # loop over individual cell in the row
        for c, (box, digit) in enumerate(zip(cellRow, boardRow)):
            # unpack the cell coordinates
            startX, startY, endX, endY = box
            # compute the coordinates of where the digit will be drawn
            # on the output puzzle image
            textX = int((endX - startX) * 0.33)
            textY = int((endY - startY) * -0.2)
            textX += startX
            textY += endY
            # draw the result digit on the Sudoku puzzle image
            if not board[r, c]:
                cv.putText(img=puzzleImage, text=str(digit), org=(textX, textY), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1.2, color=(0, 0, 255), thickness=2)
    # show the output image
    cv.imshow("Sudoku Result", puzzleImage)
    cv.waitKey(0)
        

if __name__ == "__main__":
	from camera import take_picture
	image = take_picture()
	cv.imshow("Image", image)
	image = cv.imread('input/picca.webp')
	visualize(image=image)

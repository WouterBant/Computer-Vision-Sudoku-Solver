from tensorflow import keras
from keras.models import load_model
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2 as cv
from test import solve


def find_puzzle(image, debug=False):
	"""
	Find the Sudoku puzzle grid in the input image and perform perspective transform.

	Parameters:
		image (Mat): The input image containing the Sudoku puzzle.
		debug (bool, optional): If True, shows intermediate steps using cv2.imshow.

	Returns:
		tuple: A tuple containing the original puzzle grid and the warped grid.
	"""
	gray = cv.cvtColor(src=image, code=cv.COLOR_BGR2GRAY)  # Convert to grayscale
	blurred = cv.GaussianBlur(src=gray, ksize=(0,0), sigmaX=3)  # Blendes noise away

	thresh = cv.adaptiveThreshold(src=blurred, maxValue=255, 
			       adaptiveMethod=cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
				   thresholdType=cv.THRESH_BINARY, blockSize=13, C=2)
	thresh = cv.bitwise_not(src=thresh)  # Contours become white

	contours = cv.findContours(image=thresh.copy(), mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(cnts=contours)

	puzzle_contour = None
	for contour in sorted(contours, key=cv.contourArea, reverse=True):
		perimeter = cv.arcLength(curve=contour, closed=True)
		estimate = cv.approxPolyDP(curve=contour, epsilon=0.02*perimeter, closed=True)

		if len(estimate) == 4:  # Largest contour with 4 corners most likely to be the border
			puzzle_contour = estimate
			break

	if puzzle_contour is None:
		raise Exception(("No Sudoku was found"))

	# Get bird view of the puzzles
	puzzle = four_point_transform(image=image, pts=puzzle_contour.reshape(4, 2))
	rectified_puzzle = four_point_transform(image=gray,  pts=puzzle_contour.reshape(4, 2))
	
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
		cv.drawContours(image=output, contours=[puzzle_contour], contourIdx=-1, color=(255, 0, 0), thickness=4)
		cv.imshow("Puzzle Outline", output)
		cv.waitKey(0)

		cv.imshow("Puzzle Transform", puzzle)
		cv.waitKey(0)

		cv.imshow("Rectified Puzzle ", rectified_puzzle)
		cv.waitKey(0)
	
	return (puzzle, rectified_puzzle)


def extract_digit(cell, debug=False):
	"""
	Extract a single digit from a cell of the Sudoku grid.

	Parameters:
		cell (numpy.ndarray): The cell image containing the digit.
		debug (bool, optional): If True, shows intermediate steps using cv2.imshow.

	Returns:
		numpy.ndarray or None: The extracted digit image or None if the cell is empty or noise.
	"""
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
	if cv.countNonZero(mask) / float(h * w) <= 0.05:  # Likely just noise --> 0
		return None

	digit = cv.bitwise_and(src1=thresh, src2=thresh, mask=mask)

	if debug:
		cv.imshow("Cell Thresh", thresh)
		cv.waitKey(0)
		cv.imshow("Digit", digit)
		cv.waitKey(0)

	return digit


def visualize(image):
	"""
	Process the input image to solve the Sudoku puzzle and visualize the result.

	Parameters:
		image (numpy.ndarray): The input image containing the Sudoku puzzle.

	Returns:
		None
	"""
	# Find the Sudoku puzzle and rectify it
	puzzleImage, rectified_grid = find_puzzle(image, debug=False)

	# Initialize the board and model for digit classification
	board = np.zeros((9, 9), dtype="int")
	model = load_model('models/digit_classifier2.h5', compile=False)

	dy, dx = tuple(dim // 9 for dim in rectified_grid.shape)
	cells = []

	# Process each cell in the rectified grid
	for y in range(9):
		row = []
		for x in range(9):
			startX, startY = x * dx, y * dy
			endX, endY = (x + 1) * dx, (y + 1) * dy
			cell = rectified_grid[startY:endY, startX:endX]
			row.append((startX, startY, endX, endY))

			# Extract the digit from the cell
			digit = extract_digit(cell, debug=False)
			if digit is not None:
				# Prepare the digit for classification
				roi = cv.resize(digit, (28, 28))
				roi = roi.astype("float") / 255.0
				roi = np.expand_dims(roi, axis=0)

				# Classify the digit using the model
				predictions = model.predict(roi, verbose=0)
				estimate = predictions.argmax(axis=1)[0]

				# Handle special case: recognizing '6' with low confidence
				if estimate == 8 and predictions[0][6] > 0.00002:
					estimate = 6

				# Update the Sudoku board with the estimated digit
				board[y, x] = estimate
		
		cells.append(row)

	# Solve the Sudoku puzzle
	solution = solve(board)

	# Annotate the solution on the original image
	for r, (cellRow, boardRow) in enumerate(zip(cells, solution)):
		for c, (square, digit) in enumerate(zip(cellRow, boardRow)):
			if not board[r, c]:
				startX, startY, endX, endY = square
				textX = int((endX - startX) * 0.33) + startX
				textY = int((endY - startY) * 0.81) + startY
				cv.putText(img=puzzleImage, text=str(digit), org=(textX, textY), 
						   fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1.2,
						   color=(0, 0, 255), thickness=3)

	# Display the annotated Sudoku result
	cv.imshow("Sudoku Result", puzzleImage)
	cv.waitKey(0)


if __name__ == "__main__":
	# from camera import take_picture
	# image = take_picture()
	# cv.imshow("Image", image)
	image = cv.imread('input/picca.webp')
	visualize(image=image)

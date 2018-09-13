
#######################################
# IMAGERY IN AI
# ASSIGNMENT 1 - GEOMETRIC ANALOGIES
# GROUP 6
# DEIRDER SCULLY
# CAITLIN SYNDER
#######################################


import os
from PIL import Image
import numpy as np


# function to read in all 8 images from problem
def read_in_images(path):

    # read in analogy images
    A = np.array(Image.open(os.path.join(path, 'a.gif')).convert('1', dither=Image.NONE))
    B = np.array(Image.open(os.path.join(path, 'b.gif')).convert('1', dither=Image.NONE))
    A = 1 - A
    B = 1 - B

    # read in problem image
    C = np.array(Image.open(os.path.join(path, 'c.gif')).convert('1', dither=Image.NONE))
    C = 1 - C

    # read in answer images
    a1 = np.array(Image.open(os.path.join(path, '1.gif')).convert('1', dither=Image.NONE))
    a2 = np.array(Image.open(os.path.join(path, '2.gif')).convert('1', dither=Image.NONE))
    a3 = np.array(Image.open(os.path.join(path, '3.gif')).convert('1', dither=Image.NONE))
    a4 = np.array(Image.open(os.path.join(path, '4.gif')).convert('1', dither=Image.NONE))
    a5 = np.array(Image.open(os.path.join(path, '5.gif')).convert('1', dither=Image.NONE))
    a1 = 1 - a1
    a2 = 1 - a2
    a3 = 1 - a3
    a4 = 1 - a4
    a5 = 1 - a5

    # plt.imshow(A, cmap='binary')
    # plt.show()

    return A, B, C, a1, a2, a3, a4, a5


# function to analyze other differences, split into quadrants, and find best answer
def analyze_differences(A, B, C, a1, a2, a3, a4, a5):

    # calculate difference between maps
    rows = A.shape[0]
    cols = A.shape[1]
    ab_diff = A - B

    # compare quadrant counts for each answer by each quadrant
    compare_map = np.zeros((5, 4), dtype=float)
    for i in range(5):
        if i == 0:
            ans = C - a1
        elif i == 1:
            ans = C - a2
        elif i == 2:
            ans = C - a3
        elif i == 3:
            ans = C - a4
        elif i == 4:
            ans = C - a5
        # difference maps between each quadrant
        compare_map[i, 0] = abs(sum(sum(ab_diff[0:int(rows/2), 0:int(cols/2)])) - \
            sum(sum(ans[0:int(rows/2), 0:int(cols/2)])))
        compare_map[i, 1] = abs(sum(sum(ab_diff[0:int(rows/2), int(cols/2):cols])) - \
            sum(sum(ans[0:int(rows/2), int(cols/2):cols])))
        compare_map[i, 2] = abs(sum(sum(ab_diff[int(rows/2):rows, 0:int(cols/2)])) - \
            sum(sum(ans[int(rows/2):rows, 0:int(cols/2)])))
        compare_map[i, 3] = abs(sum(sum(ab_diff[int(rows/2):rows, int(cols/2):cols])) - \
            sum(sum(ans[int(rows/2):rows, int(cols/2):cols])))

    return compare_map


# function to find answers with min difference between differences
def best_answer(compare_map):

    # use sum or average of quadrants
    quads = np.average(compare_map, axis=1)
    # quads = np.sum(compare_map, axis=1)

    # find MIN INDEX
    # min_ans = quads.min()
    # min_idx = np.where(quads == min_ans)[0][0] + 1

    # find ODERING BY SMALLEST
    min_idx = np.argsort(quads) + 1

    # skip answers that match exactly C???

    return min_idx

# function that solves problems 
def solve_problem(problem):
    #basedir = '/Users/deirdre/Documents/ImageryAI/Assignment1/'
    basedir = '/Users/Caitlin/Desktop/Imagery in AI/Project 1/'
    path = os.path.join(basedir, 'analogy problems 1-15', problem)
    # read in images for problem
    A, B, C, a1, a2, a3, a4, a5 = read_in_images(path)
    # find rotations if any from A -> B

    # find flips if any from A -> B

    # analyze additions/subtractions/movements by quadrant
    compare_map = analyze_differences(A, B, C, a1, a2, a3, a4, a5)

    # choose best answer
    choice = best_answer(compare_map)
    #print(problem + " answer in order of highest matching:")
    answers = []
    for c in choice:
        #print("Answer " + str(c))
        answers.append(c)
    return answers

# function that prints the answers in order of highest matching
def print_answers(answers):
    for answer in answers:
        print("Answer " + str(answer))

# Main function to solve geometric analogy problems
def main():
    correct_answers = [2,2,4,4,3,1,1,2,5,5,3,3,2,4,2]
    for i in range(1,16):
        problem = 'm'
        problem = problem + str(i)
        answers = solve_problem(problem)
        if(answers[0] == correct_answers[i-1]):
            #system got the answer correct
            print("Problem " + problem + " answered correctly!")
        else:
            print("Problem " + problem + " answers in order of highest matching:")
            print_answers(answers)
    ################ ANSWERS ###############
    # Problem 1 Answer: 2 *
    # Problem 2 Answer: 2 *
    # Problem 3 Answer: 4 *
    # Problem 4 Answer: 4
    # Problem 5 Answer: 3 *
    # Problem 6 Answer: 1
    # Problem 7 Answer: 1
    # Problem 8 Answer: 2 *
    # Problem 9 Answer: 5 *
    # Problem 10 Answer: 5
    # Problem 11 Answer: 3 *
    # Problem 12 Answer: 3
    # Problem 13 Answer: 2
    # Problem 14 Answer: 4
    # Problem 15 Answer: 2 *


main()

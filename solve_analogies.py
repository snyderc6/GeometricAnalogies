from __future__ import division
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
import csv

# function to read in all 8 images from problem
def read_in_images(path):

    # read in images
    A = Image.open(os.path.join(path, 'a.gif'))
    B = Image.open(os.path.join(path, 'b.gif'))
    C = Image.open(os.path.join(path, 'c.gif'))
    a1 = Image.open(os.path.join(path, '1.gif'))
    a2 = Image.open(os.path.join(path, '2.gif'))
    a3 = Image.open(os.path.join(path, '3.gif'))
    a4 = Image.open(os.path.join(path, '4.gif'))
    a5 = Image.open(os.path.join(path, '5.gif'))
    return A, B, C, a1, a2, a3, a4, a5

# function that converts image to array map
def convert_to_array_map(image):
    array_map = np.array(image.convert('1', dither=Image.NONE))
    array_map = 1 - array_map
    return array_map


# function to get images to array maps
def images_to_array_maps(A, B, C, a1, a2, a3, a4, a5):
     # read in analogy images
    A = convert_to_array_map(A)
    B = convert_to_array_map(B)

    # read in problem image
    C = convert_to_array_map(C)

    # read in answer images
    a1 = convert_to_array_map(a1)
    a2 = convert_to_array_map(a2)
    a3 = convert_to_array_map(a3)
    a4 = convert_to_array_map(a4)
    a5 = convert_to_array_map(a5)

    return A, B, C, a1, a2, a3, a4, a5


# function to analyze other differences, split into quadrants, and find best answer
def analyze_differences(A, B, C, a1, a2, a3, a4, a5):
    #images to array maps
    A, B, C, a1, a2, a3, a4, a5 = images_to_array_maps(A, B, C, a1, a2, a3, a4, a5)
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

#function that returns the number of 1 pixels in an image
def count_pixels(image):
    pixel_count = 0
    for i in range (len(image[0])):
        pixel_count = pixel_count + sum(image[i])
    return pixel_count

# function that attempts to rotate the image A to match image B
# returns the proportion of matching pixels
def check_rotation(A, B, rot_degree):   
    # rotate A
    A_rotated = A.rotate(rot_degree)
    A_rotated = convert_to_array_map(A_rotated)
    B = convert_to_array_map(B)
    num_pixels_B = count_pixels(B)
    num_total_pos_pixels = len(A_rotated)*len(B[0])
    diff = count_pixels(abs(B-A_rotated))
    diff = check_shifts(A_rotated,B)
    #if the deg rotated is not divisible, 615 pixels are added
    #to the rotation (because the image is a square 59x59 pixel img)
    #so we need to get rid of those
    if (rot_degree == 45 or rot_degree == 135 or rot_degree == 225):
        #print("in here")
        diff = diff - 615
    return ((num_total_pos_pixels-abs(diff))/num_total_pos_pixels)


#function that returns the new array map after finding the best
# matching y shift
def check_yshifts(A,B):
    best_shifted_img = 9999999999
    best_shift_val = 9999999999999
    best_shift = 0
    for i in range(0,7):
        A_roll = np.roll(A, -i, axis = 1)
        num_total_pos_pixels = len(A)*len(B[0])
        diff = count_pixels(abs(B-A_roll))
        if best_shift_val > diff:
            best_shift_val = diff
            best_shifted_img = A_roll
            best_shift = i
        #print("diff" + str(i) + ": "  + str(diff))
        #print("best: " + str(best_shift_val))
    #print("shift picked: " + str(best_shift))
    return A_roll

#function that returns the best x shift value
def check_xshifts(A,B):
    best_shift = 9999999999
    best_shift_val = 9999999999999
    for i in range(0,7):
       # A_yroll = check_yshifts(A,B)
        A_roll = np.roll(A, -i, axis = 0)
        num_total_pos_pixels = len(A)*len(B[0])
        diff = count_pixels(abs(B-A_roll))
        if best_shift_val > diff:
            best_shift_val = diff
            best_shift = -i
    return best_shift_val

#function that returns number of different 
#pixels after x and y shifts
def check_shifts(A, B):
    best_shift = 9999999999
    best_shift_val = 9999999999999
    for i in range(0,7):
        A_yroll = check_yshifts(A,B)
        A_roll = np.roll(A_yroll, -i, axis = 0)
        num_total_pos_pixels = len(A)*len(B[0])
        diff = count_pixels(abs(B-A_roll))
        if best_shift_val > diff:
            best_shift_val = diff
            best_shift = -i
    return best_shift_val

#function that returns the proportion of matchng 
# pixels after flipping image A
def check_flips(A, B, flip_type):
    A_flipped = A.transpose(flip_type)
    A_flipped = convert_to_array_map(A_flipped)
    B = convert_to_array_map(B)
    num_pixels_B = count_pixels(B)
    num_total_pos_pixels = len(A_flipped)*len(B[0])
    diff = count_pixels(abs(B-A_flipped))
    diff = check_xshifts(A_flipped,B)
    return ((num_total_pos_pixels-abs(diff))/num_total_pos_pixels)

#return the values of the best rotation and best proportion value
def find_best_rotation(A, B):
    best_rot = 0
    best_rot_val = 0
    deg = 45
    while deg < 360:
        prop = check_rotation(A, B, deg)
        if(best_rot_val < prop):
            best_rot = deg
            best_rot_val = prop
        deg = deg + 45
    return best_rot, best_rot_val

#returns the best flip and the flip proportion 
def find_best_flip(A,B):
    flip_value_l_r = check_flips(A,B,Image.FLIP_LEFT_RIGHT)
    flip_value_t_b = check_flips(A,B,Image.FLIP_TOP_BOTTOM)
    if(flip_value_l_r > flip_value_t_b):
        return Image.FLIP_LEFT_RIGHT, flip_value_l_r
    else:
        return Image.FLIP_TOP_BOTTOM, flip_value_t_b

#function that returns the the value for all options after
# rotating the same amount as image A to B
def rot_answers(best_rot, C, a1, a2, a3, a4, a5):
    answers = [check_rotation(C,a1,best_rot), check_rotation(C, a2, best_rot), \
        check_rotation(C,a3, best_rot),check_rotation(C,a4,best_rot), \
        check_rotation(C,a5, best_rot)]
    return answers

#function that returns the the value for all options after
# flipping the same way as image A to B
def flip_answers(best_flip, C, a1, a2, a3, a4, a5):
    answers = [check_flips(C,a1,best_flip), check_flips(C, a2, best_flip), \
        check_flips(C,a3, best_flip),check_flips(C,a4,best_flip), \
        check_flips(C,a5, best_flip)]
    #print(answers)
    return answers


def find_answers(A,B,C,a1,a2,a3,a4,a5):
    A = convert_to_array_map(A)
    B = convert_to_array_map(B)
    AB_diff = abs(A-B)
    answers = [check_difference(AB_diff,C,a1), check_difference(AB_diff,C,a2), \
        check_difference(AB_diff,C,a3),check_difference(AB_diff,C,a4), \
        check_difference(AB_diff,C,a5)]
    return answers


# function that solves problems 
def solve_problem(problem):
    #basedir = '/Users/deirdre/Documents/ImageryAI/Assignment1/'
    basedir = '/Users/Caitlin/Desktop/Imagery in AI/Project 1/'
    path = os.path.join(basedir, 'analogy problems 1-15', problem)
    # read in images for problem
    A, B, C, a1, a2, a3, a4, a5 = read_in_images(path)
    # find rotations if any from A -> B
    best_rot, best_rot_val = find_best_rotation(A,B)
    #print("best: " + str(best_rot))
    #print("best val: " + str(best_rot_val))
    #print(best_rot_val)
   # print(best_rot)
    if best_rot_val > .94:
        print("using rotation to solve")
        choices = rot_answers(best_rot, C, a1, a2, a3, a4, a5)
        choice = np.argsort(choices)+1
        choice = np.fliplr([choice])[0]
    else:
         # find flips if any from A -> B
        best_flip, best_flip_val = find_best_flip(A,B)
        if(best_flip_val) > 0.93:
            print("using flipping to solve")
            choices = flip_answers(best_flip, C, a1, a2, a3, a4, a5)
            choice = np.argsort(choices)+1
            choice = np.fliplr([choice])[0]
        else:
            #choices = find_answers(A,B,C,a1, a2, a3, a4, a5)
            #choice = np.argsort(choices)+1
            #choice = np.fliplr([choice])[0]

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

#function that solves all the problems, correct answers are
# checked
def solve_all_problems():
    correct_answers = [2,2,4,4,3,1,1,2,5,5,3,3,2,4,2]
    total_correct = 0
    for i in range(1,16):
        problem = 'm' + str(i)
        answers = solve_problem(problem)
        if(answers[0] == correct_answers[i-1]):
            total_correct = total_correct + 1
            #system got the answer correct
            print("Problem " + problem + " answered correctly!")
        else:
            #system got the answer wrong
            print("Problem " + problem + " answers (correct answer is " + str(correct_answers[i-1]) + '):')
            print_answers(answers)
    print("Total Correct: " + str(total_correct))

#function that solves one specific problem, correct answer
#is checked
def solve_one_problem(problem):
    correct_answers = [2,2,4,4,3,1,1,2,3,5,3,3,2,4,2]
    problem_string = 'm' + str(problem)
    answers = solve_problem(problem_string)
    if(answers[0] == correct_answers[problem-1]):
        #system got the answer correct
        print("Problem " + str(problem) + " answered correctly!")
    else:
        #system got the answer wrong
        print("Problem " + str(problem) + " answers (correct answer is " + str(correct_answers[problem-1]) + '):')
        print_answers(answers)


# Main function to solve geometric analogy problems
def main():
    solve_all_problems()
    #solve_one_problem(1)


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

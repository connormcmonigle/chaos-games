import random
from PIL import Image
import math
import sys

def basis_coordinates(sides):
    coordinates = []
    for i in range(sides):
        coordinates.append((0.5 * math.cos(2 * math.pi * i / sides) + 0.5, 0.5 * math.sin(2 * math.pi * i / sides) + 0.5))
    return coordinates

def check_validity(history, limit, offsets, node):
    for i, h, k in zip(limit, history, offsets):
        for g in k:
            if(i and (h + g) % len(history) == node):
                return False
    return True

def generate_image(samples, base_coordinates, approach, history_limit, image, offsets, r_of_sm_nd, color):
    draw_coordinates = [base_coordinates[0]]
    history = [0] * len(base_coordinates)
    sm_nd_count = 0
    for i in range(samples):
        if(i % 1000 == 0):
            percent = int(i * 100 / samples)
            sys.stdout.write("\r percent :: %d" % percent)
        x1, y1 = draw_coordinates[-1]
        next_node = random.randint(0, (len(base_coordinates) - 1))
        if(sm_nd_count >= r_of_sm_nd):
            while(not check_validity(history, history_limit, offsets, next_node)):
                next_node = random.randint(0, (len(base_coordinates) - 1))
        if(history[0] == next_node):
            sm_nd_count += 1
        else:
            sm_nd_count = 0
        del(history[0])
        history.append(next_node)
        x2, y2 = base_coordinates[next_node]
        draw_coordinates.append(((x2 * (approach - 1) + x1) / approach, (y2 * (approach - 1) + y1) / approach))
        #print(draw_coordinates[-1])
        pixels = image.load()
        min_dimension = min(image.size)
    for i in draw_coordinates:
        width, height = i
        r, g, b = pixels[int(width * min_dimension), int(height * min_dimension)]
        r = int((r + color[0]) / 2)
        g = int((g + color[1]) / 2)
        b = int((b + color[2]) / 2)
        pixels[int(width * min_dimension), int(height * min_dimension)] = (r, g, b)
    print("\n")
        
    
        

def main():
    sides = int(raw_input("Sides :: "))
    offsets = [[]]
    history_limit = []
    com = bool(int(raw_input("Apply illegality commutatively? (0|1) :: ")))
    repetitions_of_same_node_before_application = int(raw_input("Enter number of node repetitions prior to rule_set application :: "))
    for i in range(sides):
        history_limit.append(bool(int(raw_input("True that illegal if present node is shared with the ith node in history? (0|1) :: "))))
        local = []
        if(history_limit[-1] != 0):
            while(True):
                offset = raw_input("Enter offset value for ith node (type \"END\" to end) :: ")
                if(str(offset) == "END"):
                    break
                else:
                    local.append(int(offset))
                    if(com):
                        local.append(-1 * int(offset))
        offsets.append(local)
    im = Image.new("RGB", (3840, 2160), "white")
    color = (float(0), float(0), float(0))
    generate_image(int(raw_input("Enter number of samples :: ")), basis_coordinates(sides), \
                  (1 / float(raw_input("Enter fractional approach of basis coordinate :: "))), \
                   history_limit[::-1], im, offsets[::-1], repetitions_of_same_node_before_application, color)
    im.show()
    im.save(raw_input("Save file to :: "), "png")

main()

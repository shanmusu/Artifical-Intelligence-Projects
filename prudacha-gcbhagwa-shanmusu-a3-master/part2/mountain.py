#!/usr/bin/python
#
# Mountain ridge finder
# Geetanjali-Bhagwani
#Part1 of Ques2 implemented

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from scipy.misc import imsave
import sys

def naive_bayes_func(edge_strength):
    #print(edge_strength);
    #print(len(edge_strength[0]));
    ridge = [];
    for column_pointer in range(0, len(edge_strength[0])):
        rows_temp = [];
        for row_pointer in range(0, len(edge_strength)):
            rows_temp.append(edge_strength[row_pointer][column_pointer]);
        #ridge.append(max(rows_temp));
        #print(max(rows_temp));
        ridge.append(argmax(rows_temp));
    #print(ridge);
    imsave(output_filename, draw_edge(input_image, ridge, (255, 0, 0), 5))

def bayes_net(edge_strength):
    ridge = [];
    previous_column_ridge_value  = 0;
    previous_column_ridge_position = 0;
    for column_pointer in range(0, len(edge_strength[0])):
        rows_temp = [];
        for row_pointer in range(0, len(edge_strength)):
            rows_temp.append(edge_strength[row_pointer][column_pointer]);

        highest_value_so_far = -1000;
        highest_value_position = -10;
        
        if column_pointer == 0:
            ridge.append(argmax(rows_temp));
            #print("true");
            previous_column_ridge_value = max(rows_temp);
            highest_value_so_far = max(rows_temp);
            highest_value_position = argmax(rows_temp);
            previous_column_ridge_position = argmax(rows_temp);
            #ridge.append(highest_value_position);
            #print(highest_value_position);
            
        else:
            temp_list =[];
            for temp in range(previous_column_ridge_position-5, previous_column_ridge_position+5):
                if temp >0 and temp< len(rows_temp):
                    temp_list.append(rows_temp[temp]);                    
            for rows_temp_pointer in temp_list:
                product_value = 0;
                if(rows_temp_pointer > 0 and sum(rows_temp) > 0):
                    product_value = int(float(previous_column_ridge_value) / float(rows_temp_pointer))^2 * int(float(max(rows_temp)) / float(sum(rows_temp)))^3;
                #print(product_value);
                if product_value > highest_value_so_far:
                    highest_value_so_far = product_value;
                    highest_value_position  = rows_temp.index(rows_temp_pointer);
                    #print(rows_temp_pointer in rows_temp);

            ridge.append(highest_value_position);
        previous_column_ridge_value = rows_temp[highest_value_position];

    #print(ridge)
    imsave(output_filename, draw_edge(input_image, ridge, (0,0,255), 5))

def bayes_net_withuser_input(edge_strength):
    ridge = [];
    previous_column_ridge_value  = 0;
    previous_column_ridge_position = 0;
    for column_pointer in range(0, len(edge_strength[0])):
        rows_temp = [];
        for row_pointer in range(0, len(edge_strength)):
            rows_temp.append(edge_strength[row_pointer][column_pointer]);

        highest_value_so_far = -1000;
        highest_value_position = -10;
        
        if column_pointer == 0:
            ridge.append(int(gt_row));
            #print("true");
            previous_column_ridge_value = rows_temp[int(gt_row)];
            highest_value_so_far = rows_temp[int(gt_row)];
            highest_value_position = int(gt_row);
            previous_column_ridge_position = int(gt_row);
            #ridge.append(highest_value_position);
            #print(highest_value_position);
            
        else:
            temp_list =[];
            for temp in range(previous_column_ridge_position-5, previous_column_ridge_position+5):
                if temp >0 and temp< len(rows_temp):
                    temp_list.append(rows_temp[temp]);                    
            for rows_temp_pointer in temp_list:
                product_value = 0;
                if(rows_temp_pointer > 0 and sum(rows_temp) > 0):
                    product_value = int(float(previous_column_ridge_value) / float(rows_temp_pointer))^2 * int(float(max(rows_temp)) / float(sum(rows_temp)))^3;
                #print(product_value);
                if product_value > highest_value_so_far:
                    highest_value_so_far = product_value;
                    highest_value_position  = rows_temp.index(rows_temp_pointer);
                    #print(rows_temp_pointer in rows_temp);

            ridge.append(highest_value_position);
        previous_column_ridge_value = rows_temp[highest_value_position];

    #print(ridge)
    imsave(output_filename, draw_edge(input_image, ridge, (0,255,0), 5))  
 

# calculate "Edge strength map" of an image
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return filtered_y**2

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( max(y-thickness/2, 0), min(y+thickness/2, image.size[1]-1 ) ):
            image.putpixel((x, t), color)
    return image

# main program
(input_filename, output_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)
#input_image = Image.open('mountain.jpg')

# compute edge strength mask
edge_strength = edge_strength(input_image)
imsave('edges.jpg', edge_strength)

#ridge = [ edge_strength.shape[0]/2 ] * edge_strength.shape[1]
#this code generate red line on the edge reading the edge.jpg(gray image) 
#of the input image
#ridge=[]
##max_value=0
##for i in range(edge_strength.shape[1]):
##    temp=[]
##    for j in range(edge_strength.shape[0]):
##        temp=temp+[edge_strength[j][i]]#array for each column
##    max_value=argmax(temp)#find the index of maximum edge_strength in each array
##    ridge=ridge+[max_value]

naive_bayes_func(edge_strength);
bayes_net(edge_strength);
bayes_net_withuser_input(edge_strength)

# output answer
#imsave(output_filename, draw_edge(input_image, ridge, (255, 0, 0), 5))
#imsave('out.jpg', draw_edge(input_image, ridge, (255, 0, 0), 5))

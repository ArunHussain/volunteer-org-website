def split_string(string, separator): #for splitting a string [based on / around] a character. For use in simple_date_time_format method below.
      list_of_individual_parts=[]
      element=""
      for i in range(0,len(string)):
            if (string[i] == separator) or (i==len(string)-1):#if we encounter the separator or are at the end of the string then we add the current element to the list.
                  list_of_individual_parts.append(element)
                  element=""
            
            else:
                  element=element+string[i]
      return list_of_individual_parts

def date_time_format_converter(date_time): #for presenting the date-time created of tweets nicely.
      date_time=date_time[1:] #remove first element which will be a " due to how api returns date_time data!
      string_splitted=split_string(date_time,"-")
      year=string_splitted[0]
      month=string_splitted[1]
      day=(split_string(string_splitted[2],"T"))[0] 
      months=[" Jan "," Feb "," Mar "," Apr "," May "," Jun "," Jul "," Aug "," Sep "," Oct "," Nov "," Dec "]
      new_format=day+months[int(month)-1]+year
      
      return new_format


def list_contains_element(list_arg, element_arg):
      for element in list_arg:
            if  element == element_arg:                  
                  return True




#this function is for use in the function 2 below
def merge(left,right):
      left_index=0
      right_index=0
      merged_list=[]
      while right_index<len(right) and left_index<len(left):
            if left[left_index][1]>right[right_index][1]:
                  merged_list.append(left[left_index])
                  left_index+=1
            else:
                  merged_list.append(right[right_index])
                  right_index+=1
      merged_list+=left[left_index:]
      merged_list+=right[right_index:]
      return merged_list
      

def dictionary_to_key_value_list(dictionary):
      dict_items = dictionary.items() #I can't seem to find online or in my head a way to implement .items() myself.
      list_form=[]
      for key,value in dict_items:
            list_form.append((key,value))
      return(list_form)

#the below should sort the dictionary by value not key from asc to desc.
def merge_sort_list_of_key_value_pairs_by_value(list_form):
              
      if len(list_form)<=1: #this is the base case
            return(list_form)
      midpoint=len(list_form)//2
      right_half=merge_sort_list_of_key_value_pairs_by_value(list_form[midpoint:])
      left_half=merge_sort_list_of_key_value_pairs_by_value(list_form[:midpoint])
      return merge(left_half,right_half)                 








import requests
import os
import json

#"2021-12-26T23:32:30.000Z" - This is the formate of the date_created which is output, hence why I have to convert the formate using my methods above.

def latest_tweet(twitter_user_id):
      def authorisation(me):
            bearer_token = "AAAAAAAAAAAAAAAAAAAAAPXtXQEAAAAAecCUdhLOFkPRvSW%2F5V5ow6vdV4s%3DNwfI0NWyvFqmyaf0nGULhwvabpE1WqrQS9RMpMNu2TI0DdtbFh"
            #^^my bearer_token provided by twitter to me.
            me.headers["Authorization"] = f"Bearer {bearer_token}"
            me.headers["User-Agent"] = "v2UserTweetsPython"
            return me
      api_url="https://api.twitter.com/2/users/{}/tweets".format(twitter_user_id)
      api_parameters={"tweet.fields":"created_at"}
      twitter_data=requests.request("GET", api_url, auth=authorisation, params=api_parameters)
      if twitter_data.status_code != 200:
        raise Exception(
            "Sorry, something went wrong"     
        )
      else:
            json_twitter_data=twitter_data.json()
            tweet_and_date_created=[json.dumps(json_twitter_data["data"][0]["text"], indent=4, sort_keys=True),json.dumps(json_twitter_data["data"][0]["created_at"])]
            return tweet_and_date_created






import random
import numpy as np
from numpy import savetxt
import cv2
from PIL import Image 
import math

#https://stackoverflow.com/questions/63036809/how-do-i-use-only-numpy-to-apply-filters-onto-images 
def apply_filter(image_array, filter_matrix): #the input array is 80x80 as this is the image size.
    padded_image_array=np.zeros(shape=(82,82)) # this whole apply_filter function works for images
    padded_image_array[1:81,1:81]=image_array # this does the padding, i.e adds a layer of 0s around the whole array
            #the edges of the image are 0s so I will just pad it with a layer of 0s!

    
#while the image_array is always 80x80, the filter_matrix can be a variable size so I need to use its size variable (not a number value) in my code.
    filter_size_x, filter_size_y = filter_matrix.shape[:2]#this gets dimensions of filter.
    output_image_array=np.zeros(((80-filter_size_x+2)+1,  #this is the formula for the size of the output.
                                 (80-filter_size_y+2)+1,))
                                  
    for x in range(82-filter_size_x+1):#this makes sure the filter is not going to be applied past the edges of the matrix.
        for y in range(82-filter_size_y+1):
            window_of_filter=padded_image_array[x:x + filter_size_x, y:y + filter_size_y]#this puts the filter on a part of the matrix.
            output_of_window=np.sum(filter_matrix*window_of_filter, axis=(0,1))#This computes the value filter over the window its in.
            output_image_array[x,y]=output_of_window
    
    return(output_image_array)#so thsi function takes in an array and returns an array.
    

def transpose(input_array): #rotates 90 degrees clockwise
    final_transposed=[]
    for count in range(len(input_array)):
        transposed=[]
        transposed = [col[count] for col in input_array]
        final_transposed.append(transposed)
    return(final_transposed)

def concatenate_4_image_arrays(img_array_1,img_array_2,img_array_3,img_array_4): # this takes image arrays as input but returns an actual image
    concatenated_image_array=np.zeros(shape=(320,80)) # this means 320 wide by 80 high
    concatenated_image_array[0:80,0:80]=img_array_1  #this makes the first 80 x 80 section into the first image array.
    concatenated_image_array[80:160,0:80]=img_array_2
    concatenated_image_array[160:240,0:80]=img_array_3   #format is [rows, columns]
    concatenated_image_array[240:320,0:80]=img_array_4 #[x:y,a:b] is the stuff in rows x to y-1 and column a to b-1.

    concatenated_image=Image.new('1',(320,80)) #this part converts the array back into an image.
    pixels = concatenated_image.load()
    
    for x in range(320):
        for y in range(80):
            pixels[x,y]=1-int(concatenated_image_array[x,y])#unlike when I make the original image an array, in this thing, a 1 represents white and a 0 represents black!!!! THEREFORE, I NEED TO 1- [ ] IN ORDER TO KEEP THE COLOUR CONSISTENCY THE SAME AS THE ORIGINAL IMAGE!      
    
    return(concatenated_image)



    
def letter_modification_1(image_name):#this takes an image NOT an image array. This blurs and gets the outline.
    #first convert the black and white image to a matrix.
    img=Image.open("C:/Users/arunh/Python NEA/find_a_volunteer/find_a_volunteer_dir/alphabet_images/"+image_name)
    image_with_pixel_access=img.load() #you have to open then LOAD the image if you want to access pixels.
    img_array = np.zeros(shape=(80,80))#creates 80x80 array full of 0s.
    
    for x in range(80): # the dimensions of the image are 80x80 btw.
        for y in range(80):
            img_array[x,y]=image_with_pixel_access[x,y] #in this thing a 1 represents black and a 0 represents white.
    gaussian_blur_filter=np.zeros(shape=(3,3))
    gaussian_blur_filter[0,0]=0.0625
    gaussian_blur_filter[1,0]=0.125
    gaussian_blur_filter[2,0]=0.0625
    gaussian_blur_filter[0,1]=0.125
    gaussian_blur_filter[1,1]=0.25
    gaussian_blur_filter[2,1]=0.125
    gaussian_blur_filter[0,2]=0.0625
    gaussian_blur_filter[1,2]=0.125 #this sets the gaussian_blur_filter (which is actually a kernel btw)
    gaussian_blur_filter[2,2]=0.0625
    modified_image_array= apply_filter(img_array,gaussian_blur_filter) # because it's a small image the blur just makes the edges jagged which is fine.
#IT SEEMS THAT ARRAY[A,B] IS THE ELEMENT IN THE ATH ROW AND BTH COLUMN WHERE THE 0TH ROW IS THE TOP ONE AND THE OTH COLUM IS THE LEFTMOST ONE. 
    outline_filter=np.zeros(shape=(3,3))
    outline_filter[0,0]=-1
    outline_filter[0,1]=-1   #SO WITH A MATRIX, YOU SPECIFY ROW NUMBER FIRST AND THEN COLUMN NUMBER SO X IS ROW NUMBER (HORIZONTAL) WHEREAS Y IS COLUMN NUMBER (VERTICAL) SO IT IS NOT LIKE A NORMAL GRAPH
    outline_filter[0,2]=-1
    outline_filter[1,0]=-1
    outline_filter[1,1]=8.5 #this value instead of 8 is perfect for keeping the horizontal part of the A
    outline_filter[1,2]=-1
    outline_filter[2,0]=-1
    outline_filter[2,1]=-1
    outline_filter[2,2]=-1
    modified_image_array= apply_filter(modified_image_array,outline_filter)
    
##    modified_image=Image.new('1',(80,80)) #this part converts the array back into an image.
##    pixels = modified_image.load()
##    for x in range(80):
##        for y in range(80):
##            pixels[x,y]=1-int(modified_image_array[x,y])#unlike when I make the original image an array, in this thing, a 1 represents white and a 0 represents black!!!! THEREFORE, I NEED TO 1- [ ] IN ORDER TO KEEP THE COLOUR CONSISTENCY THE SAME AS THE ORIGINAL IMAGE!      
    return(modified_image_array)#this should return an image as the function should be self contained and take an img and return an img, not an array


def letter_modification_2(image_name): # This will swirl the image
    img=Image.open("C:/Users/arunh/Python NEA/find_a_volunteer/find_a_volunteer_dir/alphabet_images/"+image_name)
    image_with_pixel_access=img.load() #you have to open then LOAD the image if you want to access pixels.
    swirled_img_array = np.zeros(shape=(80,80))#creates 80x80 array full of 0s.
    centre_of_swirl_x_y=[39,39] #https://stackoverflow.com/questions/30448045/how-do-you-add-a-swirl-to-an-image-image-distortion for swirling
    radius_of_swirl=40
    twist_factor=0.15
    for x in range(80): 
        for y in range(80):
            pixel_x_dist = x - centre_of_swirl_x_y[0]
            pixel_y_dist = y - centre_of_swirl_x_y[1]
            pixel_dist = math.sqrt((pixel_x_dist * pixel_x_dist) + (pixel_y_dist * pixel_y_dist))#this is the ditance from the swirl center.
            pixel_angle = np.arctan2(pixel_x_dist,pixel_y_dist) #this is the angle from the swirl centre.
            swirl_factor = 1 - (pixel_dist/radius_of_swirl) #this is 1 at the centre and 0 at the radius.
            if (swirl_factor > 0):
                angle_for_twist = twist_factor*swirl_factor*2*math.pi
                pixel_angle+=angle_for_twist
                pixel_x_dist=(math.cos(pixel_angle))*pixel_dist
                pixel_y_dist=(math.sin(pixel_angle))*pixel_dist
            swirled_img_array[x,y]=image_with_pixel_access[centre_of_swirl_x_y[0]+pixel_x_dist, centre_of_swirl_x_y[1]+pixel_y_dist]  #I don't ever store the raw image array, only the swirled one.

    swirled_img_array=transpose(swirled_img_array)
    
##    modified_image=Image.new('1',(80,80)) #this part converts the array back into an image.
##    pixels = modified_image.load()
##    swirled_img_array=transpose(swirled_img_array)
##    for x in range(80):
##        for y in range(80):
##            pixels[x,y]=1-int(swirled_img_array[x][y])#unlike when I make the original image an array, in this thing, a 1 represents white and a 0 represents black!!!! THEREFORE, I NEED TO 1- [ ] IN ORDER TO KEEP THE COLOUR CONSISTENCY THE SAME AS THE ORIGINAL IMAGE!      
    #THE REASON I USE [X][Y] INSTEAD OF [X,Y] ABOVE IS BECAUSE MY CUSTOM TRANSPOSE FUNCTION TURNS THE MATRIX "SWIRLED_IMG_ARRAY" INTO A LIST OF TUPLES AND TO ACCESS AN ELEMENT OF A LIST OF TUPLES YOU NEED TO USE THE [X][Y] SYNTAX, NOT THE [X,Y] SYNTAX!!!
    return(swirled_img_array)

def letter_modification_3(image_name): # to explode an image. In reality, it just kinda explodes it but in a really shit way! Either way, I don't wanna waste more time on this as I've already used plenty advanced matrix operations so I'll call it here with my letter modifications.
    img=Image.open("C:/Users/arunh/Python NEA/find_a_volunteer/find_a_volunteer_dir/alphabet_images/"+image_name)
    image_with_pixel_access=img.load()
    exploded_img_array=np.zeros(shape=(80,80))
    centre_of_explosion_x_y=[39,39]
    explosion_radius=40

    for x in range(80):
        for y in range(80):
            pixel_x_dist=x-centre_of_explosion_x_y[0]
            pixel_y_dist=y-centre_of_explosion_x_y[1]
            pixel_dist=math.sqrt((pixel_x_dist*pixel_x_dist)+(pixel_y_dist*pixel_y_dist))
            pixel_angle=np.arctan2(pixel_x_dist,pixel_y_dist)
            #the amount by which the pixels get moved away from the center along the line going from them to the centre should be very large at the centre but very small at the edges of the explosion radius.
            #displacement_factor=(1-(math.pow((pixel_dist/explosion_radius),2))) #the reason above is why I have to use the power 2.
            if pixel_dist>=40:
                displacement_factor=0.95
            elif 40>pixel_dist>=30:
                displacement_factor=0.75
            elif 30>pixel_dist>=20:
                displacement_factor=0.6
            elif 20>pixel_dist>=10:
                displacement_factor=0.4
                       
            if (displacement_factor>0):
                pixel_x_dist=(math.cos(pixel_angle))*pixel_dist*displacement_factor
                pixel_y_dist=(math.sin(pixel_angle))*pixel_dist*displacement_factor
            exploded_img_array[x,y]=image_with_pixel_access[centre_of_explosion_x_y[0]+pixel_x_dist, centre_of_explosion_x_y[1]+pixel_y_dist]

    exploded_img_array=transpose(exploded_img_array)   
##    modified_image=Image.new('1',(80,80)) #this part converts the array back into an image.
##    pixels = modified_image.load()
##    for x in range(80):
##        for y in range(80):
##            pixels[x,y]=1-int(exploded_img_array[x,y])#unlike when I make the original image an array, in this thing, a 1 represents white and a 0 represents black!!!! THEREFORE, I NEED TO 1- [ ] IN ORDER TO KEEP THE COLOUR CONSISTENCY THE SAME AS THE ORIGINAL IMAGE!      
    return(exploded_img_array)


from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import CustomUser
from django.conf import settings
from .models import volunteer_profile








from django.db import connection

#This function
def fetch_table_data(table_name):
    # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object.
    
    cur = connection.cursor()
    cur.execute('select * from ' + table_name)

    header = [row[0] for row in cur.description]

    rows = cur.fetchall()

    # Closing connection
    connection.close()

    return header, rows


import datetime

#This function backs up the database to a txt file.
def backup_to_txt_file():

      date_time=str(datetime.datetime.now())
      date_time_split=split_string(date_time," ")
      date_only=date_time_split[0]
      #This uses the split_string function defined in this same file.
      #This function was shown in 3.5.3.
      
      new_txt_file = open("C:/Users/arunh/nea_database_backups/" + "UNCOMPRESSED_database_backup-" +date_only + '.txt', 'w')
      #^ The new txt file which will represent the database is created in a...
      #...specific directory on the web host machine. The filename...
      #...incorporates the date 
    
      table_names=['auth_group','auth_group_permissions','auth_permission',
                 'django_admin_log','django_content_type','django_migrations',
                 'django_session','find_a_volunteer_dir_accepted_organisations',
                 'find_a_volunteer_dir_image_upload',
                 'find_a_volunteer_dir_matched_organisations',
                 'find_a_volunteer_dir_organisation_profile',
                 'find_a_volunteer_dir_verification_details',
                 'find_a_volunteer_dir_volunteer_profile',
                 'sqlite_sequence','users_customuser',
                 'users_customuser_groups','users_customuser_user_permissions']
    #A list of all the tables in the database is created.
                 
      for counter in range(0,17): 
            header, rows = fetch_table_data(table_names[counter])
            #the for loop means the data is fetched for every table after all...
            #...the iterations.
            
            new_txt_file.write('\n' + table_names[counter] + '\n')
            new_txt_file.write(','.join(header) + '\n')
            for row in rows:
                  new_txt_file.write(','.join(str(element) for element in row) + '\n')
            #The name of the table, the name of the fields and then the values of...
            #...the fields for each object are written to the txt file.
            # The stucture is:
##            {Blank line}
##            [table name]
##            [fields of table]
##            [values of fields for first object]
##            [ "" for second object]
##            ...
                                                              
      new_txt_file.close()
    



from collections import Counter
from queue import PriorityQueue
import os


class HuffmanNode:
    def __init__(self, char, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def encode(input_text):

    dict_of_char_frequencies=Counter(input_text)
    dictionary_of_codes = {}
    priority_queue = PriorityQueue()

    for character, frequency in dict_of_char_frequencies.items():
        priority_queue.put(HuffmanNode(character,frequency))


    while priority_queue.qsize() >1:
        left_char , right_char = priority_queue.get(),priority_queue.get()
        total_freq = left_char.freq + right_char.freq
        priority_queue.put(HuffmanNode(None, total_freq,left_char,right_char))

    current_huffman_tree=priority_queue.get()
    fill_dictionary_of_codes(current_huffman_tree, "", dictionary_of_codes)

    code_of_encoded_text =""
    for character in input_text:
        code_of_encoded_text+=dictionary_of_codes[character]

    code_of_encoded_tree = encode_huffman_tree(current_huffman_tree,"")

    num_bits_under_nearest_byte = 8 - ((len(code_of_encoded_text)+len(code_of_encoded_tree))%8)
    code_of_encoded_text=num_bits_under_nearest_byte*"0"+code_of_encoded_text       

    return (f"{code_of_encoded_tree}{num_bits_under_nearest_byte:08b}{code_of_encoded_text}")                


def decode(input_encoded_text):
    list_form_of_encoded_text = []
    for char in input_encoded_text:
        list_form_of_encoded_text.append(char)
    
    encoded_tree = decode_huffman_tree(list_form_of_encoded_text)
    binary_num_extra_0=list_form_of_encoded_text[:8]
    list_form_of_encoded_text=list_form_of_encoded_text[8:]
    num_extra_0=int("".join(binary_num_extra_0),2)
    list_form_of_encoded_text=list_form_of_encoded_text[num_extra_0:]

    current_node=encoded_tree
    decoded_output_text=""
    
    for element in list_form_of_encoded_text:
        if element=="0":
            current_node=current_node.left
        else:
            current_node=current_node.right

        character=current_node.char
        if character is not None:
            decoded_output_text+=character
            current_node = encoded_tree
    
    return(decoded_output_text)


def compress(path_of_input_file, path_of_output_file):
    
    byte_array=bytearray()
    input_file = open(path_of_input_file)
    output_file = open(path_of_output_file,"wb")

    input_text=input_file.read()
    encoded_text=encode(input_text)
    for first_bit_of_byte in range(0,len(encoded_text),8):
        byte_array.append(int(encoded_text[first_bit_of_byte:first_bit_of_byte+8],2))

    output_file.write(byte_array)

    

def decompress(path_of_input_file, path_of_output_file):

    input_file = open(path_of_input_file,"rb")
    output_file=open(path_of_output_file,"w")
    encoded_text_from_input_file=""

    current_byte=input_file.read(1)
    while len(current_byte)>0:
        encoded_text_from_input_file+=f"{bin(ord(current_byte))[2:]:0>8}"
        current_byte=input_file.read(1)

    decoded_text=decode(encoded_text_from_input_file)
    output_file.write(decoded_text)




def fill_dictionary_of_codes(node,code,dictionary_of_codes):

    if node.char is None:
        fill_dictionary_of_codes(node.left,code+"0",dictionary_of_codes)
        fill_dictionary_of_codes(node.right,code+"1",dictionary_of_codes)
    
    else:
        dictionary_of_codes[node.char]=code
        

def decode_huffman_tree(array_of_encoded_text):
    first_bit=array_of_encoded_text[0] 
    del array_of_encoded_text[0]

    if first_bit=="1":
        character=""
        for x in range(8):
            character+=array_of_encoded_text[0]
            del array_of_encoded_text[0]

        return( HuffmanNode(chr(int(character,2))))
    return (HuffmanNode(None,left=decode_huffman_tree(array_of_encoded_text), right=decode_huffman_tree(array_of_encoded_text)))


def encode_huffman_tree(node,text_from_tree):
    if node.char is None:
        text_from_tree += "0"
        text_from_tree = encode_huffman_tree(node.left,text_from_tree)
        text_from_tree = encode_huffman_tree(node.right, text_from_tree)
    else:
        text_from_tree+="1"
        text_from_tree+=f"{ord(node.char):08b}"

    return text_from_tree




  











import os

#This function backs up the database to a txt file.
def backup_and_compress():
      backup_to_txt_file()
    
      date_time=str(datetime.datetime.now())
      date_time_split=split_string(date_time," ")
      date_only=date_time_split[0]
      
      compress("C:/Users/arunh/nea_database_backups/" + "UNCOMPRESSED_database_backup-" +date_only + '.txt' , "C:/Users/arunh/nea_database_backups/" + "COMPRESSED_database_backup-" +date_only+'.txt')
      os.remove("C:/Users/arunh/nea_database_backups/" + "UNCOMPRESSED_database_backup-" +date_only + '.txt') 


def decompress_backup(filename):
      split_name=split_string(filename,"-")
      date_only=split_name[1]+"-"+split_name[2]+"-"+split_name[3]
      decompress("C:/Users/arunh/nea_database_backups/" + filename , "C:/Users/arunh/nea_database_backups/" + "UNCOMPRESSED_database_backup-" +date_only+'.txt' )#the .txt isn't needed at the end of this line as it savew with it anywat.
      os.remove("C:/Users/arunh/nea_database_backups/" + filename)                                                                                                #actually just fake the filename by removing the .txt
      
      















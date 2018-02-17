

#class to store the details of each highway:
#start city, end city, highway_time, highway_distance, highway_name
class Highway:
    def __init__(self,start_city,end_city,distance,speed,highway):
        self.start_city = start_city
        self.end_city=end_city
        self.speed=speed
        self.distance=distance
        self.highway=highway
        #print(speed, " ", distance);
        if speed == "":
            self.time = 0;
        else:
            if int(speed) > 0:
                self.time = float(distance)/float(speed);
            if int(speed) == 0:
                self.time = float(distance)/float(40)
            
    def getstart_city(self):
        return self.start_city

    def getend_city(self):
        return self.end_city

    def gettime(self):
        return self.time

    def getspeed(self):
        return self.speed;

    def getdistance(self):
        return self.distance

    def gethighway(self):
        return self.highway

    def setstart_city(self,start_city):
        self.start_city=start_city

    def setend_city(self,end_city):
        self.end_city=end_city

    def settime(self,time):
        self.time=time

    def setspeed(self, speed):
        self.speed = speed;

    def setdistance(self,distance):
        self.distance=distance

    def sethighway(self,highway):
        self.highway=highway

class City:
    def __init__(self,city_name,distance_so_far, my_parent, time_so_far, g_of_x, h_of_x ):
        self.city_name=city_name
        self.distance_so_far = distance_so_far;
        self.my_parent = my_parent;
        self.time_so_far = time_so_far;
        self.g_of_x = g_of_x;
        self.h_of_x = h_of_x;
        
    def getcity_name(self):
        return self.city_name

    def setcity_name(self,city_name):
        self.city_name=city_name

    def getdistance_so_far(self):
        return self.distance_so_far;

    def setdistance_so_far(self, distance_so_far):
        self.distance_so_far = distance_so_far;

    def getmy_parent(self):
        return self.my_parent;

    def setmy_parent(self, my_parent):
        self.my_parent = my_parent;

    def gettime_so_far(self):
        return self.time_so_far;

    def settime_so_far(self, time_so_far):
        self.time_so_far = time_so_far;

    def getg_of_x(self):
        return self.g_of_x;

    def setg_of_x(self, g_of_x):
        self.g_of_x = g_of_x;

    def seth_of_x(self, h_of_x):
        self.h_of_x = h_of_x;

    def geth_of_x(self):
        return self.geth_of_x;

opened_list = [];
closed_list = [];
highway_object_list = [];
successor_city_object_temp = [];
path_taken = "";
my_parent_func = "";
goal_node_lat = 0;  
goal_node_lng = 0;
goals_reached_so_far = [];
routing_option = "";
goal_city_found = False;

#TO-DO change the sys.argv

def input_function(start_node_temp, goal_node_temp, routing_option_temp):
    global start_node;
    global goal_node;
    global routing_option;
    ##start_node = "Bloomington,_Indiana";
    ##goal_node = "Indianapolis,_Indiana";
    start_node = start_node_temp;
    goal_node = goal_node_temp;
    routing_option = routing_option_temp;

def file_reading():
    #initialise and assign an object of type City for the start city.
    city_object = City(start_node,0,0,0,0,0);
    opened_list.append(city_object);

    file_obj=open("road-segments.txt");
    file_contents= file_obj.read();
    file_obj.close();

    if start_node == goal_node:
        print("Start and Goal node are the same!");

    file_obj_split=file_contents.split('\n');
    for file_item in file_obj_split:
        file_item_split=file_item.split(' ');
        if len(file_item_split)==5:
            #print(len(highway_object_list));
            highway=Highway(file_item_split[0],file_item_split[1],file_item_split[2],file_item_split[3],file_item_split[4]);
            highway_object_list.append(highway);

    #code to calculate the heuristics for the nodes:
    file_obj=open("city-gps.txt");
    file_contents= file_obj.read();
    file_obj.close();

    

    file_obj_split=file_contents.split('\n');
    for file_item in file_obj_split:
        file_item_split=file_item.split(' ');
        if len(file_item_split) == 3:
            if file_item_split[0] == goal_node:
                goal_city_found = True;
                goal_node_lat = file_item_split[1];
                goal_node_lng = file_item_split[2];
                break;

    if not goal_city_found:
        print("Goal Cannot be reached!");

def calculate_heuristic(current_node):
    global goal_city_found;
    if goal_city_found:
        file_obj=open("city-gps.txt",'r');
        file_contents= file_obj.read();
        file_obj.close();
        
        file_obj_split=file_contents.split('\n');
        for file_item in file_obj_split:
            file_item_split=file_item.split(' ');
            if len(file_item_split) == 3:
                if file_item_split[0] == current_node:
                     distance_between_cities_for_heuristic = math.sqrt(((file_item_split[1] - goal_node_lat)*
                                             (file_item_split[1] - goal_node_lat)) +
                                            ((file_item_split[2] - goal_node_lng)*
                                             (file_item_split[2] - goal_node_lng)));
                     return distance_between_cities_for_heuristic;
                else:
                    return 0;
            else:
                return 0;
    else:
        return 0;
        
       
def getSuccessors(current_city_object):

    del successor_city_object_temp[:];
    
    for highway_object_list_item in highway_object_list:
        successor_found = False;
        
        if highway_object_list_item.getstart_city() == current_city_object.getcity_name():
            h_of_x = calculate_heuristic(highway_object_list_item.getend_city());
            #print(current_city_object.getdistance_so_far(), "  ", highway_object_list_item.getdistance(), " ", h_of_x);
            city = City(highway_object_list_item.getend_city(),
                        int(current_city_object.getdistance_so_far()) + int(highway_object_list_item.getdistance()) + int(h_of_x),
                        current_city_object.getcity_name(),
                        float(highway_object_list_item.gettime()) + float(current_city_object.gettime_so_far()),
                        int(current_city_object.getdistance_so_far()) + int(highway_object_list_item.getdistance()),
                        h_of_x);
            successor_found = True;
            successor_city_object_temp.append(city);
        elif highway_object_list_item.getend_city() == current_city_object.getcity_name():
            h_of_x = calculate_heuristic(highway_object_list_item.getend_city());
            #print(current_city_object.getdistance_so_far(), "  ", highway_object_list_item.getdistance(), " ", h_of_x);
            city = City(highway_object_list_item.getstart_city(),
                        int(current_city_object.getdistance_so_far()) + int(highway_object_list_item.getdistance()) + int(h_of_x),
                        current_city_object.getcity_name(),
                        float(highway_object_list_item.gettime()) + float(current_city_object.gettime_so_far()),
                        int(current_city_object.getdistance_so_far()) + int(highway_object_list_item.getdistance()),
                        h_of_x);
            successor_found = True;
            successor_city_object_temp.append(city);

        if successor_found:
            successor_removed = False;
            for opened_list_item in opened_list:
                
                if opened_list_item.getcity_name() == successor_city_object_temp[len(successor_city_object_temp) - 1].getcity_name():
                    successor_removed = True;
                    #print(len(successor_city_object_temp), current_city_object.getcity_name());
                    successor_city_object_temp.remove(successor_city_object_temp[len(successor_city_object_temp) -1]);
                    break;
            #print("break");
            if not successor_removed:
                for closed_list_item in closed_list:
                    if closed_list_item.getcity_name() == successor_city_object_temp[len(successor_city_object_temp) - 1].getcity_name():
                        successor_city_object_temp.remove(successor_city_object_temp[len(successor_city_object_temp) -1]);
                        break;

    return successor_city_object_temp;

def print_path():
    end_function = False;
    global my_parent_func;
    global path_taken;
    while not end_function:
        if my_parent_func == 0:
            break;
        for opened_list_item in opened_list:
            if opened_list_item.getcity_name() == my_parent_func:
                path_taken = opened_list_item.getcity_name() +" "+ path_taken;
                my_parent_func = opened_list_item.getmy_parent();
                break;
    return path_taken;

def search_algorithm():

    global opened_list, closed_list, highway_object_list;
    global successor_city_object_temp, path_taken, my_parent_func, start_node, goal_node, routing_option;
    global goal_node_lat, goal_node_lng, goals_reached_so_far, successors;

    end_program = False;
    goal_reached = False;

    while not end_program:
        #print ("opened_list" , len(opened_list));
        successors = getSuccessors(opened_list[-1]);

        count_temp = 0;
        for successors_item in successors:
            count_temp += 1;
            if successors_item.getcity_name() == goal_node:
                goals_reached_so_far.append(successors_item);
                goal_reached = True;
                successors.remove(successors_item);
                break;  

        if len(successors) > 0:

            least_pathlength_so_far = 0;
            loop_count = 0;
            least_pathlength_object_count = 0;
            for successors_temp in successors:
                loop_count += 1;
                if least_pathlength_so_far == 0:
                    least_pathlength_so_far = successors_temp.getdistance_so_far();
                    least_pathlength_object_count = loop_count -1;
                    continue;

                if successors_temp.getdistance_so_far() < least_pathlength_so_far:
                    least_pathlength_so_far = successors_temp.getdistance_so_far();
                    least_pathlength_object_count = loop_count - 1;

            loop_count = 0;
            least_pathlength_so_far = successors[least_pathlength_object_count].getdistance_so_far();

            least_pathlength_object_count_closed_list = 0;
            for closed_list_item in closed_list:
                loop_count += 1;
                if closed_list_item.getdistance_so_far() < least_pathlength_so_far:
                    least_pathlength_object_count_closed_list = loop_count-1;
                    least_pathlength_so_far = closed_list_item.getdistance_so_far();

            if least_pathlength_object_count_closed_list != 0:
                opened_list.append(closed_list[least_pathlength_object_count_closed_list]);
                closed_list.remove(closed_list[least_pathlength_object_count_closed_list]); 
                for successors_item in successors:
                    closed_list.append(successors_temp);
            else:
                opened_list.append(successors[least_pathlength_object_count]);
                successors.remove(successors[least_pathlength_object_count]);
                for successors_temp in successors:
                    closed_list.append(successors_temp);
                
        else:
            if len(closed_list) > 0:
                loop_count = 0;
                least_pathlength_so_far = 0;
                least_pathlength_object_count_closed_list = 0;
                for closed_list_item in closed_list:
                    loop_count += 1;
                    if least_pathlength_so_far == 0:
                        least_pathlength_so_far = closed_list_item.getdistance_so_far();
                        least_pathlength_object_count_closed_list = loop_count-1;
                        continue;
                    
                    if closed_list_item.getdistance_so_far() < least_pathlength_so_far:
                        least_pathlength_object_count_closed_list = loop_count-1;
                        least_pathlength_so_far = closed_list_item.getdistance_so_far();

                opened_list.append(closed_list[least_pathlength_object_count_closed_list]);
                closed_list.remove(closed_list[least_pathlength_object_count_closed_list]);
            else:
                no_more_nodes_to_search = True;
                break;            
                
    ##    if len(successors) > 0:
    ##        for successors_item in reversed(successors):
    ##            closed_list.append(successors_item);
    ##
    ##    if len(closed_list) > 0:
    ##        if closed_list[len(closed_list)-1].getcity_name() == goal_node:
    ##            end_program = True;
    ##            goal_reached = True;
    ##
    ##            
    ##            opened_list.append(closed_list[len(closed_list)-1]);
    ##            closed_list.remove(closed_list[len(closed_list)-1]);
    ##        else:
    ##            opened_list.append(closed_list[len(closed_list)-1]);
    ##            closed_list.remove(closed_list[len(closed_list)-1]);
    ##    else:
    ##        end_program = True;




    if goal_reached:
    ##    print("Goal Reahced! ", opened_list[len(opened_list)-1].getdistance_so_far());
    ##
    ##    #print the path taken
    ##    global path_taken;
    ##    global my_parent_func;
    ##    path_taken = opened_list[len(opened_list)-1].getcity_name() + path_taken;
    ##    my_parent_func = opened_list[len(opened_list)-1].getmy_parent();
    ##    print_path();

        shortest_path_so_far = 0;
        time = 0;
        for goals_reached_so_far_item in goals_reached_so_far:
            if shortest_path_so_far == 0:
                shortest_path_so_far = goals_reached_so_far_item.getg_of_x();
                time = goals_reached_so_far_item.gettime_so_far()
                continue;
            if shortest_path_so_far > goals_reached_so_far_item.getg_of_x():
                shortest_path_so_far = goals_reached_so_far_item.getg_of_x();
                time = goals_reached_so_far_item.gettime_so_far()
        print("Goal Reached! ", shortest_path_so_far);
        print str(shortest_path_so_far) + " " + str(time) + " " + start_node + " " + goal_node

    elif not goal_reached:
        print("Goal not found or cannot be reached!");

















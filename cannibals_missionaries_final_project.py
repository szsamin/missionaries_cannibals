# File: Cannibals and Missionaries
#
# Authors: Kiyasul Arif Abdul Majeeth <kiyasul@pdx.edu>, Rahul Marathe <rmarathe@pdx.edu>, Shadman Samin <shadman@pdx.edu>
#
# Date: 6/16/2018
# Portland State University
#############################################################
from global_header_file import *


class ImageProcessing:
    def __init__(self):
        pass

    def print_error_messages(self, input_object):
        if re.search("red", input_object):
            self.print_found_object(input_object + " not found", (10, 500))
        else:
            self.print_found_object(input_object + " not found", (10, 450))

    def draw_contour(self, blue, conts, green, object, red):
        cv2.drawContours(img, conts, -1, (255, 0, 0), 3)
        cordinates = {}
        temp_list = []
        # print("-----------------------------------")
        for i in range(len(conts)):
            area = cv2.contourArea(conts[i])
            # print("Countour Area : " + str(area))
            if MINIMUM_CONTOUR_AREA < area < MAXIMUMM_CONTOUR_AREA:
                x, y, w, h = cv2.boundingRect(conts[i])
                position = (x, y)
                temp_list.append(self.get_cordinates(h, w, x, y))
                string = "(" + str(x + math.ceil(0.5 * w)) + ", " + str(y + math.ceil(0.5 * h)) + ")"
                self.print_found_object(object, position)
                self.print_found_object(string, self.get_cordinates(h, w, x, y))
                cv2.rectangle(img, (x, y), (x + w, y + h), (red, green, blue), 2)
        cordinates[object] = temp_list
        return cordinates

    def get_cordinates(self, h, w, x, y):
        return x + math.ceil(0.5 * w), y + math.ceil(0.5 * h)

    def create_contour_rectangle(self, input_mask, red, green, blue, object):
        # morphology
        maskOpen = cv2.morphologyEx(input_mask, cv2.MORPH_OPEN, kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
        maskFinal = maskClose
        cv2.imshow(object, maskFinal)
        _, conts, _ = cv2.findContours(maskFinal.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        if len(conts) in range(1, CONTOUR_LIMIT):
            return self.draw_contour(blue, conts, green, object, red)
        else:
            self.print_error_messages(object)

    def print_found_object(self, input_string, position):
        font = cv2.FONT_HERSHEY_PLAIN
        fontScale = 0.8
        fontColor = (50, 175, 255)
        lineType = 1
        updateString = input_string
        cv2.putText(img, updateString,
                    position,
                    font,
                    fontScale,
                    fontColor,
                    lineType)


class Detect:
    def __init__(self, input_img, input_sequence):
        # convert BGR to HSV
        imgHSV = cv2.cvtColor(input_img, cv2.COLOR_BGR2HSV)

        # create the Mask
        red_mask_0 = cv2.inRange(imgHSV, RED_LOWER, RED_UPPER)
        red_mask_1 = cv2.inRange(imgHSV, RED_LOWER_1, RED_UPPER_1)
        red_mask = red_mask_0 | red_mask_1
        # green_mask_1 = cv2.inRange(imgHSV, GREEN_LOWER_1, GREEN_UPPER_1)
        green_mask = cv2.inRange(imgHSV, GREEN_LOWER, GREEN_UPPER)
        # green_mask = green_mask_0 | green_mask_1
        green_mask = cv2.GaussianBlur(green_mask, (5, 5), 0)

        im_pro = ImageProcessing()
        im_pro.print_found_object(str(input_sequence), (0, 0))
        r = im_pro.create_contour_rectangle(red_mask, 255, 255, 0, "red")
        g = im_pro.create_contour_rectangle(green_mask, 255, 255, 0, "green")

        cv2.imshow("cam", input_img)
        cv2.waitKey(10)

        self.output_dict = {}

        if r:
            self.output_dict.update(r)

        if g:
            self.output_dict.update(g)


class ServoMovement:
    def __init__(self, input_servo_connection):
        self.input_object = input_servo_connection

    def move_to(self, input_position):
        self.input_object.goto(1, SERVO_SETTING[input_position][1], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(4, SERVO_SETTING[input_position][4], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(2, SERVO_SETTING[input_position][2], speed=SERVO_SPEED, degrees=True)
        self.input_object.goto(3, SERVO_SETTING[input_position][3], speed=SERVO_SPEED, degrees=True)
        time.sleep(4)

    def pick_up(self):
        # time.sleep(1.5)
        self.input_object.goto(5, 85, speed=120, degrees=True)
        time.sleep(1)

    def place(self):
        # time.sleep(1.5)
        self.input_object.goto(5, 20, speed=120, degrees=True)
        time.sleep(1)

    def reset(self):
        self.input_object.goto(3, 0, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(2, 0, speed=SERVO_SPEED, degrees=True)
        self.input_object.goto(4, 0, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(1, 0, speed=SERVO_SPEED, degrees=True)
        time.sleep(4)

    def open_hand(self):
        serial_connection.goto(5, 20, speed=SERVO_SPEED, degrees=True)
        time.sleep(4)


def pick_and_place(initial_location, destination):
    servo_class.move_to(initial_location)
    servo_class.pick_up()
    servo_class.reset()
    servo_class.move_to(destination)
    servo_class.place()
    servo_class.reset()


class MatchObjectPositions:
    def __init__(self):
        pass

    def get_keys(self, input_cordinates):
        output_list = []
        temp_list = []
        for keys in input_cordinates:
            for tuple_items in input_cordinates[keys]:
                for position_matching_keys in POSITION:
                    position_x = POSITION[position_matching_keys][0]
                    position_y = POSITION[position_matching_keys][1]
                    tuple_x = tuple_items[0]
                    tuple_y = tuple_items[1]
                    temp_dic = {}
                    if ((position_x - (TOLERANCE / 100) * position_x) <= tuple_x <= (
                            position_x + (TOLERANCE / 100) * position_x)) \
                            and ((position_y - (TOLERANCE / 100) * position_y) <= tuple_y <= (
                            position_y + (TOLERANCE / 100) * position_y)):
                        temp_dic[position_matching_keys] = keys
                        output_list.append(temp_dic)
        return output_list


class CreateRuleList:
    def __init__(self, input_log_file):
        log_object = open(input_log_file, "rb")
        data_log = log_object.read().decode("utf-8")
        data = data_log.split("\n")
        self.final_rules = []
        for txns in data:
            if re.search("missionar", txns) or re.search("cannibal", txns):
                temp = txns.split(": ")[-1].split("\r")[0]
                self.final_rules.append(temp)


def get_available_blocks_to_pick(input_matching_keys, input_color, input_position_subscript):
    position_list = []
    for items in input_matching_keys:
        for key in items:
            if re.search(input_color, items[key]) and re.search(input_position_subscript, key):
                position_list.append(key)
    return position_list


def get_available_positions_to_place(input_avialable_positions, input_position_subrscript):
    position_list = []
    for items in input_avialable_positions:
        if re.search(input_position_subrscript, items):
            position_list.append(items)
    return position_list


class PlayTheGame:
    def run(self, input_sequence, input_prolog_list, matching_keys, empty_positions):
        for items in input_prolog_list:
            if re.search("missionary", items.lower()) and re.search('cannibal', items.lower()) and re.search("cross", items.lower()) and re.search("one", items.lower()) and input_sequence in {0, 10}:
                engine.say(items)
                engine.runAndWait()
                input_sequence = self.run_sequence(input_sequence, matching_keys, empty_positions, "R", "L", MISSIONARY, CANNIBAL)
                input_sequence -= 1
                break

            elif re.search("missionary", items.lower()) and re.search("cannibal", items.lower()) and re.search("other", items.lower()) and re.search("one", items.lower()) and input_sequence == 5:
                engine.say(items)
                engine.runAndWait()
                input_sequence = self.run_sequence(input_sequence, matching_keys, empty_positions, "L", "R", MISSIONARY, CANNIBAL)
                input_sequence -= 1
                break

            elif re.search("missionary", items.lower()) and re.search("other", items.lower()) and not re.search("cannibal", items.lower()) and re.search("one", items.lower()) and input_sequence in {1, 9}:
                engine.say(items)
                engine.runAndWait()
                input_sequence, _, _ = self.solve_rule(matching_keys, empty_positions, MISSIONARY, "L", "R", input_sequence)
                break

            elif re.search("cannibal", items.lower()) and re.search("one", items.lower()) and not re.search("missionary", items.lower()) and re.search("other", items.lower()) and input_sequence in {3, 7}:
                engine.say(items)
                engine.runAndWait()
                input_sequence, _, _ = self.solve_rule(matching_keys, empty_positions, CANNIBAL, "L", "R", input_sequence)
                break

            elif re.search("cannibal", items.lower()) and re.search("two", items.lower()) and not re.search("missionar", items.lower()) and re.search("cross", items.lower()) and input_sequence in {2, 8}:
                engine.say(items)
                engine.runAndWait()
                input_sequence = self.run_sequence(input_sequence, matching_keys, empty_positions, "R", "L", CANNIBAL, CANNIBAL)
                input_sequence -= 1
                break

            elif not re.search("cannibal", items.lower()) and re.search("two", items.lower()) and re.search("missionar", items.lower()) and re.search("cross", items.lower()) and input_sequence in {4, 6}:
                engine.say(items)
                engine.runAndWait()
                input_sequence = self.run_sequence(input_sequence, matching_keys, empty_positions, "R", "L", MISSIONARY, MISSIONARY)
                input_sequence -= 1
                break

        return input_sequence

    def run_sequence(self, input_sequence, input_matching_keys, input_empty_positions, input_inital_side_subscript, input_destination_side_subscript, first_player, second_player):
        input_sequence, get_destination, get_location = self.solve_rule(input_matching_keys, input_empty_positions, first_player, input_inital_side_subscript, input_destination_side_subscript, input_sequence)
        input_empty_positions, input_matching_keys = self.update_position_lists(first_player, input_empty_positions, get_destination, get_location, input_matching_keys)
        input_sequence, get_destination, get_location = self.solve_rule(input_matching_keys, input_empty_positions, second_player, input_inital_side_subscript, input_destination_side_subscript, input_sequence)
        return input_sequence

    def update_position_lists(self, input_key, input_empty_positions, input_get_destination, input_get_location, input_matching_keys):
        input_matching_keys.append({input_get_destination: input_key})
        input_matching_keys.remove({input_get_location: input_key})
        input_empty_positions.append(input_get_location)
        input_empty_positions.remove(input_get_destination)
        return input_empty_positions, input_matching_keys

    def solve_rule(self, input_matching_keys, input_empty_positions, player, initial_subscript, destination_subscript, sequence):
        possible_pick_positions = get_available_blocks_to_pick(input_matching_keys, player, initial_subscript)
        possible_drop_positions = get_available_positions_to_place(input_empty_positions, destination_subscript)
        get_location = ""
        get_destination = ""
        if possible_pick_positions and possible_drop_positions:
            get_location = random.choice(possible_pick_positions)
            get_destination = random.choice(possible_drop_positions)
            pick_and_place(get_location, get_destination)
            sequence += 1
        return sequence, get_destination, get_location


def get_empty_positions(input_matching_keys):
    filled_positions = []
    for items in input_matching_keys:
        for keys in items:
            filled_positions.append(keys)
    return [i for i in POSSIBLE_POSITIONS if i not in filled_positions]


if __name__ == "__main__":
    # prolog log file
    log_file = "C:/Users/szs_r/PycharmProjects/opencv_test/log_file.txt"

    # initialize variables
    kernelOpen = np.ones((5, 5))
    kernelClose = np.ones((20, 20))
    image_hsv = None
    count = 0
    sequence = 0

    # open camera
    serial_connection: Connection = Connection(port="COM3", baudrate=1000000)
    cv2.VideoCapture(1).isOpened()

    # initalize game objects
    solve_prolog = CreateRuleList(log_file)
    servo_class = ServoMovement(serial_connection)
    play_obj = PlayTheGame()
    matching_class = MatchObjectPositions()
    engine = pyttsx3.init()

    # start gathering data
    cam = cv2.VideoCapture(1)
    final_rule_list = CreateRuleList(log_file).final_rules

    # reset the hand before
    servo_class.reset()
    servo_class.open_hand()
    empty_positions = []

    # Begin the game
    engine.say("Three cannibals and three missionaries come to a crocodile infested river. "
               "There is a boat on their side that can be used by either one or two persons. "
               "If cannibals outnumber the missionaries at any time, the cannibals eat the missionaries. "
               "How can they use the boat to cross the river so that all missionaries survive ?")
    engine.runAndWait()
    engine.say("The " + MISSIONARY + " blocks are used as missionary and the " + CANNIBAL + " blocks are used as cannibal")
    engine.runAndWait()


    while True:
        ret, img = cam.read()
        end_of_game = ["R1", "R2", "R3", "R4", "R5", "R6"]
        # skip 60 frames - we need to do this clean the image buffer so that we look at that most recent image
        if count % 60 == 1:
            img = cv2.resize(img, (1080, 640))
            output_data = Detect(img, sequence).output_dict
            matching_keys = matching_class.get_keys(output_data)
            matching_keys = [dict(t) for t in set([tuple(d.items()) for d in matching_keys])]
            empty_positions = get_empty_positions(matching_keys)
            # DEBUG PRINTS
            print("- - - - - - - - - - - - - - - - ")
            print("Emtpy Positions -: " + str(empty_positions))
            print("Matching Keys :- " + str(matching_keys))
            # DEBUG PRINTS

            if len(matching_keys) == 6:
                sequence = play_obj.run(sequence, final_rule_list, matching_keys, empty_positions)

                # DEBUG PRINTS
                print("sequence :" + str(sequence))
                # DEBUG PRINTS

        # check if all the robots has been transferred to the other side
        if empty_positions == end_of_game:
            engine.say("Game Over")
            engine.runAndWait()
            break

        count += 1

#!/usr/bin/env python
# coding: utf-8
import copy

from gui import update_block, get_fixtures, get_toolbar, deal_with_toolbar_event, get_clicked_keys_gui
from keyboardmouse import *
from sneakysnek.keyboard_event import KeyboardEvent
from sneakysnek.recorder import Recorder

cur_key = None
key = None
key_change_ok = True

def get_key(event):
    global key
    global key_change_ok
    if event.event.value == "UP":
        key = ""
    elif type(event) == KeyboardEvent and key_change_ok:
        key = event.keyboard_key.value.lower().replace("key_","")
        key_change_ok = False

def add(event, x, y, flags, param):
    global draw
    global cur_key
    global phys
    global msg
    global board
    global key_type

    old_x = x
    old_y = y

    x_new = (x + board.translation[0] * -1)
    y_new = (y + board.translation[1] * -1)

    # check for screen move
    if event == cv2.EVENT_MBUTTONDOWN or draw.move_screen:
        """
        Used to move the screen
        """
        if event == cv2.EVENT_MBUTTONDOWN:
            draw.move_screen = True
        draw, board = move_screen(draw, board, x_new, y_new, event)

    # check if no key
    if (cur_key is None or cur_key == "") and (not draw.move_screen or not event == cv2.EVENT_MBUTTONDOWN):
        return
    elif (draw.move_screen or event == cv2.EVENT_MBUTTONDOWN):
        pass
    # check all other keys
    elif cur_key[0] == "1" and cur_key_type == 0:
        """
        Used to create fire blocks or create them.
        """
        draw, phys = fire(draw, phys, event, x_new, y_new, cur_key, board)

    elif cur_key[0] == "j" and cur_key_type == 0:

        """
        Used to create joints
        """

        if cur_key[1:] == SelectType.straight_join.value:
            if msg.message == "Distance Joint":
                draw, phys = distance_draw(draw, phys, event, x_new, y_new, cur_key)
            elif msg.message == "Rope Joint":
                draw, phys = rope(draw, phys, event, x_new, y_new, cur_key)

            elif msg.message == "Prismatic Joint":
                draw, phys = prismatic(draw, phys, event, x_new, y_new, cur_key)

            elif msg.message == "Weld Joint":
                try:
                    draw, phys = weld(draw, phys, event, x_new, y_new, cur_key)
                except AssertionError:
                    draw.reset()
                    print("Weld Selection Error")

        elif cur_key[1:] == SelectType.line_join.value:
            if msg.message == "Electric":
                draw, phys = lightning(draw, phys, event, x_new, y_new, cur_key)

        elif cur_key[1:] == SelectType.line_join2.value:
            if msg.message == "Chain":
                draw, phys = chain(draw, phys, event, x_new, y_new, cur_key)

        elif cur_key[1:] == SelectType.d_straight_join.value:
            if msg.message == "Pulley":
                draw, phys = pulley(draw, phys, event, x_new, y_new, cur_key)

        elif cur_key[1:] == SelectType.select.value:
            if msg.message == "Merge Blocks":
                draw, phys = merge_blocks(draw, phys, event, x_new, y_new, cur_key)

        elif cur_key[1:] == SelectType.rotation_select.value:
            if msg.message == "Rotation Joint":
                draw, phys = rotation(draw, phys, event, x_new, y_new, cur_key)

        elif cur_key[1:] == SelectType.rotation_select.value:
            if msg.message == "Pulley Joint":
                draw, phys = pulley(draw, phys, event, x_new, y_new, cur_key)


        elif cur_key[1:] == SelectType.circle.value:
            if msg.message == "Wheel Joint":
                draw, phys = wheel_draw(draw, phys, event, x_new, y_new, cur_key)


    elif cur_key[0] == "u" and cur_key_type == 0:
        """
        Used to remove joints
        """

        draw, phys = remove_joints(draw, phys, event, x_new, y_new, cur_key)

    elif cur_key[0] == "k" and cur_key_type == 0:
        """
        Used to create Forces sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="force")


    elif cur_key[0] == "l" and cur_key_type == 0:
        """
        Used to create Splitter sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="splitter")

    elif cur_key[0] == "/" and cur_key_type == 0:
        """
        Used to create booster sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="impulse")

    elif cur_key[0] == "{" and cur_key_type == 0:
        """
        Used to create Spawn sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="spawner")

    elif cur_key[0] == "'" and cur_key_type == 0:
        """
        Used to create Goal sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="goal")

    elif cur_key[0] == ")" and cur_key_type == 0:
        """
        Used to create Center sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="center")


    elif cur_key[0] == "^" and cur_key_type == 0:
        """
        Used to create Gravity sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="lowgravity")


    elif cur_key[0] == "#" and cur_key_type == 0:
        """
        Used to create Gravity sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="gravity")

    elif cur_key[0] == "~" and cur_key_type == 0:
        """
        Used to create motorsw sensors
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="motorsw")

    elif cur_key[0] == "%" and cur_key_type == 0:
        """
        Used to create sticky sensors

        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="sticky")


    elif cur_key[0] == "&" and cur_key_type == 0:
        """
        Used to create water sensors

        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="water")


    elif cur_key[0] == "£" and cur_key_type == 0:
        """
        Used to create Enlarger sensors
        
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="enlarger")

    elif cur_key[0] == "$" and cur_key_type == 0:
        """
        Used to create shrinker sensors

        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_sensor(draw, phys, event, x_new, y_new, cur_key, ty="shrinker")


    elif cur_key[0] == ";" and cur_key_type == 0:
        """
        Used to select blocks and print details (for now)
        """
        draw, phys = select_blocks(draw, phys, event, x_new, y_new, cur_key)
        if len(draw.player_list) >= 1:
            draw.player_list[0] = update_block(draw.player_list[0])
            phys.block_list = sorted(phys.block_list, key=lambda itm: itm.draw_position)
            draw.reset()

    elif cur_key[0] == "4" and cur_key_type == 0:
        """
        Used to select a blocks joints and print details (for now)
        """
        draw, phys = select_blocks(draw, phys, event, x_new, y_new, cur_key)
        if len(draw.player_list) >= 1:
            draw.player_list[0] = get_fixtures(draw.player_list[0], board)
            draw.reset()

    elif cur_key[0] == "v" and cur_key_type == 0:
        """
        Used to set spawn point
        """
        draw, phys, ans, coords = get_spawn(draw, phys, event, x_new, y_new, cur_key)

        if ans:
            h, w, _ = board.board.shape

            max_x, max_y = np.round(np.max(coords, axis=0)).astype(int)
            min_x, min_y = np.round(np.min(coords, axis=0)).astype(int)

            phys.options["blocks_out"]["start_pos_x_min"] = int(min_x / w * 100)
            phys.options["blocks_out"]["start_pos_x_max"] = int(max_x / w * 100)
            phys.options["blocks_out"]["start_pos_y_min"] = int(min_y / h * 100)
            phys.options["blocks_out"]["start_pos_y_max"] = int(max_y / h * 100)
            config["blocks_out"]["start_pos_x_min"] = int(min_x / w * 100)
            config["blocks_out"]["start_pos_x_max"] = int(max_x / w * 100)
            config["blocks_out"]["start_pos_y_min"] = int(min_y / h * 100)
            config["blocks_out"]["start_pos_y_max"] = int(max_y / h * 100)
            config.write()
            draw.reset()

    elif cur_key[0] == "t" and cur_key_type == 0:
        """
        Used to transform block
        """
        """
        Used to rotate blocks
        """

        if cur_key[1:] == SelectType.player_select.value:
            draw, phys = transform_block(draw, phys, event, x_new, y_new, cur_key, board=board)


    elif cur_key[0] == "2" and cur_key_type == 0:
        """
        Used to rotate blocks
        """

        if cur_key[1:] == SelectType.player_select.value:
            draw, phys = rotate_block(draw, phys, event, x_new, y_new, cur_key, board=board)

    elif cur_key[0] == "m" and cur_key_type == 0:
        """
        Used to move or clone blocks
        """

        if cur_key[1:] == SelectType.select.value and msg.message == "Mouse Move":
            draw, phys = mouse_joint_move(draw, phys, x_new, y_new, event, cur_key)


        else:
            if msg.message == "Clone Move":
                draw, phys = move_clone(draw, phys, x_new, y_new, event, True, board=True, move=False)
            elif msg.message == "Normal Move":
                draw, phys = move_clone(draw, phys, x_new, y_new, event, False, board=True, joint_move=False, move=True)
            elif msg.message == "Joint Move":
                draw, phys = move_clone(draw, phys, x_new, y_new, event, False, board=True, joint_move=True, move=True)

            phys.set_active()

    elif cur_key[0] == "x" and cur_key_type == 0:

        """
        Used to delete objects on click
        """
        draw, phys = delete(draw, phys, event, x_new, y_new, cur_key, board=board)

    elif cur_key[0] == "p" and cur_key_type == 0:
        """
        Used to create polygons

        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_shape(draw, phys, event, x_new, y_new, cur_key, board=board)

    elif cur_key[0] == "f" and cur_key_type == 0:
        """
        Used to create fractals
        """
        draw, phys = draw_fragment(draw, phys, event, x_new, y_new, cur_key, board=board)

    elif cur_key[0] == "g" and cur_key_type == 0:
        """
        Used to create ground
        """
        cur_key = cur_key[0] + str(draw.draw_type)
        draw, phys = draw_ground(draw, phys, event, x_new, y_new, cur_key, board=board)

    ###################
    # movement functions
    ###################

    elif cur_key[0] == "]" and cur_key_type == 1:

        """
        Used to select fire bullets from the player on click
        """
        draw, phys = fire_bullet(draw, phys, event, x_new, y_new, cur_key, board=board)

    elif cur_key[0] == "[" and cur_key_type == 1:

        """
        Used to select objects to be a player click
        """
        draw, phys = make_player(draw, phys, event, x_new, y_new, cur_key)


    elif cur_key[0] == "`" and cur_key_type == 1:
        """
        Used to select blocks and print details (for now)
        """
        draw, phys = select_blocks(draw, phys, event, x_new, y_new, cur_key)
        if len(draw.player_list) >= 1:
            bl = get_clicked_keys_gui(draw.player_list[0])
            draw.reset()

    elif cur_key[0] == "2" and cur_key_type == 1:
        """
        Used to center the board on the clicked player
        """
        if msg.message == "Center Clicked":
            # centers the board onto the clicked player
            draw, phys = center_clicked(draw, phys, x_new, y_new, event, cur_key)

    elif cur_key[0] == "3" and cur_key_type == 1:
        """
        Used to attach a motor spin forwards
        """
        draw, phys = attach_motor_spin(draw, phys, event, x_new, y_new, cur_key, board, clockwise=False)

    elif cur_key[0] == "4" and cur_key_type == 1:
        """
        Used to attach a motor spin backwards
        """
        draw, phys = attach_motor_spin(draw, phys, event, x_new, y_new, cur_key, board, clockwise=True)


    elif cur_key[0] == "9" and cur_key_type == 1:
        """
        Used to attach a force to a block
        """
        draw, phys = add_force(draw, phys, event, x_new, y_new, cur_key, board)

    elif cur_key[0] == "0" and cur_key_type == 1:
        """
        Used to attach a relative force to a block
        """
        draw, phys = add_force(draw, phys, event, x_new, y_new, cur_key, board, relative=True)

    elif cur_key[0] == "5" and cur_key_type == 1:
        """
        Used to attach a rotation to a block CCW
        """
        draw, phys = rotate_attach(draw, phys, event, x_new, y_new, cur_key, board, direction="CCW")

    elif cur_key[0] == "6" and cur_key_type == 1:
        """
        Used to attach a rotation to a block CCW
        """
        draw, phys = rotate_attach(draw, phys, event, x_new, y_new, cur_key, board, direction="CW")

    elif cur_key[0] == "7" and cur_key_type == 1:
        """
        Used to attach an impulse to a block
        """
        draw, phys = add_impulse(draw, phys, event, x_new, y_new, cur_key, board)

    elif cur_key[0] == "8" and cur_key_type == 1:
        """
        Used to attach an relative impulse to a block
        """
        draw, phys = add_impulse(draw, phys, event, x_new, y_new, cur_key, board, relative=True)

    # this moves the screen based on if the mouse is on the edge of the screen - hard to get to the controls
    if phys.options["screen"]["allow_x_move"] is True:
        if old_x < board.board.shape[1] * .15:
            board.x_trans_do = "up"
        elif old_x > board.board.shape[1] * .85:
            board.x_trans_do = "down"
        else:
            board.x_trans_do = None

    if phys.options["screen"]["allow_y_move"] is True:
        if old_y < board.board.shape[0] * .15:
            board.y_trans_do = "up"
        elif old_y > board.board.shape[0] * .85:
            board.y_trans_do = "down"
        else:
            board.y_trans_do = None


if __name__ == "__main__":

    # init the physics engine, board, and timer.
    timer, phys, draw, board, msg = load_gui(persistant=True)

    #record key presses
    recorder = Recorder.record(get_key)

    # load config
    config = phys.config

    # init other running vars
    force = False
    loops = 0
    timeStep = 1.0 / 50
    cur_key = ""
    cur_key_type = 0

    # key_type = 1

    # set window name and mouse callback for mouse events
    cv2.namedWindow("Board")
    cv2.setMouseCallback("Board", add)

    # get the tool bar
    toolbar = get_toolbar()

    # start loop
    if not hasattr(board, "run"):
        setattr(board, "run", True)

    snaps = 0
    while board.run:

        # read toolbar
        toolbar, click_key, name, cur_key_type, draw, msg, force = deal_with_toolbar_event(toolbar, cur_key, cur_key_type,draw, msg)
        if not click_key is None:
            key = click_key

        # move to snap to board
        #if loops % 10 == 0:
        if snaps == 0:
            toolbar.move(cv2.getWindowImageRect("Board")[0] + board.board.shape[1],cv2.getWindowImageRect("Board")[1] - 53)
            snaps +=1

        # get key press
        # if _ is None:
        _ = cv2.waitKey(1) & 0xFF

        # deal with keypress OR spawn per config file

        cur_key_type, cur_key, draw, phys, msg, timer, board = action_key_press(key, cur_key_type, cur_key, draw, phys,
                                                                                msg, timer, board, force)
        key = ""
        key_change_ok = True

        # load a blank background board
        board.copy_board()

        # draw physics
        phys.draw_blocks()

        # draw front of board
        board.draw_front()

        # draw joints
        phys.draw_joints()

        # write lines for drawwing
        draw.draw_point()

        # write message if needed
        msg.draw_message((not draw.pause is True) and (phys.pause is False))

        # show board
        cv2.imshow("Board", board.board_copy[:, :, ::-1])

        # timer log - this handles FPS
        timer.log()

        # increment loops for additional players
        loops += 1

        # step the physics engine if draw needed
        if (not draw.pause is True) and (phys.pause is False):

            # create player if needed
            if loops > phys.options["blocks"]["spawn_every"]:
                phys.create_block()
                loops = 0

            # check players off screen to kill (otherwise they would continue to be calculated off screen wasting CPU) or if they have reached the goal
            goal_hits = phys.check_off()
            msg.goal_hits += goal_hits

            # step the physics engine1
            phys.world.Step(timeStep, 6, 6)
            phys.world.ClearForces()

            # this applies impulses gathered from any booster sensors.
            phys.check_sensor_actions()

        # check if the player has hit goal and needs reset?
        timer, phys, board, draw, msg = board.reset_me(timer, phys, board, draw, msg)

    cv2.destroyAllWindows()

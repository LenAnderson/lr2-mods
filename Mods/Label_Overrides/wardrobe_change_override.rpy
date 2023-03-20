
init 6 python:
    config.label_overrides["wardrobe_change_label"] = "LENA_wardrobe_change_label_enhanced"

    def build_wardrobe_change_menu():
        return ["Choose", ["Add an outfit", "add"], ["Delete an outfit", "delete"], ["Modify an outfit", "modify"], ["Wear an outfit right now", "wear"], ["Back", "back"]]

    def build_wardrobe_change_save_menu(outfit):
        option_list = []
        option_list.append("Save Outfit As")
        option_list.append(["Full outfit", "full"])
        if outfit.is_suitable_underwear_set():
            option_list.append(["Underwear set", "under"])
        if outfit.is_suitable_overwear_set():
            option_list.append(["Overwear set", "over"])
        option_list.append(["Forget it", "none"])
        return option_list
    
    def LENA_wear_outfit(the_person, outfit, outfit_type):
        print('LENA_wear_outfit: ', the_person, outfit, outfit_type)
        outfit = outfit.get_copy()
        # if outfit in the_person.wardrobe.outfits:
        #     print('is full')
        #     outfit_type = "full"
        # elif outfit in the_person.wardrobe.overwear_sets:
        #     print('is over')
        #     outfit_type = "over"
        # elif outfit in the_person.wardrobe.underwear_sets:
        #     print('is under')
        #     outfit_type = "under"
        print('outfit_type', outfit_type)

        if outfit_type == "over":
            the_outfit = the_person.outfit.get_underwear()
        elif outfit_type == "under":
            the_outfit = the_person.outfit.get_overwear()
        
        if outfit_type == "over" or outfit_type == "under":
            if the_outfit is None:
                if outfit_type == "over":
                    the_outfit = the_person.wardrobe.pick_random_underwear()
                else:
                    the_outfit = the_person.wardrobe.pick_random_overwear()
            for upper in the_outfit.upper_body:
                outfit.upper_body.append(upper.get_copy())
            for lower in the_outfit.lower_body:
                outfit.lower_body.append(lower.get_copy())
            for feet in the_outfit.feet:
                outfit.upper_body.append(feet.get_copy())
            for accessories in the_outfit.accessories:
                outfit.upper_body.append(accessories.get_copy())
            the_outfit = None
        the_person.set_outfit(outfit)

label LENA_wardrobe_change_label_enhanced(the_person):
    call screen enhanced_main_choice_display(build_menu_items([build_wardrobe_change_menu()]))
    $ strip_choice = _return

    if strip_choice == "add":
        mc.name "[the_person.title], I've got something I'd like you to wear for me."
        $ clear_scene()
        call outfit_master_manager(main_selectable = True) from LENA_call_outfit_master_manager_change_enhanced
        $ the_person.draw_person()
        if not _return:
            mc.name "On second thought, never mind."
            return

        if isinstance(_return, list): # Newer versions
            $ new_outfit = _return[1] #Select the outfit from the returned list
        else: #Compatability for older versions.
            $ new_outfit = _return

        call screen enhanced_main_choice_display(build_menu_items([build_wardrobe_change_save_menu(new_outfit)]))
        $ outfit_type = _return

        if outfit_type != "none":
            if the_person.judge_outfit(new_outfit, as_underwear = outfit_type == "under", as_overwear = outfit_type == "over"):
                $ the_person.add_outfit(new_outfit,outfit_type)
                $ the_person.call_dialogue("clothing_accept")
            else:
                $ the_person.call_dialogue("clothing_reject")
        $ del new_outfit

    elif strip_choice == "delete":
        mc.name "[the_person.title], let's have a talk about what you've been wearing."
        $ clear_scene()
        call screen outfit_delete_manager(the_person.wardrobe)
        $ the_person.apply_planned_outfit()
        $ the_person.draw_person()

    elif strip_choice == "modify":
        mc.name "[the_person.title], let's have a talk about what you've been wearing."
        $ clear_scene()
        call screen girl_outfit_select_manager(the_person.wardrobe, slut_limit = the_person.effective_sluttiness() + 20, show_sets = True)
        if _return != "None":
            $ outfit = _return.get_copy()
            $ the_outfit = _return
            $ is_worn = False
            $ slut_limit = the_person.effective_sluttiness() + 20
            if outfit in the_person.wardrobe.outfits:
                $ outfit_type = "full"
                $ is_worn = True if the_person.outfit.matches(the_outfit) else False
            elif outfit in the_person.wardrobe.overwear_sets:
                $ outfit_type = "over"
                $ is_worn = the_person.outfit.get_overwear().matches(the_outfit)
            elif outfit in the_person.wardrobe.underwear_sets:
                $ outfit_type = "under"
                $ is_worn = the_person.outfit.get_underwear(exclude_shoes=True).matches(the_outfit)
            $ print(outfit_type, ' is_worn: ', is_worn)
            call screen outfit_creator(outfit, outfit_type = outfit_type, slut_limit = slut_limit)
            $ outfit = _return
            if outfit is None:
                $ print('outfit is None')
                pass
            else:
                if outfit != "Not_New":
                    $ the_person.wardrobe.remove_outfit(the_outfit)
                    $ new_outfit_name = renpy.input("Please name this outfit.", default = outfit.name)
                    while new_outfit_name == "":
                        $ new_outfit_name = renpy.input("Please enter a non-empty name.", default = outfit.name)
            $ print('is_worn=',is_worn, 'outfit=',outfit)
            if is_worn and outfit is not None and outfit != "Not_New":
                $ LENA_wear_outfit(the_person, outfit, outfit_type)
                if the_person.update_outfit_taboos():
                    "[the_person.title] seems nervous wearing her new outfit in front of you, but quickly warms up to it."
                the_person "Is this better?"
            $ the_outfit = None
        $ the_person.apply_planned_outfit()
        $ the_person.draw_person()

    elif strip_choice == "wear":
        mc.name "[the_person.title], I want you to get changed for me."
        $ clear_scene()
        call screen girl_outfit_select_manager(the_person.wardrobe, slut_limit = the_person.effective_sluttiness() + 20)
        if _return != "None":
            $ the_person.set_outfit(_return)
            if the_person.update_outfit_taboos():
                "[the_person.title] seems nervous wearing her new outfit in front of you, but quickly warms up to it."
            the_person "Is this better?"
        else:
            $ the_person.apply_planned_outfit()
        $ the_person.draw_person()
    return



    screen LENA_outfit_modify_manager(target_wardrobe, show_sets=True, slut_limit=9999):


        modal True
        zorder 99
        default preview_outfit = None
        default import_selection = False
        default mannequin = the_person

        hbox:
            xalign 0.1
            yalign 0.1
            spacing 20
            frame:
                background "#0a142688"
                xsize 450
                ysize 750


                has vbox
                frame:
                    background "#000080"
                    xfill True
                    text "Full Outfit Modify" style "menu_text_title_style" xalign 0.5

                viewport:

                    if __builtin__.len(target_wardrobe.get_outfit_list()) > 11:
                        scrollbars "vertical"
                    xfill True
                    yfill True
                    mousewheel True
                    vbox:
                        for outfit in sorted(target_wardrobe.get_outfit_list(), key = lambda outfit: outfit.slut_requirement):
                            textbutton "Modify " + outfit.name.replace("_", " ").title() + "\n" + get_heart_image_list_cloth(outfit.slut_requirement, 1):
                                style "textbutton_no_padding_highlight"
                                text_style "serum_text_style"

                                xfill True

                                sensitive (outfit.slut_requirement <= slut_limit)

                                action Return(["modify",outfit])

                                if the_person is not None:
                                    hovered Function(draw_mannequin, the_person, outfit)
                                    alternate Show("outfit_creator", None, outfit.get_copy(), "full", slut_limit, the_person.wardrobe)
                                else:
                                    hovered Function(draw_average_mannequin, outfit)

            if show_sets:
                frame:
                    background "#0a142688"
                    xsize 450
                    ysize 750
                    has vbox
                    frame:
                        background "#000080"
                        xfill True
                        text "Overwear Modify" style "menu_text_title_style" xalign 0.5

                    viewport:
                        if __builtin__.len(target_wardrobe.get_overwear_sets_list()) > 11:
                            scrollbars "vertical"
                        xfill True
                        yfill True
                        mousewheel True
                        vbox:
                            for outfit in sorted(target_wardrobe.get_overwear_sets_list(), key = lambda outfit: outfit.slut_requirement):
                                textbutton "Modify " + outfit.name.replace("_", " ").title() + "\n" + get_heart_image_list_cloth(outfit.slut_requirement, 1):
                                    style "textbutton_no_padding_highlight"
                                    text_style "serum_text_style"

                                    xfill True

                                    sensitive (outfit.slut_requirement <= slut_limit)

                                    action Return(["modify",outfit])
                                    if the_person is not None:
                                        hovered Function(draw_mannequin, the_person, outfit)
                                        alternate Show("outfit_creator", None, outfit.get_copy(), "over", slut_limit, the_person.wardrobe)
                                    else:
                                        hovered Function(draw_average_mannequin, outfit)


                frame:
                    background "#0a142688"
                    xsize 450
                    ysize 750
                    has vbox
                    frame:
                        background "#000080"
                        xfill True
                        text "Underwear Modify" style "menu_text_title_style" xalign 0.5

                    viewport:
                        if __builtin__.len(target_wardrobe.get_underwear_sets_list()) > 11:
                            scrollbars "vertical"
                        xfill True
                        yfill True
                        mousewheel True
                        vbox:
                            for outfit in sorted(target_wardrobe.get_underwear_sets_list(), key = lambda outfit: outfit.slut_requirement):
                                textbutton "Modify " + outfit.name.replace("_", " ").title() + "\n" + get_heart_image_list_cloth(outfit.slut_requirement, 1):
                                    style "textbutton_no_padding_highlight"
                                    text_style "serum_text_style"

                                    xfill True

                                    sensitive (outfit.slut_requirement <= slut_limit)

                                    action Return(["modify",outfit])
                                    if the_person is not None:
                                        hovered Function(draw_mannequin, the_person, outfit)
                                        alternate Show("outfit_creator", None, outfit.get_copy(), "under", slut_limit, the_person.wardrobe)
                                    else:
                                        hovered Function(draw_average_mannequin, outfit)

        frame:
            background None
            anchor [0.5,0.5]
            align [0.5,0.88]
            xysize [500,125]
            imagebutton:
                align [0.5,0.5]
                auto "gui/button/choice_%s_background.png"
                focus_mask "gui/button/choice_idle_background.png"
                action [Return("No Return"), Function(hide_mannequin)]
            textbutton "Return" align [0.5,0.5] text_style "return_button_style"

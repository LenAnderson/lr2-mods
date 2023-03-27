## This file contains events that are triggered by employees not being slutty/obedient enough for certain policies
# These are generally Limited Time Events, usually available only for a single turn, and triggered when you either walk into the room
# or when you talk to the person.


init -1 python:
    def dress_code_min_disobedience_on_move(dress_code_min_disobedience_priority): #This is an on_move function called by the business on_move phase. It is only run once, by the uniform policy with the highest priority
        print("dress_code_min_disobedience_on_move", dress_code_min_disobedience_priority)
        highest_active_priority = -1
        for policy in [x for x in mc.business.active_policy_list if "dress_code_min_disobedience_priority" in x.extra_arguments]:
            if policy.extra_arguments.get("dress_code_min_disobedience_priority", -1) > highest_active_priority:
                highest_active_priority = policy.extra_arguments.get("dress_code_min_disobedience_priority",-1) #Check all policies and make sure we are only running this function once (with the highest priority, just in case)

        print('highest_active_priority', highest_active_priority, dress_code_min_disobedience_priority)
        if highest_active_priority != dress_code_min_disobedience_priority: #ie. only run this function if we have the highest priority, otherwise some other policy is responsible for it.
            return
        
        slut_limit_lower = mc.business.get_uniform_lower_limits()

        for person in [x for x in mc.business.get_employee_list() if x.should_wear_dress_code()]:
            print('checking', person.name, 'score=',person.outfit.get_full_outfit_slut_score(), ' limit=',slut_limit_lower)
            if person.event_triggers_dict.get("forced_uniform", False):
                # person is wearing a forced (punishment) uniform
                pass
            elif person.event_triggers_dict.get('accepted_dress_code_outfit_day', -1) == day and person.event_triggers_dict.get('accepted_dress_code_outfit', None) == person.outfit:
                # person was already caught today and is currently wearing the outfit that resulted out of that interaction
                pass
            elif person.dress_code_outfit:
                if person.outfit.get_full_outfit_slut_score() < slut_limit_lower:
                    print('-> no outfit')
                    dress_code_min_disobedience_action = Action("Dress Code Min Disobedience LTE", dress_code_min_disobedience_requirement, "dress_code_min_disobedience_event", event_duration = 3, args = person.dress_code_outfit.get_copy())
                    person.on_talk_event_list.append(Limited_Time_Action(dress_code_min_disobedience_action, dress_code_min_disobedience_action.event_duration))
                else:
                    print('-> chance based')
                    disobedience_chance = 0
                    if not person.judge_outfit(person.dress_code_outfit):
                        disobedience_chance = person.dress_code_outfit.get_full_outfit_slut_score() - __builtin__.int( person.effective_sluttiness() * (person.obedience / 150.0) ) #Girls who find the outfit too slutty might disobey, scaled by their obedience
                        disobedience_chance += -5*(person.get_opinion_score("skimpy uniforms"))
                    else:
                        disobedience_chance = (150 - person.obedience)/2 #Disobedient girls sometimes don't wear uniforms, just because they don't like following orders. Less likely than when outfits are too slutty.
                        disobedience_chance += -5*(person.get_opinion_score("work uniforms"))
                    if renpy.random.randint(0,100) < __builtin__.max(disobedience_chance, 3): # minimum chance is 3%
                        dress_code_min_disobedience_action = Action("Dress Code Min Disobedience LTE", dress_code_min_disobedience_requirement, "dress_code_min_disobedience_event", event_duration = 3, args = person.dress_code_outfit.get_copy()) #Needs to be created here so we can reference what we disliked about the uniform.
                        person.on_talk_event_list.append(Limited_Time_Action(dress_code_min_disobedience_action, dress_code_min_disobedience_action.event_duration))
                        person.dress_code_outfit = person.planned_outfit #Overwrites the uniform they intended to wear for the day, so the next Move doesn't change it but the end of day will.
                        person.apply_outfit() #Change them into their planned outfits for the day

        return

    def dress_code_min_disobedience_requirement(the_person):
        if the_person.event_triggers_dict.get("forced_uniform", False):
            # person is wearing a forced (punishment) uniform
            return False
        if the_person.event_triggers_dict.get('accepted_dress_code_outfit_day', -1) == day and the_person.event_triggers_dict.get('accepted_dress_code_outfit', None) == the_person.outfit:
            # person was already caught today and is currently wearing the outfit that resulted out of that interaction
            return false
        if the_person.should_wear_dress_code() and the_person.outfit.get_full_outfit_slut_score() < mc.business.get_uniform_lower_limits():
            # person should wear a dress code outfit but sluttiness is below policy
            return True
        return False


label dress_code_min_disobedience_event(dress_code_outfit, the_person):
    $ slut_limit_lower = mc.business.get_uniform_lower_limits()
    $ has_no_outfit = False
    "As you walk up to [the_person.title] you notice that she isn't wearing an outfit adhering to the company dress code."
    $ the_person.draw_person()

    if the_person.obedience < 110:
        $ the_person.call_dialogue("greetings")
    else:
        "[the_person.possessive_title] seems nervous when she notices you approaching."
    mc.name "Is there some reason you're not following the dress code, [the_person.title]?"

    if dress_code_outfit.get_full_outfit_slut_score() < slut_limit_lower: # doesn't have an outfit matching the dress code
        $ has_no_outfit = True
        if the_person.obedience < 120:
            the_person "I don't even own something like that [the_person.mc_title], it's ridiculous!"
            the_person "It wouldn't cover anything, and would make me feel like a cheap prostitute while I'm working."
            the_person "I don't know how it's even legal to require us to wear something like that!"
        else:
            the_person "I'm sorry [the_person.mc_title]. I don't own any outfits like that, I didn't think you'd notice..."
            the_person "If we could have some variations with some underwear, I'd be a lot more comfortable with the dress code."
    else:
        if the_person.effective_sluttiness() >= dress_code_outfit.slut_requirement: #Just disobedient
            $ random_excuse = renpy.random.randint(0,2) #Get a random excuse for why she's not wearing her uniform. #TODO: Base this on her obedience/sluttiness. Personality maybe?
            if random_excuse == 0:
                the_person "I'm sorry, I just had to step out for a moment to pick something up. I was assuming that wouldn't be a problem."
            elif random_excuse == 1:
                the_person "It's so impractical, I couldn't get anything done. I'm going to wear this for a few hours and get some real work done."
            else: # random_excuse == 2:
                the_person "That dress code policy is just a suggestion, right? There's no way you expect us to actually wear it all the time."

        elif dress_code_outfit.vagina_visible():
            if the_person.obedience < 120:
                the_person "I just can't wear it [the_person.mc_title], it's ridiculous!"
                the_person "It doesn't cover anything, and makes me feel like a cheap prostitute while I'm working."
                the_person "I don't know how it's even legal to require us to wear it!"
            else:
                the_person "I'm sorry [the_person.mc_title]. It just provides so little coverage, I didn't think you'd notice..."
                the_person "If we could have some variations with some underwear, I'd be a lot more comfortable following the dress code."

        elif dress_code_outfit.tits_visible():
            if the_person.obedience < 120:
                the_person "I just can't wear it [the_person.mc_title], it's demeaning!"
                the_person "If I wear your uniform I would have my tits out, all day long! How am I supposed to focus like that?"
            else:
                the_person "I'm sorry [the_person.mc_title], I know I should be wearing it, but..."
                the_person "It's just so revealing! If I could wear a bra, or anything, to keep me a little covered I would be more comfortable."
        elif dress_code_outfit.underwear_visible():
            if the_person.obedience < 120:
                the_person "Do you really expect us to dress like that all the time? I would be half naked, all day!"
                the_person "It's demeaning, I feel like I'm just here for men to leer at."
            else:
                the_person "I'm sorry [the_person.mc_title]! I was feeling embarrassed about standing around in my underwear."
                the_person "Maybe we could have a dress code with some more coverage? Just a little would go a long way!"
        else:
            if the_person.obedience < 120:
                the_person "Do we really have to dress like that all day? It's so... revealing, it's just embarrassing to be in."
            else:
                the_person "I'm sorry [the_person.mc_title]!"
                the_person "It's nothing like what I would normally wear, I'm kind of embarrassed to be in it."
    
    $ the_person.add_infraction(Infraction.out_of_uniform_factory())
    mc.name "The dress code isn't a suggestion [the_person.title], it's a requirement for continued employment."



    menu dress_code_min_disobedience_menu:
        # wear uniform if person owns a matching outfit
        "Send her to get changed" if not has_no_outfit:
            mc.name "Go and get changed."
            if the_person.obedience < 90:
                "[the_person.possessive_title] sighs and rolls her eyes."
                the_person "Fine, I'll go put it on."
            else:
                the_person "Right away [the_person.mc_title]."
            $ clear_scene()
            "She hurries out of the room. You wait by her desk until she comes back."
            $ the_person.dress_code_outfit = dress_code_outfit
            $ the_person.wear_dress_code()
            $ the_person.draw_person()
            "A few moments later [the_person.possessive_title] comes back, now properly in uniform."
        
        "Have her change right here\n{color=#ff0000}{size=18}Requires policy: Reduced Coverage Corporate Uniforms{/size}{/color} (disabled)" if not has_no_outfit and not reduced_coverage_uniform_policy.is_active():
            pass
        "Have her change right here" if not has_no_outfit and reduced_coverage_uniform_policy.is_active():
            mc.name "Do you have your proper clothes with you?"
            the_person "I have them in my desk."
            mc.name "Good. Get them and get changed."
            "She nods and slides open one of her desk drawers, grabbing her outfit and tucking it under her arm."
            the_person "I'll be back in a moment..."
            mc.name "No, you're going to get changed here. I obviously need to make sure you're wearing it properly."
            if the_person.effective_sluttiness(["bare_pussy", "bare_tits"]) > 40: #No big deal.
                the_person "Fine, I guess it doesn't really matter."
            else: #Shy about it
                the_person "You don't really mean that, do you? Right here?"
                mc.name "Do I need to write you up for insubordination too?"
                the_person "No, I'll do it..."
                $ the_person.change_obedience(1 + the_person.get_opinion_score("being submissive"))
            $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list(strip_feet = True, strip_accessories = True))
            $ mc.change_locked_clarity(10)
            "Once stripped down [the_person.possessive_title] puts on her work clothes."
            $ the_person.dress_code_outfit = dress_code_outfit
            $ the_person.wear_dress_code()
            $ the_person.draw_person()
        
        
        # change current outfit / assign another outfit if person doesn't own a matching outfit
        "Have her remove her top (disabled)" if has_no_outfit and not dress_code_outfit.get_overwear().get_upper_top_layer():
            pass
        "Have her remove her top" if has_no_outfit and dress_code_outfit.get_overwear().get_upper_top_layer():
            $ dress_code_outfit.remove_clothing_list([dress_code_outfit.get_overwear().get_upper_top_layer()])
            $ the_person.dress_code_outfit = dress_code_outfit
            $ the_person.wear_dress_code()
            $ the_person.draw_person()
            if dress_code_outfit.get_full_outfit_slut_score() >= slut_limit_lower:
                mc.name "You can stay like this for the rest of the day. But you should go and buy an appropriate outfit after you leave work today."
                $ builder = WardrobeBuilder(the_person)
                $ new_outfit = builder.build_outfit(None, points=slut_limit_lower)
                $ print('builder: ', new_outfit.name, new_outfit.get_full_outfit_slut_score())
                $ new_outfit = the_person.personalize_outfit(new_outfit, opinion_color = the_person.favorite_colour(), coloured_underwear = True, swap_bottoms = True, allow_skimpy = True)
                $ print('personalized: ', new_outfit.name, new_outfit.get_full_outfit_slut_score())
                $ the_person.add_outfit(new_outfit, "full")
            else:
                jump dress_code_min_disobedience_menu
        "Have her remove her bottoms (disabled)" if has_no_outfit and not dress_code_outfit.get_overwear().get_lower_top_layer():
            pass
        "Have her remove her bottoms" if has_no_outfit and dress_code_outfit.get_overwear().get_lower_top_layer():
            $ dress_code_outfit.remove_clothing_list([dress_code_outfit.get_overwear().get_lower_top_layer()])
            $ the_person.dress_code_outfit = dress_code_outfit
            $ the_person.wear_dress_code()
            $ the_person.draw_person()
            if dress_code_outfit.get_full_outfit_slut_score() >= slut_limit_lower:
                mc.name "You can stay like this for the rest of the day. But you should go and buy an appropriate outfit after you leave work today."
                $ builder = WardrobeBuilder(the_person)
                $ new_outfit = the_person.personalize_outfit(builder.build_outfit(None, points=slut_limit_lower+10, min_points=slut_limit_lower), opinion_color = the_person.favorite_colour(), coloured_underwear = True, swap_bottoms = True, allow_skimpy = True)
                $ the_person.add_outfit(new_outfit, "full")
            else:
                jump dress_code_min_disobedience_menu
        "Have her remove her bra (disabled)" if has_no_outfit and not dress_code_outfit.wearing_bra():
            pass
        "Have her remove her bra" if has_no_outfit and dress_code_outfit.wearing_bra():
            $ dress_code_outfit.remove_bra()
            $ the_person.dress_code_outfit = dress_code_outfit
            $ the_person.wear_dress_code()
            $ the_person.draw_person()
            if dress_code_outfit.get_full_outfit_slut_score() >= slut_limit_lower:
                mc.name "You can stay like this for the rest of the day. But you should go and buy an appropriate outfit after you leave work today."
                $ builder = WardrobeBuilder(the_person)
                $ new_outfit = the_person.personalize_outfit(builder.build_outfit(None, points=slut_limit_lower+10, min_points=slut_limit_lower), opinion_color = the_person.favorite_colour(), coloured_underwear = True, swap_bottoms = True, allow_skimpy = True)
                $ the_person.add_outfit(new_outfit, "full")
            else:
                jump dress_code_min_disobedience_menu
        "Have her remove her panties (disabled)" if has_no_outfit and not dress_code_outfit.wearing_panties():
            pass
        "Have her remove her panties" if has_no_outfit and dress_code_outfit.wearing_panties():
            $ dress_code_outfit.remove_panties()
            $ the_person.dress_code_outfit = dress_code_outfit
            $ the_person.wear_dress_code()
            $ the_person.draw_person()
            if dress_code_outfit.get_full_outfit_slut_score() >= slut_limit_lower:
                mc.name "You can stay like this for the rest of the day. But you should go and buy an appropriate outfit after you leave work today."
                $ builder = WardrobeBuilder(the_person)
                $ new_outfit = the_person.personalize_outfit(builder.build_outfit(None, points=slut_limit_lower+10, min_points=slut_limit_lower), opinion_color = the_person.favorite_colour(), coloured_underwear = True, swap_bottoms = True, allow_skimpy = True)
                $ the_person.add_outfit(new_outfit, "full")
            else:
                jump dress_code_min_disobedience_menu
        
        "Give her an outfit to wear" if has_no_outfit:
            mc.name "Lucky for you, I have an outfit you can wear in my office."
            $ clear_scene()
            call outfit_master_manager(slut_limit = __builtin__.max(the_person.sluttiness + 10, slut_limit_lower), show_overwear = False, show_underwear = False) from _call_outfit_master_manager_dress_code_disobedience
            $ new_outfit = _return
            $ the_person.draw_person()
            if new_outfit is None:
                "You cannot find an appropriate outfit in your office after all."
                mc.name "Sorry [the_person.title], I thought I had something appropriate in my office but I guess I was wrong."
                jump dress_code_min_disobedience_menu
            else:
                "You lay the outfit out for [the_person.possessive_title]. She looks it over and nods."
                the_person "It'll just take a moment for me to slip into this."
                "[the_person.possessive_title] starts to strip down in front of you."
                $ the_person.strip_outfit(exclude_feet = False)
                "Once she's stripped naked she grabs the outfit and starts to put it on."
                $ the_person.dress_code_outfit = new_outfit
                $ the_person.apply_outfit(new_outfit, update_taboo = True)
                $ the_person.event_triggers_dict['accepted_dress_code_outfit'] = the_person.outfit
                $ the_person.event_triggers_dict['accepted_dress_code_outfit_day'] = day
                $ the_person.draw_person()
                the_person "Is this better?"
                mc.name "You can stay like this for the rest of the day. But you should go and buy an appropriate outfit after you leave work today."
                $ builder = WardrobeBuilder(the_person)
                $ new_outfit = the_person.personalize_outfit(builder.build_outfit(None, points=slut_limit_lower+10, min_points=slut_limit_lower), opinion_color = the_person.favorite_colour(), coloured_underwear = True, swap_bottoms = True, allow_skimpy = True)
                $ the_person.add_outfit(new_outfit, "full")

        "Let her stay out of uniform":
            mc.name "But, just this once, I'll make an exception. I expect you in an appropriate outfit for your next shift."
            the_person "Thank you [the_person.mc_title], the break is appreciated."
            $ the_person.change_happiness(10)
            $ the_person.change_love(1)
            $ the_person.change_obedience(-2)
            $ the_person.event_triggers_dict['accepted_dress_code_outfit'] = the_person.outfit
            $ the_person.event_triggers_dict['accepted_dress_code_outfit_day'] = day

        "Done" if has_no_outfit:
            mc.name "You can stay like this for the rest of the day. But you should go and buy an appropriate outfit after you leave work today."
            the_person "Thank you [the_person.mc_title], the break is appreciated."
            $ the_person.change_happiness(5)
            $ the_person.change_love(1)
            $ the_person.change_obedience(-1)
            $ builder = WardrobeBuilder(the_person)
            $ new_outfit = the_person.personalize_outfit(builder.build_outfit(None, points=slut_limit_lower+10, min_points=slut_limit_lower), opinion_color = the_person.favorite_colour(), coloured_underwear = True, swap_bottoms = True, allow_skimpy = True)
            $ the_person.add_outfit(new_outfit, "full")
            $ the_person.event_triggers_dict['accepted_dress_code_outfit'] = the_person.outfit
            $ the_person.event_triggers_dict['accepted_dress_code_outfit_day'] = day
    
    the_person "Is there something you needed to talk to me about?"
    call talk_person(the_person) from dress_code_min_disobedience_call_talk_person
    return
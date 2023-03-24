init 1410 python:
    dress_code_policy_min_05 = Policy(
        name = "Dress Code: min. 5",
        cost = 500,
        desc = "Employees are required to wear a full outfit of at least sluttiness 5 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [strict_uniform_policy, dress_code_policy],
        extra_arguments = {"dress_code_min_disobedience_priority":05},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_05)
    
    dress_code_policy_min_15 = Policy(
        name = "Dress Code: min. 15",
        cost = 1000,
        desc = "Employees are required to wear a full outfit of at least sluttiness 15 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [relaxed_uniform_policy, dress_code_policy, dress_code_policy_min_05],
        extra_arguments = {"dress_code_min_disobedience_priority":15},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_15)
    
    dress_code_policy_min_25 = Policy(
        name = "Dress Code: min. 25",
        cost = 2000,
        desc = "Employees are required to wear a full outfit of at least sluttiness 25 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [reduced_coverage_uniform_policy, dress_code_policy, dress_code_policy_min_15],
        extra_arguments = {"dress_code_min_disobedience_priority":25},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_25)
    
    dress_code_policy_min_35 = Policy(
        name = "Dress Code: min. 35",
        cost = 5000,
        desc = "Employees are required to wear a full outfit of at least sluttiness 35 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [reduced_coverage_uniform_policy, dress_code_policy, dress_code_policy_min_25],
        extra_arguments = {"dress_code_min_disobedience_priority":35},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_35)
    
    dress_code_policy_min_45 = Policy(
        name = "Dress Code: min. 45",
        cost = 10000,
        desc = "Employees are required to wear a full outfit of at least sluttiness 45 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [minimal_coverage_uniform_policy, dress_code_policy, dress_code_policy_min_35],
        extra_arguments = {"dress_code_min_disobedience_priority":45},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_45)
    
    dress_code_policy_min_55 = Policy(
        name = "Dress Code: min. 55",
        cost = 15000,
        desc = "Employees are required to wear a full outfit of at least sluttiness 55 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [minimal_coverage_uniform_policy, dress_code_policy, dress_code_policy_min_45],
        extra_arguments = {"dress_code_min_disobedience_priority":55},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_55)
    
    dress_code_policy_min_65 = Policy(
        name = "Dress Code: min. 65",
        cost = 25000,
        desc = "Employees are required to wear a full outfit of at least sluttiness 65 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [corporate_enforced_nudity_policy, dress_code_policy, dress_code_policy_min_55],
        extra_arguments = {"dress_code_min_disobedience_priority":65},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_65)
    
    dress_code_policy_min_75 = Policy(
        name = "Dress Code: min. 75",
        cost = 35000,
        desc = "Employees are required to wear a full outfit of at least sluttiness 75 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [corporate_enforced_nudity_policy, dress_code_policy, dress_code_policy_min_65],
        extra_arguments = {"dress_code_min_disobedience_priority":75},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_75)
    
    dress_code_policy_min_85 = Policy(
        name = "Dress Code: min. 85",
        cost = 50000,
        desc = "Employees are required to wear a full outfit of at least sluttiness 85 as part of their dress code or uniform.",
        toggleable = True,
        own_requirement = [maximal_arousal_uniform_policy, dress_code_policy, dress_code_policy_min_75],
        extra_arguments = {"dress_code_min_disobedience_priority":85},
        on_move_function = dress_code_min_disobedience_on_move,
    )
    uniform_policies_list.append(dress_code_policy_min_75)




    # An outfit selector that takes personal preferences into account
    def LENA_decide_on_outfit_enhanced(self, person, sluttiness_modifier = 0.0, slut_limit = 999, slut_limit_lower=0):
        conservative_score = person.get_opinion_score("conservative outfits") / 20.0
        skimpy_outfit_score = person.get_opinion_score("skimpy outfits") / 20.0
        marketing_score = 0
        # girls working in marketing know they make more sales when wearing a sluttier outfit, so this affects their uniform choice
        if mc.business.is_work_day() and male_focused_marketing_policy.is_active() and person in mc.business.market_team:
            marketing_score = .05

        target_sluttiness = __builtin__.int(person.sluttiness * (1.0 + skimpy_outfit_score + marketing_score + sluttiness_modifier - conservative_score))
        target_sluttiness = __builtin__.min(target_sluttiness, slut_limit)

        minimum_sluttiness = __builtin__.max(slut_limit_lower, __builtin__.int(target_sluttiness * .3))
        new_target_sluttiness = __builtin__.max(slut_limit_lower + (10 if slut_limit_lower > 0 else 0), target_sluttiness)

        print("{}: Target slut {}->{}, min slut {}".format(person.name, target_sluttiness, new_target_sluttiness, minimum_sluttiness))
        target_sluttiness = new_target_sluttiness

        if not self.outfits and not self.underwear_sets and not self.overwear_sets:
            #We have nothing to make a outfit out of. Use default builder function.
            return generate_random_appropriate_outfit(person, sluttiness = target_sluttiness)

        preferences = WardrobePreference(person)

        if self.outfits:
            #We have some full body outfits we might use. 50/50 to use that or a constructed outfit.
            outfit_choice = renpy.random.randint(0,100)
            chance_to_use_full = (50 / 12.0) * __builtin__.len(self.outfits)   # when 12 outfits chance is 50%.
            if chance_to_use_full > 60: # cap at 60%
                chance_to_use_full = 60

            #If we roll use full or we don't have the parts to make an assembled outfit.
            if outfit_choice < chance_to_use_full or not (self.underwear_sets or self.overwear_sets):
                print('picking from full outfits')
                full_outfit = self.get_random_appropriate_outfit(target_sluttiness, minimum_sluttiness, preferences = preferences)

                if not full_outfit: # fallback if we cannot find anything for our sluttiness or preferences
                    print('fallback to lowest sluttiness')
                    full_outfit = self.pick_outfit_with_lowest_sluttiness()

                if full_outfit:
                    print('found outfit: ', full_outfit.name, full_outfit.get_full_outfit_slut_score())
                    return full_outfit.get_copy()

        #If we get to here we are assembling an outfit out of underwear or overwear.
        print('assembling an outfit out of underwear and overwear')
        outfit_over = self.get_random_appropriate_overwear(target_sluttiness, minimum_sluttiness, preferences = preferences)
        outfit_under = None

        if outfit_over:
            print('found an overwear', outfit_over.name, outfit_over.get_overwear_slut_score())
            slut_limit_remaining = target_sluttiness - outfit_over.get_overwear_slut_score()
            if slut_limit_remaining < 10:
                slut_limit_remaining = 10  # don't expect 0 sluttiness underwear to be in wardrobe.

            outfit_under = self.get_random_appropriate_underwear(slut_limit_remaining, preferences = preferences)

            if not outfit_under:
                print('getting underwear with lowest sluttiness')
                outfit_under = self.pick_underwear_with_lowest_sluttiness()

            if not outfit_under:
                print('getting random underwear from person')
                outfit_under = person.wardrobe.get_random_appropriate_underwear(slut_limit_remaining, preferences = preferences)

            if not outfit_under:
                # renpy.say(None, "Unable to find underwear in wardrobe, pick any underwear from personal wardrobes.")
                print('Unable to find underwear in wardrobe, pick any underwear from personal wardrobes.')
                outfit_under = generate_random_appropriate_outfit(person, outfit_type = "UnderwearSets", sluttiness = slut_limit_remaining)

        else:
            #There are no tops, so we're going to try and get a bottom and use one of the persons tops.
            print("There are no tops, so we're going to try and get a bottom and use one of the persons tops.")
            outfit_under = self.get_random_appropriate_underwear(target_sluttiness, preferences = preferences)

            if not outfit_under:
                outfit_under = self.pick_underwear_with_lowest_sluttiness()

            if not outfit_under:
                outfit_under = person.wardrobe.get_random_appropriate_underwear(target_sluttiness, preferences = preferences)

            if not outfit_under:
                # renpy.say(None, "Unable to find underwear in wardrobe, pick any underwear from personal wardrobes.")
                outfit_under = generate_random_appropriate_outfit(person, outfit_type = "UnderwearSets", sluttiness = target_sluttiness)

            if outfit_under:
                slut_limit_remaining = target_sluttiness - outfit_under.get_underwear_slut_score()
                if slut_limit_remaining < 10:
                    slut_limit_remaining = 10 # don't expect 0 sluttiness overwear to be in personal wardrobe.

                outfit_over = self.get_random_appropriate_overwear(slut_limit_remaining, preferences = preferences)

                if not outfit_over:
                    outfit_over = self.pick_overwear_with_lowest_sluttiness()

                if not outfit_over:
                    person.wardrobe.get_random_appropriate_overwear(slut_limit_remaining, preferences = preferences)

                if not outfit_over:
                    # renpy.say(None, "Unable to find overwear in uniform wardrobe, pick any underwear from personal wardrobes.")
                    outfit_over = generate_random_appropriate_outfit(person, outfit_type = "OverwearSets", sluttiness = slut_limit_remaining)

        #At this point we have our under and over, if at all possible.
        if not outfit_over or not outfit_under:
            # Something's gone wrong and we don't have one of our sets. Last attempt on getting a full outfit from any wardrobe.
            print("Something's gone wrong and we don't have one of our sets. Last attempt on getting a full outfit from any wardrobe.")
            return generate_random_appropriate_outfit(person, sluttiness = target_sluttiness)

        return build_assembled_outfit(outfit_under, outfit_over)

    Wardrobe.decide_on_outfit2 = LENA_decide_on_outfit_enhanced




    def LENA_decide_on_uniform_enhanced(self, person):
        slut_limit = 999
        slut_limit_lower = 0
        valid_wardrobe = None
        if (person.is_employee() or person.is_intern()) and dress_code_policy.is_active():
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
            valid_wardrobe = self.build_uniform_wardrobe(slut_limit, underwear_limit, limited_to_top)
        else:
            valid_wardrobe = self.build_uniform_wardrobe()
        
        print(person.name, ' employee:',person.is_employee(), ' intern:',person.is_intern())
        if person.is_employee() or person.is_intern():
            slut_limit_lower = mc.business.get_uniform_lower_limits()
            print(person.name, 'is employee or intern, lower_limit:', slut_limit_lower)

        sluttiness_modifier = person.get_opinion_score("work uniforms") / 40.0 # low impact on sluttiness

        uniform = valid_wardrobe.decide_on_outfit2(person, sluttiness_modifier = sluttiness_modifier, slut_limit = slut_limit, slut_limit_lower = slut_limit_lower)

        if uniform and (person.is_employee() or person.is_intern()):  # only apply policies for employees
            if creative_colored_uniform_policy.is_active():
                uniform = WardrobeBuilder(person).personalize_outfit(uniform,
                    swap_bottoms = personal_bottoms_uniform_policy.is_active(),
                    allow_skimpy = creative_skimpy_uniform_policy.is_active())
            elif personal_bottoms_uniform_policy.is_active():
                (uniform, _swapped) = WardrobeBuilder(person).apply_bottom_preference(person, uniform)
            elif easier_access_policy.is_active(): # only when creative and relaxed are not active
                uniform.make_easier_access()

            if commando_uniform_policy.is_active(): # always applied, overrides uniform
                if person.has_large_tits():
                    uniform.remove_panties()    # they still need the support ;)
                    if not uniform.wearing_bra(): # probably a body suit, she will show a real bra to wear
                        uniform.add_upper(sports_bra.get_copy(), neutral_palette[renpy.random.choice(neutral_color_map["Underwear"])])
                        WardrobeBuilder.set_sexier_bra(person, uniform) # update for sexier version if slutty enough
                else:
                    uniform.remove_bra_and_panties()

        if uniform and person.job == doctor_job:
            uniform.add_upper(lab_coat.get_copy(), colour_white)

        uniform.build_outfit_name()

        # print("Picked uniform: {} ({})".format(uniform.name, uniform.get_full_outfit_slut_score()))

        return uniform

    # replace default uniform decision function
    Wardrobe.decide_on_uniform = LENA_decide_on_uniform_enhanced




    def LENA_get_uniform_lower_limits(self):
        over_limit = 0
        under_limit = 0
        outfit_limit = 0

        if dress_code_policy_min_85.is_active():
            outfit_limit = 85
        elif dress_code_policy_min_75.is_active():
            outfit_limit = 75
        elif dress_code_policy_min_65.is_active():
            outfit_limit = 65
        elif dress_code_policy_min_55.is_active():
            outfit_limit = 55
        elif dress_code_policy_min_45.is_active():
            outfit_limit = 45
        elif dress_code_policy_min_35.is_active():
            outfit_limit = 35
        elif dress_code_policy_min_25.is_active():
            outfit_limit = 25
        elif dress_code_policy_min_15.is_active():
            outfit_limit = 15
        elif dress_code_policy_min_05.is_active():
            outfit_limit = 5
        
        return outfit_limit
    Business.get_uniform_lower_limits = LENA_get_uniform_lower_limits




    

    def LENA_person_should_wear_dress_code(self):
        if not self.is_at_work():  # quick exit
            return False

        if self.is_employee() and not self.is_intern() and not self.is_strip_club_employee():
            # Casual fridays for employees only
            if not (day%7 == 4 and casual_friday_uniform_policy.is_active()):
                # Check for dress code and whether planned outfit applies
                dress_code_policy_min_list = [
                    dress_code_policy_min_05,
                    dress_code_policy_min_15,
                    dress_code_policy_min_25,
                    dress_code_policy_min_35,
                    dress_code_policy_min_45,
                    dress_code_policy_min_55,
                    dress_code_policy_min_65,
                    dress_code_policy_min_75,
                    dress_code_policy_min_85,
                ]
                return dress_code_policy.is_active() or True in [x.is_active() for x in dress_code_policy_min_list]
        return False
    Person.should_wear_dress_code = LENA_person_should_wear_dress_code
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




    def LENA_decide_on_outfit_with_hard_lower_slut_limit(self, person, sluttiness_modifier, slut_limit, slut_limit_lower):
        print("LENA_decide_on_outfit_with_hard_lower_slut_limit: {}, mod={}, limit={}, lower={}".format(person.name, sluttiness_modifier, slut_limit, slut_limit_lower))
        conservative_score = person.get_opinion_score("conservative outfits") / 20.0
        skimpy_outfit_score = person.get_opinion_score("skimpy outfits") / 20.0
        marketing_score = 0
        # girls working in marketing know they make more sales when wearing a sluttier outfit, so this affects their uniform choice
        if mc.business.is_work_day() and male_focused_marketing_policy.is_active() and person in mc.business.market_team:
            marketing_score = .05

        target_sluttiness = __builtin__.int(person.sluttiness * (1.0 + skimpy_outfit_score + marketing_score + sluttiness_modifier - conservative_score))
        target_sluttiness = __builtin__.min(target_sluttiness, slut_limit)

        print('final target:', target_sluttiness)

        outfit_list = []
        outfit_candidates = []

        if self.outfits:
            # try to find a full outfit
            print('checking full outfits')
            for outfit in self.outfits:
                if creative_colored_uniform_policy.is_active():
                    outfit = WardrobeBuilder(person).personalize_outfit(outfit,
                        swap_bottoms = personal_bottoms_uniform_policy.is_active(),
                        allow_skimpy = creative_skimpy_uniform_policy.is_active())
                if easier_access_policy.is_active():
                    outfit.make_easier_access()
                if commando_uniform_policy.is_active(): # always applied, overrides uniform
                    if person.has_large_tits():
                        outfit.remove_panties()    # they still need the support ;)
                        if not outfit.wearing_bra(): # probably a body suit, she will show a real bra to wear
                            outfit.add_upper(sports_bra.get_copy(), neutral_palette[renpy.random.choice(neutral_color_map["Underwear"])])
                            WardrobeBuilder.set_sexier_bra(person, outfit) # update for sexier version if slutty enough
                    else:
                        # outfit.remove_bra_and_panties()
                        outfit.remove_panties()
                score = outfit.get_full_outfit_slut_score()
                outfit_tuple = (outfit, score, score-slut_limit_lower, score-target_sluttiness)
                outfit_list.append(outfit_tuple)
                if score >= slut_limit_lower:
                    outfit_candidates.append(outfit_tuple)
        else:
            print('does not have full outfits')
        if self.underwear_sets and self.overwear_sets:
            # try to build an outfit from underwear and overwear
            # first, let's brute force all under+over combinations
            print('brute forcing combi outfits')
            for under in self.underwear_sets:
                for over in self.overwear_sets:
                    outfit = build_assembled_outfit(under, over)
                    if creative_colored_uniform_policy.is_active():
                        outfit = WardrobeBuilder(person).personalize_outfit(outfit,
                            swap_bottoms = personal_bottoms_uniform_policy.is_active(),
                            allow_skimpy = creative_skimpy_uniform_policy.is_active())
                    if easier_access_policy.is_active():
                        outfit.make_easier_access()
                    if commando_uniform_policy.is_active(): # always applied, overrides uniform
                        if person.has_large_tits():
                            outfit.remove_panties()    # they still need the support ;)
                            if not outfit.wearing_bra(): # probably a body suit, she will show a real bra to wear
                                outfit.add_upper(sports_bra.get_copy(), neutral_palette[renpy.random.choice(neutral_color_map["Underwear"])])
                                WardrobeBuilder.set_sexier_bra(person, outfit) # update for sexier version if slutty enough
                        else:
                            # outfit.remove_bra_and_panties()
                            outfit.remove_panties()
                    score = outfit.get_full_outfit_slut_score()
                    outfit_list.append((outfit, score, score-slut_limit_lower, score-target_sluttiness))
                    if score >= slut_limit_lower:
                        outfit_candidates.append((outfit, score, score-slut_limit_lower, score-target_sluttiness))
        else:
            print('does not have under and over sets')
        print('all candidates: ', [(x[0].name, x[1], x[2], x[3]) for x in outfit_candidates])
        
        if __builtin__.len(outfit_candidates) > 0:
            if target_sluttiness < slut_limit_lower:
                # impossible to find something person is comfortable with
                # just keep the outfits with the lowest sluttiness
                min_score = __builtin__.min([x[1] for x in outfit_candidates])
                outfit_candidates = [x for x in outfit_candidates if x[1] == min_score]
                print('could not find something comfy, lowest:', [(x[0].name, x[1], x[2], x[3]) for x in outfit_candidates])
            else:
                outfit_candidates_between_min_and_target = [x for x in outfit_candidates if x[1] >= slut_limit_lower and x[1] <= target_sluttiness]
                if len(outfit_candidates_between_min_and_target) > 0:
                    outfit_candidates = outfit_candidates_between_min_and_target
                # pick outfits closest to target sluttiness
                min_distance = __builtin__.min(__builtin__.abs(x[3]) for x in outfit_candidates)
                outfit_candidates = [x for x in outfit_candidates if __builtin__.abs(x[3]) == min_distance or x[3] >= -15]
                print('outfits closest to target:', [(x[0].name, x[1], x[2], x[3]) for x in outfit_candidates])
            
            picked_outfit = outfit_candidates[renpy.random.randint(0,__builtin__.len(outfit_candidates))-1]
            print('picked outfit:', (picked_outfit[0].name, picked_outfit[1], picked_outfit[2], picked_outfit[3]))
            return picked_outfit[0].get_copy()
         
        # we have not found any outfits following the dress code
        print('could not find any matching outfits -> pick outfit closest to dress code')
        if __builtin__.len(outfit_list) > 0:
            min_distance = __builtin__.min([__builtin__.abs(x[2]) for x in outfit_list])
            outfit_list = [x for x in outfit_list if __builtin__.abs(x[2]) == min_distance]
            if __builtin__.len(outfit_list) > 0:
                picked_outfit = outfit_list[renpy.random.randint(0,__builtin__.len(outfit_list))-1]
                print('picked outfit:', (picked_outfit[0].name, picked_outfit[1], picked_outfit[2], picked_outfit[3]))
                return picked_outfit[0].get_copy()
        
        # we have not found any outfits!
        print('could not find any outfits at all -> generate random')
        return generate_random_appropriate_outfit(person, sluttiness = target_sluttiness)

    Wardrobe.decide_on_outfit_with_hard_lower_slut_limit = LENA_decide_on_outfit_with_hard_lower_slut_limit


    def LENA_decide_on_uniform_enhanced(self, person):
        slut_limit = 999
        slut_limit_lower = 0
        valid_wardrobe = None
        if (person.is_employee() or person.is_intern()) and dress_code_policy.is_active():
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
            valid_wardrobe = self.build_uniform_wardrobe(slut_limit, underwear_limit, limited_to_top)
        else:
            valid_wardrobe = self.build_uniform_wardrobe()

        sluttiness_modifier = person.get_opinion_score("work uniforms") / 40.0 # low impact on sluttiness
        
        print(person.name, ' employee:',person.is_employee(), ' intern:',person.is_intern())
        if person.is_employee() or person.is_intern():
            slut_limit_lower = mc.business.get_uniform_lower_limits()
            print(person.name, 'is employee or intern, lower_limit:', slut_limit_lower)
            if slut_limit_lower > 0:
                return valid_wardrobe.decide_on_outfit_with_hard_lower_slut_limit(person, sluttiness_modifier = sluttiness_modifier, slut_limit = slut_limit, slut_limit_lower = slut_limit_lower)

        uniform = valid_wardrobe.decide_on_outfit2(person, sluttiness_modifier = sluttiness_modifier, slut_limit = slut_limit)

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
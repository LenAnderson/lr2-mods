init -1 python:
    def orgasm_blocker_trait_on_apply(the_person, the_serum, add_to_log):
        the_person.change_max_arousal(999, add_to_log = add_to_log)

    def orgasm_blocker_trait_on_remove(the_person, the_serum, add_to_log):
        the_person.change_max_arousal(-999, add_to_log = add_to_log)
    
    def add_orgasm_blocker_trait():
        orgasm_blocker_trait = SerumTraitMod(name = "Orgasm Blocker",
            desc = "Blocks orgasms.",
            positive_slug = "Blocks orgasms",
            negative_slug = "nothing",
            research_added = 75,
            slots_added = 0,
            production_added = 0,
            duration_added = 0,
            base_side_effect_chance = 15,
            clarity_added = 0,
            on_apply = orgasm_blocker_trait_on_apply,
            on_remove = orgasm_blocker_trait_on_remove,
            on_turn = None,
            on_day = None,
            on_move = None,
            requires = None,
            tier = 3,
            start_researched = False,
            research_needed = 300,
            exclude_tags = None,
            is_side_effect = False,
            clarity_cost = 300,
            start_unlocked = False,
            start_enabled = False,
            mental_aspect = 2,
            physical_aspect = 0,
            sexual_aspect = 0,
            medical_aspect = 2,
            flaws_aspect = 0,
            attention = 0
        )

# any label that starts with serum_mod is added to the serum mod list
label serum_mod_orgasm_blocker_trait(stack):
    python:
        add_orgasm_blocker_trait()
        # continue on the hijack stack if needed
        execute_hijack_call(stack)
    return
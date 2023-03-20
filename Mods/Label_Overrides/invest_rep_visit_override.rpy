init 6 python:
    config.label_overrides["invest_rep_visit_label"] = "LENA_invest_rep_visit_label"

label LENA_invest_rep_visit_label(rep_name):

    if time_of_day == 3:
        "Your phone rings. When you check it you recognize the name [rep_name], the representative of a mutual fund that you had promised a tour. You answer your phone."
        mc.name "[rep_name], I'm so sorry to have kept you waiting, I..."
        rep_name "Don't bother, I've been waiting here all day but if you can't be bothered to show up to your own office for a planned tour I want nothing to do with your business. Good day."
        "[rep_name] hangs up. You doubt he will be interested in rescheduling."
    elif True:

        "Your phone rings. When you check it you recognize the name [rep_name], the representative of a mutual fund that you had promised a tour. You answer your phone."
        mc.name "[rep_name], good to hear from you. How are you doing?"
        rep_name "I'm doing well. I'm just pulling into your parking lot now, do I need to check in at security?"
        mc.name "Don't worry about it, I'll come out and meet you and we can start the tour."
        "You hurry out to the parking lot and spot a man you assume to be [rep_name] getting out his car. He's middle aged, not particularly handsome, and dressed conservatively in a suit and tie."
        rep_name "Good to finally meet you in person."
        "He reaches out his hand and you shake it."
        rep_name "Before we get started I wanted to ask you some questions about what you do here."
        mc.name "I'll answer whatever I can."
        rep_name "Your business license says you're working in commercial pharmaceuticals. What, exactly, does that mean?"
        $ lobby.show_background()
        "You lead [rep_name] into the office lobby."
        mc.name "We have a number of different products that we produce, but they're all based on the same fundamental principle."
        mc.name "Our products remove personal inhibitions, limitations, fears. All of those mental roadblocks that stop us from achieving what we want to in life."
        "[rep_name] nods as if he understands."
        "You decide it would be a good idea to call up someone to help you convince [rep_name] of the value of your product."
        if mc.business.get_employee_count() == 0:
            "Unfortunately, you're the only employee of your own business, so you have nobody to show off to [rep_name]."
            "Instead you show him around the various empty departments. It becomes clear with time that he is less than impressed."
            rep_name "Thank you for taking time out of your day and showing me around, but I don't think I could suggest we invest anything in a one man operation like this."
            rep_name "I'll keep an eye on you though, if you grow your business a little bit maybe I'll call you up and we can reevaluate."
            mc.name "I understand completely. I'll walk you out."
            "You walk [rep_name] back to his car and watch as he drives away."
        elif True:
            mc.name "Actually, how about I call down one of my employees and have them give you a tour around. They've all had much more experience with our product than I have."
            rep_name "That sounds like an excellent idea, I would like to talk to someone who is involved with the day to day operations around here."
            call screen employee_overview(person_select = True)
            $ helper = _return
            "You send [helper.title] a text to meet you. You and [rep_name] grab chairs and wait in the lobby until she arrives."
            $ helper.draw_person()
            if helper.outfit.slut_requirement > 60:
                "[rep_name]'s goes slack-jawed when he sees [helper.title] wearing not much at all."
                $ mc.change_locked_clarity(15)
            elif helper.outfit.slut_requirement > 20:
                "Your idle conversation with [rep_name] trails off when [helper.title] comes into the room. You see his eyes run up and down her before he regains his composure."
                $ mc.change_locked_clarity(5)
            elif True:
                "[rep_name] smiles and nods at [helper.title] as she comes into the room."

            helper "How can I help [helper.mc_title]?"
            "You take [helper.possessive_title] to the side and tell her what you want her to do."
            $ success_chance = 10
            $ flirt_requires_string = "Flirt with " + rep_name + "\n{color=#ff0000}{size=18}Requires: Obedience 110, " + get_red_heart(10) + "{/size}{/color}"
            $ seduce_requires_string = "Seduce " + rep_name + "\n{color=#ff0000}{size=18}Requires: Obedience 130, " + get_red_heart(60) + "{/size}{/color}"

            menu:
                "Impress [rep_name]" if True:
                    mc.name "[rep_name] here is interested in learning more about the company; I would like you to give him a full tour."
                    "[helper.title] nods and turns to [rep_name]."
                    helper "[rep_name], I'll be your tour guide today. If you just follow me, there is plenty to see."
                    mc.name "I'll be in my office taking care of some paperwork, bring [rep_name] to me when you're done with the tour."
                    "[rep_name] stands and follows [helper.possessive_title] out of the lobby. You return to your office to kill some time and avoid getting in the way."
                    $ success_chance += 5*(helper.charisma + helper.market_skill)
                    $ success_chance += helper.outfit.slut_requirement/5

                "Flirt with [rep_name]" if helper.sluttiness >= 20 and helper.obedience >= 110:
                    mc.name "[rep_name] here is interested in learning more about the company; I would like you to give him a full tour."
                    helper "I can take care of that."
                    mc.name "One more thing: I doubt he spends much time around someone as beautiful as you. Lay the charm on thick for him."
                    "[helper.title] smiles and nods, then turns to [rep_name]."
                    helper "[rep_name], it's a pleasure to meet you. I will be your tour guide today, so if you just follow me we have plenty to see."
                    "[rep_name] stands up and follows [helper.possessive_title] out of the lobby. While they're walking away [helper.title] places a hand on his arm."
                    $ helper.draw_person(position = "walking_away")
                    helper "This is a wonderful suit by the way, it fits you fantastically. Where do you shop?"
                    "The sound of their conversation trails off as they leave the room. You retreat to your office to kill some time and avoid getting in the way."
                    $ success_chance += 7*(helper.charisma + helper.market_skill)
                    $ success_chance += helper.outfit.slut_requirement/4

                "[flirt_requires_string] (disabled)" if not (helper.sluttiness >= 20 and helper.obedience >= 110):
                    pass

                "Seduce [rep_name]" if helper.sluttiness >= 60 and helper.obedience >= 130:
                    mc.name "[rep_name] here is interested in learning more about the company. I need you to give him a complete tour and show him our operations."
                    helper "I can take care of that sir."
                    mc.name "Good. Now this is important so once the tour is done I want you to pull him into one of the meeting rooms and make sure he has a very pleasant visit."
                    "[helper.title] looks past you at [rep_name] and smiles mischievously."
                    helper "That I can certainly do. Excuse me, [rep_name]? I will be your tour guide today. If you follow me we can begin."
                    $ helper.draw_person(position = "walking_away")
                    "[rep_name] stands up and follows [helper.possessive_title] out of the lobby. [helper.title] seems to swing her hips a little more purposefully as she walks in front of [rep_name]."
                    "You retreat to your office to kill some time and avoid getting in the way of the tour."
                    $ success_chance += 4*(helper.charisma + helper.market_skill)
                    $ success_chance += helper.outfit.slut_requirement/3
                    python:
                        for skill in helper.sex_skills:
                            success_chance += helper.sex_skills[skill] 

                "[seduce_requires_string] (disabled)" if not (helper.sluttiness >= 60 and helper.obedience >= 130):
                    pass

            $ del flirt_requires_string
            $ del seduce_requires_string
            $ clear_scene()
            if mod_installed:
                $ mc.change_location(ceo_office)
                $ mc.location.show_background()
            elif True:
                $ office.show_background()
            "Half an hour later there is a knock on your office door."
            mc.name "Come in."
            if success_chance > 75:
                $ helper.cum_on_face(add_to_record = False)
                $ helper.cum_on_tits(add_to_record = False)
            $ helper.draw_person()
            helper "All done with the tour. Let me know if you need anything else."
            "[rep_name] steps into your office and [helper.title] closes the door behind him. [rep_name] sits down in the chair on the opposite side of your desk."
            $ clear_scene()
            if renpy.random.randint(0,100) < success_chance:
                rep_name "I won't waste any more of your time [mc.name], I can say with certainty that my investors are going to be interested in investing in your business."
                mc.name "I'm glad to hear it."
                rep_name "I would like to offer you $5000 to help you expand your business. In exchange we'll expect a small part of your ongoing revenue."
                rep_name "Say... 1%% of every sale. How does that sound?"
                menu:
                    "Accept $5000\n{color=#ff0000}{size=18}Cost: 1%% of all future sales{/size}{/color}" if True:
                        "You reach your hand across the table to shake [rep_name]'s hand."
                        mc.name "I think we have a deal. Lets sort out the paperwork."
                        $ mc.business.change_funds(5000)
                        $ update_investor_payment()
                        "Within an hour $5000 has been moved into your companies bank account. [rep_name] leaves with a report detailing your current research progress."
                    "Reject the offer" if True:

                        mc.name "That's a very tempting offer, but we keep a tight grip on all of our research material."
                        "[rep_name] nods and stands up."
                        rep_name "I understand. Maybe in the future you will reconsider. Thank you for your time and the tour."
                        "You walk [rep_name] back to his car and watch as he drives away."
            elif True:

                rep_name "I won't waste any more of your time [mc.name]. What you're doing here is certainly, ah, interesting, but I don't think I can recommend it as a sound investment at the moment."
                rep_name "In the future I might visit again to reevaluate though."
                mc.name "I understand. Thank you for your time, I'll see you out."
                "You walk [rep_name] back to his car and watch as he drives away."
            $ del helper

        if mod_installed:
            $ mc.change_location(lobby)
            $ mc.location.show_background()
    return
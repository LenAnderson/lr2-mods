init python:
    def LENA_bugfix_get_titles_extended(org_func):
        def get_titles_wrapper(person):
            list_of_titles = org_func(person)
            
            if person not in unique_character_list:
                if person.love > 30 and person.height > 1.1:
                    list_of_titles.append("Sexy Legs")
                    list_of_titles.append("Sky High")
                
                if person.love > 30 and person.height < 0.8:
                    list_of_titles.append("Tinkerbell")
                    list_of_titles.append("Little Lady")
                
                if person.love > 30 and person.sluttiness > 20 and person.get_opinion_score("high heels") >= 2:
                    list_of_titles.append("Killer Heels")
                
                if person.sluttiness > 80:
                    list_of_titles.append("Whore")
                
                if person.sluttiness > 50 and person.has_job(stripper_job):
                    list_of_titles.append("Pole-Slut")
                if person.love > 50 and person.has_job(stripclub_mistress_job):
                    list_of_titles.append("Milady")
                if person.sluttiness > 60 and person.has_job(stripclub_mistress_job):
                    list_of_titles.append("Mistress")
            
            
            return list(set(list_of_titles))
        
        return get_titles_wrapper
    
    # Person.get_titles = LENA_bugfix_get_titles_extended(Person.get_titles)
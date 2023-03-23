init -1 python:
    def LENA_generate_item_displayable(self, body_type, tit_size, position, lighting = None, regions_constrained = None, nipple_wetness = 0.0):
        if self.is_extension:
            return

        if lighting is None:
            lighting = [1,1,1]

        if not self.body_dependant:
            body_type = "standard_body"

        image_set = self.position_sets.get(position) # The image set we are using should corrispond to the set named "positon".
        if image_set is None:
            image_set = self.position_sets.get("stand3")

        if self.draws_breasts:
            the_image = image_set.get_image(body_type, tit_size)
        else:
            the_image = image_set.get_image(body_type, "AA")

        if regions_constrained is None:
            regions_constrained = []


        converted_mask_image = None
        #inverted_mask_image = None
        if self.pattern is not None:
            pattern_set = self.pattern_sets.get(position+"_"+self.pattern)
            if pattern_set is None:
                mask_image = None
            elif self.draws_breasts:
                mask_image = pattern_set.get_image(body_type, tit_size)
            else:
                mask_image = pattern_set.get_image(body_type, "AA")

            if mask_image is None:
                self.pattern = None
            # else:
                #inverted_mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,-1,1]) #Generate the masks that will be used to determine what is colour A and B
                #mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,1,0])



        brightness_matrix = im.matrix.brightness(self.whiteness_adjustment)
        contrast_matrix = im.matrix.contrast(self.contrast_adjustment)
        opacity_matrix = im.matrix.opacity(self.opacity_adjustment) #Sets the clothing to the correct colour and opacity.

        #This is the base greyscale image we have
        greyscale_image = im.MatrixColor(the_image, opacity_matrix * brightness_matrix * contrast_matrix) #Set the image, which will crush all modifiers to 1 (so that future modifiers are applied to a flat image correctly with no unusually large images


        colour_matrix = im.matrix.tint(self.colour[0], self.colour[1], self.colour[2]) * im.matrix.tint(*lighting)
        alpha_matrix = im.matrix.opacity(self.colour[3])
        shader_image = im.MatrixColor(greyscale_image, alpha_matrix * colour_matrix) #Now colour the final greyscale image


        if self.pattern is not None:
            colour_pattern_matrix = im.matrix.tint(self.colour_pattern[0], self.colour_pattern[1], self.colour_pattern[2]) * im.matrix.tint(*lighting)
            pattern_alpha_matrix = im.matrix.opacity(self.colour_pattern[3]) #The opacity of the pattern is INDEPENDENT FROM the opacity of the entire piece of clothing.
            shader_pattern_image = im.MatrixColor(greyscale_image, pattern_alpha_matrix * colour_pattern_matrix)

            mask_red_alpha_invert = im.MatrixColor(mask_image, [0,0,0,1,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,1]) #Inverts the pattern colour so the shader applies properly.

            final_image = AlphaBlend(mask_image, shader_image, shader_pattern_image, alpha=False)
        else:
            final_image = shader_image

        final_image = Composite(position_size_dict[position], self.crop_offset_dict.get(position,(0,0)), final_image) #Transform the clothing image into a composite with the image positioned correctly.
        # Images need to be put into a composite here so we can properly apply masks, which themselves need to be composited to apply correctly.

        if len(regions_constrained)>0:
            # We want to support clothing "constraining", or masking, lower images. This is done by region.
            # Each constraining region effectively subtracts itself + a blurred border around it, and then the body region is added back in so it appears through clothing.

            composite_list = None
            for region in regions_constrained:
                #Begin by building a total mask of all constrained regions
                region_mask = region.generate_raw_image(body_type, tit_size, position)
                if composite_list is None:
                    #x_size, y_size = renpy.render(region_mask, 0,0,0,0).get_size() #Only get the render size once, since all renders are the same size for a pose. Technically this could also be a lookup table if it was significantly impacting performacne
                    composite_list = [position_size_dict.get(position)]
                # composite_list.append((0,0))
                composite_list.append(region.crop_offset_dict.get(position,(0,0)))
                composite_list.append(region_mask)

            composite = im.Composite(*composite_list)
            blurred_composite = im.Blur(composite, 8) #Blur the combined region mask to make it wider than the original. This would start to incorrectly include the interior of the mask, but...
            constrained_region_mask = im.MatrixColor(blurred_composite, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,8,0]) #This is the area to be subracted from the image.
            full_body_mask = all_regions.generate_raw_image(body_type, tit_size, position)
            #full_body_mask = Image(all_regions.generate_item_image_name(body_type, tit_size, position)) #And this is the area to add back in so it is displayed only along the body in some regions
            composite_list.extend([all_regions.crop_offset_dict.get(position, (0,0)),full_body_mask])
            #BUG: It only seems to be using the first region constrain.
            full_body_comp = im.Composite(*composite_list) # This ensures all constrained regions are part of the body mask, enabling support for items like skirts w/ clothing between body parts.
            constrained_mask = AlphaBlend(constrained_region_mask, Solid("#FFFFFFFF"), full_body_comp) #This builds the proper final image mask (ie all shown, except for the region around but not including the constrained region)
            final_image = AlphaBlend(constrained_mask, Solid("#00000000"), final_image)

        if nipple_wetness > 0: #TODO: Expand this system to a generic "Wetness" system
            region_mask = wet_nipple_region.generate_raw_image(body_type, tit_size, position)
            #region_mask = Image(wet_nipple_region.generate_item_image_name(body_type, tit_size, position))
            position_size = position_size_dict[position]
            region_mask = im.MatrixColor(region_mask, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,nipple_wetness,0])
            region_composite = Composite(position_size,(0,0), Solid("00000000", xsize = position_size[0], ysize = position_size[1]), wet_nipple_region.crop_offset_dict.get(position,(0,0)), region_mask)
            #print(str(position_size))
            final_image = AlphaBlend(region_composite, final_image, Solid("#00000000"))

        if self.half_off or (self.has_extension and self.has_extension.half_off):
            #NOTE: This actually produces some really good looking effects for water/stuff. We should add these kinds of effects as a general thing, probably on the pattern level.
            #NOTE: Particularly for water/stains, this could work really well (and can use skin-tight region marking, ie. not clothing item dependant).

            composite_list = [position_size_dict.get(position)]

            total_half_off_regions = [] #Check what all of the half-off regions should be
            if self.half_off:
                total_half_off_regions.extend(self.half_off_regions)
            if (self.has_extension and self.has_extension.half_off):
                total_half_off_regions.extend(self.has_extension.half_off_regions) #TODO: Duplicates in this cause everything to run slightly slower. Fix that

            for region_to_hide in total_half_off_regions: #We first add together all of the region masks so we only operate on a single displayable
                #region_mask = Image(region_to_hide.generate_item_image_name(body_type, tit_size, position))
                region_mask = region_to_hide.generate_raw_image(body_type, tit_size, position)
                composite_list.append(region_to_hide.crop_offset_dict.get(position, (0,0)))
                composite_list.append(region_mask)

            composite = im.Composite(*composite_list)
            blurred_composite = im.Blur(composite, 12) #Blur the combined region mask to make it wider than the original. This would start to incorrectly include the interior of the mask, but...
            transparency_control_image = im.MatrixColor(blurred_composite, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,7,0]) #...We increase the contribution of alpha from the mask, so a small amount ends up being 100% (this still preserves some gradient at the edge as well)

            if self.half_off_ignore_regions: #Sometimes you want hard edges, or a section of a piece of clothing not to be moved. These regions are not blured/enlarged and are subtracted from the mask generated above.
                add_composite_list = None
                for region_to_add in self.half_off_ignore_regions:
                    region_mask = region_to_add.generate_raw_image(body_type, tit_size, position)
                    #region_mask = Image(region_to_add.generate_item_image_name(body_type, tit_size, position))
                    if add_composite_list is None:
                        add_composite_list = [position_size_dict.get(position)] #We can reuse the size from our first pass building the mask.
                    #add_composite_list.append((0,0))
                    add_composite_list.append(region_to_add.crop_offset_dict.get(position, (0,0)))
                    add_composite_list.append(region_mask)

                add_composite = im.Composite(*add_composite_list)
                transparency_control_image = AlphaBlend(add_composite, transparency_control_image, Solid("#00000000"), True) #This alpha blend effectively subtracts the half_off_ignore mask from the half_off region mask

            final_image = AlphaBlend(transparency_control_image, final_image, Solid("#00000000"), True) #Use the final mask to hide parts of the clothing image as appopriate.

        return final_image

    Clothing.generate_item_displayable = LENA_generate_item_displayable
                if ($orcid)
                {
                        $content = $CGI->p("Your ORCID iD is <strong>" . escapeHTML($orcid) . "</strong>. " .
                                $CGI->a({-href=>$orcid_config->{orcid_profile_prefix} . escapeHTML($orcid), -target=>'new'},
                                        "View your ORCID profile")) .
                                $CGI->p($CGI->a({-href=>"$prefix/unlink"}, "Remove the link to this ORCID iD."));
                }
                else
                {
                        my ($affiliation_type, @affiliations) = get_affiliation_details();

                        $content =
          "<p>You do not yet have an ORCID iD associated with your Oxford account, but can link one now.' .
         $CGI->a({-href=>"/popups/orcid-why.html",
                                                        -onClick=>"return hs.htmlExpand(this, { outlineType: 'rounded-white', wrapperClassName: 'draggable-header', objectType: 'iframe', width: 450 } )",
                                                        -class=>'popupright'},"Why would I want to do this?") .
          '</p>\n" .
          "<p>By submitting the form below you'll be redirected to the ORCID site to give permission for the" .
                                          " University to see your ORCID iD. If you don't yet have an ORCID account you'll be able to create" .
                                          " one before you give permission.</p>" .
                                        $CGI->p($CGI->div({-class=>'textwrapper'},
                                                $CGI->a({-href=>"/popups/orcid-link-existing.html",
                                                        -onClick=>"return hs.htmlExpand(this, { outlineType: 'rounded-white', wrapperClassName: 'draggable-header', objectType: 'iframe', width: 450 } )",
                                                        -class=>'popupright'},"How do I replace a manually entered Oxford affiliation with a verified one?"))) .
                                        $CGI->start_form(-method => "POST", -action=>"$prefix/link") .
                                        ((!($affiliation_type && $use_affiliations)) ? "" : (
                                                "<ul>\n" .
                                                "  <li>\n" .
                                                "    <input type=\"checkbox\" checked name=\"add_affiliation\" id=\"add_affiliation\">\n" .
                                                "    <label for=\"add_affiliation\">Update my ORCID record to include a University of Oxford affiliation if one doesn't already exist (<em>$affiliation_type; " . join(", ", map( {escapeHTML($_)} @affiliations)) . "</em>)</label><br>\n" .
                                                "    <em>This will require permission to update your ORCID profile (you can remove this later).</em>\n" .
                                                "  </li>\n" .
                                                "</ul>\n")) .
                                                $CGI->image_button(-name=>'link',-src=>'/icons/orcidlogin.gif', -title=>'Log in to ORCID') .
                                        $CGI->end_form();
                }

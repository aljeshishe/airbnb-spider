import email

headers_str = '''Host: www.airbnb.ru
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Content-Type: application/json
X-Airbnb-Supports-Airlock-V2: True
X-Airbnb-API-Key: d306zoyjsyarp7ifhu67rjxn52tv0t20
X-CSRF-Token: null
X-CSRF-Without-Token: 1
X-Airbnb-GraphQL-Platform: web
X-Airbnb-GraphQL-Platform-Client: minimalist-niobe
X-Niobe-Short-Circuited: True
x-client-request-id: 1ddg1b70v218pv0i2cbe11clxo85
Origin: https://www.airbnb.ru
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Referer: https://www.airbnb.ru/s/Antalya/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&checkin=2022-12-01&checkout=2022-12-31&adults=1&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=30&query=Antalya&price_max=248&flexible_trip_lengths%5B%5D=one_month&flexible_trip_dates%5B%5D=november&drawer_open=False
Connection: keep-alive
Cookie: frmfctr=wide; cfrmfctr=DESKTOP; previousTab=%7B%22id%22%3A%222cde734f-f3b1-491f-abbf-ed2e6bb1ad6f%22%2C%22url%22%3A%22https%3A%2F%2Fwww.airbnb.ru%2Fs%2FAntalya%2Fhomes%3Ftab_id%3Dhome_tab%26refinement_paths%255B%255D%3D%252Fhomes%26date_picker_type%3Dcalendar%26checkin%3D2022-12-01%26checkout%3D2022-12-31%26adults%3D1%26source%3Dstructured_search_input_header%26search_type%3Dfilter_change%26price_filter_num_nights%3D30%26query%3DAntalya%26price_max%3D96%26price_min%3D1%26flexible_trip_lengths%255B%255D%3Done_month%26flexible_trip_dates%255B%255D%3Dnovember%26drawer_open%3DFalse%22%7D; bev=1667318188_OGJkMjMwOTRhYmFj; jitney_client_session_id=a5b226d7-3dd0-44d4-8433-0e0ecdff7707; jitney_client_session_created_at=1667318196; jitney_client_session_updated_at=1667318196
TE: trailers'''
# will be added by scrapy
# Content-Length: 2106

# will be added by scrapy
# Accept-Encoding: gzip, deflate, br

# disables local caching
# Pragma: no-cache
# Cache-Control: no-cache

headers = email.message_from_string(headers_str)

items_per_page = 40
data = {
    "operationName": "StaysSearch",
    "variables": {
        "isInitialLoad": True,
        "hasLoggedIn": False,
        "cdnCacheSafe": False,
        "source": "EXPLORE",
        "exploreRequest": {
            "metadataOnly": False,
            "version": "1.8.3",
            "tabId": "home_tab",
            "refinementPaths": [
                "/homes"
            ],
            "flexibleTripLengths": [
                "one_week"
            ],
            "priceFilterInputType": 0,
            "priceFilterNumNights": 3,
            "placeId": "ChIJwa2t3a6awxQRMy7j-XOfxpU",
            "datePickerType": "calendar",
            "checkin": "2022-11-14",
            "checkout": "2022-11-17",
            "adults": 1,
            "source": "structured_search_input_header",
            "searchType": "autocomplete_click",
            "federatedSearchSessionId": "3e37c336-400b-48ea-8a18-4d0e6d6aa572",
            "itemsOffset": 0,
            "query": "Izmir",
            "itemsPerGrid": items_per_page,
            "cdnCacheSafe": False,
            "treatmentFlags": [
                "flex_destinations_june_2021_launch_web_treatment",
                "new_filter_bar_v2_fm_header",
                "new_filter_bar_v2_and_fm_treatment",
                "merch_header_breakpoint_expansion_web",
                "flexible_dates_12_month_lead_time",
                "storefronts_nov23_2021_homepage_web_treatment",
                "lazy_load_flex_search_map_compact",
                "lazy_load_flex_search_map_wide",
                "im_flexible_may_2022_treatment",
                "im_flexible_may_2022_treatment",
                "flex_v2_review_counts_treatment",
                "search_add_category_bar_ui_ranking_control_web",
                "flexible_dates_options_extend_one_three_seven_days",
                "super_date_flexibility",
                "micro_flex_improvements",
                "micro_flex_show_by_default",
                "search_input_placeholder_phrases",
                "pets_fee_treatment"
            ],
            "screenSize": "large",
            "isInitialLoad": True,
            "hasLoggedIn": False
        },
        "staysSearchM2Enabled": False,
        "staysSearchM3Enabled": False,
        "staysSearchM6Enabled": False
    },
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "d582c7a9fee19104cedaaed731f76093c46d5490652aa5a91055e40b776a0ff8"
        }
    }
}

STAY_SEARCH_DATA_2 = {"operationName": "StaysSearch",
                      "variables": {"isInitialLoad": True, "hasLoggedIn": True, "cdnCacheSafe": False,
                                    "source": "EXPLORE", "staysSearchRequest": {
                              "cursor": "eyJzZWN0aW9uX29mZnNldCI6MiwiaXRlbXNfb2Zmc2V0Ijo0MCwidmVyc2lvbiI6MX0=",
                              "metadataOnly": False, "searchType": "filter_change",
                              "treatmentFlags": ["flex_destinations_june_2021_launch_web_treatment",
                                                 "new_filter_bar_v2_fm_header", "new_filter_bar_v2_and_fm_treatment",
                                                 "merch_header_breakpoint_expansion_web",
                                                 "flexible_dates_12_month_lead_time",
                                                 "storefronts_nov23_2021_homepage_web_treatment",
                                                 "lazy_load_flex_search_map_compact", "lazy_load_flex_search_map_wide",
                                                 "im_flexible_may_2022_treatment", "im_flexible_may_2022_treatment",
                                                 "flex_v2_review_counts_treatment",
                                                 "search_add_category_bar_ui_ranking_web",
                                                 "decompose_stays_search_m2_treatment",
                                                 "flexible_dates_options_extend_one_three_seven_days",
                                                 "super_date_flexibility", "micro_flex_improvements",
                                                 "micro_flex_show_by_default", "search_input_placeholder_phrases",
                                                 "pets_fee_treatment"],
                              "rawParams": [{"filterName": "adults", "filterValues": ["1"]},
                                            {"filterName": "cdnCacheSafe", "filterValues": ["False"]},
                                            {"filterName": "checkin", "filterValues": ["2022-12-11"]},
                                            {"filterName": "checkout", "filterValues": ["2022-12-18"]},
                                            {"filterName": "datePickerType", "filterValues": ["calendar"]},
                                            {"filterName": "federatedSearchSessionId",
                                             "filterValues": ["283961a1-cfa3-4152-ba81-4b64cda405a8"]},
                                            {"filterName": "flexibleTripLengths", "filterValues": ["one_week"]},
                                            {"filterName": "hasLoggedIn", "filterValues": ["True"]},
                                            {"filterName": "isInitialLoad", "filterValues": ["True"]},
                                            {"filterName": "itemsPerGrid", "filterValues": ["20"]},
                                            {"filterName": "placeId", "filterValues": ["ChIJwa2t3a6awxQRMy7j-XOfxpU"]},
                                            {"filterName": "priceFilterNumNights", "filterValues": ["7"]},
                                            {"filterName": "query", "filterValues": ["Antalya, Turkey"]},
                                            {"filterName": "refinementPaths", "filterValues": ["/homes"]},
                                            {"filterName": "screenSize", "filterValues": ["large"]},
                                            {"filterName": "tabId", "filterValues": ["home_tab"]},
                                            {"filterName": "version", "filterValues": ["1.8.3"]}]},
                                    "staysSearchM2Enabled": True, "staysSearchM3Enabled": False,
                                    "staysSearchM6Enabled": False}, "extensions": {"persistedQuery": {"version": 1,
                                                                                                      "sha256Hash": "a85197ef4d7ce47444c6e49baf9405185443a687c6c58f80b849b8aba5a5c3a9"}}}

AUTO_COMPLETE_URL = 'https://www.airbnb.com/api/v2/autocompletes?country=TR&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&' \
                    'language=en&locale=en-GB&num_results=5&user_input={query}&api_version=1.2.0&' \
                    'satori_config_token=EhIiQRIiIjISEjISIRESIlFCNaoDFQYVWBUCBYoBAAA&vertical_refinement=homes&' \
                    'region=-1&options=should_filter_by_vertical_refinement|hide_nav_results|' \
                    'should_show_stays|simple_search|flex_destinations_june_2021_launch_web_treatment'

STAY_SEARCH_URL = 'https://www.airbnb.ru/api/v3/StaysSearch?operationName=StaysSearch&locale=en&currency=USD'

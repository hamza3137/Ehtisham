import config_common as common_config

account_name = 'bh'


base_file_location = common_config.base_folder + account_name + '\\'
common_file_location = common_config.common_folder

FILE_LOCATION = {
    'str_file_location' : base_file_location + 'Bh Search term report  08012019 to 09272019.xlsx',
    'target_file_location': base_file_location + 'Bh Targeting report 08012019 to 09272019.xlsx',
    'bulk_file_location': base_file_location + 'BH BULK 30days new.xlsx',
    'gen_lb_keywords_asins': base_file_location + account_name + '_gen_lb_keywords_asins.xlsx',
    #'keywords_to_add_file': base_file_location + account_name + '_keywords_to_add_file.xlsx',
    'keywords_to_add_file': base_file_location +  'CoolingMassageCream_keywords_to_add_file.xlsx',
    'asins_to_add_file': base_file_location + account_name + '_asins_to_add_file.xlsx',
    #'asins_to_add_file': base_file_location + 'bh_asins_to_add.xlsx',
    'upload_file_location' : base_file_location + 'upload\\',
    'white_list_file': common_file_location + 'white_list_file.xlsx',
    'sku_names': common_file_location + 'SKU names and Kws.xlsx',
    'low_bid_keywords_asins': common_file_location + 'low_performing_keywords_asins.xlsx',
}

override_start_date = False
start_date = '04/26/2019'

override_end_date = False
end_date = '05/26/2019'

max_bid_limit_set = True
max_bid = 1.53
no_enhance_bid_set = True
enhance_bid_multiplier = 1.0
max_highest_bid = 2.98
target_acos = 15
wl_target_acos = 65
bad_keyword_max_bid = 0.51
sales_optimized = True

PRODUCTS = [
{'search_name': 'TeaTreeWash', 'sku': 'TeaTreeWash', 'ad_group_level': True},
{'search_name': 'TeaTreeOilShampooConditionerSet', 'sku': 'TeaTreeOilShampooConditionerSet', 'ad_group_level': True},
{'search_name': 'AloeVera16oz', 'sku': 'AloeVera16oz', 'ad_group_level': True},
{'search_name': 'ArganOilKeratine', 'sku': 'ArganOilKeratine', 'ad_group_level': True},
{'search_name': 'BH-EssentialOilsSet', 'sku': 'BH-EssentialOilsSet', 'ad_group_level': True},
{'search_name': 'Muscle Jelly', 'sku': 'QV-QNQ1-4M8G', 'ad_group_level': True},
{'search_name': 'AcneScarEGFSerum', 'sku': 'AcneScarEGFSerum', 'ad_group_level': True},
{'search_name': 'CelluliteOil', 'sku': 'CelluliteOil', 'ad_group_level': True},
{'search_name': 'Caviar Set', 'sku': 'CaviarComboShampooConditioner ', 'ad_group_level': True},
{'search_name': 'Argan Hair Mask', 'sku': 'ArganHairMaskBH ', 'ad_group_level': True},
{'search_name': 'Biotin Set', 'sku': 'BiotinShampoo+Conditioner ', 'ad_group_level': True},
{'search_name': 'Caviar Blowout', 'sku': 'CaviarBlowout ', 'ad_group_level': True},
{'search_name': 'Caviar Hair Oil', 'sku': 'CaviarHairDrops ', 'ad_group_level': True},
{'search_name': 'Black soap Scrub', 'sku': 'AfricanSoap ', 'ad_group_level': True},
{'search_name': 'Cellulite body scrub', 'sku': 'CelluliteBodyScrubMassage1 ', 'ad_group_level': True},
{'search_name': 'watermelon shampoo set', 'sku': 'WatermelonShampooConditionerSet ', 'ad_group_level': True},
{'search_name': 'cellulite cream', 'sku': 'CalluliteMassageCream ', 'ad_group_level': True},
{'search_name': 'SoreMuscleMassageOil', 'sku': 'SoreMuscleMassageOil', 'ad_group_level': True},
]

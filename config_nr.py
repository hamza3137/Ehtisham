account_name = 'nr'

import config_common as common_config


base_file_location = common_config.base_folder + account_name + '\\'
common_file_location = common_config.common_folder

FILE_LOCATION = {
    'str_file_location' : base_file_location + 'NR Search term report 08012019 to 09272019.xlsx',
    'target_file_location': base_file_location + 'NR Targeting report 08012019 to 09272019.xlsx',
    'bulk_file_location': base_file_location + 'NR BULK 30days.xlsx',
    'gen_lb_keywords_asins': base_file_location + account_name + '_gen_lb_keywords_asins.xlsx',
    'low_bid_keywords_asins': base_file_location + account_name + '_low_bid_keywords_asins.xlsx',
    #'keywords_to_add_file': base_file_location + account_name + '_keywords_to_add_file.xlsx',
    'keywords_to_add_file': base_file_location + 'Natural Riches Self Cerebro Data 0912.xlsx' ,
    'asins_to_add_file': base_file_location + account_name + '_asins_to_add.xlsx',
    #'asins_to_add_file': base_file_location + 'nr_hp_asins_to_add.xlsx',
    'upload_file_location' : base_file_location + '\\upload\\',
    'sku_names': common_file_location + 'SKU names and Kws.xlsx',
    'white_list_file': common_file_location + 'white_list_file.xlsx',
    'low_bid_keywords_asins': common_file_location + 'low_performing_keywords_asins.xlsx',
}

max_bid_limit_set = True
max_bid = 1.53
enhance_bid_multiplier = 1
max_highest_bid = 2.98
target_acos = 20
wl_target_acos = 65
bad_keyword_max_bid = 0.51
sales_optimized = True


override_start_date = False
start_date = '04/26/2019'

override_end_date = False
end_date = '05/26/2019'

PRODUCTS = [
    {
    'identification' : 'Breathe', # Sheets in excel will read and write with this name
    'search_name' : 'Breathe', # Search identifier in Campaign or Ad group
    'sku' : 'KQ-CMJ2-BW91',
    'ad_group_level' : True, # Filtering will be applied on Ad Group (not campaign)
    },
    {
    'identification' : 'Castor Oil Eyelash',
    'search_name' : 'Castor Oil Eyelash',
    'sku' : 'NK-VRJM-XMOJ',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Bodywash',
    'search_name' : 'Bodywash',
    'sku' : 'QK-TF3M-TBQA',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Five Guards',
    'search_name' : 'Five Guards',
    'sku' : 'YH-W5G1-0Z7K',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Sleep',
    'search_name' : 'Sleep',
    'sku' : '6S-VKTY-8OL9',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Castor Oil Hair',
    'search_name' : 'Castor Oil Hair',
    'sku' : '2A-30QR-4XSP',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Tea Tree Shampoo Cond',
    'search_name' : 'Tea Tree Shampoo Cond',
    'sku' : 'NF-JNJQ-HPJP',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Himalayan Salt Lamp',
    'search_name' : 'Himalayan Salt Lamp',
    'sku' : '1C-SFT9-XLT3',
    'ad_group_level' : True,
    },
        {
    'identification' : 'Stress', # Sheets in excel will read and write with this name
    'search_name' : 'Stress', # Search identifier in Campaign or Ad group
    'sku' : '696305118351',
    'ad_group_level' : True, # Filtering will be applied on Ad Group (not campaign)
    },
    {
    'identification' : 'Tea Tree Oil',
    'search_name' : 'Tea Tree Oil',
    'sku' : 'P2-TQ7F-D8YN',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Omega 3',
    'search_name' : 'Omega 3',
    'sku' : 'BM-BJAR-SGQ3',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Probiotics',
    'search_name' : 'Probiotics',
    'sku' : 'G9-Y45N-E86O',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Scar Cream',
    'search_name' : 'Scar Cream',
    'sku' : 'L6-2XB6-MPAJ',
    'ad_group_level' : True,
    },
    {
    'identification' : '3 Oils Set',
    'search_name' : '3 Oils Set',
    'sku' : 'FC-Q5LO-UCZ6',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Rose Water',
    'search_name' : 'Rose Water',
    'sku' : 'CM-XO72-S7LW',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Charcoal Powder',
    'search_name' : 'Charcoal Powder',
    'sku' : '38-1PY8-TKJZ',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Argan Shampoo',
    'search_name' : 'Argan Shampoo',
    'sku' : 'C7-RDZG-KEDG',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Lashy Lash',
    'search_name' : 'Lashy Lash',
    'sku' : '6V-W1NJ-35YO',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Head Ease',
    'search_name' : 'Head Ease',
    'sku' : 'Z3-44QO-809Y',
    'ad_group_level' : True,
    },
    {
    'identification' : 'Lavender',
    'search_name' : 'Lavender',
    'sku' : '1N-5BZ0-UDCH',
    'ad_group_level' : falseee,
    },
]

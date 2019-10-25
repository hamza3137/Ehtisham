import config_common as common_config

account_name = 'nb'
base_file_location = common_config.base_folder + account_name + '\\'
common_file_location = common_config.common_folder

FILE_LOCATION = {
    'str_file_location' : base_file_location + 'NEX Search term report 08012019 to 09272019.xlsx',
    'target_file_location': base_file_location + 'NEX Targeting report 08012019 to 09272019.xlsx',
    'bulk_file_location': base_file_location + 'NEX bulk 30days.xlsx',
    'gen_lb_keywords_asins': base_file_location + account_name + '_gen_lb_keywords_asins.xlsx',
    #'keywords_to_add_file': base_file_location + account_name + '_keywords_to_add_file.xlsx',
    'keywords_to_add_file': base_file_location + 'Nexon Botanics Self Cerebro Data 0912.xlsx',
    'sb_keywords_to_add_file': base_file_location + 'Nexon SB Ad Peppermint.xlsx',
    'asins_to_add_file': base_file_location + account_name + '_asins_to_add_file.xlsx',
    #'asins_to_add_file': base_file_location + 'nb_asins_to_add.xlsx',
    'upload_file_location' : base_file_location + '\\upload\\',
    'sku_names': common_file_location + 'SKU names and Kws.xlsx',
    'white_list_file': common_file_location + 'white_list_file.xlsx',
    'low_bid_keywords_asins': common_file_location + 'low_performing_keywords_asins.xlsx',
}

max_bid_limit_set = True
max_bid = 1.53
max_highest_bid = 2.98
target_acos = 25
wl_target_acos = 65
enhance_bid_multiplier = 1.0
bad_keyword_max_bid = 0.51
sales_optimized = True

override_start_date = False
start_date = '04/26/2019'

override_end_date = False
end_date = '05/26/2019'

PRODUCTS = [
    {
    'search_name' : 'breathe blend', # Search identifier in Campaign or Ad group
    'sku' : 'NBBB0001',
    'ad_group_level' : True, # Filtering will be applied on Ad Group (not campaign)
    },
    {
    'search_name' : 'sleep blend',
    'sku' : 'NBSB0001',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'zen head',
    'sku' : 'NBZH0001',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'blend set',
    'sku' : 'BLENDSET',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'anxiety blend',
    'sku' : 'NBAB0001',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'organic set',
    'sku' : 'NBOS0001',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'mct oil',
    'sku' : 'NBMCT0001',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'health plus',
    'sku' : 'NBTB0001',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'frankincense',
    'sku' : 'T8-YCGO-S2K6',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'peppermint',
    'sku' : 'N1-318U-BQQL',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'teatree oil',
    'sku' : 'BZ-GP0D-TFVT',
    'ad_group_level' : True,
    },
    {
    'search_name' : 'teatree shampoo',
    'sku' : 'NBTTS001',
    'ad_group_level' : True,
    },
]
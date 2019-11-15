import config_common as common_config

account_name = 'mmc'


base_file_location = common_config.base_folder + account_name + '\\'
common_file_location = common_config.common_folder

FILE_LOCATION = {
    'str_file_location' : base_file_location + 'MM Search term report 08012019 to 09272019.xlsx',
    'target_file_location': base_file_location + 'MM Targeting report 08012019 to 09272019.xlsx',
    'bulk_file_location': base_file_location + 'MM BULK 30days.xlsx',
    'gen_lb_keywords_asins': base_file_location + account_name + '_gen_lb_keywords_asins.xlsx',
    #'keywords_to_add_file': base_file_location + account_name + '_keywords_to_add_file.xlsx',
    'keywords_to_add_file': base_file_location + 'Mineral Me Self Cerebro Data 0912.xlsx',
    'sb_keywords_to_add_file': base_file_location + 'Nexon Headline Search Ad.xlsx',
    #'asins_to_add_file': base_file_location + account_name + '_asins_to_add_file.xlsx',
    'white_list_file': common_file_location + 'white_list_file.xlsx',
    'asins_to_add_file': base_file_location + 'mmc_higher_price_to_add_2.xlsx',
    'upload_file_location' : base_file_location + '\\upload\\',
    'sku_names': common_file_location + 'SKU names and Kws.xlsx',
    'low_bid_keywords_asins': common_file_location + 'low_performing_keywords_asins.xlsx',
}

max_bid_limit_set = True
max_bid = 1.53
max_highest_bid = 2.98
target_acos = 20
wl_target_acos = 65
enhance_bid_multiplier = 1.0
bad_keyword_max_bid = 0.51
sales_optimized = True

override_start_date = False
start_date = '04/26/2019'

override_end_date = False
end_date = '05/26/2019'

PRODUCTS = [
{'search_name': 'SB- Original 6', 'sku': 'MineralMe-SHS001', 'ad_group_level': True},
{'search_name': 'BB-Lets Sail Away', 'sku': 'MineralMe-BathBombs-LSA001', 'ad_group_level': True},
{'search_name': 'BB-Motivational 12', 'sku': 'MineralMe-NBM001', 'ad_group_level': True},
{'search_name': 'BB- To The Moon', 'sku': 'MineralMe-TMB001', 'ad_group_level': True},
{'search_name': 'BB- To The Sun', 'sku': 'MineralMe-TMB002', 'ad_group_level': False},
]

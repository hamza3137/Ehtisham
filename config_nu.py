import config_common as common_config
account_name = 'nu'
base_file_location = common_config.base_folder + account_name + '\\'
common_file_location = common_config.common_folder

FILE_LOCATION = {
    'str_file_location' : base_file_location + 'NU Search term report 08012019 to 09272019.xlsx',
    'target_file_location': base_file_location + 'NU Targeting report 08012019 to 09272019.xlsx',
    'bulk_file_location': base_file_location + 'NU BULK 30days.xlsx',
    'gen_lb_keywords_asins': base_file_location + account_name + '_gen_lb_keywords_asins.xlsx',
    #'keywords_to_add_file': base_file_location + account_name + '_keywords_to_add_file.xlsx',
    'asins_to_add_file': base_file_location + account_name + '_asins_to_add_file.xlsx',
    #'asins_to_add_file': base_file_location + 'nu_asins_to_add.xlsx',
    'keywords_to_add_file': base_file_location +  'Nuwellix Self Cerebro Data 0912.xlsx',
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
target_acos = 30
wl_target_acos = 80
bad_keyword_max_bid = 0.51
sales_optimized = True


PRODUCTS = [
{'search_name': 'Turmeric', 'sku': 'Nuwe-Turmeric', 'ad_group_level': True},
{'search_name': 'Probiotics', 'sku': 'Nuwellix- Probiotics', 'ad_group_level': True},
{'search_name': 'Ashwagandha', 'sku': 'Nuwellix- Ashwagandha', 'ad_group_level': True},
{'search_name': 'Keto 5', 'sku': 'Nuwellix-Keto5', 'ad_group_level': True},
{'search_name': 'Krill', 'sku': 'Nuwellix-KrillOil', 'ad_group_level': True},
]
##    {
##    'identification' : 'Turmeric', # Sheets in excel will read and write with this name
##    'search_name' : 'Turmeric', # Search identifier in Campaign or Ad group
##    'sku' : 'Nuwe-Turmeric',
##    'ad_group_level' : True, # Filtering will be applied on Ad Group (not campaign)
##    },
##    {
##    'identification' : 'Probiotics',
##    'search_name' : 'Probiotics',
##    'sku' : 'Nuwellix- Probiotics',
##    'ad_group_level' : True,
##    },
##    {
##    'identification' : 'Ashwagandha',
##    'search_name' : 'Ashwagandha',
##    'sku' : 'Nuwellix- Ashwagandha',
##    'ad_group_level' : True,
##    },
##    {
##    'identification' : 'Keto 5',
##    'search_name' : 'Keto 5',
##    'sku' : 'Nuwellix-Keto5',
##    'ad_group_level' : True,
##    },
##    {
##    'identification' : 'Krill',
##    'search_name' : 'Krill',
##    'sku' : 'Nuwellix-KrillOil',
##    'ad_group_level' : True,
##    },
##]
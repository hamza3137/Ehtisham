@echo off

echo finding keywords and asins from search term report .....

python ppc_generate_keywords_asins_to_add.py %1

echo generating ppc keyword file to upload .....

python ppc_generate_upload_files_keywords.py %1

echo generating converting asin file to upload ......

python ppc_generate_upload_files_asins.py %1

@echo on
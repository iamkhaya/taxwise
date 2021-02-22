from tabula import wrapper

# read page from tariff book
df = wrapper.read_pdf('sample.pdf', pages=6)

df_trans = df.T
df_trans

# clean out the data
# df.dtypes
# df = df.drop(columns="Unnamed: 5")

# try:
#     df = df.drop(columns="Rate of Duty")
# except:
#     df = df.drop(columns="Unnamed: 6")

# df = df.drop(columns="Unnamed: 9")


# set to readable columns
# df.columns = [
#     'heading',
#     'CD',
#     'article_description',
#     'general_rate_of_duty',
#     'statistical_unit',
#     'eu_rate_of_duty',
#     'efta_rate_of_duty',
#     'sadc_rate_of_duty',
#     'mercosur_rate_of_duty',
# ]


# df_trans = df.T
# df_trans
